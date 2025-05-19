import sys
import os
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock

# Tambahkan path ke folder utama proyek
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import fungsi yang akan diuji
from utils.load import save_to_csv, save_to_gsheet, save_to_postgresql

@pytest.fixture
def sample_df():
    return pd.DataFrame({
        'col1': [1, 2],
        'col2': ['a', 'b']
    })

def test_save_to_csv_calls_to_csv(sample_df, tmp_path):
    filename = tmp_path / "test.csv"
    with patch.object(pd.DataFrame, 'to_csv') as mock_to_csv:
        save_to_csv(sample_df, filename=str(filename))
        mock_to_csv.assert_called_once_with(str(filename), index=False)

@patch('utils.load.gspread.authorize')
def test_save_to_gsheet(mock_authorize, sample_df):
    mock_client = MagicMock()
    mock_sheet = MagicMock()
    mock_spreadsheet = MagicMock()

    mock_client.open_by_key.return_value = mock_spreadsheet
    mock_spreadsheet.sheet1 = mock_sheet
    mock_authorize.return_value = mock_client

    spreadsheet_id = 'dummy_id'

    save_to_gsheet(sample_df, spreadsheet_id)

    mock_authorize.assert_called_once()
    mock_client.open_by_key.assert_called_once_with(spreadsheet_id)
    mock_sheet.clear.assert_called_once()
    mock_sheet.insert_rows.assert_called_once()

    # Cek argumen insert_rows yang diberikan, harus list berisi header + data
    args, kwargs = mock_sheet.insert_rows.call_args
    rows_passed = args[0]  # argumen pertama adalah list rows
    assert rows_passed[0] == list(sample_df.columns)
    assert rows_passed[1:] == sample_df.values.tolist()


@patch('utils.load.create_engine')
@patch('pandas.DataFrame.to_sql')
def test_save_to_postgresql_success(mock_to_sql, mock_create_engine, sample_df):
    # Siapkan mock engine
    mock_engine = MagicMock()
    mock_create_engine.return_value = mock_engine

    # Jalankan fungsi yang ingin dites
    save_to_postgresql(
        sample_df,
        db_name='test_db',
        user='test_user',
        password='test_pass',
        table_name='produk'  
    )

    mock_create_engine.assert_called_once()

    mock_to_sql.assert_called_once_with('produk', mock_engine, index=False, if_exists='replace')