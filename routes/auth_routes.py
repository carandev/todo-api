import os
from typing import Union

from fastapi import APIRouter, status, HTTPException, Header
from jwt import decode, DecodeError
from pydantic import BaseModel

from config.db import conn
from manage_token import create_token, validate_token
from models.user import users

auth_routes = APIRouter()


class UserData(BaseModel):
    username: str
    password: str


@auth_routes.post('/login')
def login(user_data: UserData):
    user = conn.execute(users.select(users.c.email == user_data.username)).fetchone()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incorrect email"
        )

    token = create_token(user.id)
    return token


@auth_routes.post('/validate/token')
def validate_token_route(authorization: Union[str, None] = Header(default=None)):
    if authorization is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header empty"
        )

    return validate_token(authorization)
