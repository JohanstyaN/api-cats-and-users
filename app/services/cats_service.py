# app/services/cats_service.py
from typing import List, Optional
import httpx
from app.config.settings import Settings
from app.models.cat import Breed

class CatService:
    
    def __init__(self, settings: Settings):
        self._api_base_url: str = settings.CAT_API_URL
        self._api_key: str      = settings.CAT_API_KEY
        self._headers: dict     = {"x-api-key": self._api_key}


    async def get_all_breeds(self) -> List[Breed]:
        async with httpx.AsyncClient() as http_client:
            response = await http_client.get(
                f"{self._api_base_url}/breeds",
                headers=self._headers
            )
            response.raise_for_status()
            breeds_json = response.json()
            return [Breed(**breed_data) for breed_data in breeds_json]


    async def get_breed_by_id(self, breed_id: str) -> Optional[Breed]:
        all_breeds = await self.get_all_breeds()
        for breed in all_breeds:
            if breed.id == breed_id:
                return breed
        return None


    async def search_breeds(
        self,
        q: str,
        attach_image: bool = False
    ) -> List[Breed]:
        params = {"q": q}
        if attach_image:
            params["attach_image"] = 1

        async with httpx.AsyncClient() as http_client:
            response = await http_client.get(
                f"{self._api_base_url}/breeds/search",
                params=params,
                headers=self._headers
            )
            response.raise_for_status()
            search_results = response.json()
            return [Breed(**breed_data) for breed_data in search_results]
