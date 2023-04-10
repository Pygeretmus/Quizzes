from httpx import AsyncClient

# Number of tests 14
# Created 6 users, 1 (id=6) deleted and recreated (id=7).
# Created 5 companies, 1 (id=5) deleted.
# User 1 in company 2, user 2 has invite to company 1.
# User 3 in company 2, company 3 has request from user 2.
# User 1 is admin in company 2.


# ========================================= GET MY NOTIFICATIONS ============================================


async def test_bad_get_notifications_unauth(ac: AsyncClient):
    response = await ac.get('/notifications/my/')
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_get_notifications(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/notifications/my/', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"
    assert len(response.json().get('result')) == 2
    assert response.json().get('result')[1].get('user_id') == 3
    assert response.json().get('result')[1].get('company_id') == 2
    assert response.json().get('result')[1].get('quiz_id') == 1
    assert response.json().get('result')[1].get('notification_read') == False
    assert response.json().get('result')[1].get('notification_content') == "Company 'test_company_2' created new quiz!"


# ========================================= READ NOTIFICATION ============================================


async def test_bad_read_notification_unauth(ac: AsyncClient):
    response = await ac.put('/notifications/1/read/')
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_bad_read_notification_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.put('/notifications/100/read/', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "It's not your notification"


async def test_read_notification(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.put('/notifications/1/read/', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"
    assert response.json().get('result')[0].get("notification_read")== True


# ========================================= READ NOTIFICATIONS ============================================


async def test_bad_read_notifications_unauth(ac: AsyncClient):
    response = await ac.get('/notifications/my/read/')
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_read_notifications(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/notifications/my/read/', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"
    assert len(response.json().get('result')) == 1
    assert response.json().get('result')[0].get('user_id') == 3
    assert response.json().get('result')[0].get('company_id') == 2
    assert response.json().get('result')[0].get('quiz_id') == 1
    assert response.json().get('result')[0].get('notification_read') == True
    assert response.json().get('result')[0].get('notification_content') == "Company 'test_company_2' created new quiz!"


# ========================================= UNREAD NOTIFICATIONS ============================================


async def test_bad_unread_notifications_unauth(ac: AsyncClient):
    response = await ac.get('/notifications/my/unread/')
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_unread_notifications(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/notifications/my/unread/', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"
    assert len(response.json().get('result')) == 1
    assert response.json().get('result')[0].get('user_id') == 3
    assert response.json().get('result')[0].get('company_id') == 2
    assert response.json().get('result')[0].get('quiz_id') == 3
    assert response.json().get('result')[0].get('notification_read') == False
    assert response.json().get('result')[0].get('notification_content') == "Company 'test_company_2' created new quiz!"

 
 # ========================================= DELETE NOTIFICATION ============================================


async def test_bad_delete_notification_unauth(ac: AsyncClient):
    response = await ac.delete('/notifications/1/delete/')
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_bad_delete_notification_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.delete('/notifications/100/delete/', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "It's not your notification"


async def test_delete_notification(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.delete('/notifications/1/delete/', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"


async def test_get_notifications_after_delete(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/notifications/my/', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"
    assert len(response.json().get('result')) == 1
    assert response.json().get('result')[0].get('user_id') == 3
    assert response.json().get('result')[0].get('company_id') == 2
    assert response.json().get('result')[0].get('quiz_id') == 3
    assert response.json().get('result')[0].get('notification_read') == False
    assert response.json().get('result')[0].get('notification_content') == "Company 'test_company_2' created new quiz!"


async def test_get_notifications_after_adding(ac: AsyncClient, users_tokens, notifications):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/notifications/my/', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"
    assert len(response.json().get('result')) == 2
    assert response.json().get('result')[0].get('user_id') == 3
    assert response.json().get('result')[0].get('company_id') == 2
    assert response.json().get('result')[0].get('quiz_id') == 3
    assert response.json().get('result')[0].get('notification_read') == False
    assert response.json().get('result')[0].get('notification_content') == "You can take a quiz '3 quiz' from company 'test_company_2'"

    
    