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
    "IBM Research": "https://research.ibm.com/blog/rss",
    "TechCrunch AI": "https://techcrunch.com/category/artificial-intelligence/feed/",
    "The Verge AI": "https://www.theverge.com/rss/artificial-intelligence/index.xml",
    "Wired AI": "https://www.wired.com/feed/tag/ai/latest/rss",
    "MIT Technology Review (AI)": "https://www.technologyreview.com/topic/artificial-intelligence/feed/",
    "VentureBeat AI": "https://venturebeat.com/category/ai/feed/",
    "KDnuggets": "https://www.kdnuggets.com/feed",
    "Unite.ai": "https://www.unite.ai/feed/",
    "Artificial Intelligence News": "https://www.artificialintelligence-news.com/feed/",
    "Cohere": "https://txt.cohere.com/rss/",
    "Stability AI": "https://stability.ai/news?format=rss",
    "Apple Machine Learning": "https://machinelearning.apple.com/rss.xml",
    "Google Cloud AI": "https://cloudblog.withgoogle.com/products/ai-machine-learning/rss/",
    "ZDNet AI": "https://www.zdnet.com/topic/artificial-intelligence/rss.xml",
    "MarkTechPost": "https://www.marktechpost.com/feed/",
    "AI Business": "https://aibusiness.com/rss.xml",
    "Towards Data Science": "https://medium.com/feed/towards-data-science",
    "Analytics Vidhya": "https://www.analyticsvidhya.com/feed/",
    "Machine Learning Mastery": "https://machinelearningmastery.com/feed/",
    "BAIR (Berkeley)": "https://bair.berkeley.edu/blog/feed.xml",
    "ArXiv (cs.AI)": "http://export.arxiv.org/rss/cs.AI"
}

IMPORTANT_KEYWORDS = [
    "gpt-4", "gpt-5", "claude 3", "claude 3.5", "llama 3", "gemini", 
    "alphafold", "sora", "midjourney", "breakthrough", "release", 
    "agi", "superintelligence", "open source", "million tokens", 
    "state of the art", "sota", "new model"
]

def fetch_news():
    news_list = []
    
    # Cargar histórico si existe
    import os
    if os.path.exists('data.json'):
        try:
            with open('data.json', 'r', encoding='utf-8') as f:
                news_list = json.load(f)
        except Exception:
            pass
            
    # Set con las URLs ya descargadas para evitar duplicados
    seen_links = {item['link'] for item in news_list}

    for source, url in FEEDS.items():
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries: # Tomar TODAS las que el feed ofrezca
                if entry.link in seen_links:
                    continue # Saltar si ya estaba en json
                
                summary = entry.get("summary", "")
                # Limpiar HTML básico
                import re
                clean_summary = re.sub('<[^<]+?>', '', summary).strip()
                if len(clean_summary) > 200:
                    clean_summary = clean_summary[:197] + "..."

                # check for importance
                is_important = False
                title_lower = entry.title.lower()
                if any(kw in title_lower for kw in IMPORTANT_KEYWORDS):
                    is_important = True

                news_list.append({
                    "title": entry.title,
                    "link": entry.link,
                    "date": entry.get("published", datetime.now().isoformat()),
                    "source": source,
                    "description": clean_summary,
                    "is_important": is_important
                })
        except Exception as e:
            print(f"Error fetching {source}: {e}")
    
    # Ordenar por fecha (asumiendo formato compatible)
    news_list.sort(key=lambda x: x['date'], reverse=True)
    
    # Quedarnos con el histórico acumulado masivo (2500 max)
    news_list = news_list[:2500]
    
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(news_list, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    fetch_news()
