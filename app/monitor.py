from telethon import TelegramClient, events
from config.settings import API_ID, API_HASH, SESSION_NAME, KEYWORDS, TARGET_CHANNEL_IDS
from app.router import route_message

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

@client.on(events.NewMessage)
async def handler(event):
    text = event.message.message.lower()
    if any(keyword.lower() in text for keyword in KEYWORDS):
        await route_message(event)

def run():
    print("Starting Telegram Monitor...")
    client.start()
    client.run_until_disconnected()
