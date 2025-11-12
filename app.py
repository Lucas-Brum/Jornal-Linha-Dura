import json
from src.get_news import NewsAPI
from src.data_manager import DBManager
from src.configs import API_TOKEN, THE_NEWS_API_TOP_STORIES

if __name__ == "__main__":
    news_api = NewsAPI()
    json = news_api.get_top_stories(API_TOKEN, THE_NEWS_API_TOP_STORIES)
    title = news_api.get_title(json)
    url = news_api.get_url(json)
    html = news_api.get_html_news(url)
    texto = NewsAPI.get_article_text(url)

    DBManager.db(
        db="news",
        table="news",
        coluns=["titulo", "url", "texto"],
        data=[(title, url, texto)]
    )