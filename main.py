import sys
from etl import run_etl, logger


def main():
    try:
        n_rows = run_etl()
        print(f'ETL klar - {n_rows} rader, se data/etl.db och logs/etl.log')
        return 0 # För att andra verktyg ska kunna se exit-kod (0 vid lyckat, 1 vid fel).

    except Exception as e:
        logger.exception(f'ETL misslyckades: {e}')
        print(f'Etl misslyckades, se logs/etl.log')
        return 1

if __name__ == '__main__': # Ser till att “startkoden” bara körs när filen körs som program, inte vid import.
    sys.exit(main()) # gör värdet till processens exit-kod (0-1)
