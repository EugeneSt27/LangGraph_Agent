from pydantic import BaseModel, Field
from typing import List, Optional

class DiagnosisResult(BaseModel):
    """
    Финальный структурированный диагноз, который выносится после цикла ReAct.
    Используется как выход DiagnosisNode, когда агент решает закончить.
    """
    diagnosis: str = Field(description="Краткий итоговый диагноз (например, 'Перелив' или 'Недостаток калия').")
    recommendations: List[str] = Field(description="Список конкретных, пошаговых рекомендаций по устранению проблемы (например, ['Сократить полив до 1 раза в неделю', 'Проверить дренаж']).")
    confidence_level: Optional[str] = Field(description="Уровень уверенности в диагнозе: 'High', 'Medium', 'Low'.")