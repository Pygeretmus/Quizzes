from httpx    import AsyncClient
from datetime import date, timedelta


# Number of tests 53
# Created 6 users, 1 (id=6) deleted and recreated (id=7).
# Created 5 companies, 1 (id=5) deleted.
# User 1 in company 2, user 2 has invite to company 1.
# User 3 in company 2, company 3 has request from user 2.
# User 1 is admin in company 2.
# Created 2 quizzes, 1 (id=2) deleted.


# ============================================= QUIZ PASSING ==============================================


async def test_bad_passing_quiz_unauth(ac: AsyncClient):
    payload = {}
    response = await ac.post('/attempt/100/', json=payload)
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_bad_passing_quiz_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    payload = {}
    response = await ac.post('/attempt/100/', headers=headers, json=payload)
    assert response.status_code == 404
    assert response.json().get('detail') == "This quiz not found"


async def test_bad_passing_quiz_not_member(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    payload = {}
    response = await ac.post('/attempt/1/', headers=headers, json=payload)
    assert response.status_code == 403
    assert response.json().get('detail') == "This user not a member of this company"
  

async def test_passing_quizzes(ac: AsyncClient, users_tokens):
    # 1 Attempt
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    payload = {
    "answers": [
    {
      "question_id": 3,
      "answer": "True"
    }
    ]}
    response = await ac.post('/attempt/2/', headers=headers, json=payload)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"
    assert response.json().get('result').get('all_questions') == 2
    assert response.json().get('result').get('right_answers') == 1
    assert response.json().get('result').get('average') == 0.5
	


async def test_bad_passing_quiz_second(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    payload = {}
    response = await ac.post('/attempt/2/', headers=headers, json=payload)
    assert response.status_code == 403
    assert response.json().get('detail') == f"This user must wait until {date.today() + timedelta(days=1)}"


# ============================================= GET RATING ==============================================


async def test_bad_get_rating_unauth(ac: AsyncClient):
    response = await ac.get('/analytics/user/1/')
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_bad_get_rating_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/analytics/user/100/', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "This user not found"


async def test_get_rating(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/analytics/user/3/', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"
    assert response.json().get('result') == 0.5
    response = await ac.get('/analytics/user/1/', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"
    assert response.json().get('result') == 0.0


# ============================================= GET MY RATING ==============================================


async def test_bad_get_my_rating_unauth(ac: AsyncClient):
    response = await ac.get('/analytics/my/')
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_get_my_rating(ac: AsyncClient, users_tokens):
    # 2 Attempt
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    payload = {
    "answers": [
    {
      "question_id": 11,
      "answer": "True"
    },
    {
      "question_id": 12,
      "answer": "True"
    }
    ]
}
    response = await ac.post('/attempt/1/', headers=headers, json=payload)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"
    assert response.json().get('result').get('all_questions') == 2
    assert response.json().get('result').get('right_answers') == 2
    assert response.json().get('result').get('average') == 1.0

    response = await ac.get('/analytics/my/', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"
    assert response.json().get('result') == 0.75


# ========================================= GET MY COMPANY RATING ===========================================


async def test_bad_get_my_company_rating_unauth(ac: AsyncClient):
    response = await ac.get('/analytics/my/company/2/')
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_bad_get_my_company_rating_not_member(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/analytics/my/company/1/', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "This user not a member of this company"


async def test_get_my_company_rating(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/analytics/my/company/2/', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"
    assert response.json().get('result') == 1.0
    response = await ac.get('/analytics/my/company/3/', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"
    assert response.json().get('result') == 0.5


# ========================================= GET MY AVERAGE ===========================================


async def test_bad_get_my_average_unauth(ac: AsyncClient):
    response = await ac.get('/analytics/my/average/')
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_get_my_average(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
        # 3 Attempt
    payload = {
    "answers": [
    {
      "question_id": 5,
      "answer": "True"
    },
    {
      "question_id": 6,
      "answer": "False"
    },
    {
      "question_id": 7,
      "answer": "True"
    },
    {
      "question_id": 8,
      "answer": "True"
    }
    ]
}
    response = await ac.post('/attempt/3/', headers=headers, json=payload)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"
    assert response.json().get('result').get('all_questions') == 4
    assert response.json().get('result').get('right_answers') == 3
    assert response.json().get('result').get('average') == 0.75
    # 4 Attempt
    payload = {
    "answers": [
    {
      "question_id": 5,
      "answer": "True"
    },
    {
      "question_id": 6,
      "answer": "True"
    },
    {
      "question_id": 7,
      "answer": "True"
    },
    {
      "question_id": 8,
      "answer": "True"
    }
    ]
}
    response = await ac.post('/attempt/3/', headers=headers, json=payload)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"
    assert response.json().get('result').get('all_questions') == 4
    assert response.json().get('result').get('right_answers') == 4
    assert response.json().get('result').get('average') == 1


    response = await ac.get('/analytics/my/average/', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == 'success'
    assert len(response.json().get('result')) == 3
    assert response.json().get('result')[1].get('quiz_id') == 3
    assert len(response.json().get('result')[1].get('result')) == 2
    assert response.json().get('result')[1].get('result')[0].get('quiz_average') == 0.75
    assert response.json().get('result')[1].get('result')[0].get('quizzes_average') == 0.75
    assert response.json().get('result')[1].get('result')[1].get('quiz_average') == 1.0
    assert response.json().get('result')[1].get('result')[1].get('quizzes_average') == 0.875


# ========================================= GET MY AVERAGE COMPANY ===========================================


async def test_bad_get_my_average_company_unauth(ac: AsyncClient):
    response = await ac.get('/analytics/my/average/company/2/')
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_bad_get_my_average_company_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/analytics/my/average/company/100/', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == 'This company not found'


async def test_bad_get_my_average_company_not_member(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/analytics/my/average/company/4/', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == 'This user not a member of this company'


async def test_get_my_average_company(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/analytics/my/average/company/2/', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == 'success'
    assert len(response.json().get('result')) == 2
    assert response.json().get('result')[1].get('quiz_id') == 1
    assert len(response.json().get('result')[1].get('result')) == 1
    assert response.json().get('result')[1].get('result')[0].get('quiz_average') == 1.0
    assert response.json().get('result')[1].get('result')[0].get('quizzes_average') == 1.0


# ========================================= GET MY AVERAGE QUIZ ===========================================


async def test_bad_get_my_average_quiz_unauth(ac: AsyncClient):
    response = await ac.get('/analytics/my/average/quiz/2/')
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_bad_get_my_average_quiz_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/analytics/my/average/quiz/100/', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == 'This quiz not found'


async def test_get_my_average_quiz(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/analytics/my/average/quiz/2/', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == 'success'
    assert len(response.json().get('result')) == 1
    assert response.json().get('result')[0].get('quiz_id') == 2
    assert len(response.json().get('result')[0].get('result')) == 1
    assert response.json().get('result')[0].get('result')[0].get('quiz_average') == 0.5
    assert response.json().get('result')[0].get('result')[0].get('quizzes_average') == 0.5


# ========================================= GET MY DATAS ===========================================


async def test_bad_get_my_datas_unauth(ac: AsyncClient):
    response = await ac.get('/analytics/my/datas/')
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_get_my_datas(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/analytics/my/datas/', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == 'success'
    assert len(response.json().get('result')) == 3
    assert response.json().get('result')[0].get('quiz_id') == 1
    assert response.json().get('result')[0].get('quiz_passed_at') == str(date.today())
    

# ========================================= GET COMPANY AVERAGE ===========================================


async def test_bad_get_company_average_unauth(ac: AsyncClient):
    response = await ac.get('/analytics/company/2/average/')
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_bad_get_company_average_company_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/analytics/company/100/average/', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "This company not found"


async def test_bad_get_company_average_not_admin(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/analytics/company/2/average/', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "User doesn't have permission for this"


async def test_get_company_average(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/analytics/company/2/average/', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"
    assert len(response.json().get('result')) == 3
    assert response.json().get('result')[0].get("user_id") == 3
    assert len(response.json().get('result')[0].get("result")) == 3
    assert response.json().get('result')[0].get("result")[0].get('quiz_id') == 1
    assert response.json().get('result')[0].get("result")[0].get('company_average') == 1.0
    assert response.json().get('result')[0].get("result")[1].get('quiz_id') == 3
    assert response.json().get('result')[0].get("result")[1].get('company_average') == 0.8333333333333334
    assert response.json().get('result')[0].get("result")[2].get('quiz_id') == 3
    assert response.json().get('result')[0].get("result")[2].get('company_average') == 0.9


# # ========================================= GET COMPANY AVERAGE USER ===========================================


async def test_bad_get_company_average_user_unauth(ac: AsyncClient):
    response = await ac.get("/analytics/company/2/average/user/3/")
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_bad_get_company_average_user_company_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/analytics/company/100/average/user/3/', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "This company not found"


async def test_bad_get_company_average_user_not_admin(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/analytics/company/2/average/user/3/', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "User doesn't have permission for this"


async def test_bad_get_company_average_user_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/analytics/company/2/average/user/100/', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "This user not found"


async def test_bad_get_company_average_user_not_in_company(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/analytics/company/2/average/user/4/', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "This user not a member of this company"


async def test_get_company_average_user(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/analytics/company/2/average/user/3/', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"
    assert len(response.json().get('result')) == 1
    assert response.json().get('result')[0].get("user_id") == 3
    assert len(response.json().get('result')[0].get("result")) == 3
    assert response.json().get('result')[0].get("result")[0].get('quiz_id') == 1
    assert response.json().get('result')[0].get("result")[0].get('quiz_average') == 1.0
    assert response.json().get('result')[0].get("result")[1].get('quiz_id') == 3
    assert response.json().get('result')[0].get("result")[1].get('quiz_average') == 0.75
    assert response.json().get('result')[0].get("result")[1].get('quizzes_average') == 0.75
    assert response.json().get('result')[0].get("result")[2].get('quiz_id') == 3
    assert response.json().get('result')[0].get("result")[2].get('quiz_average') == 1.0
    assert response.json().get('result')[0].get("result")[2].get('quizzes_average') == 0.875


# ========================================= GET COMPANY AVERAGE QUIZ ===========================================


async def test_bad_get_company_average_quiz_unauth(ac: AsyncClient):
    response = await ac.get("/analytics/company/2/average/quiz/1/")
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_bad_get_company_average_quiz_company_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/analytics/company/100/average/quiz/1/', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "This company not found"


async def test_bad_get_company_average_quiz_not_admin(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/analytics/company/2/average/quiz/1/', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "User doesn't have permission for this"


async def test_bad_get_company_average_quiz_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/analytics/company/2/average/quiz/100/', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "This quiz not found"


async def test_bad_get_company_average_quiz_not_in_company(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/analytics/company/2/average/quiz/2/', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "This quiz not in this company"


async def test_get_company_average_quiz(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/analytics/company/2/average/quiz/1/', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"
    assert len(response.json().get('result')) == 3
    assert response.json().get('result')[0].get("user_id") == 3
    assert len(response.json().get('result')[0].get("result")) == 1
    assert response.json().get('result')[0].get("result")[0].get('quiz_id') == 1
    assert response.json().get('result')[0].get("result")[0].get('quiz_average') == 1.0
    assert response.json().get('result')[0].get("result")[0].get('quizzes_average') == 1.0
 

# ========================================= GET COMPANY RATING ===========================================


async def test_bad_get_company_rating_unauth(ac: AsyncClient):
    response = await ac.get("/analytics/company/2/rating/")
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_bad_get_company_rating_company_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/analytics/company/100/rating/', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "This company not found"


async def test_bad_get_company_rating_not_admin(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/analytics/company/2/rating/', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "User doesn't have permission for this"


async def test_get_company_rating(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/analytics/company/2/rating/', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"
    assert len(response.json().get('result')) == 3
    assert response.json().get('result')[0].get("user_id") == 3
    assert response.json().get('result')[1].get("user_id") == 2
    assert response.json().get('result')[2].get("user_id") == 1 
    assert response.json().get('result')[0].get("company_average") == 0.9
    assert response.json().get('result')[1].get("company_average") == 0.0
    assert response.json().get('result')[2].get("company_average") == 0.0


# ========================================= GET COMPANY RATING USER ===========================================


async def test_bad_get_company_rating_user_unauth(ac: AsyncClient):
    response = await ac.get("/analytics/company/2/user/3/rating/")
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_bad_get_company_rating_user_company_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/analytics/company/100/user/3/rating/', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "This company not found"


async def test_bad_get_company_rating_user_not_admin(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/analytics/company/2/user/3/rating/', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "User doesn't have permission for this"


async def test_bad_get_company_rating_user_not_member(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/analytics/company/2/user/4/rating/', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "This user not a member of this company"


async def test_get_company_rating_user(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/analytics/company/2/user/3/rating/', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"
    assert len(response.json().get('result')) == 1
    assert response.json().get('result')[0].get("user_id") == 3 
    assert response.json().get('result')[0].get("company_average") == 0.9


# ========================================= GET COMPANY DATAS ===========================================


async def test_bad_get_company_datas_unauth(ac: AsyncClient):
    response = await ac.get("/analytics/company/2/datas/")
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_bad_get_company_datas_company_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/analytics/company/100/datas/', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "This company not found"


async def test_bad_get_company_datas_not_admin(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/analytics/company/2/datas/', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "User doesn't have permission for this"


async def test_get_company_datas(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/analytics/company/2/datas/', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"
    assert len(response.json().get('result')) == 3
    assert response.json().get('result')[1].get("user_id") == 2 
    assert response.json().get('result')[1].get("quiz_passed_at") == None
    assert response.json().get('result')[0].get("user_id") == 3 
    assert response.json().get('result')[0].get("quiz_passed_at") == str(date.today())