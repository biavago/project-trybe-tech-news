from tech_news.database import search_news
from datetime import datetime


# Requisito 7
def search_by_title(title):
    result = []
    query = {"title": {"$regex": title, "$options": "i"}}
    news = search_news(query)

    for new in news:
        news_list_item = (new["title"], new["url"])
        result.append(news_list_item)

    return result


# Requisito 8
def search_by_date(date):
    # datetime.strptime(date_string, format)
    try:
        iso_format = datetime.strptime(date, "%Y-%m-%d").strftime("%d/%m/%Y")
    except ValueError:
        raise ValueError("Data inválida")

    result = []
    query = {"timestamp": iso_format}
    news = search_news(query)

    for new in news:
        news_list_item = (new["title"], new["url"])
        result.append(news_list_item)

    return result


# Requisito 9
def search_by_category(category):
    result = []
    query = {"category": {"$regex": category, "$options": "i"}}
    news = search_news(query)

    for new in news:
        news_list_item = (new["title"], new["url"])
        result.append(news_list_item)

    return result
