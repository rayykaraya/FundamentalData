import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

def get_text(el):
    return el.text.strip() if el else '-'

def fetch_data():
    all_data = []
    for page in range(1, 51):
        print(f"Scraping halaman {page}...")
        if page == 1:
            url = "https://fashion-studio.dicoding.dev/"
        else:
            url = f"https://fashion-studio.dicoding.dev/page{page}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"}

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Gagal akses halaman {page}")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        cards = soup.find_all('div', class_='collection-card')

        for card in cards:
            detail = card.find('div', class_='product-details')
            if not detail:
                continue

            title = get_text(detail.find('h3', class_='product-title'))
            price = get_text(detail.find('div', class_='price-container'))

            paras = detail.find_all('p')
            rating = get_text(paras[0]) if len(paras) > 0 else '-'
            colors = get_text(paras[1]) if len(paras) > 1 else '-'
            size = get_text(paras[2]) if len(paras) > 2 else '-'
            gender = get_text(paras[3]) if len(paras) > 3 else '-'

            all_data.append({
                'Title': title,
                'Price': price,
                'Rating': rating,
                'Colors': colors,
                'Size': size,
                'Gender': gender
            })

        time.sleep(0.5)

    df = pd.DataFrame(all_data)
    return df

if __name__ == "__main__":
    df = fetch_data()
    print(df.head())
    print(f"Total data: {len(df)}")



