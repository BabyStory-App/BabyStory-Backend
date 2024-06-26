from typing import List, Optional
from auth.auth_handler import decodeJWT,signJWT
from uuid import uuid4

# test_create_data = {
#     "reveal": 0,
#     "title": "qq",
#     "content": "qq",
#     "photoId": None,
#     "createTime": "2024-06-7T07:00:00",
#     "modifyTime": None,
#     "deleteTime": None,
#     "pHeart": 0,
#     "pScript": 0,
#     "pView": 10,
#     "pComment": 0,
#     "hashList": "string,qq"
# }

# def test_create_post(client,test_jwt):
#     response = client.post(
#         "/post/create",
#         headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
#         json=test_create_data
#     )

#     assert response.status_code == 200
#     response_json = response.json()

#     assert "post" in response_json

#     for key in test_create_data:
#         assert response_json["post"][key] == test_create_data[key]

#     assert "x-jwt" in response_json
#     assert "access_token" in response_json["x-jwt"]

#     jwt = response.json()["x-jwt"]['access_token']
#     check_id = decodeJWT(jwt).get('user_id')
#     assert check_id == test_create_data["parent_id"]


# def test_get_post(client,test_jwt):
#     response = client.get(
#         "/post",
#         headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
#     )

#     assert response.status_code == 200

# def test_create_postmain(client,test_jwt):
#     response = client.post(
#         "/main/create",
#         headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
#     )

#     assert response.status_code == 200
#     response_json = response.json()

#     assert "banner" in response_json
#     assert "friend" in response_json
#     assert "friend_read" in response_json
#     assert "neighbor" in response_json
#     assert "neighbor_post" in response_json
#     assert "highview" in response_json

#     assert response_json["highview"][0]["post_id"] == 2
#     assert response_json["highview"][0]["photoId"] == None
#     assert response_json["highview"][0]["title"] == "Example Title"
#     assert response_json["highview"][0]["author_name"] == "string"
#     assert response_json["highview"][0]["desc"] == "This is an example content for the post."
    
#     assert "hashtag" in response_json
#     assert response_json["hashtag"][0]["post_id"] == 2
#     assert response_json["hashtag"][0]["photoId"] == None
#     assert response_json["hashtag"][0]["title"] == "Example Title"
#     assert response_json["hashtag"][0]["author_name"] == "string"
#     assert response_json["hashtag"][0]["desc"] == "This is an example content for the post."
#     assert response_json["hashtag"][0]["hash"] == "string,example,hash,tags"


