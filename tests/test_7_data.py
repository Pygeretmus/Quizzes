from httpx    import AsyncClient


#----------------------------------------------------------------------------- MY DATA ------------------------------------------------------------------------------


async def test_my_data(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/data/me/', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"
    assert len(response.json().get('result').get('datas')) == 6
    assert response.json().get('result').get('datas')[0].get('user_id') == 1
    assert response.json().get('result').get('datas')[1].get('user_id') == 1
    assert response.json().get('result').get('datas')[0].get('attempt') == 1
    assert response.json().get('result').get('datas')[0].get('answer') == "Question 'question 5': True is Right answer"


async def test_my_data_quiz(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/data/me/quiz/1/', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"
    assert len(response.json().get('result').get('datas')) == 2
    assert response.json().get('result').get('datas')[0].get('user_id') == 1
    assert response.json().get('result').get('datas')[1].get('quiz_id') == 1
    assert response.json().get('result').get('datas')[0].get('attempt') == 1
    assert response.json().get('result').get('datas')[0].get('answer') == "Question '7 question': True is Right answer"
    

async def test_my_data_company(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/data/me/company/1/', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"
    assert len(response.json().get('result').get('datas')) == 0
    
    
async def test_company_data(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/data/company/2/', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"
    assert len(response.json().get('result').get('datas')) == 10
    assert response.json().get('result').get('datas')[0].get('user_id') == 2
    assert response.json().get('result').get('datas')[1].get('user_id') == 1
    assert response.json().get('result').get('datas')[0].get('attempt') == 1
    assert response.json().get('result').get('datas')[0].get('answer') == "Question '7 question': True is Right answer"
    

async def test_company_data_quiz(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/data/company/2/quiz/1/', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"
    assert len(response.json().get('result').get('datas')) == 6
    assert response.json().get('result').get('datas')[0].get('user_id') == 2
    assert response.json().get('result').get('datas')[1].get('quiz_id') == 1
    assert response.json().get('result').get('datas')[0].get('attempt') == 1
    assert response.json().get('result').get('datas')[0].get('answer') == "Question '7 question': True is Right answer"
    print(response.json())


async def test_company_data_user(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/data/company/2/user/1/', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"
    assert len(response.json().get('result').get('datas')) == 6
    assert response.json().get('result').get('datas')[0].get('user_id') == 1
    assert response.json().get('result').get('datas')[1].get('user_id') == 1
    assert response.json().get('result').get('datas')[0].get('attempt') == 1
    assert response.json().get('result').get('datas')[0].get('answer') == "Question 'question 5': True is Right answer"


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
    assert response.json().get('result').get('datas')[0].get('attempt') == 1
    assert response.json().get('result').get('datas')[0].get('answer') == "Question '7 question': True is Right answer"






