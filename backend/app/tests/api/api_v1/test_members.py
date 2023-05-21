import logging

from fastapi.testclient import TestClient

from app.core.config import settings


def test_create_member_id(
    client: TestClient
) -> None:

    logger.info("Running test_create_member_id")
    data = {"first_name": "Heidi", "last_name": "Schuster", "dob": "01/21/1988", "country": "us"}
    r = client.post(
        f"{settings.API_V1_STR}/", json=data,
    )

    r = client.get(f"{settings.API_V1_STR}/")
    assert 200 <= r.status_code < 300
    created_member = r.json()
    assert data["first_name"] == created_member["first_name"]
    assert data["last_name"] == created_member["last_name"]
    assert data["dob"] == created_member["dob"]
    assert data["country"] == created_member["country"]
    assert len(created_member["member_id"]) > 4
