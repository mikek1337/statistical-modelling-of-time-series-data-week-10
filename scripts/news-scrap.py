from newsapi import NewsApiClient
from dotenv import load_dotenv
import os
import json
load_dotenv()

newsapi = NewsApiClient(api_key=os.getenv("NEWS_API_KEY"))

def query_news(query:str, start_date:str, end_date:str):
    return newsapi.get_everything(q=query, from_param=start_date, to=end_date, sort_by="relevancy")

def scrap_news():
    start_date = "1987-05-20"
    end_date = "2022-11-14"
    query = "oil and gas"
    newsJSON = query_news(query, start_date, end_date)
    with open('data/news.json', 'w') as f:
        json.dump(newsJSON, f)


if __name__ == "__main__":
    scrap_news()
