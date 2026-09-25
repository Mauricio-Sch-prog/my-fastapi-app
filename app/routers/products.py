from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dto import AiPromptDto, CreateProductDto
from app.models.Product import Product
from app.services.ai_model import model_service

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)

db_dependency = Depends(get_db)

@router.post("/")
async def create_product(product: CreateProductDto, db: AsyncSession = db_dependency):

    new_product = Product(
        name=product.name,
        price=product.price,
        desc=product.desc,
        is_offer=product.is_offer,
        embedding= await model_service.get_embed(product.model_dump())
    )
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    
    return new_product


@router.post("/search_products")
async def search_products(prompt: AiPromptDto, db: AsyncSession = db_dependency):

    query_vector = await model_service.get_embed(prompt.prompt)

    stmt = (
        select(Product)
        .order_by(Product.embedding.cosine_distance(query_vector))
        .limit(prompt.limit)
    )

    result = await db.execute(stmt)
    return result.scalars().all()

@router.get("/")
async def list_products(db: AsyncSession = db_dependency):
    result = await db.execute(select(Product))
    return result.scalars().all()