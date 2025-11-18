from models.trefle_models import TreflePlant
from utils.api_utils import fetch_trefle


class TrefleNode:
    """
    Узел для получения информации о растении из Trefle API.
    """

    async def run(self, plant_name: str) -> TreflePlant | None:
        data = await fetch_trefle(plant_name)

        if data is None:
            return None

        return TreflePlant.model_validate(data)