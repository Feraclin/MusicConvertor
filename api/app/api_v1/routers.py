from fastapi import APIRouter
from .endpoints import records, user

api_routers = APIRouter()


api_routers.include_router(records.router, tags=["user"])
api_routers.include_router(user.router, tags=["records"])
