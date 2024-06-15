import pytest
from apis.post import router
from fastapi.testclient import TestClient
from auth.auth_handler import decodeJWT, signJWT
from uuid import uuid4, uuid3
from main import app  # assuming your FastAPI app is defined in main.py
from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

client = TestClient(router)
test_user_jwt = None

test_CreatePostInput = {
    "post_id": str(uuid4()),
    "reveal": 1,
    "title": "test title",
    "content": "test post",
    "photoId": "test photo",
    "createTime": "2021-10-01T00:00:00",
    "hashList": "test hash"
}

test_UpdatePostInput = {
    "post_id": str(uuid4()),
    "reveal": 2,
    "title": "test title",
    "content": "test post",
    "photoId": "test photo",
    "modifyTime": "2021-10-01T00:00:00",
    "hashList": "test hash"
}

# Create post test
def test_create_post():
    response = client.post("/create", json=test_CreatePostInput)
    assert response.status_code == 200
    res_json = response.json()
    post_json = res_json["post"]

    # post 객체 확인
    assert post_json["reveal"] == test_CreatePostInput["reveal"]
    assert post_json["title"] == test_CreatePostInput["title"]
    assert post_json["content"] == test_CreatePostInput["content"]
    assert post_json["photoId"] == test_CreatePostInput["photoId"]
    assert post_json["createTime"] == test_CreatePostInput["createTime"]
    assert post_json["hashList"] == test_CreatePostInput["hashList"]

    # jwt 확인
    jwt = response.json()["x-jwt"]['access_token']
    check_id = decodeJWT(jwt).get('user_id')
    assert check_id == test_CreatePostInput["parent_id"]

    # jwt를 저장 -> 다른 함수에서 사용하기 위함
    global test_user_jwt
    test_user_jwt = jwt

# Create post test fail
def test_createPost_fail():
    with pytest.raises(HTTPException) as err:
        client.post("/404test")
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "Failed to create post"



# Get all post test
def test_get_post():
    response = client.get("/")
    assert response.status_code == 200
    res_json = response.json()

    # parnet_id 확인
    


# Get post by post_id test
def test_get_all_post():
    response = client.get("/{post_id}", params={"post_id": test_CreatePostInput["post_id"]})
    assert response.status_code == 200
    assert response.json()["post_id"] == test_CreatePostInput["post_id"]

# Get post by post_id test fail
def test_get_post_fail():
    with pytest.raises(HTTPException) as err:
        client.get("/{post_id}")
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "Failed to get post"



# Update post test
def test_update_post():
    response = client.put("/{post_id}", json=test_UpdatePostInput)
    assert response.status_code == 200
    res_json = response.json()
    post_json = res_json["post"]

    # post 객체 확인
    assert post_json["reveal"] == test_CreatePostInput["reveal"]
    assert post_json["title"] == test_UpdatePostInput["title"]
    assert post_json["content"] == test_UpdatePostInput["content"]
    assert post_json["photoId"] == test_UpdatePostInput["photoId"]
    assert post_json["modifyTime"] == test_UpdatePostInput["modifyTime"]
    assert post_json["hashList"] == test_UpdatePostInput["hashList"]

# Update post test fail
def test_update_post_fail():
    with pytest.raises(HTTPException) as err:
        client.put("/{post_id}")
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "Failed to update post"



# Delete post test
def test_delete_post():
    response = client.delete("/{post_id}")
    assert response.status_code == 200
    assert response.json()["success"] == 200

# Delete post test fail
def test_delete_post_fail():
    with pytest.raises(HTTPException) as err:
        client.delete("/{post_id}")
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "Failed to delete post"