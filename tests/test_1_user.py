from httpx import AsyncClient


# Number of tests 33
# Created 6 users, 1 (id=6) deleted and recreated (id=7).


# ============================================= BAD USER CREATE ==============================================


async def test_bad_create_user__not_password(ac: AsyncClient):
    payload = {
        "user_email": "test@test.com",
        "user_name": "test"
    }
    response = await ac.post("/user/", json=payload)
    assert response.status_code == 400
    assert response.json().get('detail') == "Password required"


async def test_bad_create_user__low_password(ac: AsyncClient):
    payload = {
        "user_password": "tet",
        "user_password_repeat": "tet",
        "user_email": "test@test.com",
        "user_name": "test"
    }
    response = await ac.post("/user/", json=payload)
    assert response.status_code == 422
    assert response.json().get('detail') == "Password must be longer than three characters"


async def test_bad_create_user__dont_match(ac: AsyncClient):
    payload = {
        "user_password": "test",
        "user_password_repeat": "tess",
        "user_email": "test@test.com",
        "user_name": "test"
    }
    response = await ac.post("/user/", json=payload)
    assert response.status_code == 422
    assert response.json().get('detail') == "Password and Confirm Password must be match"


async def test_bad_create_user__empty_name(ac:AsyncClient):
    payload = {
        "user_password": "test",
        "user_password_repeat": "test",
        "user_email": "test@test.com",
    }
    response = await ac.post("/user/", json=payload)
    assert response.status_code == 400
    assert response.json().get('detail') == "Name required"


async def test_bad_create_user__no_valid_email(ac: AsyncClient):
    payload = {
        "user_password": "test",
        "user_password_repeat": "test",
        "user_email": "test",
        "user_name": "test"
    }
    response = await ac.post("/user/", json=payload)
    assert response.status_code == 422
    assert response.json().get('detail')[0].get('type') == "value_error.email"
    assert response.json().get('detail')[0].get('msg') == "value is not a valid email address"


async def test_bad_create_user__empty_email(ac: AsyncClient):
    payload = {
        "user_password": "test",
        "user_password_repeat": "test",
        "user_name": "test"
    }
    response = await ac.post("/user/", json=payload)
    assert response.status_code == 422
    assert response.json().get('detail')[0].get('type') == "value_error.missing"
    assert response.json().get('detail')[0].get('msg') == "field required"


# =========================================== SUCCESS USER CREATE ============================================    


async def test_create_users(ac: AsyncClient):
    # USER 1
    payload = {
        "user_password": "test1",
        "user_password_repeat": "test1",
        "user_email": "test1@test.com",
        "user_name": "test1",
    }
    response = await ac.post("/user/", json=payload)
    assert response.status_code == 200
    assert response.json().get("result").get("user_id") == 1
    assert response.json().get("result").get("user_email") == "test1@test.com"
    assert response.json().get("result").get("user_name") == "test1"
    assert response.json().get('result').get('user_password') == None
    assert response.json().get('detail') == "success"
    # USER 2
    payload = {
        "user_password": "test2",
        "user_password_repeat": "test2",
        "user_email": "test2@test.com",
        "user_name": "test2",
    }
    await ac.post("/user/", json=payload)
    # USER 3
    payload = {
        "user_password": "test3",
        "user_password_repeat": "test3",
        "user_email": "test3@test.com",
        "user_name": "test3",
    }
    await ac.post("/user/", json=payload)
    # USER 4
    payload = {
        "user_password": "test4",
        "user_password_repeat": "test4",
        "user_email": "test4@test.com",
        "user_name": "test4",
    }
    await ac.post("/user/", json=payload)
    # USER 5
    payload = {
        "user_password": "test5",
        "user_password_repeat": "test5",
        "user_email": "test5@test.com",
        "user_name": "test5",
    }
    await ac.post("/user/", json=payload)
    # USER 6 
    payload = {
        "user_password": "test6",
        "user_password_repeat": "test6",
        "user_email": "test6@test.com",
        "user_name": "test6",
    }
    await ac.post("/user/", json=payload)



async def test_bad_create_user__email_exists(ac: AsyncClient):
    payload = {
        "user_password": "test",
        "user_password_repeat": "test",
        "user_email": "test1@test.com",
        "user_name": "test",
    }
    response = await ac.post("/user/", json=payload)
    assert response.status_code == 403
    assert response.json().get('detail') == "Email already exists"


# ================================================== LOGIN ===================================================


async def test_bad_login__empty_password(ac: AsyncClient, login_user):
    response = await login_user("test1@test.com", "")
    assert response.status_code == 400
    assert response.json().get('detail') == "Password required"


async def test_bad_login__incorrect_email(ac: AsyncClient, login_user):
    response = await login_user("test@test.test", "test")
    assert response.status_code == 422
    assert response.json().get('detail')[0].get('type') == "value_error.email"
    assert response.json().get('detail')[0].get('msg') == "value is not a valid email address"


async def test_bad_login__empty_email(ac: AsyncClient, login_user):
    response = await login_user("", "test")
    assert response.status_code == 422
    assert response.json().get('detail')[0].get('type') == "value_error.email"
    assert response.json().get('detail')[0].get('msg') == "value is not a valid email address"


async def test_bad_login(ac: AsyncClient, login_user):
    response = await login_user("test1@test.com", "test_bad")
    assert response.status_code == 401
    assert response.json().get('detail') == 'Incorrect username or password'


