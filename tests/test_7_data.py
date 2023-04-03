from httpx    import AsyncClient


#----------------------------------------------------------------------------- MY DATA ------------------------------------------------------------------------------


async def test_my_data(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/data/my/', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"
    assert len(response.json().get('result').get('datas')) == 6
    assert response.json().get('result').get('datas')[0].get('user_id') == 1


async def test_my_data_quiz(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/data/my/quiz/1/', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"
    assert len(response.json().get('result').get('datas')) == 2
    assert response.json().get('result').get('datas')[0].get('user_id') == 1
    assert response.json().get('result').get('datas')[1].get('quiz_id') == 1
    

async def test_my_data_company(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/data/my/company/2/', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"
    assert len(response.json().get('result').get('datas')) == 2
    assert response.json().get('result').get('datas')[0].get('user_id') == 2
    

async def test_company_data(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/data/company/2/', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"
    assert len(response.json().get('result').get('datas')) == 10
    

async def test_company_data_quiz(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/data/company/2/quiz/1/', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"
    assert len(response.json().get('result').get('datas')) == 6
    assert response.json().get('result').get('datas')[0].get('company_id') == 2
    assert response.json().get('result').get('datas')[1].get('quiz_id') == 1


async def test_company_data_user(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/data/company/2/user/1/', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"
    assert len(response.json().get('result').get('datas')) == 6
    assert response.json().get('result').get('datas')[0].get('user_id') == 1


async def test_company_data_quiz_user(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/data/company/2/quiz/1/user/1/', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"
    assert len(response.json().get('result').get('datas')) == 2
    assert response.json().get('result').get('datas')[0].get('user_id') == 1
    assert response.json().get('result').get('datas')[1].get('quiz_id') == 1


async def test_analytics(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/analytics/user/1/', headers=headers)
    assert response.status_code == 200
    
    response = await ac.get('/analytics/my/', headers=headers)
    assert response.status_code == 200
    
    response = await ac.get('/analytics/my/company/2/', headers=headers)
    assert response.status_code == 200
    
    response = await ac.get('/analytics/my/average/', headers=headers)
    assert response.status_code == 200
    
    response = await ac.get('/analytics/my/average/company/2/', headers=headers)
    assert response.status_code == 200
    
    response = await ac.get('/analytics/my/average/quiz/1/', headers=headers)
    assert response.status_code == 200
    
    response = await ac.get('/analytics/my/datas/', headers=headers)
    assert response.status_code == 200
    
    response = await ac.get('/analytics/company/2/average/', headers=headers)
    assert response.status_code == 200
    
    response = await ac.get('/analytics/company/2/average/user/2/', headers=headers)
    assert response.status_code == 200
    
    response = await ac.get('/analytics/company/2/average/quiz/1/', headers=headers)
    assert response.status_code == 200
    
    response = await ac.get('/analytics/company/2/user/1/rating/', headers=headers)
    assert response.status_code == 200
    
    response = await ac.get('/analytics/company/2/rating/', headers=headers)
    assert response.status_code == 200

    response = await ac.get('/analytics/company/2/datas/', headers=headers)
    assert response.status_code == 200



