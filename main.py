from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.auth_routes import auth_routes
from routes.user_routes import user_route

app = FastAPI()

load_dotenv()

origins = [
        "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_route, prefix="/api")
app.include_router(auth_routes, prefix="/api")
