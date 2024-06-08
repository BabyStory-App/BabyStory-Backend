from typing import List, Optional
from auth.auth_handler import decodeJWT,signJWT
from uuid import uuid4

def test_create_postmain(client,test_jwt):
    response = client.post(
        "/post/mian/create",
        headers={"Authorization": f"Bearer {test_jwt}"}
    )
    assert response.status_code == 200
    assert response.json() == {
        'banner' : createpostmain,
        'friend' : createpostmainfriend,
        'friend_read' : createpostmainfriendread,
        'neighbor' : getneighbor,
        'neighbor_post' : createpostmainneighbor,
        'highview' : createpostmainhighview
        #'hashtag' : createpostmainhashtag
    }