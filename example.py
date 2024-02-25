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