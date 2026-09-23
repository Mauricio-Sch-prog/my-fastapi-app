from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dto.product import CreateProductDto
from app.gemini import add_product_with_embedding
from app.models.Product import Product

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)

db_dependency = Depends(get_db)

@router.post("/")
async def create_product(product: CreateProductDto, db: AsyncSession = db_dependency):


    product = await add_product_with_embedding(
        db=db,
        name=product.name,
        price=product.price,
        desc=product.desc,
        is_offer=product.is_offer,
    )

    print(product)
    
    return product

@router.get("/")
async def list_products(db: AsyncSession = db_dependency):
    result = await db.execute(select(Product))
    return result.scalars().all()