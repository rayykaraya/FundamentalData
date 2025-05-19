import pytest
from unittest.mock import patch, Mock
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.extract import fetch_data

# Sample HTML yang mirip struktur asli supaya parser bs jalan
sample_html = """
<div class="collection-card">
  <div class="product-details">
    <h3 class="product-title">Test Product</h3>
    <div class="price-container">$100</div>
    <p>4.5 stars</p>
    <p>3 colors</p>
    <p>Size: M</p>
    <p>Gender: Male</p>
  </div>
</div>
"""

def mocked_requests_get(*args, **kwargs):
    mock_resp = Mock()
    # Status OK
    mock_resp.status_code = 200
    # Return HTML yang kita buat
    mock_resp.text = sample_html
    return mock_resp

@patch('utils.extract.requests.get', side_effect=mocked_requests_get)
def test_fetch_data(mock_get):
    df = fetch_data()
    # Cek dataframe tidak kosong
    assert not df.empty
    # Cek kolom
    expected_cols = {'Title', 'Price', 'Rating', 'Colors', 'Size', 'Gender'}
    assert expected_cols == set(df.columns)
    # Cek isi sesuai sample
    assert df.iloc[0]['Title'] == 'Test Product'
    assert df.iloc[0]['Price'] == '$100'
    assert df.iloc[0]['Rating'] == '4.5 stars'
    assert df.iloc[0]['Colors'] == '3 colors'
    assert df.iloc[0]['Size'] == 'Size: M'
    assert df.iloc[0]['Gender'] == 'Gender: Male'
    # Cek jumlah row (karena loop 50 kali, maka 50 baris)
    assert len(df) == 50
