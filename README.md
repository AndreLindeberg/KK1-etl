## Översikt
Ett minimalt ETL-flöde som läser `data/sales.csv`, beräknar `revenue = units * unit_price` och skriver resultatet till SQLite (`data/etl.db`). Flödet kan köras manuellt eller schemaläggas (Windows Task Scheduler / cron).

## Varför detta uppfyller uppgiften
- ✅ Automatiserat flöde som uppdaterar en SQL-tabell (SQLite).
- ✅ Felhantering och **loggning till fil** (`logs/etl.log`) + stacktrace via `main.py`.
- ✅ **Separata automatiska tester** (pytest): null-värde, saknad CSV, felaktiga kolumner.
- ✅ Kod med docstrings och grundläggande kodstandard.

## Projektstruktur
    KK1/
    ├─ data/
    │  └─ sales.csv              # källdata (exempel)
    ├─ logs/                     # loggar (skapas vid körning)
    ├─ tests/
    │  └─ test_etl.py            # 3 tester (pytest)
    ├─ etl.py                    # ETL-logik + loggning
    ├─ main.py                   # CLI + robust felhantering (logger.exception)
    ├─ run_etl.bat               # körskript för Task Scheduler (Windows)
    ├─ requirements.txt          # beroenden
    └─ README.md

## Kom igång

### Miljö & installation
    # Windows
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt

    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

### Testning
    # Från mappen KK1/
    pytest

### Manuell körning
    # Från mappen KK1/
    python main.py --csv data/sales.csv --db data/etl.db

### CLI-flaggor
- `--csv` sökväg till CSV (default: `data/sales.csv`)
- `--db`  sökväg till SQLite-DB (default: `data/etl.db`)

## Loggning & fel
- Loggar skrivs till **`logs/etl.log`** (skapas automatiskt).
- **Saknad CSV** → loggas som **ERROR** och körningen stoppar (`FileNotFoundError`).
- **Felaktiga kolumner** (`units`/`unit_price` saknas) → **ERROR** + stoppar (`ValueError`).
- **Null i `units` eller `unit_price`** → **WARNING**, körningen fortsätter (revenue blir `NaN` för de raderna).
- `main.py` fångar oväntade fel och loggar **stacktrace** med `logger.exception`. Exit-kod: `0` vid success, `1` vid fel.

## Schemaläggning

### Windows (Task Scheduler)
1. Öppna **Task Scheduler** → *Create Basic Task…*
2. **Name:** `KK1_ETL_daily`
3. **Trigger:** t.ex. Daily 06:00
4. **Action:** *Start a program* → peka på `run_etl.bat` i projektroten.
5. (Valfritt) **Start in:** projektets mapp (samma som `.bat`).
6. Testa med **Run** och kontrollera `logs/etl.log`.

> Använder du virtualenv? Justera sökvägen till `venv\Scripts\python.exe` i `run_etl.bat`.

### macOS/Linux (cron)
Exempel – kör varje dag 06:00:
    
    0 6 * * * /usr/bin/env bash -lc 'cd /SÖKVÄG/TILL/KK1 && source venv/bin/activate && python main.py --csv data/sales.csv --db data/etl.db >> logs/cron_run.log 2>&1'

## VS Code (valfritt)
Lägg till `.vscode/settings.json` för att köra tester via Testing-panelen:

    {
      "python.testing.pytestEnabled": true,
      "python.testing.unittestEnabled": false,
      "python.testing.cwd": "${workspaceFolder}/KK1",
      "python.testing.pytestArgs": ["tests"]
    }

Välj interpreter: **Python: Select Interpreter** → din `venv`.

## Krav
- Python 3.11+ (fungerar på 3.12)
- Paket (se `requirements.txt`): `pandas`, `SQLAlchemy`, `pytest`

## Inlämning
Gör repot publikt på GitHub och lämna länken i Omniway. README, tester och loggning ska finnas med.
