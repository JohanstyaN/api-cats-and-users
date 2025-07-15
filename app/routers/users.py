# app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List
from pymongo.errors import PyMongoError

from app.services.users_services import UserService
from app.models.user import UserCreate, UserResponse, UserLogin
from app.config.settings import Settings

router = APIRouter(prefix="/users", tags=["users"])


def get_user_service() -> UserService:
    return UserService(Settings())


@router.get("", response_model=List[UserResponse])
def list_users(svc: UserService = Depends(get_user_service)):
    try:
        return svc.get_users()
    except PyMongoError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"No se pudo conectar con la base de datos: {e}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno listando usuarios: {e}"
        )


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, svc: UserService = Depends(get_user_service)):
    try:
        return svc.create_user(payload)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except PyMongoError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Error al escribir en la base de datos: {e}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno creando usuario: {e}"
        )


@router.get("/login", response_model=UserResponse)
def login(
    username: str = Query(..., description="El nombre de usuario"),
    password: str = Query(..., description="La contraseña del usuario"),
    svc: UserService = Depends(get_user_service)
) -> UserResponse:
    try:
        user = svc.authenticate(username=username, password=password)
    except PyMongoError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"No se pudo conectar con la base de datos: {e}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno durante autenticación: {e}"
        )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )
    return user
