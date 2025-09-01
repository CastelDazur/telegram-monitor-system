def keyword_filter(message: str, keywords: list[str]) -> bool:
    return any(kw.lower() in message.lower() for kw in keywords)

