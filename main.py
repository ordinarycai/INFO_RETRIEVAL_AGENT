import os
import re
from dotenv import load_dotenv
from openai import OpenAI

from tools.news_fetcher import get_news
from tools.article_reader import fetch_article_content
from agent.llm_agent import build_system_prompt, ask_llm_with_memory, summarize_article
from utils.logger import log_tool, log_error


def extract_article_index(question):
    """
    从用户问题中提取“第几条新闻”
    """
    match = re.search(r"第\s*(\d+)\s*条", question)

    if match:
        return int(match.group(1))

    return None


def create_openai_client():
    """
    创建 OpenAI 客户端
    """
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("没有读取到 OPENAI_API_KEY，请检查 .env 文件。")

    client = OpenAI(api_key=api_key)

    return client


def show_news(news_items):
    """
    打印新闻列表
    """
    print("\n抓取到的新闻：\n")

    for i, item in enumerate(news_items, 1):
        print(f"{i}. {item['title']}")
        print(f"   {item['link']}")


def main():
    client = create_openai_client()

    news_items = get_news()

    if not news_items:
        print("没有抓取到新闻，程序结束。")
        return

    show_news(news_items)

    conversation_history = [
        {
            "role": "system",
            "content": build_system_prompt(news_items)
        }
    ]

    print("\n" + "=" * 50)
    print("你现在可以连续提问，Agent 会记住前面的对话。")
    print("如果想读取某条新闻正文，可以这样问：")
    print("- 请读取第 3 条新闻并总结")
    print("- 帮我分析第 2 条")
    print("- 总结第 5 条新闻的主要内容")
    print("输入 exit / quit / 退出 可以结束程序。")
    print("=" * 50 + "\n")

    while True:
        question = input("请输入你的问题：").strip()

        if question.lower() in ["exit", "quit"] or question in ["退出", "结束"]:
            print("程序已结束。")
            break

        if not question:
            print("你还没有输入问题，请重新输入。\n")
            continue

        print()

        article_index = extract_article_index(question)

        if article_index is not None:
            log_tool(f"用户请求读取第 {article_index} 条新闻")

            if article_index < 1 or article_index > len(news_items):
                log_error(f"新闻编号无效：{article_index}")
                print(f"新闻编号无效，请输入 1 到 {len(news_items)} 之间的编号。\n")
                continue

            news_item = news_items[article_index - 1]

            article_result = fetch_article_content(news_item["link"])

            answer = summarize_article(
                question=question,
                article_result=article_result,
                news_item=news_item,
                conversation_history=conversation_history,
                client=client
            )
        else:
            answer = ask_llm_with_memory(
                question=question,
                conversation_history=conversation_history,
                client=client
            )

        print("\nAgent 回答：\n")
        print(answer)
        print("\n" + "-" * 50 + "\n")


if __name__ == "__main__":
    main()