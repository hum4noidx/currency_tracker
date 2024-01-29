from fastapi import APIRouter

from app.api.v1 import courses, ping

api_router = APIRouter()

api_router.include_router(courses.router, tags=["courses"])
api_router.include_router(ping.router, tags=["ping"])
