from httpx    import AsyncClient


# Number of tests 58
# Created 6 users, 1 (id=6) deleted and recreated (id=7).
# Created 5 companies, 1 (id=5) deleted.
# User 1 in company 2, user 2 has invite to company 1.
# User 3 in company 2, company 3 has request from user 2.
# User 1 is admin in company 2.


# ================================================ MY DATA =================================================


async def test_bad_my_data_unauth(ac: AsyncClient):
    response = await ac.get('/data/my/')
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_bad_my_data_csv_unauth(ac: AsyncClient):
    response = await ac.get('/data/my/csv/')
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_my_data_csv(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/data/my/csv/', headers=headers)
    assert response.status_code == 200


async def test_my_data(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/data/my/', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"
    assert len(response.json().get('result').get("datas")) == 12
    assert response.json().get('result').get("datas")[0].get("user_id") == 3
    

# ============================================= MY DATA COMPANY ================================================


async def test_bad_my_data_company_unauth(ac: AsyncClient):
    response = await ac.get('/data/my/company/3/')
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_bad_my_data_company_csv_unauth(ac: AsyncClient):
    response = await ac.get('/data/my/company/3/csv/')
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_my_data_company_csv(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/data/my/company/3/csv/', headers=headers)
    assert response.status_code == 200


async def test_my_data_company(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/data/my/company/3/', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"
    assert len(response.json().get('result').get("datas")) == 2
    assert response.json().get('result').get("datas")[0].get("user_id") == 3
    assert response.json().get('result').get("datas")[0].get("company_id") == 3


# ============================================= MY DATA QUIZ ================================================


async def test_bad_my_data_quiz_unauth(ac: AsyncClient):
    response = await ac.get('/data/my/quiz/3/')
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_bad_my_data_quiz_csv_unauth(ac: AsyncClient):
    response = await ac.get('/data/my/quiz/3/csv/')
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_bad_my_data_quiz_csv_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/data/my/quiz/100/csv/', headers=headers)
    assert response.status_code == 404
    assert response.json().get("detail") == "This quiz not found"


async def test_bad_my_data_quiz_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/data/my/quiz/100/', headers=headers)
    assert response.status_code == 404
    assert response.json().get("detail") == "This quiz not found"


async def test_my_data_quiz_csv(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/data/my/quiz/3/csv/', headers=headers)
    assert response.status_code == 200


async def test_my_data_quiz(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/data/my/quiz/3/', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"
    assert len(response.json().get('result').get("datas")) == 8
    assert response.json().get('result').get("datas")[0].get("user_id") == 3
    assert response.json().get('result').get("datas")[0].get("company_id") == 2
    assert response.json().get('result').get("datas")[0].get("quiz_id") == 3


# ============================================== COMPANY DATA ===============================================


async def test_bad_company_data_unauth(ac: AsyncClient):
    response = await ac.get('/data/company/3/')
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_bad_company_data_csv_unauth(ac: AsyncClient):
    response = await ac.get('/data/company/3/csv/')
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_bad_company_data_csv_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/data/company/100/csv/', headers=headers)
    assert response.status_code == 404
    assert response.json().get("detail") == "This company not found"


async def test_bad_company_data_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/data/company/100/', headers=headers)
    assert response.status_code == 404
    assert response.json().get("detail") == "This company not found"


async def test_bad_company_data_csv_not_admin(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/data/company/2/csv/', headers=headers)
    assert response.status_code == 403
    assert response.json().get("detail") == "User doesn't have permission for this"


async def test_bad_company_data_not_admin(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/data/company/2/', headers=headers)
    assert response.status_code == 403
    assert response.json().get("detail") == "User doesn't have permission for this"


async def test_company_data_csv(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/data/company/2/csv/', headers=headers)
    assert response.status_code == 200


async def test_company_data(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/data/company/2/', headers=headers)
    assert response.status_code == 200
    assert response.json().get("detail") == 'success'
    assert len(response.json().get('result').get('datas')) == 10
    assert response.json().get('result').get('datas')[0].get("company_id") == 2
    assert response.json().get('result').get('datas')[0].get("user_id") == 3


# ============================================== COMPANY DATA QUIZ ===============================================


async def test_bad_company_data_quiz_unauth(ac: AsyncClient):
    response = await ac.get('/data/company/3/quiz/2/')
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_bad_company_data_quiz_csv_unauth(ac: AsyncClient):
    response = await ac.get('/data/company/3/quiz/2/csv/')
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_bad_company_data_quiz_csv_company_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/data/company/100/quiz/2/csv/', headers=headers)
    assert response.status_code == 404
    assert response.json().get("detail") == "This company not found"


async def test_bad_company_data_quiz_company_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/data/company/100/quiz/2/', headers=headers)
    assert response.status_code == 404
    assert response.json().get("detail") == "This company not found"


async def test_bad_company_data_quiz_csv_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/data/company/2/quiz/100/csv/', headers=headers)
    assert response.status_code == 404
    assert response.json().get("detail") == "This quiz not found"


async def test_bad_company_data_quiz_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/data/company/2/quiz/100/', headers=headers)
    assert response.status_code == 404
    assert response.json().get("detail") == "This quiz not found"


async def test_bad_company_data_quiz_csv_not_in_company(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/data/company/2/quiz/2 /csv/', headers=headers)
    assert response.status_code == 403
    assert response.json().get("detail") == "This quiz not in this company"


async def test_bad_company_data_quiz_not_in_company(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/data/company/2/quiz/2/', headers=headers)
    assert response.status_code == 403
    assert response.json().get("detail") == "This quiz not in this company"


async def test_bad_company_data_quiz_csv_not_admin(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/data/company/2/quiz/3/csv/', headers=headers)
    assert response.status_code == 403
    assert response.json().get("detail") == "User doesn't have permission for this"


async def test_bad_company_data_quiz_not_admin(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/data/company/2/quiz/3/', headers=headers)
    assert response.status_code == 403
    assert response.json().get("detail") == "User doesn't have permission for this"


async def test_company_data_quiz_csv(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/data/company/2/quiz/3/csv/', headers=headers)
    assert response.status_code == 200


async def test_company_data_quiz(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/data/company/2/quiz/3/', headers=headers)
    assert response.status_code == 200
    assert response.json().get("detail") == 'success'
    assert len(response.json().get('result').get('datas')) == 8
    assert response.json().get('result').get('datas')[0].get("company_id") == 2
    assert response.json().get('result').get('datas')[0].get("user_id") == 3
    assert response.json().get('result').get('datas')[0].get("quiz_id") == 3


# ============================================== COMPANY DATA USER ===============================================


async def test_bad_company_data_user_unauth(ac: AsyncClient):
    response = await ac.get('/data/company/3/user/2/')
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_bad_company_data_user_csv_unauth(ac: AsyncClient):
    response = await ac.get('/data/company/3/user/2/csv/')
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_bad_company_data_user_csv_company_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/data/company/100/user/2/csv/', headers=headers)
    assert response.status_code == 404
    assert response.json().get("detail") == "This company not found"


async def test_bad_company_data_user_company_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/data/company/100/user/2/', headers=headers)
    assert response.status_code == 404
    assert response.json().get("detail") == "This company not found"


async def test_bad_company_data_user_csv_not_member(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/data/company/2/user/4/csv/', headers=headers)
    assert response.status_code == 403
    assert response.json().get("detail") == "User with id 4 not a member of this company"


async def test_bad_company_data_user_not_member(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/data/company/2/user/4/', headers=headers)
    assert response.status_code == 403
    assert response.json().get("detail") == "User with id 4 not a member of this company"


async def test_bad_company_data_user_csv_not_admin(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/data/company/2/user/3/csv/', headers=headers)
    assert response.status_code == 403
    assert response.json().get("detail") == "User doesn't have permission for this"


async def test_bad_company_data_user_not_admin(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/data/company/2/user/3/', headers=headers)
    assert response.status_code == 403
    assert response.json().get("detail") == "User doesn't have permission for this"


async def test_company_data_user_csv(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/data/company/2/user/3/csv/', headers=headers)
    assert response.status_code == 200


async def test_company_data_user(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/data/company/2/user/3/', headers=headers)
    assert response.status_code == 200
    assert response.json().get("detail") == 'success'
    assert len(response.json().get('result').get('datas')) == 10
    assert response.json().get('result').get('datas')[0].get("company_id") == 2
    assert response.json().get('result').get('datas')[0].get("user_id") == 3


# ============================================ COMPANY DATA USER QUIZ =============================================


async def test_bad_company_data_quiz_user_unauth(ac: AsyncClient):
    response = await ac.get('/data/company/3/quiz/2/user/2/')
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_bad_company_data_quiz_user_csv_unauth(ac: AsyncClient):
    response = await ac.get('/data/company/3/quiz/2/user/2/csv/')
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_bad_company_data_quiz_user_csv_company_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/data/company/100/quiz/2/user/2/csv/', headers=headers)
    assert response.status_code == 404
    assert response.json().get("detail") == "This company not found"


async def test_bad_company_data_quiz_user_company_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/data/company/100/quiz/2/user/2/', headers=headers)
    assert response.status_code == 404
    assert response.json().get("detail") == "This company not found"


async def test_bad_company_data_quiz_user_csv_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/data/company/2/quiz/100/user/2/csv/', headers=headers)
    assert response.status_code == 404
    assert response.json().get("detail") == "This quiz not found"


async def test_bad_company_data_quiz_user_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/data/company/2/quiz/100/user/2/', headers=headers)
    assert response.status_code == 404
    assert response.json().get("detail") == "This quiz not found"


async def test_bad_company_data_quiz_user_csv_not_in_company(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/data/company/2/quiz/2/user/2/csv/', headers=headers)
    assert response.status_code == 403
    assert response.json().get("detail") == "This quiz not in this company"


async def test_bad_company_data_quiz_user_not_in_company(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/data/company/2/quiz/2/user/2/', headers=headers)
    assert response.status_code == 403
    assert response.json().get("detail") == "This quiz not in this company"


async def test_bad_company_data_quiz_user_csv_not_member(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/data/company/2/quiz/1/user/4/csv/', headers=headers)
    assert response.status_code == 403
    assert response.json().get("detail") == "User with id 4 not a member of this company"


async def test_bad_company_data_quiz_user_not_member(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/data/company/2/quiz/1/user/4/', headers=headers)
    assert response.status_code == 403
    assert response.json().get("detail") == "User with id 4 not a member of this company"


async def test_bad_company_data_quiz_user_csv_not_admin(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/data/company/2/quiz/1/user/3/csv/', headers=headers)
    assert response.status_code == 403
    assert response.json().get("detail") == "User doesn't have permission for this"


async def test_bad_company_data_quiz_user_not_admin(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/data/company/2/quiz/1/user/3/', headers=headers)
    assert response.status_code == 403
    assert response.json().get("detail") == "User doesn't have permission for this"


async def test_company_data_quiz_user_csv(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/data/company/2/quiz/1/user/3/csv/', headers=headers)
    assert response.status_code == 200


async def test_company_data_quiz_user(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/data/company/2/quiz/1/user/3/', headers=headers)
    assert response.status_code == 200
    assert response.json().get("detail") == 'success'
    assert len(response.json().get('result').get('datas')) == 2
    assert response.json().get('result').get('datas')[0].get("company_id") == 2
    assert response.json().get('result').get('datas')[0].get("user_id") == 3
    assert response.json().get('result').get('datas')[0].get("quiz_id") == 1
    assert response.json().get('result').get('datas')[0].get("attempt") == 1