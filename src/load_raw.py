import json
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)
cur = conn.cursor()

base = "data/raw/telegram_messages"

for date in os.listdir(base):
    for file in os.listdir(f"{base}/{date}"):
        with open(f"{base}/{date}/{file}", encoding="utf-8") as f:
            for line in f:
                d = json.loads(line)
                cur.execute(
                    """
                    INSERT INTO raw.telegram_messages
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                    """,
                    (
                        d["message_id"],
                        d["channel_name"],
                        d["message_date"],
                        d["message_text"],
                        d["views"],
                        d["forwards"],
                        d["has_media"],
                        d["image_path"]
                    )
                )

conn.commit()
cur.close()
conn.close()
