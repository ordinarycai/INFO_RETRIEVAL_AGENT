def log_tool(message):
    """
    打印工具调用日志
    """
    print(f"[Tool] {message}")


def log_llm(message):
    """
    打印 LLM 调用日志
    """
    print(f"[LLM] {message}")


def log_error(message):
    """
    打印错误日志
    """
    print(f"[Error] {message}")