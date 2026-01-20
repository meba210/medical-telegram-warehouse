from fastapi import FastAPI
from sqlalchemy import text
from api.database import engine

app = FastAPI(title="Medical Telegram Analytics API")

@app.get("/api/reports/top-products")
def top_products(limit: int = 10):
    query = text("""
        select word as term, count(*) as count
        from (
            select unnest(string_to_array(lower(message_text),' ')) as word
            from fct_messages
        ) t
        group by word
        order by count desc
        limit :limit
    """)
    with engine.connect() as conn:
        result = conn.execute(query, {"limit": limit}).fetchall()
    return result
