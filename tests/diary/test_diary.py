from datetime import *
from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST
import pytest
from utils.os import *
from constants.path import *

test_jwt_tmp = None

test_MaternityDiary = {
    "baby_id": "test_baby_id",
    "born": 0,
    "title": "Maternity Diary"
}

test_ParentingDiary = {
    "baby_id": "test_baby_id",
    "born": 1,
    "title": "Parenting Diary"
}


""" Create diary """
# 산모수첩 생성
def test_create_diary1(client, test_jwt):
    response = client.post(
        "/diary/create",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
        json=test_MaternityDiary
    )
    test_MaternityDiary["baby_id"] = test_jwt["foetus"]

    assert response.status_code == 200
    response_json = response.json()
    assert "diary" in response_json

    assert response_json["diary"]["parent_id"] == test_jwt["access_token"]


# 육아일기 생성
def test_create_diary2(client, test_jwt):
    response = client.post(
        "/diary/create",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
        json=test_ParentingDiary
    )
    test_ParentingDiary["baby_id"] = test_jwt["baby"]

    assert response.status_code == 200
    response_json = response.json()
    assert "diary" in response_json

    assert response_json["diary"]["parent_id"] == test_jwt["access_token"]