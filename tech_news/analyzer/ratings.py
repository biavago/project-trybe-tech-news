import collections
from tech_news.database import db


# Requisito 10
def top_5_categories():
    categories = [news["category"] for news in db.news.find()]

    top_all = sorted(
        collections.Counter(categories).items(),
        key=lambda x: (-x[1], x[0]))[:5]

    return [category for category, _ in top_all]
