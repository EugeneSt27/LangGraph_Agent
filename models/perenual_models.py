from pydantic import BaseModel
from typing import Optional, List


class PerenualImage(BaseModel):
    """Изображения из Perenual."""
    license: Optional[int] = None
    original_url: Optional[str] = None
    regular_url: Optional[str] = None


class PerenualPlant(BaseModel):
    """Упрощённая модель растения из Perenual."""
    id: int
    common_name: Optional[str] = None
    scientific_name: Optional[str] = None
    other_name: Optional[List[str]] = None
    cycle: Optional[str] = None
    watering: Optional[str] = None
    sunlight: Optional[List[str]] = None
    default_image: Optional[PerenualImage] = None

    model_config = {"extra": "ignore"}