from httpx    import AsyncClient


# Number of tests 41
# Created 6 users, 1 (id=6) deleted and recreated (id=7).
# Created 5 companies, 1 (id=5) deleted.
# User 1 in company 2, user 2 has invite to company 1.
# User 3 in company 2, company 3 has request from user 2.
# User 1 is admin in company 2.
# Created 2 quizzes, 1 (id=2) deleted.


# ============================================== QUIZ CREATE ===============================================


async def test_bad_create_quiz_unauth(ac: AsyncClient):
    payload = {
        "quiz_name": "quiz1",
        "quiz_frequency": 1,
        "questions": [
        {
        "question_name": "question 1",
        "question_answers": [
        "True", "False"
                            ],
        "question_right": "True"
        },
        {
        "question_name": "question 3",
        "question_answers": [
        "True", "False"
        ],
        "question_right": "False"
        }
        ]
    }
    response = await ac.post('/company/100/quiz/', json=payload)
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_bad_create_quiz_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    payload = {
        "quiz_name": "quiz1",
        "quiz_frequency": 1,
        "questions": [
        {
        "question_name": "question 1",
        "question_answers": [
        "True", "False"
      ],
        "question_right": "True"
    },
{
        "question_name": "question 3",
        "question_answers": [
        "True", "False"
      ],
        "question_right": "False"
    }
    ]
    }
    response = await ac.post('/company/100/quiz/', headers=headers, json=payload)
    assert response.status_code == 404
    assert response.json().get('detail') == "This company not found"


async def test_bad_create_quiz_not_admin(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    payload = {
        "quiz_name": "quiz1",
        "quiz_frequency": 1,
        "questions": [
        {
        "question_name": "question 1",
        "question_answers": [
        "True", "False"
      ],
        "question_right": "True"
    },
{
        "question_name": "question 3",
        "question_answers": [
        "True", "False"
      ],
        "question_right": "False"
    }
  ]
    }
    response = await ac.post('/company/2/quiz/', headers=headers, json=payload)
    assert response.status_code == 403
    assert response.json().get('detail') == "User doesn't have permission for this"


async def test_bad_create_quiz_empty_name(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "quiz_name": "",
        "quiz_frequency": 1,
        "questions": [
        {
        "question_name": "question 1",
        "question_answers": [
        "True", "False"
      ],
        "question_right": "True"
    },
{
        "question_name": "question 3",
        "question_answers": [
        "True", "False"
      ],
        "question_right": "False"
    }
  ]
    }
    response = await ac.post('/company/2/quiz/', headers=headers, json=payload)
    assert response.status_code == 400
    assert response.json().get('detail') == "Quiz name required"


async def test_bad_create_quiz_one_question(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "quiz_name": "1 quiz",
        "quiz_frequency": 1,
        "questions": [
        {
        "question_name": "question 1",
        "question_answers": [
        "True", "False"
      ],
        "question_right": "True"
    },
  ]
    }
    response = await ac.post('/company/2/quiz/', headers=headers, json=payload)
    assert response.status_code == 422
    assert response.json().get('detail') == "Quiz must have more than one question"


async def test_bad_create_quiz_question_empty_name(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "quiz_name": "1 quiz",
        "quiz_frequency": 1,
        "questions": [
        {
        "question_name": "",
        "question_answers": [
        "True", "False"
      ],
        "question_right": "True"
    },
{
        "question_name": "question 3",
        "question_answers": [
        "True", "False"
      ],
        "question_right": "False"
    }
  ]
    }
    response = await ac.post('/company/2/quiz/', headers=headers, json=payload)
    assert response.status_code == 400
    assert response.json().get('detail') == "Question name required"


async def test_bad_create_quiz_one_answer(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "quiz_name": "1 quiz",
        "quiz_frequency": 1,
        "questions": [
        {
        "question_name": "question 1",
        "question_answers": [
        "True"
      ],
        "question_right": "True"
    },
{
        "question_name": "question 3",
        "question_answers": [
        "True", "False"
      ],
        "question_right": "False"
    }
  ]
    }
    response = await ac.post('/company/2/quiz/', headers=headers, json=payload)
    assert response.status_code == 422
    assert response.json().get('detail') == "Question must have more than one answer"


async def test_bad_create_quiz_question_not_unique(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "quiz_name": "1 quiz",
        "quiz_frequency": 1,
        "questions": [
        {
        "question_name": "question 1",
        "question_answers": [
        "True", "False"
      ],
        "question_right": "True"
    },
{
        "question_name": "question 1",
        "question_answers": [
        "True", "False"
      ],
        "question_right": "False"
    }
  ]
    }
    response = await ac.post('/company/2/quiz/', headers=headers, json=payload)
    assert response.status_code == 422
    assert response.json().get('detail') == "Question must have unique name"


async def test_bad_create_quiz_answer_empty_name(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "quiz_name": "1 quiz",
        "quiz_frequency": 1,
        "questions": [
        {
        "question_name": "question 1",
        "question_answers": [
        "True", ""
      ],
        "question_right": "True"
    },
{
        "question_name": "question 3",
        "question_answers": [
        "True", "False"
      ],
        "question_right": "False"
    }
  ]
    }
    response = await ac.post('/company/2/quiz/', headers=headers, json=payload)
    assert response.status_code == 400
    assert response.json().get('detail') == "Answer name required"


async def test_bad_create_quiz_answer_unique(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "quiz_name": "1 quiz",
        "quiz_frequency": 1,
        "questions": [
        {
        "question_name": "question 1",
        "question_answers": [
        "True", "True"
      ],
        "question_right": "True"
    },
{
        "question_name": "question 3",
        "question_answers": [
        "True", "False"
      ],
        "question_right": "False"
    }
  ]
    }
    response = await ac.post('/company/2/quiz/', headers=headers, json=payload)
    assert response.status_code == 422
    assert response.json().get('detail') == "Answer must have unique name"


async def test_bad_create_quiz_right_answer_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "quiz_name": "1 quiz",
        "quiz_frequency": 1,
        "questions": [
        {
        "question_name": "question 1",
        "question_answers": [
        "True", "False"
      ],
        "question_right": "Hello"
    },
{
        "question_name": "question 3",
        "question_answers": [
        "True", "False"
      ],
        "question_right": "False"
    }
  ]
    }
    response = await ac.post('/company/2/quiz/', headers=headers, json=payload)
    assert response.status_code == 422
    assert response.json().get('detail') == "Right answer not in the answers"


