import os
import json
import logging
from datetime import datetime
from dotenv import load_dotenv
from telethon import TelegramClient

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

channels = [
    "chemed",
    "lobelia4cosmetics",
    "tikvahpharma"
]

os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

client = TelegramClient("session", api_id, api_hash)

async def scrape():
    today = datetime.now().strftime("%Y-%m-%d")
    out_dir = f"data/raw/telegram_messages/{today}"
    os.makedirs(out_dir, exist_ok=True)

    for channel in channels:
        logging.info(f"Scraping {channel}")
        img_dir = f"data/raw/images/{channel}"
        os.makedirs(img_dir, exist_ok=True)

        async for msg in client.iter_messages(channel, limit=300):
            data = {
                "message_id": msg.id,
                "channel_name": channel,
                "message_date": msg.date.isoformat() if msg.date else None,
                "message_text": msg.text,
                "views": msg.views,
                "forwards": msg.forwards,
                "has_media": bool(msg.photo),
                "image_path": None
            }

            if msg.photo:
                img_path = f"{img_dir}/{msg.id}.jpg"
                await client.download_media(msg.photo, img_path)
                data["image_path"] = img_path

            with open(f"{out_dir}/{channel}.json", "a", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False)
                f.write("\n")

if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(scrape())
