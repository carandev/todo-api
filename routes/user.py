from fastapi import APIRouter
from models.user import users
from config.db import conn
from schemas.user import User
from cryptography.fernet import Fernet

key = Fernet.generate_key()
f = Fernet(key)

user = APIRouter()


@user.get("/users")
def get_users():
    return conn.execute(users.select()).fetchall()


@user.get("/users/{id}")
def get_user(id: str):
    user_selected = conn.execute(users.select().where(users.c.id == id)).first()

    return user_selected


@user.post("/users")
def create_user(user_create: User):
    new_user = {"name": user_create.name, "email": user_create.email, "password": f.encrypt(user_create.password.encode("utf-8"))}

    result = conn.execute(users.insert().values(new_user))

    return conn.execute(users.select().where(users.c.id == result.lastrowid)).first()


@user.delete("/users/{id}")
def delete_user(id: str):
    conn.execute(users.delete().where(users.c.id == id))

    return "User deleted"
