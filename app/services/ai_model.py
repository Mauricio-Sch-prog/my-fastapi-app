from google import genai

from app.config import get_settings


class Gemini():
 
    def __init__(self):
        self.client = genai.Client(api_key=get_settings().GOOGLE_API_KEY)

    async def get_embed(self, entry):

        text_to_embed = ""
        for (key,value) in entry.items():
            text_to_embed = text_to_embed + f" {key}:{value};"

        response = await self.client.aio.models.embed_content(
                model="gemini-embedding-001",
                contents=text_to_embed
            )
        return response.embeddings[0].values


model_service = Gemini()

    