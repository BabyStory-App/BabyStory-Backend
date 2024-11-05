from datetime import *
from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST
import pytest
from utils.os import *
from constants.path import *

test_jwt_tmp = None

test_dday = {
    'diary_id': 1,
    'createTime': '2021-08-01',
    'title': 'test',
    'content': 'test'
}

test_UploadPhoto = {
    "fileList": ["test1.png", "test2.png", "test3.png"]
}


""" Create DDay """
def test_create_dday(client, test_jwt):
    test_dday['diary_id'] = test_jwt['parenting_diary']
    response = client.post(
    '/dday/create',
    headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
    json=test_dday
    )

    assert response.status_code == 200
    response_json = response.json()
    assert 'dday' in response_json

    assert response_json['dday']['diary_id'] == test_jwt['parenting_diary']
    test_jwt['dday_id'] = response_json['dday']['dday_id']


""" Upload DDay Photo """
def test_upload_dday_photo(client, test_jwt):
    files = [("fileList", (file, open(os.path.join(TEST_ASSET_DIR, file), "rb")))
             for file in test_UploadPhoto["fileList"]]
    response = client.post(
        f'/dday/photoUpload/{test_jwt["dday_id"]}',
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
        files=files
    )

    assert response.status_code == 200
    response_json = response.json()
    assert 'success' in response_json

    for i in range(len(test_UploadPhoto["fileList"])):
        file_type = test_UploadPhoto["fileList"][i].split('.')[-1]
        assert create_file_exist(os.path.join(
            DIARY_DAY_PHOTO_DIR, str(test_jwt['dday_id']), f"{test_jwt['dday_id']}-{i+1}.{file_type}"))