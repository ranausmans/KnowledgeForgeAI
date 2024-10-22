import os
from newsapi import NewsApiClient
from typing import List, Dict

class NewsAPIClient:
    def __init__(self):
        self.api_key = os.getenv("NEWS_API_KEY")
        self.newsapi = NewsApiClient(api_key=self.api_key)

    def fetch_articles(self, query: str, from_date: str, to_date: str, language: str = "en", page_size: int = 5) -> List[Dict]:
        all_articles = self.newsapi.get_everything(q=query,
                                                   from_param=from_date,
                                                   to=to_date,
                                                   language=language,
                                                   sort_by='relevancy',
                                                   page_size=page_size)
        
        return all_articles.get("articles", [])
