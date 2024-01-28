from fastapi import APIRouter

from app.api.v1 import cources

api_router = APIRouter()

api_router.include_router(cources.router, tags=["image_process"])
