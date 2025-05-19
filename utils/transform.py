import pandas as pd
import re
import numpy as np
from datetime import datetime

def clean_data(raw_data):
    df = pd.DataFrame(raw_data)
    print(f"Data awal: {len(df)} baris")

    df = df[df['Title'] != 'Unknown Product']
    print(f"Setelah filter 'Unknown Product': {len(df)} baris")

    # Bersihkan price
    df['Price'] = df['Price'].str.replace(r'[^0-9.]', '', regex=True)
    df.loc[df['Price'] == '', 'Price'] = np.nan
    df['Price'] = df['Price'].astype(float)
    df = df.dropna(subset=['Price'])
    # Konversi ke Rupiah
    df['Price'] = df['Price'] * 16000
    print(f"Setelah bersihkan Price: {len(df)} baris")

    # Bersihkan Rating
    df = df[~df['Rating'].str.contains('Invalid', na=False)]
    df['Rating'] = df['Rating'].str.extract(r'([\d.]+)').astype(float)
    df = df.dropna(subset=['Rating'])
    print(f"Setelah bersihkan Rating: {len(df)} baris")

    # Bersihkan Colors, jika ada yang kosong isi dengan 0
    df['Colors'] = df['Colors'].str.extract(r'(\d+)')
    df['Colors'] = df['Colors'].fillna(0).astype(int)
    print(f"Setelah bersihkan Colors: {len(df)} baris")

    # Bersihkan Size dan Gender
    df['Size'] = df['Size'].str.replace('Size:', '').str.strip()
    df['Gender'] = df['Gender'].str.replace('Gender:', '').str.strip()

     # Menghapus data yang kosong
    df.dropna(inplace=True)
    print(f"Setelah bersihkan Null: {len(df)} baris")

    # Hapus duplikat
    before_dedup = len(df)
    df.drop_duplicates(inplace=True)
    print(f"Setelah hapus duplikat: {len(df)} baris (hapus {before_dedup - len(df)} baris)")

    df['Timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


    return df.reset_index(drop=True)
