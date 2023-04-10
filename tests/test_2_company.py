from httpx import AsyncClient


# Number of tests 20
# Created 6 users, 1 (id=6) deleted and recreated (id=7).
# Created 5 companies, 1 (id=5) deleted.


# ============================================== COMPANY CREATE ==============================================


async def test_bad_create_company_unauth(ac: AsyncClient):
    payload = {
        "company_name": "company1",
        "company_description": "string"
    }
    response = await ac.post("/company/", json=payload)
    assert response.status_code == 403
    assert response.json().get("detail") == "Not authenticated" 


async def test_bad_create_company__no_name(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
        "company_description": "company_description"
    }
    response = await ac.post("/company/", json=payload, headers=headers)
    assert response.status_code == 400
    assert response.json().get("detail") == "Name required"


async def test_create_companies(users_tokens, ac: AsyncClient):
    # Company 1
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
        "company_name": "test_company_1",
        "company_description": "company_description_1"
    }
    response = await ac.post("/company/", json=payload, headers=headers)
    assert response.status_code == 201
    assert response.json().get("result").get("company_id") == 1
    assert response.json().get("result").get("company_name") == "test_company_1"
    assert response.json().get("result").get("company_description") == "company_description_1"
    assert response.json().get("detail") == "success"
    # Company 2
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "company_name": "test_company_2",
    }
    await ac.post("/company/", json=payload, headers=headers)
    # Company 3
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    payload = {
        "company_name": "test_company_3",
    }
    response = await ac.post("/company/", json=payload, headers=headers)
    # Company 4
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    payload = {
        "company_name": "test_company_4",
        "company_description": "company_description_4"
    }
    response = await ac.post("/company/", json=payload, headers=headers)
    # Company 5
    headers = {
        "Authorization": f"Bearer {users_tokens['test5@test.com']}",
    }
    payload = {
        "company_name": "test_company_5",
        "company_description": "company_description_5"
    }
    response = await ac.post("/company/", json=payload, headers=headers)


# ============================================== GET COMPANIES ===============================================


async def test_bad_get_all_unauth(ac: AsyncClient):
    response = await ac.get("/companies/")
    assert response.status_code == 403
    assert response.json().get("detail") == "Not authenticated" 


async def test_get_all_companies(users_tokens, ac: AsyncClient):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/companies/", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get("result").get('companies')) == 5
    assert response.json().get("detail") == "success" 


# ============================================ GET COMPANY BY ID =============================================


async def test_bad_get_company_by_id_unauth(ac: AsyncClient):
    response = await ac.get("/company/100/")
    assert response.status_code == 403
    assert response.json().get("detail") == "Not authenticated" 


async def test_bad_get_company_by_id_not_found(users_tokens, ac: AsyncClient):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/company/100/", headers=headers)
    assert response.status_code == 404
    assert response.json().get("detail") == "This company not found"


async def test_get_company_by_id(users_tokens, ac: AsyncClient):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get("/company/1/", headers=headers)
    assert response.status_code == 200
    assert response.json().get("result").get("company_id") == 1
    assert response.json().get("result").get("company_name") == "test_company_1"
    assert response.json().get("result").get("company_description") == "company_description_1"
    assert response.json().get("result").get("company_owner_id") == 1
    assert response.json().get("detail") == "success"


# ============================================= UPDATE COMPANY ==============================================


async def test_bad_update_company__unauth(ac: AsyncClient):
    payload = {
        "company_name": "company_name_1_NEW",
        "company_description": "company_description_1_NEW"
    }
    response = await ac.put("/company/1/", json=payload)
    assert response.status_code == 403
    assert response.json().get("detail") == "Not authenticated"
    

async def test_bad_update_company__not_found(users_tokens, ac: AsyncClient):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
        "company_name": "company_name_1_NEW",
        "company_description": "company_description_1_NEW"
    }
    response = await ac.put("/company/100/", json=payload, headers=headers)
    assert response.status_code == 404
    assert response.json().get("detail") == "This company not found"


async def test_bad_update_company__not_your_company(users_tokens, ac: AsyncClient):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
        "company_name": "company_name_2_NEW",
        "company_description": "company_description_2_NEW"
    }
    response = await ac.put("/company/2/", json=payload, headers=headers)
    assert response.status_code == 403
    assert response.json().get("detail") == "It's not your company"


async def test_update_company(users_tokens, ac: AsyncClient):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
        "company_name": "company_name_1_NEW",
        "company_description": "company_description_1_NEW"
    }
    response = await ac.put("/company/1/", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json().get("detail") == "success"


async def test_get_company_by_id_one_updated(users_tokens, ac: AsyncClient):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/company/1/", headers=headers)
    assert response.status_code == 200
    assert response.json().get("result").get("company_id") == 1
    assert response.json().get("result").get("company_name") == "company_name_1_NEW"
    assert response.json().get("result").get("company_description") == "company_description_1_NEW"
    assert response.json().get("result").get("company_owner_id") == 1


async def test_update_company_empty(users_tokens, ac: AsyncClient):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {}
    response = await ac.put("/company/1/", json=payload, headers=headers)
    assert response.status_code == 200


async def test_get_company_by_id_two_updated(users_tokens, ac: AsyncClient):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/company/1/", headers=headers)
    assert response.status_code == 200
    assert response.json().get("result").get("company_id") == 1
    assert response.json().get("result").get("company_name") == "company_name_1_NEW"
    assert response.json().get("result").get("company_description") == "company_description_1_NEW"
    assert response.json().get("result").get("company_owner_id") == 1


# ============================================= DELETE COMPANY ==============================================


async def test_bad_delete_company__unauth(ac: AsyncClient):
    response = await ac.delete("/company/100/")
    assert response.status_code == 403
    assert response.json().get("detail") == "Not authenticated"


async def test_bad_delete_company__not_found(users_tokens, ac: AsyncClient):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.delete("/company/100/", headers=headers)
    assert response.status_code == 404
    assert response.json().get("detail") == "This company not found"


async def test_bad_delete_company_one__not_your_company(users_tokens, ac: AsyncClient):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.delete("/company/5/", headers=headers)
    assert response.status_code == 403
    assert response.json().get("detail") == "It's not your company"


async def test_delete_company_five(users_tokens, ac: AsyncClient):
    headers = {
        "Authorization": f"Bearer {users_tokens['test5@test.com']}",
    }
    response = await ac.delete("/company/5/", headers=headers)
    assert response.status_code == 200
    assert response.json().get("detail") == "success"


async def test_get_all_companies_after_delete(users_tokens, ac: AsyncClient):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/companies/", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get("result").get('companies')) == 4