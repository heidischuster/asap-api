from typing import Any, Annotated
import logging
from fastapi import APIRouter, Form
from starlette.responses import FileResponse
from app import schemas


#from app.api import deps
#from app.core.config import settings


router = APIRouter()

@router.post("/")
def create_member_id(
    member: schemas.Member
) -> Any:
    """
    Create member id by encoding the fields
    """
    return member.generate_id()


@router.get("/validate")
async def read_index():
    return FileResponse('app/static/validate.html')

@router.post("/validate")
async def validate_member_id(member_id: Annotated[str, Form()]):
    return validate_member_id_json(member_id)

@router.post("/validate/api")
def validate_member_id_json(
    member_id: str
) -> Any:
    """
    Validate member id
    """
    member = schemas.Member(
        first_name = " ",
        last_name = " ",
        dob = "01/01/1971",
        country = "")
    try:
        return member.decode_id(member_id)
    except Exception as e:
        return str(e)
