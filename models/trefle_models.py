from pydantic import BaseModel
from typing import Optional


class TreflePlant(BaseModel):
    """Упрощённая модель данных растения из Trefle API."""
    id: int
    common_name: Optional[str] = None
    scientific_name: Optional[str] = None
    family: Optional[str] = None
    genus: Optional[str] = None
    image_url: Optional[str] = None

    model_config = {"extra": "ignore"}