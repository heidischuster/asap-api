
from app import schemas

def test_create_member_id() -> None:
    member = schemas.Member(
        first_name = "Heidi",
        last_name = "Schuster",
        dob = "01/01/1971",
        country = "US")
    member.generate_id()
    assert len(member.member_id) > 4



