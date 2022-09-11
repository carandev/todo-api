import os

from fastapi import HTTPException, status
from jwt import encode, decode, DecodeError


def create_token(user_id):
    encoded_jwt = encode({"user_id": user_id}, os.getenv('JWT_SECRET_KEY'))

    return encoded_jwt


def validate_token(token):
    try:
        payload = decode(token, os.getenv('JWT_SECRET_KEY'), ["HS256"])

        return payload

    except DecodeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header invalid"
        )