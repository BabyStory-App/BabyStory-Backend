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

test_CreatePostInput = {
    "reveal": 0,
    "title": "test title",
    "content": "test content",
    "hashList": "string,qq"
}

test_UpdatePostInput = {
    "post_id": 1,
    "reveal": 2,
    "title": "update title",
    "content": "update content",
    "hashList": "test,hash"
}
test_UploadPhoto = {
    "fileList": ["test1.png", "test2.png", "test3.png"]
}



""" Create post test """
def test_create_post(client, test_jwt):
    response = client.post(
        "/post/create",
        # 자물쇠 있는 애들에 넣어주기
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
        json=test_CreatePostInput
    )

    assert response.status_code == 200
    response_json = response.json()
    assert "post" in response_json

    # post 객체 확인
    for key in test_CreatePostInput:
        if key in response_json["post"]:
            if key == "createTime":
                assert response_json["post"]["createTime"][:10] == test_CreatePostInput["createTime"][:10]
            assert response_json["post"][key] == test_CreatePostInput[key]

    # content 파일이 있는지 확인
    assert create_file_exist(os.path.join(POST_CONTENT_DIR, str(response_json["post"]["post_id"]) + '.txt'))

    # post_id를 test_jwt에 저장하여 다른곳 에서도 사용 가능하게 합니다.
    test_jwt["post_id"] = response_json["post"]["post_id"]


# Create post test fail ( 잘못된 jwt )
async def test_createPost_fail():
    with pytest.raises(HTTPException) as err:
        headers = {"Authorization": f"Bearer wrong_jwt_token"}
        client.post("/post/create", headers=headers)
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "Failed to create post"

# Create post test fail ( reveal 값이 0 ~ 3이 아닌 경우 )
async def test_createPost_fail():
    with pytest.raises(HTTPException) as err:
        test_CreatePostInput["reveal"] != 0 or test_CreatePostInput[
            "reveal"] != 1 or test_CreatePostInput["reveal"] != 2 or test_CreatePostInput["reveal"] != 3
        client.post("/post/create", json=test_CreatePostInput)
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "Invalid reveal value"



""" upload post photo test """
def test_upload_post_photo(client, test_jwt):
    response = client.post(
        "/post/photoUpload",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
        files={"fileList": [open(os.path.join(TEST_ASSET_DIR, file), "rb") for file in test_UploadPhoto["fileList"]]},
        data={"postid": test_jwt["post_id"]}
    )
    assert response.status_code == 200
    response_json = response.json()
    assert "post" in response_json

    # post 객체 확인
    assert response_json["post_id"] == test_jwt["post_id"]

    # photo 파일이 있는지 확인
    for file in test_UploadPhoto["fileList"]:
        file_type = file.split('.')[-1]
        assert create_file_exist(os.path.join(POST_PHOTO_DIR, f"{response_json['post']['post_id']}.{file_type}"))



""" Get all post test """
def test_get_all_post(client, test_jwt):
    response = client.get(
        "/post/",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"}
    )
    assert response.status_code == 200, response.text
    response_json = response.json()
    assert isinstance(response_json, list)

# Get all post test fail ( 잘못된 jwt )
async def test_getPost_fail():
    with pytest.raises(HTTPException) as err:
        headers = {"Authorization": f"Bearer wrong_jwt_token"}
        client.get("/", headers=headers)
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "Failed to get all post"



""" Get post by post_id test """
def test_get_post(client, test_jwt):
    response = client.get(
        f"/post/{test_jwt['post_id']}",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert isinstance(response_json, dict)

    # post 객체 확인
    assert response_json["post_id"] == test_jwt["post_id"]

# Get post by post_id test fail ( 잘못된 jwt )
async def test_getPost_fail():
    with pytest.raises(HTTPException) as err:
        headers = {"Authorization": f"Bearer wrong_jwt_token"}
        client.get("/{post_id}", headers=headers)
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "Failed to get post"

# Get post by post_id test fail ( 잘못된 post_id )
async def test_getPost_fail():
    with pytest.raises(HTTPException) as err:
        client.get("/{post_id}")
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "post not found"

# Get post by post_id test fail ( 데이터가 없는 경우 )
async def test_getPost_fail():
    with pytest.raises(HTTPException) as err:
        client.get("/{post_id}")
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "Failed to get one post"



""" Update post test """
def test_update_post(client, test_jwt):
    test_UpdatePostInput["post_id"] = test_jwt["post_id"]

    response = client.put(
        f"/post/update/{test_jwt['post_id']}",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
        json=test_UpdatePostInput
    )
    assert response.status_code == 200
    response_json = response.json()
    assert "post" in response_json

    # post 객체 확인
    for key in test_UpdatePostInput:
        if key in response_json["post"]:
            assert response_json["post"][key] == test_UpdatePostInput[key]

    assert response_json["success"] == 200

# Update post test fail ( 잘못된 jwt )
async def test_updatePost_fail():
    with pytest.raises(HTTPException) as err:
        headers = {"Authorization": f"Bearer wrong_jwt_token"}
        client.put("/post/update/{post_id}", headers=headers)
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "Failed to update post"

# Update post test fail ( 잘못된 post_id )
async def test_updatePost_fail():
    with pytest.raises(HTTPException) as err:
        client.put("/post/update/{post_id}")
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "post not found"

# Update post test fail ( reveal 값이 0 ~ 3이 아닌 경우 )
async def test_updatePost_fail():
    with pytest.raises(HTTPException) as err:
        test_UpdatePostInput["reveal"] != 0 or test_UpdatePostInput[
            "reveal"] != 1 or test_UpdatePostInput["reveal"] != 2 or test_UpdatePostInput["reveal"] != 3
        client.put("/post/update/{post_id}", json=test_UpdatePostInput)
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "Invalid reveal value"

# Update post test fail ( 데이터수정에 실패한 경우 )
async def test_updatePost_fail():
    with pytest.raises(HTTPException) as err:
        client.put("/post/update/{post_id}", json=test_UpdatePostInput)
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "Failed to update post"



""" Delete post test """
def test_delete_post(client, test_jwt):
    response = client.put(
        f"/post/delete/{test_jwt['post_id']}",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
        json={"post_id": test_jwt["post_id"]}
    )
    assert response.status_code == 200
    response_json = response.json()
    assert "post" in response_json

    # post 객체 확인
    assert response_json["post"]["post_id"] == test_jwt["post_id"]

# Delete post test fail ( 잘못된 jwt )
async def test_deletePost_fail():
    with pytest.raises(HTTPException) as err:
        headers = {"Authorization": f"Bearer wrong_jwt_token"}
        client.delete("/post/delete/{post_id}", headers=headers)
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "Failed to delete post"

# Delete post test fail ( 잘못된 post_id )
async def test_deletePost_fail():
    with pytest.raises(HTTPException) as err:
        client.delete("/post/delete/{post_id}")
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "post not found"

# Delete post test fail ( 데이터삭제에 실패한 경우 )
async def test_deletePost_fail():
    with pytest.raises(HTTPException) as err:
        client.delete("/post/delete/{post_id}")
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "Failed to delete post"