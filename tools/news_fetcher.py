import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from utils.logger import log_tool, log_error


def get_news():
    """
    抓取 Hacker News 首页的前 8 条新闻标题和链接
    """
    url = "https://news.ycombinator.com/"

    log_tool("正在抓取 Hacker News 首页...")

    try:
        response = requests.get(url, timeout=10)
    except requests.RequestException as e:
        log_error(f"请求 Hacker News 失败：{e}")
        return []

    if response.status_code != 200:
        log_error(f"Hacker News 请求失败，状态码：{response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    news_items = []

    for item in soup.select(".titleline a")[:8]:
        title = item.get_text(strip=True)
        link = item.get("href")

        if not title or not link:
            continue

        full_link = urljoin(url, link)

        news_items.append({
            "title": title,
            "link": full_link
        })

    log_tool(f"新闻列表抓取成功，共 {len(news_items)} 条")

    return news_items