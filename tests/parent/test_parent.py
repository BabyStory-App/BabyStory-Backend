from typing import List, Optional
from auth.auth_handler import decodeJWT,signJWT
from uuid import uuid4

test_jwt = None

test_create_data={
    "parent_id": str(uuid4()),
    "password": "qq",
    "email": str(uuid4()),
    "name": "qq",
    "nickname": "qq",
    "gender": 0,
    "signInMethod": "qq",
    "emailVerified": 1,
    "photoId": "qq",
    "description": "qq",
    "mainAddr": "qq",
    "subAddr": "qq",
    "hashList": "qq"
}

update_data = {
            "parent_id": test_create_data["parent_id"],
            "password": "qw",
            "email": str(uuid4()),
            "name": "qw",
            "nickname": "qw",
            "gender": 1,
            "signInMethod": "qw",
            "emailVerified": 0,
            "photoId": "qw",
            "description": "qw",
            "mainAddr": "qw",
            "subAddr": "qw",
            "hashList": "qw"
        }

def test_create_parent(client):
    response = client.post(
        "/parent",
        json=test_create_data
    )
    
    assert response.status_code == 201
    response_json = response.json()
    assert "parent" in response_json

    # 각 필드를 반복문으로 확인하여 일치하는지 검사
    for key in test_create_data:
        print(key)
        assert response_json["parent"][key] == test_create_data[key]

    assert "x-jwt" in response_json
    assert "access_token" in response_json["x-jwt"]

    # jwt 확인
    jwt = response.json()["x-jwt"]['access_token']
    check_id = decodeJWT(jwt).get('user_id')
    assert check_id == test_create_data["parent_id"]

    global test_jwt
    test_jwt = response_json["x-jwt"]["access_token"]

def test_modify_jwt(test_jwt):
    test_jwt = test_jwt

def test_create_parent_badtoken(client):
    response = client.post(
        "/parent",
        json=test_create_data
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Failed to create parent"}

def test_get_parent(client):
    response = client.get(
        "/parent",
        headers={"Authorization": f"Bearer {test_jwt}"}
    )
    assert response.status_code == 200
    response_json = response.json()
    assert "parent" in response_json

    # 각 필드를 반복문으로 확인하여 일치하는지 검사
    for key in test_create_data:
        assert response_json["parent"][key] == test_create_data[key]

    assert "x-jwt" in response_json
    assert "access_token" in response_json["x-jwt"]

    # jwt 확인
    jwt = response.json()["x-jwt"]['access_token']
    check_id = decodeJWT(jwt).get('user_id')
    assert check_id == test_create_data["parent_id"]

# 삭제하고 나서 다시해보자
def test_get_parent_badtoken(client):
    response = client.get(
        "/parent",
        headers={"Authorization": f"Bearer {11}"}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "user id not found in token."}


def test_update_parent(client):
    response = client.put(
        "/parent",
        headers={"Authorization": f"Bearer {test_jwt}"},
        json=update_data
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["success"] == 200
    assert "parent" in response_json

    # json과 동일한지 확인
    for key in response_json["parent"]:
        assert response_json["parent"][key] == update_data[key]

def test_update_parent_badtoken(client):
    response = client.put(
        "/parent",
        headers={"Authorization": f"Bearer {11}"},
        json=update_data
    )
    response_json = response.json()
    assert response.status_code == 403
    assert response.json() == {"detail": "user id not found in token."}


def test_delete_parent(client):
    response = client.delete(
        "/parent",
        headers={"Authorization": f"Bearer {test_jwt}"}
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["success"] == 200

def test_delete_parent_badtoken(client):
    response = client.delete(
        "/parent",
        headers={"Authorization": f"Bearer {11}"}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "user id not found in token."}

# babyid가 이미 존재해야함
# def test_create_pbconnect(client):
#     response = client.post(
#         "/parent/pbconnect",
#         headers={"Authorization": f"Bearer {test_jwt}"},
#         json={"baby_id": str(uuid4())}
#     )
#     assert response.status_code == 200
#     response_json = response.json()
#     assert response_json["success"] == 200