async def test_create_quiz_owner(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "quiz_name": "1 quiz",
        "quiz_frequency": 1,
        "questions": [
        {
        "question_name": "question 1",
        "question_answers": [
        "True", "False"
      ],
        "question_right": "True"
    },
{
        "question_name": "question 2",
        "question_answers": [
        "True", "False"
      ],
        "question_right": "True"
    }
  ]
    }
    response = await ac.post('/company/2/quiz/', headers=headers, json=payload)
    assert response.status_code == 200
    assert response.json().get('result').get("quiz_name") == "1 quiz"
    assert response.json().get('result').get("quiz_id") == 1
    assert response.json().get('result').get("quiz_frequency") == 1
    assert response.json().get('result').get("company_id") == 2
    assert response.json().get('detail') == "success"
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    payload = {
        "quiz_name": "2 quiz",
        "quiz_frequency": 1,
        "questions": [
        {
        "question_name": "question 3",
        "question_answers": [
        "True", "False"
      ],
        "question_right": "True"
    },
{
        "question_name": "question 4",
        "question_answers": [
        "True", "False"
      ],
        "question_right": "True"
    }
  ]
    }
    await ac.post('/company/3/quiz/', headers=headers, json=payload)


async def test_create_quiz_admin(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
        "quiz_name": "3 quiz",
        "quiz_frequency": 0,
        "questions": [
        {
        "question_name": "question 5",
        "question_answers": [
        "True", "False"
      ],
        "question_right": "True"
    },
    {
        "question_name": "question 6",
        "question_answers": [
        "True", "False"
      ],
        "question_right": "True"
    },
    {
        "question_name": "question 7",
        "question_answers": [
        "True", "False"
      ],
        "question_right": "True"
    },
{
        "question_name": "question 8",
        "question_answers": [
        "True", "False"
      ],
        "question_right": "True"
    }
  ]
    }
    response = await ac.post('/company/2/quiz/', headers=headers, json=payload)
    assert response.status_code == 200
    assert response.json().get('result').get("quiz_name") == "3 quiz"
    assert response.json().get('result').get("quiz_id") == 3
    assert response.json().get('result').get("quiz_frequency") == 0
    assert response.json().get('result').get("company_id") == 2
    assert response.json().get('detail') == "success"

    payload = {
        "quiz_name": "4 quiz",
        "quiz_frequency": 0,
        "questions": [
        {
        "question_name": "question 9",
        "question_answers": [
        "True", "False"
      ],
        "question_right": "True"
    },
    {
        "question_name": "question 10",
        "question_answers": [
        "True", "False"
      ],
        "question_right": "True"
    }
  ]
    }
    await ac.post('/company/2/quiz/', headers=headers, json=payload)


# =============================================== GET QUIZZES ===============================================


async def test_bad_get_quizzes_unauth(ac: AsyncClient):
    response = await ac.get('/company/100/quizes')
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_bad_get_quizzes_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/company/100/quizes', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "This company not found"


