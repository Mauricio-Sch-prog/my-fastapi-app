from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import Base, engine, get_db
from app.models.User import User
from app.routers.users import router as users_router

db_dependency = Depends(get_db)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

# app.include_router(users_router)
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

@app.post("/users/")
async def create_user(name: str, email: str, db: AsyncSession = db_dependency):
    user = User(name=name, email=email)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

@app.get("/users/")
async def list_users(db: AsyncSession = db_dependency):
    result = await db.execute(select(User))
    return result.scalars().all()