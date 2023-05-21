from fastapi import APIRouter

from app.api.api_v1.endpoints import members

api_router = APIRouter()
api_router.include_router(members.router, prefix="/member_id", tags=["members"])
