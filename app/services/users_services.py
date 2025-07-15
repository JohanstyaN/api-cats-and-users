# app/services/users_services.py
from typing import List, Optional
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from passlib.hash import bcrypt
import uuid

from app.models.user import UserCreate, UserResponse
from app.utils.generate_user import generate_username
from app.config.settings import Settings

class UserService:
    
    def __init__(self, settings: Settings):
        client = MongoClient(settings.MONGO_URI)
        self._db = client[settings.MONGO_DB]
        self._users = self._db.get_collection("users")


    def get_users(self) -> List[UserResponse]:
        docs = list(self._users.find({}, {"hashed_password": 0}))
        users: List[UserResponse] = []
        for doc in docs:
            user_id = doc.get("id") or str(doc.get("_id"))
            user_dict = {
                "id":         user_id,
                "name":       doc.get("name"),
                "last_name":  doc.get("last_name"),
                "username":   doc.get("username"),
                "created_at": doc.get("created_at"),
            }
            users.append(UserResponse(**user_dict))
        return users


    def create_user(self, user_create: UserCreate) -> UserResponse:
        base = generate_username(user_create.name, user_create.last_name)
        username = base
        suffix = 1
        while self._users.find_one({"username": username}):
            suffix += 1
            username = f"{base}{suffix}"

        hashed_password = bcrypt.hash(user_create.password)
        new_user = {
            "id":              str(uuid.uuid4()),
            "name":            user_create.name,
            "last_name":       user_create.last_name,
            "username":        username,
            "hashed_password": hashed_password,
            "created_at":      datetime.now(),
        }
        self._users.insert_one(new_user)

        return UserResponse(
            id=new_user["id"],
            name=new_user["name"],
            last_name=new_user["last_name"],
            username=new_user["username"],
            created_at=new_user["created_at"],
        )


    def authenticate(self, username: str, password: str) -> Optional[UserResponse]:
        try:
            doc = self._users.find_one({"username": username})
        except PyMongoError:
            return None

        if not doc or not bcrypt.verify(password, doc["hashed_password"]):
            return None

        user_id = doc.get("id") or str(doc.get("_id"))
        return UserResponse(
            id=user_id,
            name=doc.get("name"),
            last_name=doc.get("last_name"),
            username=doc.get("username"),
            created_at=doc.get("created_at"),
        )
