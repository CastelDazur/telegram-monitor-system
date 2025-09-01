from config.settings import TARGET_CHANNEL_IDS

async def route_message(event):
    # Здесь можно добавить отправку в каналы через client.send_message
    print(f"[MATCH] {event.chat.title}: {event.message.message}")

