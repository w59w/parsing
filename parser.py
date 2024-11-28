import requests
from bs4 import BeautifulSoup

BASE_URL = "http://quotes.toscrape.com"


def parse_quotes():

    all_quotes = []

    next_page = "/page/1/"

    while next_page:
        print(f"Парсим страницу: {BASE_URL}{next_page}")
        response = requests.get(BASE_URL + next_page)
        soup = BeautifulSoup(response.text, 'html.parser')

        quotes = soup.find_all('div', class_='quote')

        for quote in quotes:
            text = quote.find('span', class_='text').get_text(strip=True)
            author = quote.find('small', class_='author').get_text(strip=True)
            tags = [tag.get_text(strip=True) for tag in quote.find_all('a', class_='tag')]
            author_url = BASE_URL + quote.find('a')['href']

            all_quotes.append({
                "text": text,
                "author": author,
                "tags": tags,
                "author_url": author_url
            })

        next_btn = soup.find('li', class_='next')
        next_page = next_btn.find('a')['href'] if next_btn else None

    return all_quotes


if __name__ == "__main__":
    quotes_data = parse_quotes()

    for i, quote in enumerate(quotes_data[:5], 1):
        print(f"Цитата {i}:")
        print(f"  Текст: {quote['text']}")
        print(f"  Автор: {quote['author']}")
        print(f"  Теги: {', '.join(quote['tags'])}")
        print(f"  Ссылка на автора: {quote['author_url']}")
        print("-" * 50)

    with open("quotes.json", "w", encoding="utf-8") as file:
        import json

        json.dump(quotes_data, file, ensure_ascii=False, indent=4)

