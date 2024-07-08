from typing import Optional
from auth.auth_handler import decodeJWT
from uuid import uuid4
from datetime import datetime, timedelta

test_friend_jwt=None
# 친구 생성 json
test_friend_data={
    "parent_id": str(uuid4()),
    "password": "qw",
    "email": str(uuid4()),
    "name": "qw",
    "nickname": "qw",
    "gender": 0,
    "signInMethod": "qw",
    "emailVerified": 1,
    "photoId": "qw",
    "description": "qw",
    "mainAddr": "qq",
    "subAddr": "qw",
    "hashList": "qw,string"
}
# 이웃유저 json
test_neighbor_data={
    "parent_id": str(uuid4()),
    "password": "ww",
    "email": str(uuid4()),
    "name": "ww",
    "nickname": "ww",
    "gender": 0,
    "signInMethod": "ww",
    "emailVerified": 1,
    "photoId": "ww",
    "description": "ww",
    "mainAddr": "qq",
    "subAddr": "ww",
    "hashList": "qw,string"
}
# 친구 아이디 json
json_friend={
    "friend": test_friend_data['parent_id']
}
# 유저 아이디 json
json_user={
    "friend": None
}

# 게시물 생성 시간
test_time = (datetime.now() - timedelta(days=1)).replace(microsecond=0).isoformat()
# 게시물 생성 json
test_CreatePostInput = {
    "reveal": 1,
    "title": "test title",
    "content": "test post",
    "createTime": test_time,
    "hashList": "qq"
}
# 친구 게시물 생성 json
test_CreatePostInput_friend = {
    "reveal": 0,
    "title": "tt tle",
    "content": "tt post",
    "createTime": test_time,
    "hashList": "qw"
}
# 친구유저생성
def test_create_friend(client):
    response = client.post(
        "/parent",
        json=test_friend_data
    )
    
    assert response.status_code == 201
    response_json = response.json()

    assert "x-jwt" in response_json
    assert "access_token" in response_json["x-jwt"]

    # jwt 확인
    jwt = response.json()["x-jwt"]['access_token']

    global test_friend_jwt
    test_friend_jwt = jwt

# 이웃유저생성
def test_create_neighbor(client):
    client.post(
        "/parent",
        json=test_neighbor_data
    )

# # 유저가 친구를 등록
# def test_create_friend_relation1(client,test_jwt):
#     response = client.post(
#         "/friend/create",
#         headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
#         json=json_friend
#     )
    
#     assert response.status_code == 200
#     response_json = response.json()

#     jwt = test_jwt['access_token']
#     check_id = decodeJWT(jwt).get('user_id')
#     global json_user
#     json_user["friend"] = check_id

#     assert "friend" in response_json
#     assert response_json["friend"]["parent_id"] == check_id
#     assert response_json["friend"]["friend"] == test_friend_data["parent_id"]

# # 친구가 유저를 등록
# def test_create_friend_relation2(client):
#     global test_friend_jwt
#     print(test_friend_jwt)
#     response = client.post(
#         "/friend/create",
#         headers={"Authorization": f"Bearer {test_friend_jwt}"},
#         json=json_user
#     )
    
#     assert response.status_code == 200
#     response_json = response.json()

#     check_id = decodeJWT(test_friend_jwt).get('user_id')

#     assert "friend" in response_json
#     assert response_json["friend"]["parent_id"] == check_id
#     assert response_json["friend"]["friend"] == json_user["friend"]
    

# # 유저 게시물 생성
# def test_create_post(client,test_jwt):
#     response = client.post(
#         "/post/create",
#         headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
#         json=test_CreatePostInput
#     )
    
#     assert response.status_code == 200
#     response_json = response.json()

#     assert "post" in response_json

#     # post 객체 확인
#     assert response_json["post"]["reveal"] == test_CreatePostInput["reveal"]
#     assert response_json["post"]["title"] == test_CreatePostInput["title"]
#     assert response_json["post"]["createTime"] == test_CreatePostInput["createTime"]
#     assert response_json["post"]["hashList"] == test_CreatePostInput["hashList"]

# # 친구 게시물 생성
# def test_create_post_friend(client):
#     global test_friend_jwt
#     response = client.post(
#         "/post/create",
#         headers={"Authorization": f"Bearer {test_friend_jwt}"},
#         json=test_CreatePostInput_friend
#     )
    
#     assert response.status_code == 200
#     response_json = response.json()

#     assert "post" in response_json

#     # post 객체 확인
#     assert response_json["post"]["reveal"] == test_CreatePostInput_friend["reveal"]
#     assert response_json["post"]["title"] == test_CreatePostInput_friend["title"]
#     assert response_json["post"]["createTime"] == test_CreatePostInput_friend["createTime"]
#     assert response_json["post"]["hashList"] == test_CreatePostInput_friend["hashList"]

# # 메인페이지 생성
# def test_create_postmain(client,test_jwt):
#     response = client.post(
#         "/main/create",
#         headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
#     )

#     assert response.status_code == 200
#     response_json = response.json()

#     assert "banner" in response_json
#     assert response_json["banner"][0]["title"] == "test title"
#     assert response_json["banner"][0]["author_name"] == "qq"

#     assert "friend" in response_json
#     assert response_json["friend"][0]["title"] == "tt tle"
#     assert response_json["friend"][0]["author_name"] == "qw"

#     assert "friend_read" in response_json
#     assert response_json["friend_read"][0]["title"] == "tt tle"
#     assert response_json["friend_read"][0]["author_name"] == "qw"

#     assert "neighbor" in response_json
#     assert response_json["neighbor"][0]["name"] == "ww"
#     assert response_json["neighbor"][0]["mainAddr"] == "qq"
#     assert response_json["neighbor"][0]["desc"] == "ww"

#     assert "neighbor_post" in response_json
#     assert response_json["neighbor_post"][0]["title"] == "tt tle"
#     assert response_json["neighbor_post"][0]["author_name"] == "qw"

#     assert "highview" in response_json
#     assert response_json["highview"][0]["title"] == "test title"
#     assert response_json["highview"][0]["author_name"] == "qq"
    
#     assert "hashtag" in response_json
#     assert response_json["hashtag"][0]["title"] == "test title"
#     assert response_json["hashtag"][0]["author_name"] == "qq"
#     assert response_json["hashtag"][0]["hash"] == "qq"