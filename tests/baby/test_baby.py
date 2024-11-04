from datetime import *
from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST
import pytest
from utils.os import *
from constants.path import *

test_jwt_tmp = None


test_foetus = {
    "baby_id": "test_baby_id",
    "obn": "딱풀",
}

test_baby = {
    "baby_id": "test_baby_id",
    "obn": "딱풀",
    "name": "아기"
}


""" Create baby """
def test_create_baby1(client, test_jwt):
    response = client.post(
        "/baby/create",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
        json=test_foetus
    )

    assert response.status_code == 200
    response_json = response.json()
    assert "baby" in response_json

    print(response_json)
    test_jwt["foetus"] = response_json["baby"]["baby_id"]


def test_create_baby2(client, test_jwt):
    response = client.post(
        "/baby/create",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
        json=test_baby
    )

    assert response.status_code == 200
    response_json = response.json()
    assert "baby" in response_json

    test_jwt["baby"] = response_json["baby"]["baby_id"]