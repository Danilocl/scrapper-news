from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import re
import unicodedata

app = Flask(__name__) 

def clean_source(source):
    normalized_source = unicodedata.normalize('NFKD', source).encode('ASCII', 'ignore').decode('utf-8')
    cleaned_source = normalized_source.lower().replace(".com", "").replace("mais", "").strip()
    return cleaned_source


def format_title(title):
    normalized_title = unicodedata.normalize('NFKD', title).encode('ASCII', 'ignore').decode('utf-8')
    formatted_title = re.sub(r'\s+', ' ', normalized_title)
    formatted_title = re.sub(r'[^\w\s]', '', formatted_title) 
    return formatted_title.strip()



def scrape_news():
    url = 'https://news.google.com/rss?hl=pt-BR&gl=BR&ceid=BR:pt-419'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        xml_content = response.content

        news_articles = []
        soup = BeautifulSoup(xml_content, 'xml')
        items = soup.find_all('item')

        for item in items:
            title = item.title.get_text().strip()
            link = item.link.get_text().strip()
            source = item.source.get_text().strip()

            news_articles.append({
                'title': format_title(title),
                'link': link,
                'source': clean_source(source)
            })

        return news_articles

    except requests.exceptions.RequestException as e:
        # Log the error and return an empty list
        print(f"Error accessing the page: {str(e)}")
        return []

@app.route('/')
def index():
    return "Welcome to the News Scraper API!"

@app.route('/news')
def get_news():
    news = scrape_news()
    if news:
        return jsonify(news)
    else:
        return jsonify({"error": "Failed to fetch news articles."}), 500

if __name__ == '__main__':
    app.run(debug=True)
