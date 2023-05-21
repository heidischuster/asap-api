from fastapi import APIRouter

from app.api.api_v1.endpoints import members

# setting ng the prefix here since all routes for this micro service are currently under member_id
api_router = APIRouter()
api_router.include_router(members.router, prefix="/member_id", tags=["members"])