async def test_bad_get_quizzes_not_member(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    response = await ac.get('/company/2/quizes', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "This user not a member of this company"


async def test_get_quizzes_company_two(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/company/2/quizes', headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('result').get('quizzes')) == 3
    assert response.json().get('detail') == "success"


# ============================================= GET QUIZ BY ID ===============================================


async def test_bad_get_quiz_by_id_unauth(ac: AsyncClient):
    response = await ac.get('/quiz/100/')
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_bad_get_quiz_by_id_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/quiz/100/', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "This quiz not found"


async def test_bad_get_quiz_by_id_not_member(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    response = await ac.get('/quiz/1/', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "This user not a member of this company"


async def test_get_quiz_by_id(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/quiz/1/', headers=headers)
    assert response.status_code == 200
    assert response.json().get('result').get("quiz_name") == "1 quiz"
    assert response.json().get('result').get("quiz_id") == 1
    assert response.json().get('result').get("quiz_frequency") == 1
    assert response.json().get('result').get("company_id") == 2
    assert response.json().get('detail') == "success"


# =============================================== DELETE QUIZ =================================================


async def test_bad_delete_quiz_by_id_unauth(ac: AsyncClient):
    response = await ac.delete('/quiz/100/')
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_bad_delete_quiz_by_id_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.delete('/quiz/100/', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "This quiz not found"


async def test_bad_delete_quiz_by_id_not_member(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    response = await ac.delete('/quiz/2/', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "This user not a member of this company"


async def test_bad_delete_quiz_by_id_not_admin(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.delete('/quiz/3/', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "User doesn't have permission for this"


async def test_delete_quiz_by_id(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.delete('/quiz/4/', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"


async def test_get_quizzes_company_two_after_delete(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/company/2/quizes', headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('result').get('quizzes')) == 2
    assert response.json().get('detail') == "success"


# ============================================== QUIZ UPDATE ===============================================


async def test_bad_update_quiz_unauth(ac: AsyncClient):
    payload = {
        "quiz_name": "quiz1",
        "quiz_frequency": 1,
        "questions": [
        {
        "question_name": "question 1",
        "question_answers": [
        "True", "False"
                            ],
        "question_right": "True"
        },
        {
        "question_name": "question 3",
        "question_answers": [
        "True", "False"
        ],
        "question_right": "False"
        }
        ]
    }
    response = await ac.put('/quiz/100/', json=payload)
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_bad_update_quiz_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    payload = {
        "quiz_name": "quiz1",
        "quiz_frequency": 1,
        "questions": [
        {
        "question_name": "question 1",
        "question_answers": [
        "True", "False"
      ],
        "question_right": "True"
    },
{
        "question_name": "question 3",
        "question_answers": [
        "True", "False"
      ],
        "question_right": "False"
    }
    ]
    }
    response = await ac.put('/quiz/100/', headers=headers, json=payload)
    assert response.status_code == 404
    assert response.json().get('detail') == "This quiz not found"


async def test_bad_update_quiz_not_admin(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    payload = {
        "quiz_name": "quiz1",
        "quiz_frequency": 1,
        "questions": [
        {
        "question_name": "question 1",
        "question_answers": [
        "True", "False"
      ],
        "question_right": "True"
    },
{
        "question_name": "question 3",
        "question_answers": [
        "True", "False"
      ],
        "question_right": "False"
    }
  ]
    }
    response = await ac.put('/quiz/1/', headers=headers, json=payload)
    assert response.status_code == 403
    assert response.json().get('detail') == "User doesn't have permission for this"


async def test_bad_update_quiz_one_question(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "quiz_name": "1 quiz",
        "quiz_frequency": 1,
        "questions": [
        {
        "question_name": "question 1",
        "question_answers": [
        "True", "False"
      ],
        "question_right": "True"
    },
  ]
    }
    response = await ac.put('/quiz/1/', headers=headers, json=payload)
    assert response.status_code == 422
    assert response.json().get('detail') == "Quiz must have more than one question"


async def test_bad_update_quiz_question_empty_name(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "quiz_name": "1 quiz",
        "quiz_frequency": 1,
        "questions": [
        {
        "question_name": "",
        "question_answers": [
        "True", "False"
      ],
        "question_right": "True"
    },
{
        "question_name": "question 3",
        "question_answers": [
        "True", "False"
      ],
        "question_right": "False"
    }
  ]
    }
    response = await ac.put('/quiz/1/', headers=headers, json=payload)
    assert response.status_code == 400
    assert response.json().get('detail') == "Question name required"


async def test_bad_put_quiz_one_answer(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "quiz_name": "1 quiz",
        "quiz_frequency": 1,
        "questions": [
        {
        "question_name": "question 1",
        "question_answers": [
        "True"
      ],
        "question_right": "True"
    },
{
        "question_name": "question 3",
        "question_answers": [
        "True", "False"
      ],
        "question_right": "False"
    }
  ]
    }
    response = await ac.put('/quiz/1/', headers=headers, json=payload)
    assert response.status_code == 422
    assert response.json().get('detail') == "Question must have more than one answer"


async def test_bad_update_quiz_question_not_unique(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "quiz_name": "1 quiz",
        "quiz_frequency": 1,
        "questions": [
        {
        "question_name": "question 1",
        "question_answers": [
        "True", "False"
      ],
        "question_right": "True"
    },
{
        "question_name": "question 1",
        "question_answers": [
        "True", "False"
      ],
        "question_right": "False"
    }
  ]
    }
    response = await ac.put('/quiz/1/', headers=headers, json=payload)
    assert response.status_code == 422
    assert response.json().get('detail') == "Question must have unique name"


async def test_bad_update_quiz_answer_empty_name(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "quiz_name": "1 quiz",
        "quiz_frequency": 1,
        "questions": [
        {
        "question_name": "question 1",
        "question_answers": [
        "True", ""
      ],
        "question_right": "True"
    },
{
        "question_name": "question 3",
        "question_answers": [
        "True", "False"
      ],
        "question_right": "False"
    }
  ]
    }
    response = await ac.put('/quiz/1/', headers=headers, json=payload)
    assert response.status_code == 400
    assert response.json().get('detail') == "Answer name required"


async def test_bad_update_quiz_answer_unique(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "quiz_name": "1 quiz",
        "quiz_frequency": 1,
        "questions": [
        {
        "question_name": "question 1",
        "question_answers": [
        "True", "True"
      ],
        "question_right": "True"
    },
{
        "question_name": "question 3",
        "question_answers": [
        "True", "False"
      ],
        "question_right": "False"
    }
  ]
    }
    response = await ac.put('/quiz/1/', headers=headers, json=payload)
    assert response.status_code == 422
    assert response.json().get('detail') == "Answer must have unique name"


async def test_bad_update_quiz_right_answer_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "quiz_name": "1 quiz",
        "quiz_frequency": 1,
        "questions": [
        {
        "question_name": "question 1",
        "question_answers": [
        "True", "False"
      ],
        "question_right": "Hello"
    },
{
        "question_name": "question 3",
        "question_answers": [
        "True", "False"
      ],
        "question_right": "False"
    }
  ]
    }
    response = await ac.put('/quiz/1/', headers=headers, json=payload)
    assert response.status_code == 422
    assert response.json().get('detail') == "Right answer not in the answers"


async def test_update_quiz_owner(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "quiz_name": "NEW QUIZ NAME"
        }
    response = await ac.put('/quiz/1/', headers=headers, json=payload)
    assert response.status_code == 200
    assert response.json().get('result').get("quiz_name") == "NEW QUIZ NAME"
    assert response.json().get('result').get("quiz_id") == 1
    assert response.json().get('result').get("quiz_frequency") == 1
    assert response.json().get('result').get("company_id") == 2
    assert response.json().get('detail') == "success"


async def test_get_quiz_by_id_after_update(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/quiz/1/', headers=headers)
    assert response.status_code == 200
    assert response.json().get('result').get("quiz_name") == "NEW QUIZ NAME"
    assert response.json().get('result').get("quiz_id") == 1
    assert response.json().get('result').get("quiz_frequency") == 1
    assert response.json().get('result').get("company_id") == 2
    assert response.json().get('detail') == "success"


async def test_update_quiz_admin(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
        "questions": [
        {
        "question_name": "11 question",
        "question_answers": [
        "True", "False", "None"
      ],
        "question_right": "True"
    },
{
        "question_name": "12 question",
        "question_answers": [
        "True", "False"
      ],
        "question_right": "True"
    }
  ]
    }
    response = await ac.put('/quiz/1/', headers=headers, json=payload)
    assert response.status_code == 200
    assert response.json().get('result').get("questions")[0].get("question_name") == "11 question"
    assert response.json().get('result').get("questions")[0].get("question_answers") == ["True", "False", "None"]
    assert response.json().get('result').get("questions")[0].get("question_right") == "True"
    assert response.json().get('detail') == "success"


async def test_get_quiz_by_id_after_update2(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/quiz/1/', headers=headers)
    assert response.status_code == 200
    assert response.json().get('result').get("quiz_name") == "NEW QUIZ NAME"
    assert response.json().get('result').get("quiz_id") == 1
    assert response.json().get('result').get("quiz_frequency") == 1
    assert response.json().get('result').get("company_id") == 2
    assert response.json().get('result').get("questions")[0].get("question_name") == "11 question"
    assert response.json().get('result').get("questions")[0].get("question_answers") == ["True", "False", "None"]
    assert response.json().get('result').get("questions")[0].get("question_right") == "True"
    assert response.json().get('detail') == "success"