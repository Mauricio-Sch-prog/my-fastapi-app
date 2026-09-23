from google import genai
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.models.Product import Product

client = genai.Client(api_key=get_settings().GOOGLE_API_KEY)

async def add_product_with_embedding(
    db: AsyncSession, 
    name: str, 
    price: int, 
    desc: str, 
    is_offer: bool
) -> Product:
    text_to_embed = f"Product: {name}. Description: {desc}"

    response = await client.aio.models.embed_content(
        model="gemini-embedding-001",
        contents=text_to_embed
    )
    
    embedding_vector = response.embeddings[0].values

    new_product = Product(
        name=name,
        price=price,
        desc=desc,
        is_offer=is_offer,
        embedding=embedding_vector
    )

    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    
    return new_product