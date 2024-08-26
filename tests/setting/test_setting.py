from apis.post import router
from fastapi.testclient import TestClient
from auth.auth_handler import decodeJWT
from uuid import uuid4
from main import app  # assuming your FastAPI app is defined in main.py
from datetime import *
from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST
import pytest
from utils.os import *
from constants.path import *

client = TestClient(router)

""" Get setting overview """
def test_get_overview(client, test_jwt):
    response = client.get(
        "/setting/overview",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"}
    )

    assert response.status_code == 200
    response_json = response.json()
    assert "data" in response_json

# test_get_overview ( 잘못된 jwt )
async def test_get_overview_fail():
    with pytest.raises(HTTPException) as err:
        headers = {"Authorization": f"Bearer wrong_jwt_token"}
        client.get("/overview", headers=headers)
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "Failed to get overview"