async def test_login_all(ac: AsyncClient, login_user):
    response = await login_user("test1@test.com", "test1")
    assert response.status_code == 200
    assert response.json().get('result').get('token_type') == 'Bearer'
    assert response.json().get('detail') == "success"

    await login_user("test2@test.com", "test2")

    await login_user("test3@test.com", "test3")

    await login_user("test4@test.com", "test4")

    await login_user("test5@test.com", "test5")

    await login_user("test6@test.com", "test6")


# ============================================== AUTHENTICATION ==============================================


async def test_auth_me_one(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/auth/my/", headers=headers)
    assert response.status_code == 200
    assert response.json().get('result').get('user_name') == "test1"
    assert response.json().get('result').get('user_email') == "test1@test.com"
    assert response.json().get('result').get('user_id') == 1
    assert response.json().get('result').get('user_password') == None
    assert response.json().get('detail') == "success"


async def test_bad_auth_me(ac: AsyncClient):
    headers = {
        "Authorization": "Bearer retretwetrt.rqwryerytwetrty",
    }
    response = await ac.get("/auth/my/", headers=headers)
    assert response.status_code == 401
    assert response.json().get('detail') == "Incorrect token"


# ================================================ GET USERS =================================================


async def test_bad_get_users_list_unauth(ac: AsyncClient):
    response = await ac.get("/users/")
    assert response.status_code == 403
    assert response.json().get("detail") == "Not authenticated" 


async def test_get_users_list(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/users/", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get("result").get("users")) == 6
    assert response.json().get('result').get("users")[0].get('user_name') == "test1"
    assert response.json().get('result').get("users")[0].get('user_email') == "test1@test.com"
    assert response.json().get('result').get("users")[0].get('user_id') == 1
    assert response.json().get('result').get("users")[0].get('user_password') == None
    assert response.json().get('detail') == "success"


# ============================================== GET USER BY ID ==============================================


async def test_bad_get_user_by_id_unauth(ac: AsyncClient):
    response = await ac.get("/user/100/")
    assert response.status_code == 403
    assert response.json().get("detail") == "Not authenticated" 


async def test_bad_get_user_by_id__not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/user/100/", headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "This user not found"


async def test_get_user_by_id(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/user/2/", headers=headers)
    assert response.status_code == 200
    assert response.json().get('result').get('user_name') == "test2"
    assert response.json().get('result').get('user_email') == "test2@test.com"
    assert response.json().get('result').get('user_id') == 2
    assert response.json().get('result').get('user_password') == None
    assert response.json().get('detail') == "success"


# =============================================== UPDATE USER ================================================


async def test_bad_update_user_unauth(ac: AsyncClient):
    response = await ac.put("/user/100/")
    assert response.status_code == 403
    assert response.json().get("detail") == "Not authenticated" 


async def test_bad_update_user_one__not_your_acc(ac: AsyncClient, users_tokens):
    payload = {
        "user_name": "test1NEW",
    }
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.put("/user/100/", json=payload, headers=headers)
    assert response.status_code == 403
    assert response.json().get("detail") == "It's not your account"


async def test_bad_update_user_one__incorrect_password(ac: AsyncClient, users_tokens):
    payload = {
        "user_password": "tet",
    }
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.put("/user/1/", json=payload, headers=headers)
    assert response.status_code == 422
    assert response.json().get('detail') == "Password must be longer than three characters"


async def test_update_user_one(ac: AsyncClient, users_tokens):
    payload = {
        "user_name": "test1NEW",
    }
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.put("/user/1/", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json().get("result").get("user_id") == 1
    assert response.json().get("result").get("user_email") == 'test1@test.com'
    assert response.json().get("result").get("user_name") == 'test1NEW'
    assert response.json().get('result').get('user_password') == None
    assert response.json().get('detail') == "success"


async def test_get_user_by_id_updated(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/user/1/", headers=headers)
    assert response.status_code == 200
    assert response.json().get("result").get("user_id") == 1
    assert response.json().get("result").get("user_email") == 'test1@test.com'
    assert response.json().get("result").get("user_name") == 'test1NEW'


async def test_update_user_one_empty(ac: AsyncClient, users_tokens):
    payload = {
        "user_name": "",
        "user_password": ""
    }
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.put("/user/1/", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json().get("result").get("user_name") == 'test1NEW'


async def test_get_user_by_id_updated_twice(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/user/1/", headers=headers)
    assert response.status_code == 200
    assert response.json().get("result").get("user_id") == 1
    assert response.json().get("result").get("user_name") == 'test1NEW'


# =============================================== DELETE USER ================================================


async def test_bad_delete_user_unauth(ac: AsyncClient):
    response = await ac.delete("/user/100/")
    assert response.status_code == 403
    assert response.json().get("detail") == "Not authenticated"


async def test_bad_delete_user__not_your_acc(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.delete("/user/100/", headers=headers)
    assert response.status_code == 403
    assert response.json().get("detail") == "It's not your account"


async def test_delete_user_six(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test6@test.com']}",
    }
    response = await ac.delete("/user/6/", headers=headers)
    assert response.status_code == 200
    assert response.json().get("detail") == "success"


async def test_get_users_list_after_delete(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/users/", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get("result").get("users")) == 5


async def test_auth_me_two(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test6@test.com']}",
    }
    response = await ac.get("/auth/my/", headers=headers)
    assert response.status_code == 200
    assert response.json().get('result').get('user_name') == "User"
    assert response.json().get('result').get('user_email') == "test6@test.com"
    assert response.json().get('result').get('user_id') == 7
    assert response.json().get('result').get('user_password') == None


async def test_get_users_list_after_auth_by_token(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/users/", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get("result").get("users")) == 6