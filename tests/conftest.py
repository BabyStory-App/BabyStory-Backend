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


def pytest_collection_modifyitems(session, config, items):
    # 원하는 테스트 폴더 순서 지정 (절대 경로로 변환)
    folder_order = [
        os.path.abspath(os.path.join(config.rootdir, 'tests/parent')),
        os.path.abspath(os.path.join(config.rootdir, 'tests/post'))
    ]

    def get_folder_index(item):
        # item.fspath.dirname을 절대 경로로 변환하고, folder_order에서 해당 경로의 인덱스 반환
        item_dir = os.path.abspath(item.fspath.dirname)
        return folder_order.index(item_dir) if item_dir in folder_order else len(folder_order)

    # items를 folder_order에 따라 정렬
    items[:] = sorted(items, key=get_folder_index)