from models.perenual_models import PerenualPlant
from utils.api_utils import fetch_perenual


class PerenualNode:
    """
    Узел для получения информации о растении из Perenual API.
    """

    async def run(self, plant_name: str) -> PerenualPlant | None:
        data = await fetch_perenual(plant_name)

        if data is None:
            return None

        try:
            return PerenualPlant.model_validate(data)
        except Exception as e:
            print("PERENUAL VALIDATION FAILED:", e)
            print("RAW DATA:", data)
            return None
    