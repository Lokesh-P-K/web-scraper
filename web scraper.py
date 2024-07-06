import requests
from bs4 import BeautifulSoup
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

def fetch_page(url):
    response = requests.get(url)
    return response.text

def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    data = []

    table = soup.find('table')
    for row in table.find_all('tr'):
        cols = row.find_all('td')
        data.append([col.text.strip() for col in cols])

    return data

def main():
    base_url = 'http://example.com/page/'
    pages = 10  # Number of pages to scrape
    all_data = []

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(fetch_page, base_url + str(i)) for i in range(1, pages + 1)]
        for future in futures:
            html = future.result()
            page_data = parse_html(html)
            all_data.extend(page_data)

    headers = ['Column1', 'Column2', 'Column3']  # Replace with actual column names
    df = pd.DataFrame(all_data, columns=headers)
    df.to_csv('output.csv', index=False)
    print("Data saved to output.csv")

if __name__ == "__main__":
    main()
