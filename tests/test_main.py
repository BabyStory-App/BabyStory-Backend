from typing import List, Optional
from auth.auth_handler import decodeJWT,signJWT
from uuid import uuid4

def test_main(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {'hello': 'world'}