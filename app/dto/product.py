from pydantic import BaseModel


class CreateProductDto(BaseModel):
    name: str
    price: int
    desc: str
    is_offer: bool