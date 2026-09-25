from google import genai

from app.config import get_settings


class Gemini():
 
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


model_service = Gemini()

    