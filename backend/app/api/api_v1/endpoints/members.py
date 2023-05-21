from typing import Any, Annotated
from fastapi import APIRouter, Form
from starlette.responses import FileResponse
from app import schemas

# the prefix is set to /member_id in api_v1/api.py

# FastApi ruter
router = APIRouter()

# Creating the member ID, which is defined in the class in case this is ever saved
# to the DB..
@router.post("/")
def create_member_id(
    member: schemas.Member
) -> Any:
    return member.generate_id()

# Loading a static HtML file with the form for validating the ID
@router.get("/validate")
async def read_index():
    return FileResponse('app/static/validate.html')

# This works for HtML form submits that don't send JSON
@router.post("/validate")
async def validate_member_id(member_id: Annotated[str, Form()]):
    return validate_member_id_json(member_id)

# And this is excepts string for API calls
@router.post("/validate/api")
def validate_member_id_json(
    member_id: str
) -> Any:
    # need to set default values otherwise the validation rules kick in - something to lok at later...
    member = schemas.Member(
        first_name=" ",
        last_name=" ",
        dob="01/01/1971",
        country="")
    # simple format validation of the string. this probably should set the response code to an error
    if member.validate_id(member_id):
        return "The id is valid!"
    return "The id does not match the format!"
