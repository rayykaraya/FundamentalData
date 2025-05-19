import pandas as pd
import pytest
import sys
import os
from datetime import datetime

# Tambahkan path ke folder utama proyek agar bisa impor modul dari utils
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.transform import clean_data

# Sample raw data sebagai fixture
@pytest.fixture
def sample_raw_data():
    return [
        {'Title': 'Product A', 'Price': '$120.00', 'Rating': '4.5 stars', 'Colors': '3 colors', 'Size': 'Size: M', 'Gender': 'Gender: Male'},
        {'Title': 'Unknown Product', 'Price': 'Free', 'Rating': 'Invalid', 'Colors': '', 'Size': '', 'Gender': ''},
        {'Title': 'Product B', 'Price': '150', 'Rating': '5', 'Colors': '5', 'Size': 'Size: L', 'Gender': 'Gender: Female'},
        {'Title': 'Product C', 'Price': '200', 'Rating': '3.0 stars', 'Colors': '2', 'Size': 'Size: S', 'Gender': 'Gender: Male'},
        {'Title': 'Product C', 'Price': '200', 'Rating': '3.0 stars', 'Colors': '2', 'Size': 'Size: S', 'Gender': 'Gender: Male'}
    ]

# 1. Tes bahwa unknown product dan data invalid dibuang
def test_clean_data_removes_unknown_and_invalid(sample_raw_data):
    df = clean_data(sample_raw_data)
    assert 'Unknown Product' not in df['Title'].values
    assert not df['Price'].isnull().any()
    assert not df['Rating'].isnull().any()
    assert 'Timestamp' in df.columns

# 2. Tes bahwa Price dan Rating bertipe float
def test_clean_data_price_and_rating_types(sample_raw_data):
    df = clean_data(sample_raw_data)
    assert pd.api.types.is_float_dtype(df['Price']), "Price bukan float"
    assert pd.api.types.is_float_dtype(df['Rating']), "Rating bukan float"

# 3. Tes Colors terisi 0 jika kosong dan tipe integer
def test_clean_data_colors_filled(sample_raw_data):
    df = clean_data(sample_raw_data)
    assert pd.api.types.is_integer_dtype(df['Colors']), "Colors bukan integer"
    assert (df['Colors'] >= 0).all(), "Colors harus >= 0"

# 4. Tes apakah duplikat masih ada (clean_data tidak menghapus duplikat)
def test_clean_data_duplicates(sample_raw_data):
    df = clean_data(sample_raw_data)
    assert not df.duplicated().any(), "Masih ada duplikat setelah cleaning"
    assert len(df) == len(df.drop_duplicates()), "Duplikat belum sepenuhnya dihapus"
    
# 5. Tes Size dan Gender sudah dibersihkan dari label awal
def test_size_gender_strip(sample_raw_data):
    df = clean_data(sample_raw_data)
    assert all(not str(val).startswith('Size:') for val in df['Size']), "Size masih mengandung 'Size:'"
    assert all(not str(val).startswith('Gender:') for val in df['Gender']), "Gender masih mengandung 'Gender:'"

# 6. Tes struktur kolom output
def test_clean_data_output_structure(sample_raw_data):
    df = clean_data(sample_raw_data)
    expected_columns = ['Title', 'Price', 'Rating', 'Colors', 'Size', 'Gender', 'Timestamp']
    for col in expected_columns:
        assert col in df.columns, f"Kolom {col} tidak ditemukan"
    assert len(df) > 0, "DataFrame kosong setelah cleaning"
