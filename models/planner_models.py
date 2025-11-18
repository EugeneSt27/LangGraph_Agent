from pydantic import BaseModel
from typing import List, Optional

class DiagnosisPlan(BaseModel):
    """
    Контракт, который возвращает PlannerNode.
    plant_name может быть None, если пользователь не указал растение.
    symptoms — список (может быть пустой, но лучше минимум [])
    severity — опционально: 'low'|'medium'|'high' или None
    additional_notes — опционально, для свободной информации
    """
    plant_name: Optional[str] = None
    symptoms: List[str] = []
    severity: Optional[str] = None
    additional_notes: Optional[str] = None

    model_config = {
        "extra": "forbid"  # если LLM вернёт лишние поля — pydantic выбросит ошибку
    }