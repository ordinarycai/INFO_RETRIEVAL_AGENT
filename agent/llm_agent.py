from utils.logger import log_llm, log_error


def format_news(news_items):
    """
    把新闻列表整理成适合 LLM 阅读的文本
    """
    formatted = []

    for i, item in enumerate(news_items, 1):
        formatted.append(
            f"{i}. 标题：{item['title']}\n   链接：{item['link']}"
        )

    return "\n".join(formatted)


def build_system_prompt(news_items):
    """
    构建系统提示词
    """
    news_text = format_news(news_items)

    system_prompt = f"""
你是一个信息检索与分析 Agent。

你当前拥有以下从 Hacker News 抓取到的新闻列表：

{news_text}

你的任务：
1. 根据这些新闻标题和链接回答用户问题
2. 帮用户总结、筛选、分类、生成日报或做简单推荐
3. 如果用户要求读取某条新闻正文，你可以基于程序提供的正文内容进行总结
4. 在信息不足时，明确说明“仅根据当前信息无法判断”

重要限制：
1. 不要编造新闻正文
2. 不要假装你读取了没有提供给你的内容
3. 如果只有标题和链接，就只能基于标题和链接分析
4. 如果程序提供了正文内容，则可以基于正文总结
5. 输出要清晰、有条理，适合初学者阅读
"""

    return system_prompt


def ask_llm_with_memory(question, conversation_history, client):
    """
    普通带记忆问答
    """
    conversation_history.append({
        "role": "user",
        "content": question
    })

    log_llm("正在基于新闻列表生成回答...")

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=conversation_history
        )
    except Exception as e:
        log_error(f"LLM 调用失败：{e}")
        answer = "LLM 调用失败，请检查 API Key、网络连接或模型名称。"

        conversation_history.append({
            "role": "assistant",
            "content": answer
        })

        return answer

    answer = response.choices[0].message.content

    conversation_history.append({
        "role": "assistant",
        "content": answer
    })

    return answer


def summarize_article(question, article_result, news_item, conversation_history, client):
    """
    针对某条新闻正文进行总结
    """
    if not article_result["success"]:
        user_message = f"""
用户的问题是：
{question}

用户要求分析的新闻是：
标题：{news_item["title"]}
链接：{news_item["link"]}

但是程序没有成功抓取到正文。
失败原因：{article_result["message"]}

请你基于已有的标题和链接，给用户一个诚实回答。
要求：
1. 明确说明没有成功读取正文
2. 不要编造文章内容
3. 可以基于标题做非常有限的判断
"""
    else:
        user_message = f"""
用户的问题是：
{question}

用户要求分析的新闻是：
标题：{news_item["title"]}
链接：{news_item["link"]}

下面是程序抓取到的正文内容：
{article_result["content"]}

请你基于正文内容回答用户问题。

要求：
1. 先给出简短总结
2. 再提炼 3 个关键点
3. 如果正文抓取内容明显不完整，请提醒用户
4. 不要编造正文里没有的信息
"""

    conversation_history.append({
        "role": "user",
        "content": user_message
    })

    log_llm("正在基于文章正文生成回答...")

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=conversation_history
        )
    except Exception as e:
        log_error(f"LLM 调用失败：{e}")
        answer = "LLM 调用失败，请检查 API Key、网络连接或模型名称。"

        conversation_history.append({
            "role": "assistant",
            "content": answer
        })

        return answer

    answer = response.choices[0].message.content

    conversation_history.append({
        "role": "assistant",
        "content": answer
    })

    return answer