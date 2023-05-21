import pytest
from app import schemas

from pydantic import  ValidationError

def test_create_member_id() -> None:
    member = schemas.Member(
        first_name = "Heidi",
        last_name = "Schuster",
        dob = "01/21/1999",
        country = "de")
    member.generate_id()
    assert member.validate_id(member.member_id)
    first_id=member.member_id
    member.generate_id()
    assert str(member.member_id) != str(first_id)

def test_create_member_id_validation() -> None:
    with pytest.raises(ValueError):
        member = schemas.Member(
            last_name = "Schuster",
            dob = "01/21/1999",
            country = "de")
    with pytest.raises(ValueError):
        member = schemas.Member(
            first_name = "Heidi",
            dob = "01/21/1999",
            country = "de")
    with pytest.raises(ValidationError):
        member = schemas.Member(
            first_name = "Heidi",
            last_name = "Schuster",
            dob = "01/21/1999")
    with pytest.raises(ValidationError):
        member = schemas.Member(
            first_name = "Heidi",
            last_name = "Schuster",
            dob = "01/21/1999",
            country = "Deutschland")

def test_create_member_id_validation_date() -> None:
    with pytest.raises(ValueError):
        member = schemas.Member(
            first_name = "Heidi",
            last_name = "Schuster",
            dob = "31/21/1999",
            country = "de")
    with pytest.raises(ValueError):
        member = schemas.Member(
            first_name = "Heidi",
            last_name = "Schuster",
            dob = "1/21/1999",
            country = "de")
    with pytest.raises(ValueError):
        member = schemas.Member(
            first_name = "Heidi",
            last_name = "Schuster",
            dob = "1/21/99",
            country = "de")

def test_validate_id() -> None:
    member = schemas.Member(
        first_name = "Heidi",
        last_name = "Schuster",
        dob = "01/21/1999",
        country = "de")
    assert member.validate_id("aeaa98d9-1647-5ceb-9b4e-ac31ae25c04f")
    assert member.validate_id("AAAA98d9-1647-5ceb-9b4e-ac31ae25c04f")

def test_validate_invalid_id() -> None:
    member = schemas.Member(
        first_name = "Heidi",
        last_name = "Schuster",
        dob = "01/21/1999",
        country = "de")
    isValid = False
    if member.validate_id("AA98d9-1647-5ceb-9b4e-ac31ae25c04f"):
        isValid = True
    if member.validate_id("   "):
        isValid = True
    if member.validate_id("AAA98d9-167-5ceb-9b4e-ac31ae25c04f"):
        isValid = True
    if member.validate_id("AAA98d9-16ff47-5ceb-9b4e-ac31ae25c04f"):
        isValid = True
    if member.validate_id("AAA98d9-1!47-5ceb-9b4e-ac31ae25c04f"):
        isValid = True
    if member.validate_id("AAA98d9-1!47-5ceb-9b4e-   31ae25c04f"):
        isValid = True
    assert isValid is False

def test_decod_id() -> None:
    member = schemas.Member(
        first_name = "",
        last_name = "",
        dob = "01/21/1996",
        country = "us")
    member.decode_id("gAAAAABkajTbNMqMY4U_PkkBzqJ9uh7PqbE9lvnULq60YkfzT8lHnDCs6Zycw9AR-Bc8PguQSRZNak8b3xZ9EXiexhYsaTY47kwKc0bfuSUCaktPvVjx7zihGkgbytHm8teY1WrIjvks")
    assert member.first_name == "heidi"
    assert member.last_name == "schuster"
    assert member.dob == "01/21/1999"
    assert member.country == "DE"
