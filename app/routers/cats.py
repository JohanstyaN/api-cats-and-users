# app/routers/cats.py
from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List
import httpx

from app.services.cats_service import CatService
from app.models.cat import Breed
from app.config.settings import Settings

router = APIRouter(prefix="/breeds", tags=["cats"])


def get_cat_service() -> CatService:
    return CatService(Settings())


@router.get("", response_model=List[Breed])
async def list_breeds(service: CatService = Depends(get_cat_service)):
    try:
        return await service.get_all_breeds()
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"No se pudo conectar al servicio externo: {e}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=502, detail=f"Error en la respuesta del servicio externo: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno listando razas: {e}")


@router.get("/search", response_model=List[Breed])
async def search_breeds(
    q: str = Query(..., description="Término de búsqueda de la raza (param `q`)"),
    attach_image: bool = Query(False, description="attach_image=1 para incluir imagen"),
    service: CatService = Depends(get_cat_service)
) -> List[Breed]:
    try:
        return await service.search_breeds(q=q, attach_image=attach_image)
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"No se pudo conectar al servicio externo: {e}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=502, detail=f"Error en la respuesta del servicio externo: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno buscando razas: {e}")


@router.get("/{breed_id}", response_model=Breed)
async def get_breed(
    breed_id: str,
    service: CatService = Depends(get_cat_service)
):
    try:
        breed = await service.get_breed_by_id(breed_id)
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"No se pudo conectar al servicio externo: {e}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=502, detail=f"Error en la respuesta del servicio externo: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno obteniendo raza '{breed_id}': {e}")

    if not breed:
        raise HTTPException(status_code=404, detail="Breed not found")
    return breed
