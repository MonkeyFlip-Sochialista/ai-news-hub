import feedparser
import json
from datetime import datetime

# Lista extendida de feeds RSS de la industria IA y tecnología
FEEDS = {
    "OpenAI": "https://openai.com/news/rss.xml",
    "Google DeepMind": "https://deepmind.google/blog/rss.xml",
    "Hugging Face": "https://huggingface.co/blog/feed.xml",
    "Google AI": "https://blog.research.google/atom.xml",
    "AWS Machine Learning": "https://aws.amazon.com/blogs/machine-learning/feed/",
    "Microsoft AI": "https://blogs.microsoft.com/ai/feed/",
    "NVIDIA Blog": "https://blogs.nvidia.com/feed/",
    "Meta AI": "https://ai.meta.com/blog/rss/", 
    "Anthropic": "https://www.anthropic.com/news/rss",
    "TechCrunch AI": "https://techcrunch.com/category/artificial-intelligence/feed/"
}

def fetch_news():
    news_list = []
    for source, url in FEEDS.items():
        feed = feedparser.parse(url)
        for entry in feed.entries[:8]: # Tomar las 8 más recientes por fuente
            # Extract basic text for description without tags to avoid breaking layout
            summary = entry.get("summary", "")
            # Limpiar HTML básico
            import re
            clean_summary = re.sub('<[^<]+?>', '', summary).strip()
            if len(clean_summary) > 200:
                clean_summary = clean_summary[:197] + "..."

            news_list.append({
                "title": entry.title,
                "link": entry.link,
                "date": entry.get("published", datetime.now().isoformat()),
                "source": source,
                "description": clean_summary
            })
    
    # Ordenar por fecha (asumiendo formato compatible)
    news_list.sort(key=lambda x: x['date'], reverse=True)
    
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(news_list, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    fetch_news()
