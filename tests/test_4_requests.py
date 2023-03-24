from httpx import AsyncClient

# Number of tests 37
# User 1 in company 2, user 3 in company 2.


# ============================================== REQUEST CREATE ==============================================


async def test_bad_send_request_unauth(ac: AsyncClient):
    payload = {
        "to_company_id": 1,
        "request_message": "string"
    }
    response = await ac.post("/request/", json=payload)
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_bad_send_request_not_found_company(ac: AsyncClient, users_tokens):
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


async def test_bad_send_request_already_in_company(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
        "to_company_id": 1,
        "request_message": "string"
    }
    response = await ac.post("/request/", json=payload, headers=headers)
    assert response.status_code == 400
    assert response.json().get('detail') == "User is already in this company"


async def test_send_requests_success(ac: AsyncClient, users_tokens):
    # Request 1
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    payload = {
        "to_company_id": 1,
        "request_message": "1 request"
    }
    response = await ac.post("/request/", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"
    # Request 2
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    payload = {
        "to_company_id": 2,
        "request_message": "2 request"
    }
    await ac.post("/request/", json=payload, headers=headers)
    # Request 3
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    payload = {
        "to_company_id": 4,
        "request_message": "3 request"
    }
    await ac.post("/request/", json=payload, headers=headers)


async def test_bad_send_request_already_sent(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    payload = {
        "to_company_id": 1,
        "request_message": "string"
    }
    response = await ac.post("/request/", json=payload, headers=headers)
    assert response.status_code == 400
    assert response.json().get('detail') == "Request already exists"


async def test_bad_send_request_invited_already(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "to_company_id": 1,
        "request_message": "string"
    }
    response = await ac.post("/request/", json=payload, headers=headers)
    assert response.status_code == 400
    assert response.json().get('detail') == "Company already made the invite to this user"


async def test_bad_send_invite_requested_already(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "to_user_id": 3,
        "from_company_id": 2,
        "invite_message": "string"
    }
    response = await ac.post("/invite/", json=payload, headers=headers)
    assert response.status_code == 400
    assert response.json().get('detail') == "User already made the request to this company"


# =============================================== MY REQUESTS ================================================


async def test_my_requests_unauth(ac: AsyncClient):
    response = await ac.get("/request/my/")
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_my_requests(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get("/request/my/", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('result').get('requests')) == 3
    assert response.json().get('detail') == "success"

# ============================================= COMPANY REQUESTS =============================================


async def test_bad_company_requests_unauth(ac: AsyncClient):
    response = await ac.get("/request/company/100/")
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_bad_company_requests_company_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("/request/company/100/", headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "This company not found"


async def test_requests_company_one_not_owner(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("/request/company/1/", headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "It's not your company"


async def test_requests_company_one(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/request/company/1/", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('result').get('requests')) == 1
    assert response.json().get('detail') == "success"


# ============================================= GET REQUEST BY ID ==============================================


async def test_bad_request_get_by_id_unauth(ac: AsyncClient):
    response = await ac.get("/request/1/")
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_bad_request_get_by_id_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get("/request/100/", headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "This request not found"


async def test_bad_request_get_by_id_not_your(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("/request/1/", headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "It's not your request"


async def test_request_get_by_id_from_user(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get("/request/1/", headers=headers)
    assert response.status_code == 200
    assert response.json().get('result').get('request_id') == 1
    assert response.json().get('result').get('from_user_id') == 3
    assert response.json().get('result').get('to_company_id') == 1
    assert response.json().get('result').get('request_message') == "1 request"
    assert response.json().get('detail') == "success"


async def test_request_get_by_id_from_company(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/request/1/", headers=headers)
    assert response.status_code == 200
    assert response.json().get('result').get('request_id') == 1
    assert response.json().get('result').get('from_user_id') == 3
    assert response.json().get('result').get('to_company_id') == 1
    assert response.json().get('result').get('request_message') == "1 request"
    assert response.json().get('detail') == "success"


# ============================================= CANCEL REQUESTS =============================================


async def test_bad_cancel_request_not_auth(ac: AsyncClient):
    response = await ac.delete("/request/100/")
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_bad_cancel_request_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.delete("/request/100/", headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "This request not found"


async def test_bad_cancel_request_not_your(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.delete("/request/1/", headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "It's not your request"


async def test_cancel_request_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.delete("/request/3/", headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"


async def test_requests_company_four_after_cancel(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    response = await ac.get("/request/company/4/", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('result').get('requests')) == 0


async def test_my_requests_after_cancel(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get("/request/my/", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('result').get('requests')) == 2


# =============================================== ACCEPT REQUEST ===============================================


async def test_accept_request_not_auth(ac: AsyncClient):
    response = await ac.get("/request/1/accept/")
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_accept_request_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/request/100/accept/", headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "This request not found"


async def test_accept_request_not_your(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("/request/1/accept/", headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "It's not your request"
 

async def test_accept_request_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("/request/2/accept/", headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"


async def test_company_members_user(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("/company/2/members/", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get("result").get("users")) == 3
    assert response.json().get('result').get("users")[2].get('user_id') == 3
    assert response.json().get('result').get("users")[2].get('company_id') == 2
    assert response.json().get('result').get("users")[2].get('role') == "user"
    assert response.json().get('detail') == "success"


async def test_my_requests_after_accept(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get("/request/my/", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('result').get('requests')) == 1


async def test_requests_company_two_after_accept(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("/request/company/2/", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('result').get('requests')) == 0


# =============================================== DECLINE REQUEST ===============================================


async def test_decline_request_not_auth(ac: AsyncClient):
    response = await ac.get("/request/1/decline/")
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_decline_request_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/request/100/decline/", headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "This request not found"


async def test_decline_request_not_your(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("/request/1/decline/", headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "It's not your request"
 

async def test_decline_request_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/request/1/decline/", headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"


async def test_my_requests_after_decline(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get("/request/my/", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('result').get('requests')) == 0


async def test_requests_company_one_after_decline(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",    
    }
    response = await ac.get("/request/company/2/", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('result').get('requests')) == 0