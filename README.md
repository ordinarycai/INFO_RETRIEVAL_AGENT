# Info Retrieval Agent

一个基于 LLM 的信息检索与分析 Agent 项目。

本项目可以从 Hacker News 抓取新闻列表，支持用户围绕新闻进行多轮提问，并可以读取指定新闻链接的正文内容，调用大语言模型进行总结、筛选和分析。

## 项目功能

- 抓取 Hacker News 首页新闻
- 展示新闻标题和链接
- 支持用户连续提问
- 支持对话记忆
- 支持读取指定编号新闻正文
- 支持正文总结和关键信息提取
- 支持工具调用日志
- 支持基础错误处理
- 使用配置文件统一管理模型、新闻数量、超时时间等参数

## 技术栈

- Python
- OpenAI API
- Requests
- BeautifulSoup4
- python-dotenv

## 项目结构

```text
info_retrieval_agent/
│
├── main.py
├── config.py
├── requirements.txt
├── .env
├── .gitignore
├── README.md
│
├── tools/
│   ├── __init__.py
│   ├── news_fetcher.py
│   └── article_reader.py
│
├── agent/
│   ├── __init__.py
│   └── llm_agent.py
│
└── utils/
    ├── __init__.py
    └── logger.py
