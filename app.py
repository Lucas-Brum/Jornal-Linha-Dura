import json
from src.get_news import NewsAPI

if __name__ == "__main__":
    news_api = NewsAPI()
    news = news_api.get_top_stories(limit=1)
    print(json.dumps(news, indent=2, ensure_ascii=False))
