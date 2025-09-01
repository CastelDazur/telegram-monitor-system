from telethon import TelegramClient, events
from config.settings import API_ID, API_HASH, SESSION_NAME, KEYWORDS

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

@client.on(events.NewMessage)
async def handler(event):
    message = event.message.message.lower()
    if any(keyword.lower() in message for keyword in KEYWORDS):
        print(f"[MATCH] {event.chat.title}: {message}")

def run():
    print("Starting Telegram Monitor...")
    client.start()
    client.run_until_disconnected()
