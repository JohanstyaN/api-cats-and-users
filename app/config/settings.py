from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    MONGO_URI: str    = Field("mongodb://localhost:27017", env="MONGO_URI")
    MONGO_DB:  str    = Field("api_db", env="MONGO_DB")
    CAT_API_KEY: str  = Field(..., env="CAT_API_KEY")
    CAT_API_URL: str  = Field("https://api.thecatapi.com/v1", env="CAT_API_URL")

    class Config:
        env_file = ".env"
