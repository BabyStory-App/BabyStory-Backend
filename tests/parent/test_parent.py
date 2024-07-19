from typing import List, Optional
from auth.auth_handler import decodeJWT, signJWT
from uuid import uuid4

from db import get_db_session
from model.parent import ParentTable

db = get_db_session()

test_jwt_tmp = None

test_create_data = {
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
    "hashList": "qq,string"
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

update_data2 = {
    "password": "qw",
    "email": test_create_data['email'],
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


def test_create_parent(client, test_jwt):
    response = client.post(
        "/parent",
        json=test_create_data
    )

    assert response.status_code == 201
    response_json = response.json()
    assert "parent" in response_json

    assert response_json["parent"]["parent_id"] == test_create_data["parent_id"]
    assert response_json["parent"]["password"] == test_create_data["password"]
    assert response_json["parent"]["email"] == test_create_data["email"]
    assert response_json["parent"]["nickname"] == test_create_data["nickname"]
    assert response_json["parent"]["signInMethod"] == test_create_data["signInMethod"]
    assert response_json["parent"]["emailVerified"] == test_create_data["emailVerified"]

    assert "x-jwt" in response_json
    assert "access_token" in response_json["x-jwt"]

    # jwt 확인
    jwt = response.json()["x-jwt"]['access_token']
    check_id = decodeJWT(jwt).get('user_id')
    assert check_id == test_create_data["parent_id"]

    test_jwt["access_token"] = response_json["x-jwt"]["access_token"]


def test_create_parent_badtoken(client):
    response = client.post(
        "/parent",
        json=test_create_data
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Failed to create parent"}


def test_get_parent(client, test_jwt):
    response = client.get(
        "/parent",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"}
    )
    assert response.status_code == 200
    response_json = response.json()
    assert "parent" in response_json

    assert response_json["parent"]["parent_id"] == test_create_data["parent_id"]
    assert response_json["parent"]["password"] == test_create_data["password"]
    assert response_json["parent"]["email"] == test_create_data["email"]
    assert response_json["parent"]["nickname"] == test_create_data["nickname"]
    assert response_json["parent"]["signInMethod"] == test_create_data["signInMethod"]
    assert response_json["parent"]["emailVerified"] == test_create_data["emailVerified"]

    assert "x-jwt" in response_json
    assert "access_token" in response_json["x-jwt"]

    # jwt 확인
    jwt = response.json()["x-jwt"]['access_token']
    check_id = decodeJWT(jwt).get('user_id')
    assert check_id == test_create_data["parent_id"]


def test_get_parent_badtoken(client):
    response = client.get(
        "/parent",
        headers={"Authorization": f"Bearer {11}"}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "user id not found in token."}


login_data = {
    "email": test_create_data["email"],
    "password": test_create_data["password"]
}


def test_login_parent(client):
    response = client.post(
        "/parent/login",
        json=login_data
    )

    assert response.status_code == 200
    response_json = response.json()
    assert "parent" in response_json

    assert response_json["parent"]["parent_id"] == test_create_data["parent_id"]
    assert response_json["parent"]["password"] == test_create_data["password"]
    assert response_json["parent"]["email"] == test_create_data["email"]
    assert response_json["parent"]["nickname"] == test_create_data["nickname"]
    assert response_json["parent"]["signInMethod"] == test_create_data["signInMethod"]
    assert response_json["parent"]["emailVerified"] == test_create_data["emailVerified"]

    assert "x-jwt" in response_json
    assert "access_token" in response_json["x-jwt"]

    # jwt 확인
    jwt = response.json()["x-jwt"]['access_token']
    check_id = decodeJWT(jwt).get('user_id')
    assert check_id == test_create_data["parent_id"]


def test_login_nonexist_email(client):
    login_data2 = login_data.copy()
    login_data2['email'] = str(uuid4())
    response = client.post(
        "/parent/login",
        json=login_data2
    )

    assert response.status_code == 406
    assert response.json() == {"detail": "Email not found"}


def test_login_wrong_password(client):
    login_data3 = login_data.copy()
    login_data3['password'] = str(uuid4())
    response = client.post(
        "/parent/login",
        json=login_data3
    )

    assert response.status_code == 406
    assert response.json() == {"detail": "wrong password"}


def test_update_parent(client, test_jwt):
    response = client.put(
        "/parent",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
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

    assert response.status_code == 403
    assert response.json() == {"detail": "user id not found in token."}

# gender를 문자열 100으로 수정한 경우


def test_update_parent_badgender(client, test_jwt):
    update_data2 = update_data.copy()
    update_data2['gender'] = '100'
    response = client.put(
        "/parent",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
        json=update_data2
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Gender must be 0, 1, 2"}
    # db에 적용되지 않았는지 확인
    assert db.query(ParentTable).filter(
        ParentTable.parent_id == update_data2['parent_id'],
        ParentTable.gender == '100').first() is None


def test_delete_parent(client, test_jwt):
    response = client.delete(
        "/parent",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"}
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
# def test_create_pbconnect(client,test_jwt):
#     response = client.post(
#         "/parent/pbconnect",
#         headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
#         json={"baby_id": str(uuid4())}
#     )
#     assert response.status_code == 200
#     response_json = response.json()
#     assert response_json["success"] == 200


def test_create_parent_two(client, test_jwt):
    response = client.post(
        "/parent",
        json=test_create_data
    )

    assert response.status_code == 201
    response_json = response.json()
    assert "parent" in response_json

    assert response_json["parent"]["parent_id"] == test_create_data["parent_id"]
    assert response_json["parent"]["password"] == test_create_data["password"]
    assert response_json["parent"]["email"] == test_create_data["email"]
    assert response_json["parent"]["nickname"] == test_create_data["nickname"]
    assert response_json["parent"]["signInMethod"] == test_create_data["signInMethod"]
    assert response_json["parent"]["emailVerified"] == test_create_data["emailVerified"]

    assert "x-jwt" in response_json
    assert "access_token" in response_json["x-jwt"]

    # jwt 확인
    jwt = response.json()["x-jwt"]['access_token']
    check_id = decodeJWT(jwt).get('user_id')
    assert check_id == test_create_data["parent_id"]

    test_jwt["access_token"] = response_json["x-jwt"]["access_token"]


def test_update_parent_two(client, test_jwt):
    response = client.put(
        "/parent",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
        json=update_data2
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["success"] == 200
    assert "parent" in response_json


def test_get_friends(client, test_jwt):
    response = client.get(
        "/parent/friends",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"}
    )
    assert response.status_code == 200
    response_json = response.json()
    assert "friends" in response_json
    assert response_json["friends"] == {}
