from httpx import AsyncClient

# Number of tests 16
# User 1 in company 2, user 3 in company 2, user 1 is admin in company 2.


# ============================================== ADMIN CREATE ===============================================


async def test_bad_create_admin_unauth(ac: AsyncClient):
    payload = {
        "user_id": 1
    }
    response = await ac.post('/company/2/admin/', json=payload)
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_bad_create_admin_not_owner(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    payload = {
        "user_id": 100,
    }
    response = await ac.post('/company/2/admin/', headers=headers, json=payload)
    assert response.status_code == 403
    assert response.json().get('detail') == "It's not your company"


async def test_bad_create_admin_user_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "user_id": 100,
    }
    response = await ac.post('/company/2/admin/', headers=headers, json=payload)
    assert response.status_code == 404
    assert response.json().get('detail') == "This user not a member of this company"


async def test_bad_create_admin_company_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "user_id": 2,
    }
    response = await ac.post('/company/100/admin/', headers=headers, json=payload)
    assert response.status_code == 404
    assert response.json().get('detail') == "This company not found"


async def test_create_admins(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "user_id": 1,
    }
    response = await ac.post('/company/2/admin/', headers=headers, json=payload)
    assert response.status_code == 200
    assert response.json().get('detail') == 'success'
    payload = {
        "user_id": 3,
    }
    response = await ac.post('/company/2/admin/', headers=headers, json=payload)


# =============================================== GET ADMINS ===============================================


async def test_bad_admin_list_not_auth(ac: AsyncClient):
    response = await ac.get('/company/2/admins/')
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_bad_admin_list_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/company/100/admins/', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "This company not found"


async def test_bad_admin_list_not_member(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    response = await ac.get('/company/3/admins/', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "You are not member of this company"


async def test_admin_list_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/company/2/admins/', headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('result').get('users')) == 2
    assert response.json().get('result').get('users')[0].get('role') == "admin"
    assert response.json().get('result').get('users')[0].get('user_id') == 1
    assert response.json().get('result').get('users')[0].get('company_id') == 2
    assert response.json().get('detail') == "success"


# ============================================= REMOVE ADMIN ==============================================


async def test_admin_remove_not_auth(ac: AsyncClient):
    response = await ac.delete('/company/2/admin/1/')
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_admin_remove_user_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.delete('/company/2/admin/100/', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "This user not a member of this company"
    

async def test_admin_remove_company_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.delete('/company/100/admin/1/', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == 'This company not found'


async def test_admin_remove_not_owner(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.delete('/company/2/admin/1/', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "It's not your company"


async def test_bad_remove_admin_user_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.delete('/company/2/admin/100/', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "This user not a member of this company"


async def test_admin_remove_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }

    response = await ac.delete('/company/2/admin/3/', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"


async def test_admin_list_success_after_remove(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/company/2/admins/', headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('result').get('users')) == 1



