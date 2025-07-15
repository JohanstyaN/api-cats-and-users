from fastapi import FastAPI
from app.routers.cats import router as cats_router
from app.routers.users import router as users_router

app = FastAPI(title="Cats & Users API")

app.include_router(cats_router)
app.include_router(users_router)
