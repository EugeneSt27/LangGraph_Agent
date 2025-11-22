from pydantic import BaseModel
from typing import List

class DiagnosisDraft(BaseModel):
    possible_causes: List[str]
    recommended_actions: List[str]
    confidence: float  # в диапазоне 0.0 - 1.0

    model_config = {"extra": "ignore"}
