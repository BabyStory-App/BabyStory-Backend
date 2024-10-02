from apis.post import router
from fastapi.testclient import TestClient
from auth.auth_handler import decodeJWT
from uuid import uuid4
from main import app  # assuming your FastAPI app is defined in main.py
from datetime import *
from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST
import pytest
import json

client = TestClient(router)

test_jwt_tmp = None

test_CreatePHeartInput = {
    "post_id": 1
}

test_DeletePHeartInput = {
    "post_id": "1"
}


""" Manage post heart test 1 """
def test_manage_pheartc(client, test_jwt):
    response = client.post(
        "pheart",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
        json=test_CreatePHeartInput
    )
    
    assert response.status_code == 200
    response_json = response.json()
    assert isinstance(response_json, dict)

    # pheart 객체 확인
    assert response_json["post_id"] == test_CreatePHeartInput["post_id"]

# Manage post heart test fail ( post_id가 없는 경우 )
async def test_managePHeartc_fail():
    with pytest.raises(HTTPException) as err:
        headers={"Authorization": f"Bearer {test_jwt_tmp['access_token']}"}
        client.post("pheart", headers=headers)
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "Failed to manage pheart"


""" Manage post heart test 2 """
def test_manage_pheartd(client, test_jwt):
    response = client.post(
        "pheart",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
        json=test_CreatePHeartInput
    )
    
    assert response.status_code == 200
    response_json = response.json()
    assert isinstance(response_json, dict)

    # pheart 객체 확인
    assert response_json["post_id"] == test_CreatePHeartInput["post_id"]

# Manage post heart test fail ( post_id가 없는 경우 )
async def test_managePHeartd_fail():
    with pytest.raises(HTTPException) as err:
        headers={"Authorization": f"Bearer {test_jwt_tmp['access_token']}"}
        client.post("pheart", headers=headers)
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "Failed to manage pheart"


""" Create post heart test """
def test_create_pheart(client, test_jwt):
    response = client.post(
        "pheart/create",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
        json=test_CreatePHeartInput
    )
    
    assert response.status_code == 200
    response_json = response.json()
    assert isinstance(response_json, dict)

    # pheart 객체 확인
    assert response_json["post_id"] == test_CreatePHeartInput["post_id"]

# Create post heart test fail ( 잘못된 jwt )
async def test_createPHeart_fail():
    with pytest.raises(HTTPException) as err:
        headers={"Authorization": f"Bearer wrong_jwt_token"}
        client.post("pheart/create", headers=headers)
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "Failed to create pheart"

# Create post heart test fail ( post_id가 없는 경우 )
async def test_createPHeart_fail():
    with pytest.raises(HTTPException) as err:
        headers={"Authorization": f"Bearer {test_jwt_tmp['access_token']}"}
        client.post("pheart/create", headers=headers)
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "Failed to create pheart"



""" Delete post heart test """
def test_delete_pheart(client, test_jwt):
    response = client.request(
        method="DELETE",
        url="pheart/delete",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
        json=test_DeletePHeartInput
    )

    assert response.status_code == 200
    response_json = response.json()
    assert isinstance(response_json, list)

    # pheart 객체 확인
    for item in response_json:
        assert item["post_id"] == int(test_DeletePHeartInput["post_id"])

# Delete post heart test fail ( 잘못된 jwt )
async def test_deletePHeart_fail():
    with pytest.raises(HTTPException) as err:
        headers={"Authorization": f"Bearer wrong_jwt_token"}
        client.delete("pheart/delete", headers=headers)
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "Failed to delete pheart"

# Delete post heart test fail ( post_id가 없는 경우 )
async def test_deletePHeart_fail():
    with pytest.raises(HTTPException) as err:
        headers={"Authorization": f"Bearer {test_jwt_tmp['access_token']}"}
        client.delete("pheart/delete", headers=headers)
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "Failed to delete pheart"