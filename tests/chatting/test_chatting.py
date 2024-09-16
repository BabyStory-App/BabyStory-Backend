from typing import List, Optional
from auth.auth_handler import decodeJWT, signJWT
from uuid import uuid4
#from fastapi.testclient import TestClient
#from apis.chat.chatroom import router

from db import get_db_session

db = get_db_session()

#client = TestClient(router)
#test_jwt_tmp = None

test_create_chatroom_data = {
    "name": str(uuid4())
}

update_create_chatroom_data = {
    "room_id": 0,
    "name": str(uuid4())
}

def test_create_chatroom(client, test_jwt):
    response = client.post(
        "/chatroom/create",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
        json=test_create_chatroom_data
    )
    print(response.json())

    assert response.status_code == 200
    response_json = response.json()
    assert "chatroom" in response_json
    assert response_json["chatroom"]["name"] == test_create_chatroom_data["name"]
    assert response_json["chatroom"]["parent_id"] == decodeJWT(test_jwt["access_token"]).get('user_id')
    assert response_json["chatroom"]["memberCount"] == 0

# def test_update_chatroom(client, test_jwt):
#     response = client.post(
#         "/chatroom/update",
#         headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
#         json=update_create_chatroom_data
#     )

#     assert response.status_code == 200
#     response_json = response.json()
#     assert "chatroom" in response_json
#     assert response_json["chatroom"]["name"] == update_create_chatroom_data["name"]
#     assert response_json["chatroom"]["parent_id"] == decodeJWT(test_jwt["access_token"]).get('user_id')
#     assert response_json["chatroom"]["memberCount"] == 0

# def test_get_chatroom_list(client, test_jwt):
#     response = client.get(
#         "/chatroom/list",
#         headers={"Authorization": f"Bearer {test_jwt['access_token']}"}
#     )

#     assert response.status_code == 200
#     response_json = response.json()
#     assert "chatrooms" in response_json
#     assert len(response_json["chatrooms"]) > 0
#     for chatroom in response_json["chatrooms"]:
#         assert "name" in chatroom
#         assert "parent_id" in chatroom
#         assert "memberCount" in chatroom
