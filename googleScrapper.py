from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to the News Scraper API!"

@app.route('/news')
def scrape_news():
    url = 'https://news.google.com/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Lança uma exceção se a solicitação falhar
        
        html_content = response.content
        
        def format_title(title):    
            formatted_title = re.sub(r'\s+', ' ', title) 
            formatted_title = re.sub(r'[^\w\s]', '', formatted_title) 
            return formatted_title.strip() 

        def clean_source(source):    
            sourceL = source.lower()
            source = sourceL.replace(".com", "").replace("mais", "").strip()
            return source

        def raspaGoogleNews(html_content):
            news_articles = []    

            if html_content:
                soup = BeautifulSoup(html_content, 'html.parser')
                articles = soup.find_all('article')               
                for article in articles:        	
                    title = article.find_all('a')                        
                    link = article.find('a')['href'] if article.find('a') else None            
                    source = article.find_all('div')
                    if title and link:            	
                        last_a_tag = format_title(title[-1].get_text().strip())
                        source_div = clean_source(source[4].get_text().strip())
                        if not title[-1].get_text().strip():
                            last_a_tag = format_title(title[-2].get_text().strip())
                        news_articles.append({
                            'title': last_a_tag,
                            'link': f"https://news.google.com{link}" if link else None,
                            'source': source_div
                        })
                return news_articles
            else:
                return None

        result = raspaGoogleNews(html_content)
        if result:
            return jsonify(result)
        else:
            return jsonify({"error": "Não foi possível obter os dados."})

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Erro ao acessar a página: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
