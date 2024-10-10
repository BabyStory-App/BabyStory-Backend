from apis.post import router
from fastapi.testclient import TestClient
from auth.auth_handler import decodeJWT
from uuid import uuid4
from main import app  # assuming your FastAPI app is defined in main.py
from datetime import *
from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST
import pytest

client = TestClient(router)

test_jwt_tmp = None

test_CreatePCommentInput = {
    "post_id": 2,
    "reply_id": None,
    "content": "test"
}

test_CreateReplyInput = {
    "post_id": 2,
    "reply_id": None,
    "content": "test"
}

test_GetReplyComment = {
    "comment_id": None
}

test_UpdatePCommentInput = {
    "comment_id": 1,
    "content": "update content"
}

test_DeleteReply = {
    "comment_id": 1
}

""" Create pcomment test """
def test_create_pcomment(client, test_jwt):
    response = client.post(
        "/pcomment/create",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
        json=test_CreatePCommentInput
    )

    assert response.status_code == 200
    response_json = response.json()
    assert "pcomment" in response_json

    # pcomment 객체 확인
    for key in test_CreatePCommentInput:
        if key in response_json["pcomment"]:
            if key == "createTime":
                assert response_json["pcomment"]["createTime"][:10] == datetime.now().strftime('%Y-%m-%d')
            assert response_json["pcomment"][key] == test_CreatePCommentInput[key]

    # comment_id를 test_jwt에 저장
    test_jwt["comment_id"] = response_json["pcomment"]["comment_id"]

# Create pcomment test fail ( post_id가 없는 경우 )
async def test_create_pcomment_fail():
    with pytest.raises(HTTPException) as err:
        headers = {"Authorization": f"Bearer {test_jwt_tmp['access_token']}"}
        client.post("/pcomment/create", headers=headers)
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "Failed to create pcomment"


""" Create reply test """
def test_create_reply(client, test_jwt):
    test_CreateReplyInput["reply_id"] = test_jwt["comment_id"]

    response = client.post(
        "/pcomment/create",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
        json=test_CreateReplyInput
    )

    assert response.status_code == 200
    response_json = response.json()
    assert "pcomment" in response_json

    # pcomment 객체 확인
    for key in test_CreateReplyInput:
        if key in response_json["pcomment"]:
            if key == "createTime":
                assert response_json["pcomment"]["createTime"][:10] == datetime.now().strftime('%Y-%m-%d')
            assert response_json["pcomment"][key] == test_CreateReplyInput[key]
    
# Create reply test fail ( post_id가 없는 경우 )
async def test_create_reply_fail():
    with pytest.raises(HTTPException) as err:
        headers = {"Authorization": f"Bearer {test_jwt_tmp['access_token']}"}
        client.post("/pcomment/create", headers=headers)
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "Failed to create pcomment"


""" Get all pcomment test """
def test_get_all_comment(client, test_jwt):
    response = client.get(
        "/pcomment/all",
        params={"post_id": 2},
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"}
    )
    assert response.status_code == 200
    response_json = response.json()
    assert isinstance(response_json, list)

    print(response_json)

    # pcomment 객체 확인
    if response_json[0]["reply_id"] is None:
        assert response_json[0]["comment_id"] == test_jwt["comment_id"]
    else:
        assert response_json[0]["reply_id"] == test_jwt["comment_id"]

# Get all pcomment test fail ( post_id가 없는 경우 )
async def test_get_all_comment_fail():
    with pytest.raises(HTTPException) as err:
        headers = {"Authorization": f"Bearer {test_jwt_tmp['access_token']}"}
        client.get("/pcomment/all", headers=headers)
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "Failed to get all comment"


""" Get reply pcomment test """
def test_get_reply_comment(client, test_jwt):
    test_GetReplyComment["comment_id"] = test_jwt["comment_id"]
    print(test_GetReplyComment)

    response = client.get(
        "/pcomment/reply",
        params=test_GetReplyComment,
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"}
    )
    print(response.json())

    assert response.status_code == 200
    response_json = response.json()
    assert isinstance(response_json, list)

    # pcomment 객체 확인
    assert response_json[0]["reply_id"] == test_jwt["comment_id"]

# Get reply pcomment test fail ( comment_id가 없는 경우 )
async def test_get_reply_comment_fail():
    with pytest.raises(HTTPException) as err:
        headers = {"Authorization": f"Bearer {test_jwt_tmp['access_token']}"}
        client.get("/pcomment/reply", headers=headers)
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "Failed to get all reply comment"


""" Update pcomment test """
def test_update_pcomment(client, test_jwt):
    test_UpdatePCommentInput["comment_id"] = test_jwt["comment_id"]

    response = client.put(
        "/pcomment/update",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
        json=test_UpdatePCommentInput
    )
    assert response.status_code == 200
    response_json = response.json()
    assert "pcomment" in response_json

    # pcomment 객체 확인
    for key in test_UpdatePCommentInput:
        if key in response_json["pcomment"]:
            assert response_json["pcomment"][key] == test_UpdatePCommentInput[key]

# Update pcomment test fail ( comment_id가 없는 경우 )
async def test_update_pcomment_fail():
    with pytest.raises(HTTPException) as err:
        headers = {"Authorization": f"Bearer {test_jwt_tmp['access_token']}"}
        client.put("/pcomment/update", headers=headers)
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "Failed to update comment"


""" Delete pcomment test """
def test_delete_pcomment(client, test_jwt):
    response = client.request(
        method="PUT",
        url="/pcomment/delete",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
        json={"comment_id": test_jwt["comment_id"]}
    )
    assert response.status_code == 200
    response_json = response.json()
    assert "pcomment" in response_json

    # pcomment 객체 확인
    assert response_json["pcomment"]["comment_id"] == test_jwt["comment_id"]

# Delete pcomment test fail ( comment_id가 없는 경우 )
async def test_delete_pcomment_fail():
    with pytest.raises(HTTPException) as err:
        headers = {"Authorization": f"Bearer {test_jwt_tmp['access_token']}"}
        client.delete("/pcomment/delete", headers=headers)
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "Failed to delete comment"

# Delet pcomment test fail ( 데이터 삭제에 실패한 경우 )
async def test_delete_pcomment_fail():
    with pytest.raises(HTTPException) as err:
        headers = {"Authorization": f"Bearer {test_jwt_tmp['access_token']}"}
        client.delete("/pcomment/delete", headers=headers)
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "Failed to delete comment"


""" Delete reply test """
def test_delete_reply(client, test_jwt):
    test_DeleteReply["comment_id"] = test_jwt["comment_id"] + 1

    response = client.put(
        "/pcomment/delete",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
        json=test_DeleteReply
    )
    assert response.status_code == 200
    response_json = response.json()
    assert "pcomment" in response_json

    # pcomment 객체 확인
    assert response_json["pcomment"]["comment_id"] == test_jwt["comment_id"] + 1

# Delete reply test fail ( comment_id가 없는 경우 )
async def test_delete_reply_fail():
    with pytest.raises(HTTPException) as err:
        headers = {"Authorization": f"Bearer {test_jwt_tmp['access_token']}"}
        client.put("/pcomment/delete", headers=headers)
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "Failed to delete comment"