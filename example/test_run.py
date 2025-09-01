from app.filters import keyword_filter
from app.router import route_message

# Эмуляция входящих сообщений
test_messages = [
    {"chat_title": "Crypto Chat", "text": "Новый проект запускается!"},
    {"chat_title": "Random Talk", "text": "Сегодня хорошая погода"},
    {"chat_title": "Startup Hub", "text": "Ищем инвесторов для стартапа"},
]

# Ключевые слова для теста
keywords = ["проект", "инвесторов"]

class FakeEvent:
    def __init__(self, chat_title, text):
        self.chat = type("Chat", (), {"title": chat_title})
        self.message = type("Message", (), {"message": text})

# Прогон теста
for msg in test_messages:
    if keyword_filter(msg["text"], keywords):
        fake_event = FakeEvent(msg["chat_title"], msg["text"])
        # Здесь мы просто выводим в консоль
        import asyncio
        asyncio.run(route_message(fake_event))
