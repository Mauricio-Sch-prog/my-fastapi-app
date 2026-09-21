from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from app.database import Base, engine, get_db
from app.routers.products import router as product_router

db_dependency = Depends(get_db)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(product_router)

@app.get("/v")
def read_root():
    return {"status": "Active", "message": "Welcome to FastAPI", "Version": "1.0"}