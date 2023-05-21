from fastapi.testclient import TestClient

from app.core.config import settings


def test_create_member_id(
    client: TestClient
) -> None:
    data = {"first_name": "Heidi", "last_name": "Schuster", "dob": "01/21/1999", "country": "de"}
    r = client.post(
        f"{settings.API_V1_STR}/member_id/", json=data,
    )
    assert 200 <= r.status_code < 300
    created_member = r.json()
    assert data["first_name"] == created_member["first_name"]
    assert data["last_name"] == created_member["last_name"]
    assert data["dob"] == created_member["dob"]
    assert data["country"] == created_member["country"]
    assert len(created_member["member_id"]) > 4

def test_create_member_id_invalid(
    client: TestClient
) -> None:
    data = {"first_name": "Heidi", "dob": "01/21/1999", "country": "de"}
    r = client.post(
        f"{settings.API_V1_STR}/member_id/", json=data,
    )
    assert 422 == r.status_code

def test_validate_member_id(
    client: TestClient
) -> None:
    r = client.post(
        f"{settings.API_V1_STR}/member_id/validate/api?member_id=599f4d2d-886e-5211-aa4d-022e5b66df3f"
    )
    assert 200 == r.status_code

def test_validate_member_id_invalid(
    client: TestClient
) -> None:
    data = {"member_id": "xxx"}
    r = client.post(
        f"{settings.API_V1_STR}/member_id/validate/api", json=data,
    )
    assert 422 == r.status_code
