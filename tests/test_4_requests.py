from httpx import AsyncClient

# send request

async def test_request_send_not_auth(ac: AsyncClient):
    payload = {
        "to_company_id": 0,
        "invite_message": "string"
    }
    response = await ac.post("/request/", json=payload)
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_request_send_not_found_company(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
        "to_company_id": 100,
        "request_message": "string"
    }
    response = await ac.post("/request/", json=payload, headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == 'This company not found'


async def test_request_send_from_owner(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
        "to_company_id": 1,
        "request_message": "string"
    }
    response = await ac.post("/request/", json=payload, headers=headers)
    assert response.status_code == 400
    assert response.json().get('detail') == "User is already a member of the company"


async def test_request_send_one_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
        "to_company_id": 2,
        "request_message": "string"
    }
    response = await ac.post("/request/", json=payload, headers=headers)
    assert response.status_code == 400
    assert response.json().get('detail') == "User is already a member of the company"


async def test_request_send_two_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "to_company_id": 1,
        "request_message": "string"
    }
    response = await ac.post("/request/", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"


async def test_request_send_three_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    payload = {
        "to_company_id": 1,
        "request_message": "string"
    }
    response = await ac.post("/request/", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"


async def test_request_send_exist(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "to_company_id": 1,
        "request_message": "string"
    }
    response = await ac.post("/request/", json=payload, headers=headers)
    assert response.status_code == 400
    assert response.json().get('detail') == "Request already sent"


async def test_request_send_four_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    payload = {
        "to_company_id": 2,
        "request_message": "string"
    }
    response = await ac.post("/request/", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"


# my requests

async def test_request_my_all_not_auth(ac: AsyncClient):
    response = await ac.get("/request/my")
    assert response.status_code == 403


async def test_request_my_all_user_one(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/request/my", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('result').get('requests')) == 0


async def test_request_my_all_user_two(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("/request/my", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('result')) == 1


async def test_request_my_all_user_three(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get("/request/my", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('result')) == 1


# company requests

async def test_request_company_all_not_auth(ac: AsyncClient):
    response = await ac.get("/request/company/1")
    assert response.status_code == 403


async def test_requests_company_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("/request/company/100", headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "This company not found"


async def test_requests_company_one_not_owner(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("/request/company/1", headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "It's not your company"


async def test_requests_company_one_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/request/company/1", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('result').get('requests')) == 2


# request cancel


async def test_request_cancels_not_auth(ac: AsyncClient):
    response = await ac.delete("/request/1")
    assert response.status_code == 403


async def test_request_cancels_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.delete("/request/12", headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "Request not found"


async def test_request_cancels_not_your(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.delete("/request/1", headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "It's not your request"


async def test_request_cancel_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.delete("/request/1", headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"


# accept request

async def test_request_accepts_not_auth(ac: AsyncClient):
    response = await ac.get("/request/2/accept")
    assert response.status_code == 403


async def test_request_accepts_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/request/12/accept", headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "Request not found"


async def test_request_accepts_not_owner(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("/request/2/accept", headers=headers)
    assert response.status_code == 403


# decli request


async def test_request_decline_not_auth(ac: AsyncClient):
    response = await ac.get('/request/3/decline')
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_request_decline_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/request/100/decline', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "Request not found"


async def test_request_decline_not_owner(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/request/2/decline', headers=headers)
    assert response.status_code == 403


async def test_request_decline_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/request/2/decline', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"



#===============================


async def test_members_only_owner(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("/company/2/members", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('result').get('users')) == 3


async def test_request_accepts(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("/request/3/accept", headers=headers)
    assert response.status_code == 200


async def test_members_after_accept(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("/company/2/members", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('result').get('users')) == 4


# ===========

async def test_member_kick(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.delete("/company/2/member/3", headers=headers)
    assert response.status_code == 200


async def test_members_after_kick(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("/company/2/members", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('result').get('users')) == 3


async def test_leave_member(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    response = await ac.delete("/company/2/leave", headers=headers)
    assert response.status_code == 200


async def test_members_after_leave(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("/company/2/members", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('result').get('users')) == 2

