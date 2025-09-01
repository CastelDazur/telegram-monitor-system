"""
example/test_run.py

Тестовый сценарий для проверки логики фильтрации и маршрутизации
без подключения к Telegram API.

Запуск:
    python example/test_run.py
"""

import asyncio
from app.filters import keyword_filter
from app.router import route_message

# 🎯 Тестовые входящие сообщения (эмуляция)
test_messages = [
    {"chat_title": "Crypto Chat", "text": "Новый проект запускается!"},
    {"chat_title": "Random Talk", "text": "Сегодня хорошая погода"},
    {"chat_title": "Startup Hub", "text": "Ищем инвесторов для стартапа"},
    {"chat_title": "Dev Community", "text": "Обсуждаем Python и AI"},
]

# 🔑 Ключевые слова для теста
keywords = ["проект", "инвесторов"]

# 🛠 Эмуляция объекта события Telethon
class FakeEvent:
    def __init__(self, chat_title: str, text: str):
        self.chat = type("Chat", (), {"title": chat_title})
        self.message = type("Message", (), {"message": text})

# 🚀 Запуск теста
if __name__ == "__main__":
    print("\n=== 🧪 Запуск тестового сценария Telegram Monitor System ===\n")
    for msg in test_messages:
        if keyword_filter(msg["text"], keywords):
            fake_event = FakeEvent(msg["chat_title"], msg["text"])
            asyncio.run(route_message(fake_event))
        else:
            print(f"[SKIP] {msg['chat_title']}: {msg['text']}")
    print("\n=== ✅ Тест завершён ===\n")
