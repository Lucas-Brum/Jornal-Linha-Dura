import requests
from src.configs import API_TOKEN, THE_NEWS_API_TOP_STORIES

class NewsAPI:
    def __init__(self):
        self.api_token = API_TOKEN
        self.the_news_api_top_stories = THE_NEWS_API_TOP_STORIES

    def get_top_stories(self, locale="br", language="pt", limit=1):
        params = {
            "locale": locale,
            "language": language,
            "limit": limit,
            "api_token": self.api_token
        }

        resp = requests.get(self.the_news_api_top_stories, params=params)
        return resp.json()