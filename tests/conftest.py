import sys
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIRS = os.path.abspath(os.path.join(CURRENT_DIR, "../"))
sys.path.append(PROJECT_DIRS)

import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client

@pytest.fixture(scope="session")
def test_jwt():
    return {"access_token": None}
