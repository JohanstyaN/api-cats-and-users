import os, sys
import pytest
from fastapi.testclient import TestClient
sys.path.insert(0, os.getcwd())

from main import app
from app.config.settings import Settings
from pymongo import MongoClient

@pytest.fixture(scope="session")
def client():
    return TestClient(app)

@pytest.fixture(autouse=True)
def clear_db():
    settings = Settings()
    mongo = MongoClient(settings.MONGO_URI)
    db = mongo[settings.MONGO_DB]
    db.users.delete_many({})
    yield
    db.users.delete_many({})
