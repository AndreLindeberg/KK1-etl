import os
import logging
import pandas as pd
import pytest
from etl import run_etl


# Test 1
def test_missing_csv(tmp_path, caplog):
    caplog.set_level(logging.ERROR, logger='csv_etl')

    fake_csv = tmp_path / 'saknas.csv'
    db_path = tmp_path / 'etl.db'

    with pytest.raises(FileNotFoundError):
        run_etl(csv_path=str(fake_csv), db_path=str(db_path))

    assert 'Hittar inte CSV-filen' in caplog.text



# Test 2
def test_invalid_columns(tmp_path, caplog):
    caplog.set_level(logging.ERROR, logger="csv_etl")

    csv_file = tmp_path / "bad.csv"
    pd.DataFrame({
        "date": ["2025-01-01"],   # Unit_price saknas
        "sku": ["A-001"],
        "units": [5]
    }).to_csv(csv_file, index=False)

    db_path = tmp_path / "etl.db"
    with pytest.raises(ValueError):
        run_etl(csv_path=str(csv_file), db_path=str(db_path))

    assert "CSV saknar kolumner" in caplog.text




#Test 3
def test_null_values(tmp_path, caplog):
    caplog.set_level(logging.WARNING, logger="csv_etl") 

    csv_file = tmp_path / "null.csv"
    pd.DataFrame({
        "date": ["2025-01-01"],
        "sku": ["A-001"],
        "units": [5],
        "unit_price": [None]
    }).to_csv(csv_file, index=False)

    db_path = tmp_path / "etl.db"
    rows = run_etl(csv_path=str(csv_file), db_path=str(db_path))

    assert rows == 1
    assert os.path.exists(db_path)
    assert "Null-värden hittades i units/unit_price" in caplog.text