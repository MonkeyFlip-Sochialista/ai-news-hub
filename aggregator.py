import feedparser
import json
from datetime import datetime

# Lista de feeds RSS de confianza
FEEDS = {
    "OpenAI": "https://openai.com/news/rss.xml",
    "Google DeepMind": "https://deepmind.google/blog/rss.xml",
    "Hugging Face": "https://huggingface.co/blog/feed.xml"
}

def fetch_news():
    news_list = []
    for source, url in FEEDS.items():
        feed = feedparser.parse(url)
        for entry in feed.entries[:5]: # Tomar las 5 más recientes por fuente
            news_list.append({
                "title": entry.title,
                "link": entry.link,
                "date": entry.get("published", datetime.now().isoformat()),
                "source": source
            })
    
    # Ordenar por fecha (asumiendo formato compatible)
    news_list.sort(key=lambda x: x['date'], reverse=True)
    
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(news_list, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    fetch_news()
