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

test_jwt_tmp = None

test_CreatePCommentInput = {
    "post_id": 1,
    "reply_id": 0,
    "content": "test content"
}

test_CreatePCommentReplyInput = {
    "post_id": 1,
    "reply_id": 1,
    "content": "test content"
}

test_UpdatePCommentInput = {
    "comment_id": 1,
    "content": "update content"
}

""" Create post comment test """
def test_create_pcomment(client, test_jwt):
    response = client.post(
        "pcomment/create",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
        json=test_CreatePCommentInput
    )

    assert response.status_code == 200
    response_json = response.json()
    assert "pcomment" in response_json
    print("response_json : ", response_json)

    # pcomment 객체 확인
    for key in test_CreatePCommentInput:
        if key in response_json["pcomment"]:
            if key == "createTime":
                assert response_json["pcomment"]["createTime"][:10] == test_CreatePCommentInput["createTime"][:10]
            elif key == "reply_id":
                if test_CreatePCommentInput["reply_id"] == 0:
                    assert response_json["pcomment"]["reply_id"] is None
                else:
                    assert response_json["pcomment"]["reply_id"] == test_CreatePCommentInput["reply_id"]
            else:
                assert response_json["pcomment"][key] == test_CreatePCommentInput[key]

    # comment_id 저장
    test_jwt["comment_id"] = response_json["pcomment"]["comment_id"]

    # 대댓글 생성
    response = client.post(
        "/pcomment/create",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
        json=test_CreatePCommentReplyInput
    )
    print("Status Code:", response.status_code)
    print("Response Text:", response.text)
    print("Response JSON:", response.json())

    assert response.status_code == 200
    response_json = response.json()
    print("response_json : ", response_json)
    assert "pcomment" in response_json

    # pcomment 객체 확인
    for key in test_CreatePCommentReplyInput:
        if key in response_json["pcomment"]:
            if key == "createTime":
                assert response_json["pcomment"]["createTime"][:
                                                           10] == test_CreatePCommentReplyInput["createTime"][:10]
            assert response_json["pcomment"][key] == test_CreatePCommentReplyInput[key]

# Create post comment test fail ( 잘못된 jwt )
async def test_createPComment_fail():
    with pytest.raises(HTTPException) as err:
        response = client.post(
            "/pcomment/create",
            headers={"Authorization": "Bearer " + str(uuid4())},
            json=test_CreatePCommentInput
        )
        assert err.value.status_code == HTTP_400_BAD_REQUEST
        assert err.value.detail == "Failed to create pcomment"


""" Get all post comment test """
def test_get_all_comment(client, test_jwt):
    response = client.get(
        "/pcomment/all",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
        params={"post_id": test_CreatePCommentInput["post_id"]}
    )
    assert response.status_code == 200, response.text
    response_json = response.json()
    assert isinstance(response_json, list)

# Get all post comment test fail ( 잘못된 jwt )
async def test_get_all_comment_fail():
    with pytest.raises(HTTPException) as err:
        response = client.get(
            "/pcomment/all",
            headers={"Authorization": "Bearer " + str(uuid4())},
            params={"post_id": test_CreatePCommentInput["post_id"]}
        )
        assert err.value.status_code == HTTP_400_BAD_REQUEST
        assert err.value.detail == "Failed to get all comment"


""" Get reply post comment test """
def test_get_reply_comment(client, test_jwt):
    response = client.get(
        "/pcomment/reply",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
        params={"comment_id": 1}
    )
    assert response.status_code == 200, response.text
    response_json = response.json()
    assert isinstance(response_json, list)

# Get reply post comment test fail ( 잘못된 jwt )
async def test_get_reply_comment_fail():
    with pytest.raises(HTTPException) as err:
        response = client.get(
            "/pcomment/reply",
            headers={"Authorization": "Bearer " + str(uuid4())},
            params={"comment_id": 1}
        )
        assert err.value.status_code == HTTP_400_BAD_REQUEST
        assert err.value.detail == "Failed to get all reply comment"


""" Update post comment test """
def test_update_comment(client, test_jwt):
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

# Update post comment test fail ( 잘못된 jwt )
async def test_update_comment_fail():
    with pytest.raises(HTTPException) as err:
        response = client.put(
            "/pcomment/update",
            headers={"Authorization": "Bearer " + str(uuid4())},
            json=test_UpdatePCommentInput
        )
        assert err.value.status_code == HTTP_400_BAD_REQUEST
        assert err.value.detail == "Failed to update comment"


""" Delete post comment test """
def test_delete_comment(client, test_jwt):
    response = client.put(
        "/pcomment/delete",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
        json={"comment_id": test_jwt["comment_id"]}
    )
    assert response.status_code == 200
    response_json = response.json()
    assert "pcomment" in response_json

    # pcomment 객체 확인
    assert response_json["pcomment"]["comment_id"] == test_jwt["comment_id"]

# Delete post comment test fail ( 잘못된 jwt )
async def test_delete_comment_fail():
    with pytest.raises(HTTPException) as err:
        response = client.put(
            "/pcomment/delete",
            headers={"Authorization": "Bearer " + str(uuid4())},
            json={"comment_id": 0}
        )
        assert err.value.status_code == HTTP_400_BAD_REQUEST
        assert err.value.detail == "Failed to delete comment"