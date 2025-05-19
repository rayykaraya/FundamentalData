import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from sqlalchemy.exc import SQLAlchemyError

# Simpan ke CSV 
def save_to_csv(df, filename="products.csv"):
    df.to_csv(filename, index=False)
    print(f"Data berhasil disimpan ke {filename}")

# Simpan ke Gsheet
def save_to_gsheet(df, spreadsheet_id):
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name("google-sheets-api.json", scope)
    client = gspread.authorize(creds)

    try:
        sheet = client.open_by_key(spreadsheet_id).sheet1
    except gspread.SpreadsheetNotFound:
        # Kalau spreadsheet tidak ditemukan, bisa buat baru tapi ini jarang karena ID spesifik
        sheet = client.create("New Spreadsheet").sheet1

    sheet.clear()
    sheet.insert_rows([df.columns.values.tolist()] + df.values.tolist())
    print("Data berhasil disimpan ke Google Sheets")


# Simpan ke PostgreeSQL
def save_to_postgresql(
    df,
    db_name="produk",                  
    user="datauser",                  
    password="1412",                 
    host="localhost",
    port=5432,
    table_name="fashion_products",    
    mode="replace"                    
):
    try:
        # Buat koneksi engine
        db_url = f'postgresql://{user}:{password}@{host}:{port}/{db_name}'
        engine = create_engine(db_url)  # , echo=True jika ingin debug

        # Cek koneksi
        with engine.connect() as conn:
            print("[INFO] Koneksi ke PostgreSQL berhasil")

        # Simpan DataFrame ke PostgreSQL
        df.to_sql(table_name, engine, index=False, if_exists=mode)
        print(f"[SUCCESS] Data disimpan ke PostgreSQL (tabel '{table_name}')")

    except SQLAlchemyError as e:
        print(f"[ERROR] Gagal menyimpan ke PostgreSQL: {e}")