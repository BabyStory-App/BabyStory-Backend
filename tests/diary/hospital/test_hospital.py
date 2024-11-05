from datetime import *
from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST
import pytest
from utils.os import *
from constants.path import *

test_jwt_tmp = None

test_hospital = {
    "diary_id": 1,
    "createTime": "2021-01-01",
    "parent_kg": 60.0,
    "bpressure": 120.0,
    "special": "쿼드 검사 (Quad Test) /split 정상 /seq 양수검사 (Amniocentesis) /split 정상",
}


""" Create Hospital """
def test_create_hospital(client, test_jwt):
    test_hospital["diary_id"] = test_jwt["maternity_diary"]
    print(test_hospital)
    response = client.post(
        "/hospital/create",
        json=test_hospital,
        headers={"Authorization": "Bearer " + test_jwt["access_token"]}
    )

    assert response.status_code == 200
    response_json = response.json()
    assert "hospital" in response_json
    print(response_json)

    assert response_json["hospital"]["diary_id"] == test_jwt["maternity_diary"]
    test_jwt["hospital_id"] = response_json["hospital"]["hospital_id"]


""" Get all Hospital by diary_id """
def test_get_all_hospital(client, test_jwt):
    diary = test_jwt["maternity_diary"]
    print(diary)
    response = client.get(
        f"/hospital/all/{diary}",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"}
    )
    print(response.text)
    assert response.status_code == 200
    response_json = response.json()
    assert "hospitals" in response_json
    print(response_json)

    assert response_json["hospitals"][0]["hospital_id"] == test_jwt["hospital_id"]


""" Get Hospital by hospital_id """
def test_get_hospital(client, test_jwt):
    hospital = test_jwt["hospital_id"]
    response = client.get(
        f"/hospital/get/{hospital}",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
    )
    print(response.text)

    assert response.status_code == 200
    response_json = response.json()
    assert "hospital" in response_json

    assert response_json["hospital"]["baby_id"] == test_jwt["foetus"]


""" Update Hospital """
def test_update_hospital(client, test_jwt):
    test_hospital["hospital_id"] = test_jwt["hospital_id"]
    test_hospital["parent_kg"] = 70.0
    response = client.put(
        "/hospital/update",
        json=test_hospital,
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"}
    )

    assert response.status_code == 200
    response_json = response.json()
    assert "hospital" in response_json

    assert response_json["hospital"]["diary_id"] == test_jwt["maternity_diary"]


""" Delete Hospital """
def test_delete_hospital(client, test_jwt):
    hospital = test_jwt["hospital_id"]
    response = client.delete(
        f"/hospital/delete/{hospital}",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"}
    )

    assert response.status_code == 200
    response_json = response.json()
    assert "success" in response_json

    assert response_json["success"] == 200