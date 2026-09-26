from google import genai
from google.genai import types

from app.config import get_settings


class Gemini:
 
    def __init__(self):
        self.client = genai.Client(api_key=get_settings().GOOGLE_API_KEY)

    async def get_embed(self, entry: str | dict) -> list[float]:
        if isinstance(entry, dict):
            text_to_embed = "".join([f" {k}:{v};" for k, v in entry.items()])
        else:
            text_to_embed = entry

        response = await self.client.aio.models.embed_content(
            model="gemini-embedding-001",
            contents=text_to_embed
        )
        return response.embeddings[0].values

    async def chat(self, user_query: str, matching_products: list[dict] | None = None,):

        if not matching_products:
            context_str = "No products found matching these exact criteria."
        else:
            context_str = "\n".join([
            f"- Product: {p.name} | Price: ${p.price} | On Offer: {p.is_offer}\n  Description: {p.desc}"
            for p in matching_products
        ])
            
        system_instruction = """
        You are an e-commerce assistant for our store. 
        Answer customer queries politely using ONLY the provided product context. 
        If a product is not listed in the context, state that we do not have it in stock.
        Never invent prices, discounts, or products.
        """

        prompt = f"""
        Product Context from Store Database:
        {context_str}

        Customer Question: {user_query}
        """

        return self.client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.2,
        ),
    )


model_service = Gemini()

    