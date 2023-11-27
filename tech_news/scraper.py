import requests
import time
import parsel
from tech_news.database import create_news


# Requisito 1
def fetch(url):
    headers = {"user-agent": "Fake user-agent"}

    try:
        time.sleep(1)
        response = requests.get(url, headers=headers, timeout=3)

        if response.status_code == 200:
            return response.text
        else:
            return None
    except requests.Timeout:
        return None


# Requisito 2
def scrape_updates(html_content):
    if html_content:
        selector = parsel.Selector(text=html_content)
        updates = selector.css(".entry-title a::attr(href)").getall()
        return updates
    else:
        return []


# Requisito 3
def scrape_next_page_link(html_content):
    selector = parsel.Selector(text=html_content)
    next_page_link = selector.css("a.next::attr(href)").get()
    if next_page_link:
        return next_page_link
    else:
        return None


# Requisito 4
def scrape_news(html_content):
    selector = parsel.Selector(text=html_content)

    return {
        "url": selector.css("link[rel=canonical]::attr(href)").get(),
        "title": selector.css(".entry-title::text").get().strip(),
        "timestamp": selector.css(".meta-date::text").get(),
        "writer": selector.css(".fn a::text").get().strip(),
        "reading_time": int(selector.css(
            ".meta-reading-time::text").get()[0:2]),
        "summary": "".join(selector.css(
            "div.entry-content > p:first-of-type *::text").getall()).strip(),
        "category": selector.css(".category-style .label::text").get(),
    }


# Requisito 5
def get_tech_news(amount):
    url = "https://blog.betrybe.com/"
    html = fetch(url)
    news_list = []

    while amount > len(news_list):
        if html:
            update = scrape_updates(html)
            news_list.extend(update)
            nextpage = scrape_next_page_link(html)
            url = nextpage

    news_itens = news_list[:amount]
    scraped = [scrape_news(fetch(news)) for news in news_itens]

    create_news(scraped)
    return scraped
