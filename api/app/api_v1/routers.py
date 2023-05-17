from fastapi import APIRouter
from endpoints import records, user
api_routers = APIRouter()


api_routers.include_router(records.router)
api_routers.include_router(user.router)
