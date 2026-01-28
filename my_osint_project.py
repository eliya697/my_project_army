from telethon import TelegramClient
from elasticsearch import Elasticsearch
import json
import re

es = Elasticsearch("http://localhost:9200")

api_id = 37136520
api_hash = "e020db40ff6610920b4bee616b4b2234"

with TelegramClient("my_session", api_id, api_hash) as client:

    channel = client.get_entity("ynet")
    messages = client.get_messages(channel, limit=100)

    all_my_messages = []
    for my_message in messages:

        if not my_message.text:
            continue

        text = my_message.text.strip()
        text = re.sub(r'http\S+', '', text)

        if not text:
            continue

        my_document = {"source" : "ynet", "message_id" : my_message.id,
                       "time" : str(my_message.date), "text" : text}
        all_my_messages.append(my_document)
        print(my_document)

with open("osint.json", "w", encoding="utf-8") as f:
    json.dump(all_my_messages, f, ensure_ascii=False, indent=2)
