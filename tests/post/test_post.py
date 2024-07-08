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

test_CreatePostInput = {
    "reveal": 0,
    "title": "qq",
    "content": "qq",
    "hashList": "string,qq"
}

test_UpdatePostInput = {
    "post_id": 1,
    "reveal": 2,
    "title": "test title",
    "hashList": "test hash"
}



""" Create post test """
def test_create_post(client,test_jwt):
    response = client.post(
        "/post/create",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"},   # 자물쇠 있는 애들에 넣어주기
        json=test_CreatePostInput
    )
    
    assert response.status_code == 200
    response_json = response.json()


    assert "post" in response_json

    # post 객체 확인
    for key in test_CreatePostInput:
        if key in response_json["post"]:
            assert response_json["post"][key] == test_CreatePostInput[key]


# Create post test fail ( 잘못된 jwt )
async def test_createPost_fail():
    with pytest.raises(HTTPException) as err:
        headers={"Authorization": f"Bearer wrong_jwt_token"}
        client.post("/post/create", headers=headers)
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "Failed to create post"


# Create post test fail ( reveal 값이 0 ~ 3이 아닌 경우 )
async def test_createPost_fail():
    with pytest.raises(HTTPException) as err:
        test_CreatePostInput["reveal"] != 0 or test_CreatePostInput["reveal"] != 1 or test_CreatePostInput["reveal"] != 2 or test_CreatePostInput["reveal"] != 3
        client.post("/post/create", json=test_CreatePostInput)
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "Invalid reveal value"



""" Get all post test """
# def test_get_post(client,test_jwt):
#     response = client.get(
#         "/post/",
#         headers={"Authorization": f"Bearer {test_jwt['access_token']}"}
#     )
#     assert response.status_code == 200
#     response_json = response.json()
#     assert "post" in response_json

#     # post 객체 확인
#     for key in test_CreatePostInput:
#         if key in response_json["post"]:
#             assert response_json["post"][key] == test_CreatePostInput[key]

# Get all post test fail ( 잘못된 jwt )
async def test_getPost_fail():
    with pytest.raises(HTTPException) as err:
        headers={"Authorization": f"Bearer wrong_jwt_token"}
        client.get("/", headers=headers)
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "Failed to get all post"



""" Get post by post_id test """
# def test_get_all_post(client,test_jwt):
#     response = client.get(
#         "/post/{post_id}",
#         headers={"Authorization": f"Bearer {test_jwt['access_token']}"}
#     )
#     assert response.status_code == 200
#     response_json = response.json()
#     assert "post" in response_json

#     # post 객체 확인
#     for key in test_CreatePostInput:
#         if key in response_json["post"]:
#             assert response_json["post"][key] == test_CreatePostInput[key]   

# Get post by post_id test fail ( 잘못된 jwt )
async def test_getPost_fail():
    with pytest.raises(HTTPException) as err:
        headers={"Authorization": f"Bearer wrong_jwt_token"}
        client.get("/{post_id}", headers=headers)
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "Failed to get post" 

# Get post by post_id test fail ( 잘못된 post_id )
async def test_getPost_fail():
    with pytest.raises(HTTPException) as err:
        client.get("/{post_id}")
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "Failed to get post"



""" Update post test """
# def test_update_post(client,test_jwt):
#     response = client.put(
#         "/post/update/{post_id}",
#         headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
#         json=test_UpdatePostInput
#     )
    
#     assert response.status_code == 200
#     response_json = response.json()

#     assert "post" in response_json

#     # post 객체 확인
#     for key in test_UpdatePostInput:
#         if key in response_json["post"]:
#             assert response_json["post"][key] == test_UpdatePostInput[key]

# Update post test fail ( 잘못된 jwt )
async def test_updatePost_fail():
    with pytest.raises(HTTPException) as err:
        headers={"Authorization": f"Bearer wrong_jwt_token"}
        client.put("/post/update/{post_id}", headers=headers)
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "Failed to update post"

# Update post test fail ( 잘못된 post_id )
async def test_updatePost_fail():
    with pytest.raises(HTTPException) as err:
        client.put("/post/update/{post_id}")
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "Failed to update post"

# Update post test fail ( reveal 값이 0 ~ 3이 아닌 경우 )
async def test_updatePost_fail():
    with pytest.raises(HTTPException) as err:
        test_UpdatePostInput["reveal"] != 0 or test_UpdatePostInput["reveal"] != 1 or test_UpdatePostInput["reveal"] != 2 or test_UpdatePostInput["reveal"] != 3
        client.put("/post/update/{post_id}", json=test_UpdatePostInput)
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "Invalid reveal value"

    