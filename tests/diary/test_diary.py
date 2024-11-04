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
    "title": "산모수첩"
}

test_ParentingDiary = {
    "baby_id": "test_baby_id",
    "born": 1,
    "title": "육아일지"
}

test_cover = {
    "file": "test1.png"
}


""" Create diary """
# 산모수첩 생성
def test_create_diary1(client, test_jwt):
    test_MaternityDiary["baby_id"] = test_jwt["foetus"]
    response = client.post(
        "/diary/create",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
        json=test_MaternityDiary
    )
    
    assert response.status_code == 200
    response_json = response.json()
    assert "diary" in response_json

    assert response_json["diary"]["baby_id"] == test_jwt["foetus"]


# 육아일기 생성
def test_create_diary2(client, test_jwt):
    test_ParentingDiary["baby_id"] = test_jwt["baby"]
    response = client.post(
        "/diary/create",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
        json=test_ParentingDiary
    )

    assert response.status_code == 200
    response_json = response.json()
    assert "diary" in response_json

    assert response_json["diary"]["baby_id"] == test_jwt["baby"]
    test_jwt["parenting_diary"] = response_json["diary"]["diary_id"]


""" upload diary cover image """
def test_upload_diary_cover_image(client, test_jwt):
    file = [
        ("file", (test_cover["file"], open(os.path.join(TEST_ASSET_DIR, test_cover["file"]), "rb")))
    ]

    response = client.post(
        f"/diary/coverUpload/{test_jwt['parenting_diary']}",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
        files=file,
        data={"diary_id": test_jwt["parenting_diary"]}
    )

    assert response.status_code == 200
    response_json = response.json()
    assert "success" in response_json

    file_type = test_cover["file"].split(".")[-1]
    assert create_file_exist(os.path.join(
        DIARY_COVER_PATH, f"{test_jwt['parenting_diary']}.{file_type}"))
    

""" get all diary by baby_id """
def test_get_all_diary(client, test_jwt):
    baby_id = test_jwt["baby"]
    response = client.get(
        f"/diary/{baby_id}",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"
    })

    assert response.status_code == 200
    response_json = response.json()
    assert "diary" in response_json

    assert response_json["diary"][0]["baby_id"] == test_jwt["baby"]