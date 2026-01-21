from pydantic import BaseModel

class TopProduct(BaseModel):
    term: str
    count: int
