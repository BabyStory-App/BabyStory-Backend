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

    assert response_json["data"]["mateCount"] == 1
    assert response_json["data"]["friendCount"] == 1
    assert response_json["data"]["myStoryCount"] == 1

# test_get_overview ( 잘못된 jwt )
async def test_get_overview_fail():
    with pytest.raises(HTTPException) as err:
        headers = {"Authorization": f"Bearer wrong_jwt_token"}
        client.get("/setting/overview", headers=headers)
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "Failed to get overview"



""" Get my friends """
def test_get_my_friends(client, test_jwt):
    response = client.get(
        "/setting/myfriends/0",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"}
    )

    assert response.status_code == 200
    response_json = response.json()
    assert "parents" in response_json
    assert "paginationInfo" in response_json
    
    # assert response_json["status"] == "success"
    # assert response_json["message"] == "Successfully get my friends"
    # assert response_json['paginationInfo']['page'] == 0
    # assert response_json['paginationInfo']['take'] == 10
    # assert response_json['paginationInfo']['total'] == 1


# test_get_my_friends ( 잘못된 jwt )
async def test_get_my_friends_fail():
    with pytest.raises(HTTPException) as err:
        headers = {"Authorization": f"Bearer wrong_jwt_token"}
        client.get("/setting/myfriends/0", headers=headers)
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "Failed to get my friends"



""" Get my views """
def test_get_my_views(client, test_jwt):
    response = client.get(
        "/setting/myviews/0",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"}
    )

    assert response.status_code == 200
    response_json = response.json()
    assert "post" in response_json
    assert "paginationInfo" in response_json

# test_get_my_views ( 잘못된 jwt )
async def test_get_my_views_fail():
    with pytest.raises(HTTPException) as err:
        headers = {"Authorization": f"Bearer wrong_jwt_token"}
        client.get("/setting/myviews/0", headers=headers)
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "Failed to get view post"



""" Get my scripts """
def test_get_scripts(client, test_jwt):
    response = client.get(
        "/setting/scripts/0",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"}
    )

    assert response.status_code == 200
    response_json = response.json()
    assert "post" in response_json
    assert "paginationInfo" in response_json

# test_get_scripts ( 잘못된 jwt )
async def test_get_scripts_fail():
    with pytest.raises(HTTPException) as err:
        headers = {"Authorization": f"Bearer wrong_jwt_token"}
        client.get("/setting/scripts/0", headers=headers)
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "Failed to get script post"



""" Get my likes """
def test_get_likes(client, test_jwt):
    response = client.get(
        "/setting/likes/0",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"}
    )

    assert response.status_code == 200
    response_json = response.json()
    assert "post" in response_json
    assert "paginationInfo" in response_json

# test_get_likes ( 잘못된 jwt )
async def test_get_likes_fail():
    with pytest.raises(HTTPException) as err:
        headers = {"Authorization": f"Bearer wrong_jwt_token"}
        client.get("//settinglikes/0", headers=headers)
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "Failed to get like post"



""" Get my post """
def test_get_my_post(client, test_jwt):
    response = client.get(
        "/setting/mystories/0",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"}
    )

    assert response.status_code == 200
    response_json = response.json()
    assert "post" in response_json
    assert "paginationInfo" in response_json

# test_get_my_post ( 잘못된 jwt )
async def test_get_my_post_fail():
    with pytest.raises(HTTPException) as err:
        headers = {"Authorization": f"Bearer wrong_jwt_token"}
        client.get("/setting/mystories/0", headers=headers)
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "Failed to get my post"



""" Get my mates """
def test_get_my_mates(client, test_jwt):
    response = client.get(
        "/setting/mymates/0",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"}
    )

    assert response.status_code == 200
    response_json = response.json()
    assert "parents" in response_json
    assert "paginationInfo" in response_json

# test_get_my_mates ( 잘못된 jwt )
async def test_get_my_mates_fail():
    with pytest.raises(HTTPException) as err:
        headers = {"Authorization": f"Bearer wrong_jwt_token"}
        client.get("/setting/mymates/0", headers=headers)
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "Failed to get my mates"