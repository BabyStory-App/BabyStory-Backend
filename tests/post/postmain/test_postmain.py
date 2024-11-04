from typing import Optional
from auth.auth_handler import decodeJWT
from uuid import uuid4
from datetime import datetime, timedelta

test_friend_jwt = None
test_neighbor_jwt = None
# 친구 생성 json
test_friend_data = {
    "parent_id": str(uuid4()),
    "password": "qw",
    "email": str(uuid4()),
    "nickname": "qw",
    "signInMethod": "qw",
    "emailVerified": 1
}
# 친구 수정 json
test_friend_data_update = {
    "password": "qw",
    "email": test_friend_data['email'],
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
test_neighbor_data = {
    "parent_id": str(uuid4()),
    "password": "ww",
    "email": str(uuid4()),
    "nickname": "ww",
    "signInMethod": "ww",
    "emailVerified": 1
}
# 이웃유저 수정 json
test_neighbor_data_update = {
    "password": "qw",
    "email": test_neighbor_data['email'],
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

# 친구 아이디 json
json_friend = {
    "friend": test_friend_data['parent_id']
}
# 유저 아이디 json
json_user = {
    "friend": None
}

# 게시물 생성 시간
test_time = (datetime.now() - timedelta(days=1)
             ).replace(microsecond=0).isoformat()

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
    "reveal": 1,
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


def test_update_friend(client):
    response = client.put(
        "/parent",
        headers={"Authorization": f"Bearer {test_friend_jwt}"},
        json=test_friend_data_update
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["success"] == 200
    assert "parent" in response_json

    assert response_json["parent"]["mainAddr"] == test_friend_data_update["mainAddr"]


# 이웃유저생성
def test_create_neighbor(client):
    response = client.post(
        "/parent",
        json=test_neighbor_data
    )

    assert response.status_code == 201
    jwt = response.json()["x-jwt"]['access_token']

    global test_neighbor_jwt
    test_neighbor_jwt = jwt


def test_update_neighbor(client):
    response = client.put(
        "/parent",
        headers={
            "Authorization": f"Bearer {test_neighbor_jwt}"},
        json=test_neighbor_data_update
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["success"] == 200
    assert "parent" in response_json

    assert response_json["parent"]["mainAddr"] == test_neighbor_data_update["mainAddr"]


# 유저가 친구를 등록
def test_create_friend_relation1(client, test_jwt):
    response = client.post(
        "/friend/create",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
        json=json_friend
    )

    assert response.status_code == 200
    response_json = response.json()

    jwt = test_jwt['access_token']
    check_id = decodeJWT(jwt).get('user_id')
    global json_user
    json_user["friend"] = check_id

    assert "friend" in response_json
    assert response_json["friend"]["parent_id"] == check_id
    assert response_json["friend"]["friend"] == test_friend_data["parent_id"]


def test_create_friend_relation1_wrong_jwt(client):
    response = client.post(
        "/friend/create",
        headers={"Authorization": "Bearer 1234"},
        json=json_friend
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "user id not found in token."}


def test_create_friend_relation1_not_exist_id(client, test_jwt):
    json_friend["friend"] = "notexist"
    response = client.post(
        "/friend/create",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
        json=json_friend
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Failed to create friend"}


# 친구가 유저를 등록
def test_create_friend_relation2(client, test_jwt):
    global test_friend_jwt
    print(test_friend_jwt)
    response = client.post(
        "/friend/create",
        headers={"Authorization": f"Bearer {test_friend_jwt}"},
        json=json_user
    )

    assert response.status_code == 200
    response_json = response.json()

    check_id = decodeJWT(test_friend_jwt).get('user_id')

    assert "friend" in response_json
    assert response_json["friend"]["parent_id"] == check_id
    assert response_json["friend"]["friend"] == json_user["friend"]

    # friend_id 저장
    test_jwt["friend"] = check_id


# 유저 게시물 생성
def test_create_post(client, test_jwt):
    response = client.post(
        "/post/create",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
        json=test_CreatePostInput
    )

    assert response.status_code == 200
    response_json = response.json()

    assert "post" in response_json

    # post 객체 확인
    assert response_json["post"]["reveal"] == test_CreatePostInput["reveal"]
    assert response_json["post"]["title"] == test_CreatePostInput["title"]
    assert response_json["post"]["hashList"] == test_CreatePostInput["hashList"]

    # post_id 저장
    test_jwt["post_id"] = response_json["post"]["post_id"]


# 친구 게시물 생성
def test_create_post_friend(client):
    global test_friend_jwt
    response = client.post(
        "/post/create",
        headers={"Authorization": f"Bearer {test_friend_jwt}"},
        json=test_CreatePostInput_friend
    )

    assert response.status_code == 200
    response_json = response.json()

    assert "post" in response_json

    # post 객체 확인
    assert response_json["post"]["reveal"] == test_CreatePostInput_friend["reveal"]
    assert response_json["post"]["title"] == test_CreatePostInput_friend["title"]
    assert response_json["post"]["hashList"] == test_CreatePostInput_friend["hashList"]


# 메인페이지 생성
def test_create_postmain(client, test_jwt):
    response = client.post(
        "/main/create",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
    )

    assert response.status_code == 200
    response_json = response.json()

    # create time을 전날로 설정 후에 테스트했었는데 service에서 create time을 현재
    # 시간으로 강제 설정했기 때문에 코드 사용 불가
    # assert "banner" in response_json
    # assert response_json["banner"][0]["title"] == "test title"
    # assert response_json["banner"][0]["author_name"] == "qq"

    assert "friend" in response_json
    assert response_json["friend"][0]["title"] == "tt tle"
    assert response_json["friend"][0]["author_name"] == "qw"

    assert "friend_read" in response_json
    assert response_json["friend_read"][0]["title"] == "tt tle"
    assert response_json["friend_read"][0]["author_name"] == "qw"

    assert "neighbor" in response_json
    assert response_json["neighbor"][0]["name"] == "qw"
    assert response_json["neighbor"][0]["mainAddr"] == "qq"
    assert response_json["neighbor"][0]["desc"] == "qw"

    assert "neighbor_post" in response_json
    assert response_json["neighbor_post"][0]["title"] == "test title"
    assert response_json["neighbor_post"][0]["author_name"] == "qw"

    assert "highview" in response_json
    assert response_json["highview"][0]["title"] == "test title"
    assert response_json["highview"][0]["author_name"] == "qw"

    assert "hashtag" in response_json
    assert response_json["hashtag"][0]["title"] == "tt tle"
    assert response_json["hashtag"][0]["author_name"] == "qw"
    assert response_json["hashtag"][0]["hash"] == "qw"


def test_create_postmain_wrong_jwt(client):
    response = client.post(
        "/main/create",
        headers={"Authorization": "Bearer 1234"}
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "user id not found in token."}


def test_create_recommend_friend(client, test_jwt):
    response = client.post(
        "post/search/recommend",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
        json={
            "type": "friend",
            "size": 1,
            "page": 1
        }
    )

    assert response.status_code == 200
    response_json = response.json()

    assert "result" in response_json
    print(response_json)
    assert response_json["result"][0]["title"] == "tt tle"
    assert response_json["result"][0]["author_name"] == "qw"


def test_create_recommend_friend_read(client, test_jwt):
    response = client.post(
        "post/search/recommend",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
        json={
            "type": "friend_read",
            "size": 1,
            "page": 1
        }
    )

    assert response.status_code == 200
    response_json = response.json()

    assert "result" in response_json
    assert response_json["result"][0]["title"] == "tt tle"
    assert response_json["result"][0]["author_name"] == "qw"


def test_create_recommend_wrong_type(client, test_jwt):
    response = client.post(
        "post/search/recommend",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
        json={
            "type": "wrong_type",
            "size": 1,
            "page": 1
        }
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "recommend not found"}


def test_create_recommend_wrong_size(client, test_jwt):
    response = client.post(
        "post/search/recommend",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
        json={
            "type": "friend",
            "size": -2,
            "page": 1
        }
    )

    assert response.status_code == 406
    assert response.json() == {"detail": "size must be -1 or greater than 0"}


def test_create_recommend_wrong_page(client, test_jwt):
    response = client.post(
        "post/search/recommend",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
        json={
            "type": "friend",
            "size": 1,
            "page": -2
        }
    )

    assert response.status_code == 406
    assert response.json() == {"detail": "page must be -1 or greater than 0"}