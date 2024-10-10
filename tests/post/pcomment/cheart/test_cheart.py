from apis.post import router
from fastapi.testclient import TestClient
from datetime import *
from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST
import pytest

client = TestClient(router)
test_jwt_tmp = None

test_CreateCHeartInput = {
    "comment_id": 1
}

test_DeleteCHeartInput = {
    "comment_id": "1"
}


""" Manage comment heart test 1 """
def test_manage_cheartc(client, test_jwt):
    response = client.post(
        "cheart",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
        json=test_CreateCHeartInput
    )
    
    assert response.status_code == 200
    response_json = response.json()
    assert isinstance(response_json, dict)

    # cheart 객체 확인
    assert response_json["cheart"]["comment_id"] == test_CreateCHeartInput["comment_id"]

# Manage comment heart test fail ( comment_id가 없는 경우 )
async def test_manageCHeartc_fail():
    with pytest.raises(HTTPException) as err:
        headers={"Authorization": f"Bearer {test_jwt_tmp['access_token']}"}
        client.post("cheart", headers=headers)
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "Failed to manage cheart"


""" Manage comment heart test 2 """
def test_manage_cheartd(client, test_jwt):
    response = client.post(
        "cheart",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
        json=test_CreateCHeartInput
    )
    
    assert response.status_code == 200
    response_json = response.json()
    assert isinstance(response_json, dict)

    # cheart 객체 확인
    assert response_json["cheart"]["comment_id"] == test_CreateCHeartInput["comment_id"]

# Manage comment heart test fail ( comment_id가 없는 경우 )
async def test_manageCHeartd_fail():
    with pytest.raises(HTTPException) as err:
        headers={"Authorization": f"Bearer {test_jwt_tmp['access_token']}"}
        client.post("cheart", headers=headers)
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "Failed to manage cheart"

    
""" Create comment heart test """
def test_create_cheart(client, test_jwt):
    response = client.post(
        "cheart/create",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
        json=test_CreateCHeartInput
    )
    
    assert response.status_code == 200
    response_json = response.json()
    assert isinstance(response_json, dict)

    # cheart 객체 확인
    assert response_json["cheart"]["comment_id"] == test_CreateCHeartInput["comment_id"]

# Create comment heart test fail ( comment_id가 없는 경우 )
async def test_createCHeart_fail():
    with pytest.raises(HTTPException) as err:
        headers={"Authorization": f"Bearer {test_jwt_tmp['access_token']}"}
        client.post("cheart/create", headers=headers)
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "Failed to create cheart"


""" Delete comment heart test """
def test_delete_cheart(client, test_jwt):
    response = client.request(
        method="DELETE",
        url="cheart/delete",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
        json=test_DeleteCHeartInput
    )

    assert response.status_code == 200
    response_json = response.json()
    assert isinstance(response_json["cheart"], list)

    # cheart 객체 확인
    assert response_json["cheart"][0]["comment_id"] == int(test_DeleteCHeartInput["comment_id"])

# Delete comment heart test fail ( comment_id가 없는 경우 )
async def test_deleteCHeart_fail():
    with pytest.raises(HTTPException) as err:
        headers={"Authorization": f"Bearer {test_jwt_tmp['access_token']}"}
        client.delete("cheart/delete", headers=headers)
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "Failed to delete cheart"