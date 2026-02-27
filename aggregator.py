import feedparser
import json
from datetime import datetime
import os
import re

# ==============================================================================
# 1. MEGA-DICCIONARIO DE FUENTES RSS DE INTELIGENCIA ARTIFICIAL (100+ sitios)
# ==============================================================================
FEEDS = {
    # --- Laboratorios de IA y Gigantes Tech ---
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
    "Mistral AI": "https://mistral.ai/feed.xml",
    "Perplexity": "https://www.perplexity.ai/hub/feed",
    "Scale AI": "https://scale.com/blog/rss",
    "AI2 (Allen Institute)": "https://allenai.org/blog/rss",
    "EleutherAI": "https://blog.eleuther.ai/rss/",
    "RunwayML": "https://runwayml.com/blog/rss",

    # --- Universidades e Instituciones ---
    "BAIR (Berkeley)": "https://bair.berkeley.edu/blog/feed.xml",
    "Stanford HAI": "https://hai.stanford.edu/news/feed",
    "MIT News AI": "https://news.mit.edu/rss/topic/artificial-intelligence2",
    "CMU ML Blog": "https://blog.ml.cmu.edu/feed/",
    "Harvard AI": "https://computationalthinking.harvard.edu/feed/",
    "Oxford AI": "https://www.oii.ox.ac.uk/news-events/news/feed/",
    "Cambridge AI": "https://www.cst.cam.ac.uk/news/feed",
    "UCL AI Centre": "https://www.ucl.ac.uk/ai-centre/news/feed",
    "MILA (Quebec)": "https://mila.quebec/en/news/feed/",
    "Vector Institute": "https://vectorinstitute.ai/news/feed/",
    "Alan Turing Institute": "https://www.turing.ac.uk/news/feed",
    
    # --- Publicaciones Científicas (ArXiv) ---
    "ArXiv (cs.AI)": "http://export.arxiv.org/rss/cs.AI",
    "ArXiv (cs.CL)": "http://export.arxiv.org/rss/cs.CL",
    "ArXiv (cs.CV)": "http://export.arxiv.org/rss/cs.CV",
    "ArXiv (cs.LG)": "http://export.arxiv.org/rss/cs.LG",
    "ArXiv (cs.NE)": "http://export.arxiv.org/rss/cs.NE",
    "ArXiv (cs.RO)": "http://export.arxiv.org/rss/cs.RO",
    
    # --- Blogs de Mentes Brillantes y Data Science ---
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
    
    # --- Frameworks y Librerías Core ---
    "PyTorch Blog": "https://pytorch.org/blog/feed.xml",
    "TensorFlow Blog": "https://blog.tensorflow.org/feeds/posts/default?alt=rss",
    "Keras Blog": "https://keras.io/feed.xml",
    "Scikit-Learn Blog": "https://blog.scikit-learn.org/feed.xml",
    "OpenCV Blog": "https://opencv.org/blog/feed/",

    # --- Medios de Comunicación (Tier 1 en Tech) ---
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
    
    # --- Periodismo Internacional ---
    "Forbes AI": "https://www.forbes.com/artificial-intelligence/feed/",
    "BBC Tech": "http://feeds.bbci.co.uk/news/technology/rss.xml",
    "The Guardian AI": "https://www.theguardian.com/technology/artificialintelligenceai/rss",
    "NYT Tech": "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
    "The Register AI": "https://www.theregister.com/Offbeat/AI/headline.rss",
    
    # --- Comunidades y Substacks Destacados ---
    "r/MachineLearning": "https://www.reddit.com/r/MachineLearning/.rss",
    "r/ArtificialIntelligence": "https://www.reddit.com/r/ArtificialIntelligence/.rss",
    "r/LocalLLaMA": "https://www.reddit.com/r/LocalLLaMA/.rss",
    "Hacker Noon AI": "https://hackernoon.com/feed/tag/ai",
    "Hashnode AI": "https://hashnode.com/n/ai/rss",
    "Dev.to AI": "https://dev.to/feed/tag/ai",
    "Import AI (Jack Clark)": "https://jackclark.substack.com/feed",
    "The Sequence": "https://thesequence.substack.com/feed",
    "Latent Space": "https://www.latent.space/feed",
    "AI Snake Oil": "https://www.aisnakeoil.com/feed"
}


# ==============================================================================
# 2. SISTEMA DE DETECCIÓN INTELIGENTE
# ==============================================================================

IMPORTANT_KEYWORDS = [
    "gpt-4", "gpt-5", "claude 3", "claude 3.5", "llama 3", "gemini", 
    "alphafold", "sora", "midjourney", "breakthrough", "release", 
    "agi", "superintelligence", "open source", "million tokens", 
    "state of the art", "sota", "new model", "revolutionary"
]

CATEGORIES = {
    "💬 LLMs & NLP": ["llm", "llms", "gpt", "claude", "llama", "mistral", "gemini", "prompt", "nlp", "language model", "chatgpt"],
    "🤖 Robótica": ["robot", "robotics", "boston dynamics", "figure", "humanoid", "drone", "autonomous"],
    "👁️ Visión por Computador": ["vision", "image generation", "midjourney", "dall-e", "sora", "video generation", "diffusion", "stable diffusion"],
    "⚖️ Ética y Regulación": ["ethics", "policy", "regulation", "eu ai act", "bias", "safety", "alignment", "deepfake", "copyright"],
    "⚙️ Hardware de IA": ["gpu", "nvidia", "amd", "tpu", "silicon", "chip", "semiconductor", "cuda"]
}

# ==============================================================================
# 3. LÓGICA PRINCIPAL (ETL)
# ==============================================================================

def fetch_news():
    news_list = []
    
    # Cargar histórico si existe
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
            for entry in feed.entries[:15]: # Limitar a 15 por fuente por pasada para balancear (incluso las hiper-frecuentes)
                if entry.link in seen_links:
                    continue # Saltar si ya estaba en json
                
                summary = entry.get("summary", "")
                # Limpiar HTML básico
                clean_summary = re.sub('<[^<]+?>', '', summary).strip()
                if len(clean_summary) > 200:
                    clean_summary = clean_summary[:197] + "..."

                title_lower = entry.title.lower()
                desc_lower = clean_summary.lower()
                
                # Check for importance VIP badge
                is_important = any(kw in title_lower for kw in IMPORTANT_KEYWORDS)

                # Auto-Tagging System (Categorización Autónoma)
                tags = []
                for cat_name, keywords in CATEGORIES.items():
                    if any(kw in title_lower or kw in desc_lower for kw in keywords):
                        tags.append(cat_name)

                news_list.append({
                    "title": entry.title,
                    "link": entry.link,
                    "date": entry.get("published", datetime.now().isoformat()),
                    "source": source,
                    "description": clean_summary,
                    "is_important": is_important,
                    "tags": tags  # <-- NUEVA CARACTERÍSTICA EXTRAORDINARIA
                })
        except Exception as e:
            print(f"Error fetching {source}: {e}")
    
    # Ordenar por fecha 
    news_list.sort(key=lambda x: x['date'], reverse=True)
    
    # Quedarnos con el histórico acumulado masivo (2500 max)
    news_list = news_list[:2500]
    
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(news_list, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    fetch_news()
