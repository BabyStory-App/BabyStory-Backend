# from apis.post import router
# from fastapi.testclient import TestClient
# from auth.auth_handler import decodeJWT
# from uuid import uuid4
# from main import app  # assuming your FastAPI app is defined in main.py
# from datetime import *
# from fastapi import HTTPException
# from starlette.status import HTTP_400_BAD_REQUEST
# import pytest

# client = TestClient(router)

# test_jwt_tmp = None

# test_CreatePHeartInput = {
#     "post_id": 1
# }

# """ Create post heart test """
# def test_create_pheart(client, test_jwt):
#     response = client.post(
#         "/post/pheart/create",
#         headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
#         json=test_CreatePHeartInput
#     )
    
#     assert response.status_code == 200
#     response_json = response.json()
#     assert "pheart" in response_json

#     # pheart 객체 확인
#     assert response_json["pheart"]["post_id"] == test_CreatePHeartInput["post_id"]