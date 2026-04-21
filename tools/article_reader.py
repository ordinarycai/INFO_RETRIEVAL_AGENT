import requests
from bs4 import BeautifulSoup

from utils.logger import log_tool, log_error


def fetch_article_content(url):
    """
    访问新闻链接，并尝试提取正文内容
    """
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    log_tool(f"正在访问文章链接：{url}")

    try:
        response = requests.get(url, headers=headers, timeout=10)
    except requests.RequestException as e:
        log_error(f"文章请求失败：{e}")
        return {
            "success": False,
            "content": "",
            "message": f"文章请求失败：{e}"
        }

    if response.status_code != 200:
        log_error(f"文章请求失败，状态码：{response.status_code}")
        return {
            "success": False,
            "content": "",
            "message": f"文章请求失败，状态码：{response.status_code}"
        }

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()

    paragraphs = soup.find_all("p")

    texts = []

    for p in paragraphs:
        text = p.get_text(strip=True)

        if len(text) > 30:
            texts.append(text)

    article_text = "\n".join(texts)

    if not article_text:
        body = soup.find("body")
        if body:
            article_text = body.get_text(separator="\n", strip=True)

    article_text = article_text[:6000]

    if not article_text:
        log_error("没有成功提取到正文内容")
        return {
            "success": False,
            "content": "",
            "message": "没有成功提取到正文内容"
        }

    log_tool(f"正文提取成功，共 {len(article_text)} 字")

    return {
        "success": True,
        "content": article_text,
        "message": "正文提取成功"
    }