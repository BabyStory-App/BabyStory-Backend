import os

PROJECT_DIR = os.getcwd()
ASSET_DIR = f'{PROJECT_DIR}/assets'

BABY_CRY_DATASET_DIR = f'{PROJECT_DIR}/dataset/baby_cry'
CRY_INSPECT_LOG_DIR = f'{PROJECT_DIR}/logs/cry_inspect'
PROFILE_IMAGE_DIR = f'{PROJECT_DIR}/dataset/profile'
BABY_PROFILE_DIR = f'{PROJECT_DIR}/dataset/baby/profile'
POST_PHOTO_DIR = f'{PROJECT_DIR}/dataset/post/photo'
POST_CONTENT_DIR = f'{PROJECT_DIR}/dataset/post/content'
TEST_ASSET_DIR = f'{PROJECT_DIR}/tests/assets'
POSTMAIN_BANNER_DIR = f'{PROJECT_DIR}/dataset/post/postmain/banner'


os.makedirs(BABY_CRY_DATASET_DIR, exist_ok=True)
os.makedirs(CRY_INSPECT_LOG_DIR, exist_ok=True)
os.makedirs(PROFILE_IMAGE_DIR, exist_ok=True)
os.makedirs(BABY_PROFILE_DIR, exist_ok=True)
os.makedirs(POST_PHOTO_DIR, exist_ok=True)
os.makedirs(POST_CONTENT_DIR, exist_ok=True)
os.makedirs(TEST_ASSET_DIR, exist_ok=True)
os.makedirs(POSTMAIN_BANNER_DIR, exist_ok=True)