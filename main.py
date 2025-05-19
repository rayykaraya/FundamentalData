from utils.extract import fetch_data
from utils.transform import clean_data
from utils.load import save_to_csv, save_to_gsheet, save_to_postgresql

def main():
    print("Mulai proses scraping...")
    raw = fetch_data()  # Menghasilkan DataFrame

    print("Mulai proses cleaning...")
    cleaned = clean_data(raw)  # Terima DataFrame dan kembalikan DataFrame bersih

    print("Contoh hasil bersih:")
    print(cleaned.head())
    print(f"Total data akhir: {len(cleaned)}")

    # Simpan ke CSV
    save_to_csv(cleaned, 'products.csv')

    # Simpan ke Google Sheets
    save_to_gsheet(cleaned, spreadsheet_id='1UXyc_ulWQZkK6rXhelkvYcbTDK5EkA4yfDtFEdb18G8')


    # Simpan ke PostgreSQL
    save_to_postgresql(
        cleaned,
        db_name="produk",
        user="datauser",
        password="1412",
        host="localhost",
        port=5432,
        table_name="fashion_products",
        mode="replace"
    )

if __name__ == '__main__':
    main()

