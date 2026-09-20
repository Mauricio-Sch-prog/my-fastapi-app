from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None

@app.get("/")
def read_root():
    return {"status": "Active", "message": "Welcome to FastAPI"}

@app.post("/items/")
def create_item(item: Item):
    return {"item_name": item.name, "item_price": item.price, "created": True}