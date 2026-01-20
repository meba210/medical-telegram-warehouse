import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

df = pd.read_csv("data/yolo_detections.csv")

conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)

cur = conn.cursor()

for _, row in df.iterrows():
    cur.execute(
        "INSERT INTO raw.image_detections VALUES (%s,%s,%s,%s)",
        (row.message_id, row.channel_name, row.detected_object, row.confidence_score)
    )

conn.commit()
cur.close()
conn.close()
