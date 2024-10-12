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

test_CreatePViewInput = {
    "post_id": 1
}

test_DeletePViewInput = {
    "post_id": "1"
}


""" Manage post view test 1 """
def test_manage_pviewc(client, test_jwt):
    response = client.post(
        "pview",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
        json=test_CreatePViewInput
    )
    
    assert response.status_code == 200
    response_json = response.json()
    assert isinstance(response_json, dict)

    # pview 객체 확인
    assert response_json["pview"]["post_id"] == test_CreatePViewInput["post_id"]

# Manage post view test fail ( post_id가 없는 경우 )
async def test_managePViewc_fail():
    with pytest.raises(HTTPException) as err:
        headers={"Authorization": f"Bearer {test_jwt_tmp['access_token']}"}
        client.post("pview", headers=headers)
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "Failed to manage pview"


""" Manage post view test 2 """
def test_manage_pviewd(client, test_jwt):
    response = client.post(
        "pview",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
        json=test_CreatePViewInput
    )
    
    assert response.status_code == 200
    response_json = response.json()
    assert isinstance(response_json, dict)

    # pview 객체 확인
    assert response_json["pview"]["post_id"] == test_CreatePViewInput["post_id"]

# Manage post view test fail ( post_id가 없는 경우 )
async def test_managePViewd_fail():
    with pytest.raises(HTTPException) as err:
        headers={"Authorization": f"Bearer {test_jwt_tmp['access_token']}"}
        client.post("pview", headers=headers)
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "Failed to manage pview"


""" Create post view test """
def test_create_pview(client, test_jwt):
    response = client.post(
        "pview/create",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
        json=test_CreatePViewInput
    )
    
    assert response.status_code == 200
    response_json = response.json()
    assert isinstance(response_json, dict)

    # pview 객체 확인
    assert response_json["pview"]["post_id"] == test_CreatePViewInput["post_id"]

# Create post view test fail ( 잘못된 jwt )
async def test_createPView_fail():
    with pytest.raises(HTTPException) as err:
        headers={"Authorization": f"Bearer wrong_jwt_token"}
        client.post("pview/viewCreate", headers=headers)
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "Failed to create pview"

# Create post view test fail ( post_id가 없는 경우 )
async def test_createPView_fail():
    with pytest.raises(HTTPException) as err:
        headers={"Authorization": f"Bearer {test_jwt_tmp['access_token']}"}
        client.post("pview/viewCreate", headers=headers)
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "Failed to create pview"


""" Delete post view test """
def test_delete_pview(client, test_jwt):
    response = client.request(
        method="DELETE",
        url="pview/delete",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
        json=test_DeletePViewInput
    )

    assert response.status_code == 200
    response_json = response.json()
    assert isinstance(response_json['pview'], list)

    # pview 객체 확인
    assert response_json['pview'][0]['post_id'] == int(test_DeletePViewInput['post_id'])

# Delete post view test fail ( 잘못된 jwt )
async def test_deletePView_fail():
    with pytest.raises(HTTPException) as err:
        headers={"Authorization": f"Bearer wrong_jwt_token"}
        client.request("DELETE", "pview/delete", headers=headers)
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "Failed to delete pview"

# Delete post view test fail ( post_id가 없는 경우 )
async def test_deletePView_fail():
    with pytest.raises(HTTPException) as err:
        headers={"Authorization": f"Bearer {test_jwt_tmp['access_token']}"}
        client.request("DELETE", "pview/delete", headers=headers)
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "Failed to delete pview"