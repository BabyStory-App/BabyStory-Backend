from datetime import *
from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST
import pytest
from utils.os import *
from constants.path import *

test_jwt_tmp = None

test_milk = {
    "diary_id": "test_diary_id",
    "baby_id": "test_baby_id",
    "milk": 0,
    "amount": 100,
    "mtime": "2024-11-04, 12:30"
}

update_milk = {
    "milk_id": 1,
    "milk": 1,
    "amount": 120,
    "mtime": "2024-11-04, 12:30"
}

""" Create milk """
def test_create_milk(client, test_jwt):
    test_milk["baby_id"] = test_jwt["baby"]
    test_milk["diary_id"] = test_jwt["parenting_diary"]

    response = client.post(
        "/milk/create",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
        json=test_milk
    )

    assert response.status_code == 200
    response_json = response.json()
    assert "milk" in response_json

    assert response_json["milk"]["baby_id"] == test_jwt["baby"]
    test_jwt["milk"] = response_json["milk"]["milk_id"]


""" Get all milk """
def test_get_all_milk(client, test_jwt):
    response = client.get(
        f"/milk/{test_jwt['parenting_diary']}",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"}
    )

    assert response.status_code == 200
    response_json = response.json()
    assert "milks" in response_json

    assert response_json["milks"][0]["baby_id"] == test_jwt["baby"]


""" Get milk by mtime """
def test_get_milk_by_mtime(client, test_jwt):
    mtime = "2024-11-04"
    response = client.get(
        f"/milk/{test_jwt['parenting_diary']}/{mtime}",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"}
    )

    assert response.status_code == 200
    response_json = response.json()
    assert "milks" in response_json

    assert response_json["milks"][0]["baby_id"] == test_jwt["baby"]


""" Get milk by range """
def test_get_milk_range(client, test_jwt):
    start = "2024-11-04"
    end = "2024-11-05"
    response = client.get(
        f"/milk/{test_jwt['parenting_diary']}/{start}/{end}",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"}
    )

    assert response.status_code == 200
    response_json = response.json()
    assert "milks" in response_json

    assert response_json["milks"][0]["baby_id"] == test_jwt["baby"]


""" Update milk """
def test_update_milk(client, test_jwt):
    update_milk["milk_id"] = test_jwt["milk"]
    response = client.put(
        "/milk/update",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
        json=update_milk
    )

    assert response.status_code == 200
    response_json = response.json()
    assert "milk" in response_json

    assert response_json["milk"]["baby_id"] == test_jwt["baby"]


""" Delete milk """
def test_delete_milk(client, test_jwt):
    milk_id = test_jwt["milk"]
    response = client.delete(
        f"/milk/delete/{milk_id}",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"}
    )

    assert response.status_code == 200
    response_json = response.json()
    assert "success" in response_json

    assert response_json["success"] == 200