# routes/users/post.py
import logging

from fastapi import HTTPException, Depends
from pydantic import BaseModel

from utils.router import validate_token


class User(BaseModel):
    username: str
    email: str
    full_name: str = None


async def handler(user: User, token: str = Depends(validate_token)):
    logging.info(f"Token: {token}")
    # Logic to add the user to the database or process the data
    return {"username": user.username, "email": user.email, "full_name": user.full_name}
