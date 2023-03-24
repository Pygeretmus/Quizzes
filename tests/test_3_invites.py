from httpx import AsyncClient

# Number of tests 49
# User 1 in company 2, user 2 has invite to company 1.


# ============================================== INVITE CREATE ==============================================


async def test_bad_send_invite_unauth(ac: AsyncClient):
    payload = {
        "to_user_id": 1,
        "from_company_id": 1,
        "invite_message": "string"
    }
    response = await ac.post("/invite/", json=payload)
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_bad_send_invite_not_found_user(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
        "to_user_id": 100,
        "from_company_id": 1,
        "invite_message": "string"
    }
    response = await ac.post("/invite/", json=payload, headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == 'This user not found'


async def test_bad_send_invite_not_found_company(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
        "to_user_id": 1,
        "from_company_id": 100,
        "invite_message": "string"
    }
    response = await ac.post("/invite/", json=payload, headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == 'This company not found'


async def test_bad_send_invite_not_your_company(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "to_user_id": 1,
        "from_company_id": 1,
        "invite_message": "string"
    }
    response = await ac.post("/invite/", json=payload, headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "It's not your company"


async def test_bad_send_invite_already_in_company(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
        "to_user_id": 1,
        "from_company_id": 1,
        "invite_message": "string"
    }
    response = await ac.post("/invite/", json=payload, headers=headers)
    assert response.status_code == 400
    assert response.json().get('detail') == "User already in this company"


async def test_send_invites_success(ac: AsyncClient, users_tokens):
    # Invite 1
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "to_user_id": 1,
        "from_company_id": 2,
        "invite_message": "1 invite"
    }
    response = await ac.post("/invite/", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"
    # Invite 2
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    payload = {
        "to_user_id": 1,
        "from_company_id": 3,
        "invite_message": "2 invite"
    }
    await ac.post("/invite/", json=payload, headers=headers)
    # Invite 3
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    payload = {
        "to_user_id": 1,
        "from_company_id": 4,
        "invite_message": "3 invite"
    }
    await ac.post("/invite/", json=payload, headers=headers)
    # Invite 4
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
        "to_user_id": 2,
        "from_company_id": 1,
        "invite_message": "4 invite"
    }
    await ac.post("/invite/", json=payload, headers=headers)
    # Invite 5
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    payload = {
        "to_user_id": 3,
        "from_company_id": 4,
        "invite_message": "5 invite"
    }
    await ac.post("/invite/", json=payload, headers=headers)


async def test_bad_send_invite_already_sent(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "to_user_id": 1,
        "from_company_id": 2,
        "invite_message": "string"
    }
    response = await ac.post("/invite/", json=payload, headers=headers)
    assert response.status_code == 400
    assert response.json().get('detail') == "Invite already exists"


# =============================================== MY INVITES ================================================


async def test_my_invites_unauth(ac: AsyncClient):
    response = await ac.get("/invite/my/")
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_my_invites(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/invite/my/", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('result').get('invites')) == 3
    assert response.json().get('detail') == "success"


# ============================================= COMPANY INVITES =============================================


async def test_bad_company_invites_unauth(ac: AsyncClient):
    response = await ac.get("/invite/company/1/")
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_bad_company_invites_company_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("/invite/company/100/", headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "This company not found"


async def test_invites_company_one_not_owner(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("/invite/company/1/", headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "It's not your company"


async def test_invites_company_four(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    response = await ac.get("/invite/company/4/", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('result').get('invites')) == 2
    assert response.json().get('detail') == "success"


# ============================================ GET INVITE BY ID=============================================


async def test_bad_invite_get_by_id_unauth(ac: AsyncClient):
    response = await ac.get("/invite/1/")
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_bad_invite_get_by_id_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get("/invite/100/", headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "This invite not found"


async def test_bad_invite_get_by_id_not_your(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get("/invite/1/", headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "It's not your invite"


async def test_invite_get_by_id_from_user(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/invite/1/", headers=headers)
    assert response.status_code == 200
    assert response.json().get('result').get('invite_id') == 1
    assert response.json().get('result').get('to_user_id') == 1
    assert response.json().get('result').get('from_company_id') == 2
    assert response.json().get('result').get('invite_message') == "1 invite"
    assert response.json().get('detail') == "success"


async def test_invite_get_by_id_from_company(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("/invite/1/", headers=headers)
    assert response.status_code == 200
    assert response.json().get('result').get('invite_id') == 1
    assert response.json().get('result').get('to_user_id') == 1
    assert response.json().get('result').get('from_company_id') == 2
    assert response.json().get('result').get('invite_message') == "1 invite"
    assert response.json().get('detail') == "success"


# ============================================= CANCEL INVITES =============================================


async def test_bad_cancel_invite_not_auth(ac: AsyncClient):
    response = await ac.delete("/invite/100/")
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_bad_cancel_invite_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.delete("/invite/100/", headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "This invite not found"


async def test_bad_cancel_invite_not_your(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.delete("/invite/1/", headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "It's not your company"


async def test_cancel_invite_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    response = await ac.delete("/invite/3/", headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"


async def test_invites_company_four_after_cancel(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    response = await ac.get("/invite/company/4/", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('result').get('invites')) == 1


async def test_my_invites_after_cancel(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/invite/my/", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('result').get('invites')) == 2


# =========================================== COMPANY MEMBERS ===========================================


async def test_bad_company_members_not_auth(ac: AsyncClient):
    response = await ac.get("/company/100/members/")
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_bad_company_members_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/company/100/members/", headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "This company not found"


async def test_bad_company_members_not_your(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/company/2/members/", headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "You are not member of this company"


async def test_company_members_owner(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("/company/2/members/", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get("result").get("users")) == 1
    assert response.json().get('result').get("users")[0].get('user_id') == 2
    assert response.json().get('result').get("users")[0].get('company_id') == 2
    assert response.json().get('result').get("users")[0].get('role') == "owner"
    assert response.json().get('detail') == "success"


# =========================================== ACCEPT INVITE ===========================================


async def test_accept_invite_not_auth(ac: AsyncClient):
    response = await ac.get("/invite/1/accept/")
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_accept_invite_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/invite/100/accept/", headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "This invite not found"


async def test_accept_invite_not_your(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("/invite/1/accept/", headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "It's not your invite"
 

async def test_accept_invite_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/invite/1/accept/", headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    await ac.get("/invite/5/accept/", headers=headers)
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    await ac.get("/invite/6/accept/", headers=headers)


async def test_company_members_user(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("/company/2/members/", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get("result").get("users")) == 2
    assert response.json().get('result').get("users")[1].get('user_id') == 1
    assert response.json().get('result').get("users")[1].get('company_id') == 2
    assert response.json().get('result').get("users")[1].get('role') == "user"
    assert response.json().get('detail') == "success"


async def test_my_invites_after_accept(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/invite/my/", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('result').get('invites')) == 1


async def test_invites_company_two_after_accept(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("/invite/company/2/", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('result').get('invites')) == 0


# =========================================== DECLINE INVITE ===========================================


async def test_decline_invite_not_auth(ac: AsyncClient):
    response = await ac.get("/invite/1/decline/")
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_decline_invite_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/invite/100/decline/", headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "This invite not found"


async def test_decline_invite_not_your(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("/invite/2/decline/", headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "It's not your invite"
 

async def test_decline_invite_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/invite/2/decline/", headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"


async def test_my_invites_after_decline(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/invite/my/", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('result').get('invites')) == 0


async def test_invites_company_three_after_decline(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",    
    }
    response = await ac.get("/invite/company/2/", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('result').get('invites')) == 0


# =========================================== KICK MEMBER ===========================================


async def test_bad_kick_member_not_auth(ac: AsyncClient):
    response = await ac.delete("/company/1/member/1/")
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_bad_kick_member_company_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",    
    }
    response = await ac.delete("/company/100/member/1/", headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "This company not found"


async def test_bad_kick_member_not_owner(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",    
    }
    response = await ac.delete("/company/2/member/3/", headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "It's not your company"


async def test_kick_member(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",    
    }
    response = await ac.delete("/company/4/member/1/", headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"


async def test_company_four_members_after_kick(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    response = await ac.get("/company/4/members/", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get("result").get("users")) == 2
    assert response.json().get('result').get("users")[1].get('user_id') == 3
    assert response.json().get('result').get("users")[1].get('company_id') == 4
    assert response.json().get('result').get("users")[1].get('role') == "user"


# =========================================== LEAVE COMPANY ===========================================


async def test_bad_leave_company_not_auth(ac: AsyncClient):
    response = await ac.delete("/company/{company_id}/leave/")
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_leave_company(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",    
    }
    response = await ac.delete("/company/4/leave/", headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"


async def test_company_four_members_after_leave(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    response = await ac.get("/company/4/members/", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get("result").get("users")) == 1
    assert response.json().get('result').get("users")[0].get('user_id') == 4
    assert response.json().get('result').get("users")[0].get('company_id') == 4
    assert response.json().get('result').get("users")[0].get('role') == "owner"