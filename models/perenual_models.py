from pydantic import BaseModel, field_validator
from typing import Optional, List


class PerenualImage(BaseModel):
    license: Optional[int] = None
    original_url: Optional[str] = None
    regular_url: Optional[str] = None


class PerenualPlant(BaseModel):
    id: int
    common_name: Optional[str] = None
    scientific_name: Optional[str] = None
    other_name: Optional[List[str]] = None
    cycle: Optional[str] = None
    watering: Optional[str] = None
    sunlight: Optional[List[str]] = None
    default_image: Optional[PerenualImage] = None

    model_config = {"extra": "ignore"}

    @field_validator("scientific_name", mode="before")
    def scientific_name_fix(cls, v):
        if isinstance(v, list) and v:
            return v[0]
        if isinstance(v, str):
            return v
        return None

    @field_validator("sunlight", mode="before")
    def sunlight_fix(cls, v):
        if v is None:
            return None
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            if "Upgrade Plans" in v:
                return None
            return [v]
        return None