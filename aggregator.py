import feedparser
import json
from datetime import datetime

# Lista extendida de feeds RSS de la industria IA y tecnología
FEEDS = {
    # Laboratorios e Investigadores Principales
    "OpenAI": "https://openai.com/news/rss.xml",
    "Google DeepMind": "https://deepmind.google/blog/rss.xml",
    "Google AI Research": "https://blog.research.google/atom.xml",
    "Meta AI": "https://ai.meta.com/blog/rss/", 
    "Anthropic": "https://www.anthropic.com/news/rss",
    "Hugging Face": "https://huggingface.co/blog/feed.xml",
    "Microsoft Research": "https://www.microsoft.com/en-us/research/feed/",
    "Microsoft AI": "https://blogs.microsoft.com/ai/feed/",
    "Apple Machine Learning": "https://machinelearning.apple.com/rss.xml",
    "AWS Machine Learning": "https://aws.amazon.com/blogs/machine-learning/feed/",
    "Google Cloud AI": "https://cloudblog.withgoogle.com/products/ai-machine-learning/rss/",
    "IBM Research": "https://research.ibm.com/blog/rss",
    "NVIDIA Blog": "https://blogs.nvidia.com/feed/",
    "NVIDIA Developer": "https://developer.nvidia.com/blog/feed/",
    "Intel AI": "https://blogs.intel.com/technology/category/artificial-intelligence/feed/",
    "Cohere": "https://txt.cohere.com/rss/",
    "Stability AI": "https://stability.ai/news?format=rss",
    "BAIR (Berkeley)": "https://bair.berkeley.edu/blog/feed.xml",
    "Stanford HAI": "https://hai.stanford.edu/news/feed",
    "MIT News AI": "https://news.mit.edu/rss/topic/artificial-intelligence2",
    
    # Publicaciones Técnicas y Científicas (ArXiv)
    "ArXiv (cs.AI)": "http://export.arxiv.org/rss/cs.AI",
    "ArXiv (cs.CL)": "http://export.arxiv.org/rss/cs.CL",
    "ArXiv (cs.CV)": "http://export.arxiv.org/rss/cs.CV",
    "ArXiv (cs.LG)": "http://export.arxiv.org/rss/cs.LG",
    "ArXiv (cs.NE)": "http://export.arxiv.org/rss/cs.NE",
    "ArXiv (cs.RO)": "http://export.arxiv.org/rss/cs.RO",
    
    # Blogs de Científicos y Data Science
    "Karpathy Blog": "https://karpathy.github.io/feed.xml",
    "Lilian Weng": "https://lilianweng.github.io/index.xml",
    "Sebastian Ruder": "https://ruder.io/rss/",
    "Jay Alammar": "https://jalammar.github.io/feed.xml",
    "Fast.ai": "https://www.fast.ai/index.xml",
    "Towards Data Science": "https://medium.com/feed/towards-data-science",
    "Analytics Vidhya": "https://www.analyticsvidhya.com/feed/",
    "Machine Learning Mastery": "https://machinelearningmastery.com/feed/",
    "KDnuggets": "https://www.kdnuggets.com/feed",
    "Data Science Central": "https://www.datasciencecentral.com/feed/",
    "Analytics India Mag": "https://analyticsindiamag.com/feed/",
    "Towards AI": "https://towardsai.net/feed",
    "SmartData Collective": "https://www.smartdatacollective.com/feed/",
    "DataCamp": "https://www.datacamp.com/tutorial/rss.xml",
    "Springboard AI": "https://www.springboard.com/blog/category/ai-machine-learning/feed/",
    
    # Revistas de Noticias de Tecnología e IA (Tier 1)
    "TechCrunch AI": "https://techcrunch.com/category/artificial-intelligence/feed/",
    "The Verge AI": "https://www.theverge.com/rss/artificial-intelligence/index.xml",
    "Wired AI": "https://www.wired.com/feed/tag/ai/latest/rss",
    "MIT Technology Review": "https://www.technologyreview.com/topic/artificial-intelligence/feed/",
    "VentureBeat AI": "https://venturebeat.com/category/ai/feed/",
    "ZDNet AI": "https://www.zdnet.com/topic/artificial-intelligence/rss.xml",
    "MarkTechPost": "https://www.marktechpost.com/feed/",
    "Unite.ai": "https://www.unite.ai/feed/",
    "Artificial Intelligence News": "https://www.artificialintelligence-news.com/feed/",
    "AI Business": "https://aibusiness.com/rss.xml",
    
    # Revistas de Tecnología Expandidas
    "Ars Technica AI": "https://arstechnica.com/tag/ai/feed/",
    "Singularity Hub": "https://singularityhub.com/tag/artificial-intelligence/feed/",
    "Futurism AI": "https://futurism.com/categories/artificial-intelligence/feed",
    "ScienceDaily AI": "https://www.sciencedaily.com/rss/computers_math/artificial_intelligence.xml",
    "ReadWrite AI": "https://readwrite.com/category/ai/feed/",
    "SiliconANGLE AI": "https://siliconangle.com/category/ai/feed/",
    "InfoQ AI/ML": "https://feed.infoq.com/ai-ml/news",
    "Computerworld AI": "https://www.computerworld.com/category/artificial-intelligence/index.rss",
    "InfoWorld AI": "https://www.infoworld.com/category/machine-learning/index.rss",
    "TechRepublic AI": "https://www.techrepublic.com/rss/artificial-intelligence/",
    "Hackaday AI": "https://hackaday.com/category/artificial-intelligence/feed/",
    "GeekWire AI": "https://www.geekwire.com/category/ai-machine-learning/feed/",
    "DZone AI": "https://feeds.dzone.com/ai",
    "TNW Neural": "https://thenextweb.com/neural/feed",
    "Gizmodo AI": "https://gizmodo.com/c/artificial-intelligence/rss",
    "Nature AI": "https://www.nature.com/subjects/artificial-intelligence.rss",
    
    # Comunidades de Desarrollo y Substack de IA
    "Hacker Noon AI": "https://hackernoon.com/feed/tag/ai",
    "Hacker Noon ML": "https://hackernoon.com/feed/tag/machine-learning",
    "Hashnode AI": "https://hashnode.com/n/ai/rss",
    "Dev.to AI": "https://dev.to/feed/tag/ai",
    "Dev.to ML": "https://dev.to/feed/tag/machinelearning",
    "Import AI": "https://jackclark.substack.com/feed",
    "The Sequence": "https://thesequence.substack.com/feed",
    "Latent Space": "https://www.latent.space/feed",
    "Interconnects": "https://www.interconnects.ai/feed",
    "Understanding AI": "https://www.understandingai.org/feed",
    "AI Snake Oil": "https://www.aisnakeoil.com/feed",
    "Scott Aaronson": "https://scottaaronson.blog/?feed=rss2",
    "Gary Marcus": "https://garymarcus.substack.com/feed",
    "AI Supremacy": "https://aisupremacy.substack.com/feed",
    "AI Breakfast": "https://aibreakfast.substack.com/feed",
    "Zvi's Blog": "https://thezvi.substack.com/feed",
    
    # Reddit (Comunidades Open Source & Charla)
    "r/MachineLearning": "https://www.reddit.com/r/MachineLearning/.rss",
    "r/ArtificialIntelligence": "https://www.reddit.com/r/ArtificialIntelligence/.rss",
    "r/LocalLLaMA": "https://www.reddit.com/r/LocalLLaMA/.rss",
    "r/singularity": "https://www.reddit.com/r/singularity/.rss",
    "r/OpenAI": "https://www.reddit.com/r/OpenAI/.rss",
    
    # Más Publicaciones Globales 
    "O'Reilly Radar": "https://www.oreilly.com/radar/feed/",
    "Emerj": "https://emerj.com/feed/",
    "Topbots": "https://www.topbots.com/feed/",
    "AI Trends": "https://www.aitrends.com/feed/",
    "Forbes AI": "https://www.forbes.com/artificial-intelligence/feed/",
    "Datanami": "https://www.datanami.com/feed/"
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
