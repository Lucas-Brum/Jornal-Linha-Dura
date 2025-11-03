from src.ReadFile import ReadFile

THE_NEWS_API_TOP_STORIES = "https://api.thenewsapi.com/v1/news/top"
API_TOKEN = ReadFile("secrets/secrets.txt").read_file()