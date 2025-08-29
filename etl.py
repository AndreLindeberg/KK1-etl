import os 
import logging
import pandas as pd
from sqlalchemy import create_engine

# Filvägar 
CSV_path = 'data/sales.csv'
DB_path = 'data/etl.db'
LOG_DIR ='logs'
LOG_FILE = os.path.join(LOG_DIR, "etl.log")

# Se till att loggmapp finns
os.makedirs(LOG_DIR, exist_ok=True)

# Skapa egen logger
logger = logging.getLogger('csv_etl')
logger.setLevel(logging.INFO)

formatter = logging.Formatter("[%(asctime)s][%(name)s][%(levelname)s] %(message)s")

# Filhandler - skriver loggarna till en fil
fh = logging.FileHandler(LOG_FILE, encoding='utf-8')
fh.setFormatter(formatter)
logger.addHandler(fh)

# Streamhandler - skriver loggarna till konsolen
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)



def run_etl(csv_path: str = CSV_path, db_path: str = DB_path) -> int: 
    '''
     Kör CSV -> SQLite:
      - Läser csv_path
      - Validerar obligatoriska kolumner
      - Loggar WARNING om null-värden i units/unit_price men fortsätter ändå
      - Beräknar revenue = units * unit_price
      - Skriver till SQLite (tabell 'sales') i db_path
      - Returnerar antal rader som skrevs
    '''

    logger.info('Startar ETL-processen')

    # Läs CSV fil
    if not os.path.exists(csv_path):
        logger.error(f'Hittar inte CSV-filen: {csv_path}')
        raise FileNotFoundError(f'Hittar inte CSV-filen: {csv_path}') # Kontrollera att filen finns
    logger.info(f'Läser CSV: {csv_path}')
    df = pd.read_csv(csv_path, parse_dates=['date']) #
    logger.info(f'Inläst {len(df)} rader från CSV')


    # Validera kolumner
    required_cols = {'units', 'unit_price'}
    missing = required_cols - set(df.columns)                      
    if missing:
        logger.error(f'CSV saknar kolumner: {missing}')             
        raise ValueError(f'CSV saknar kolumner: {missing}')
    
    # Null-värden, logga WARNING men fortsätt.
    null_mask = df['units'].isna() | df['unit_price'].isna()
    null_count = int(null_mask.sum())
    if null_count > 0:
        logger.warning(
            f'Null-värden hittades i units/unit_price (antal: {null_count}). '
            'Raderna sparas ändå och revenue blir NaN för de raderna.'
        )
    
    # Transformera
    df['revenue'] = df['units'] * df['unit_price']
    logger.info('Beräknade kolumnen "revenue"')

    # Skriv till SQLite    
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    engine = create_engine(f'sqlite:///{db_path}') # Skapa anslutning till DB
    logger.info(f'Skriver till SQLite: {db_path} (tabell: sales)') # Skriv df till tabell
    
    with engine.begin() as conn:
        df.to_sql('sales', conn, if_exists='replace', index=False)

    logger.info('ETL klar - tabell "sales" uppdaterad')
    return len(df)
