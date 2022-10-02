from flask import json


mimetype = 'application/json'
url = "/user/"


def test_update_user_no_auth(client):
    """
    1. PATCH data with invalid token;
    2. Check error message and status 403.
    """

    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    token = ''
    headers['Authorization'] = f"Bearer {token}"
    data = {
        "name": "Luis Lopes",
        "email": "luislopes@hotmail.com",
        "password": "123Mudar!"
    }
    response = client.patch(f'{url}update/5', data=json.dumps(data), headers=headers)

    assert response.json['error'] == "Invalid token."
    assert response.status_code == 403

def test_update_user_no_permission(client, logged_in_client):
    """
    1. Login;
    2. POST new user without permission;
    3. Login user without permission;
    4. Try PATCH user data;
    5. Check error message and status 403.
    """

    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    headers['Authorization'] = f"Bearer {logged_in_client}"
    data = {
        "role_id": 1,
        "name": "Marcelo Coelho",
        "email": "mcoelho2011@hotmail.com",
        "password": "mc5447#@T"
    }
    response = client.post('/user/create', data=json.dumps(data), headers=headers)
    
    user = {
        "email": "mcoelho2011@hotmail.com",
        "password": "mc5447#@T"
    }
    login_response = client.post('/user/login', data=json.dumps(user), headers=headers)

    token = login_response.json['token']
    headers['Authorization'] = f"Bearer {token}"
    update_user = {
        "name": "Luis Lopes",
        "email": "luislopes@hotmail.com",
        "password": "123Mudar!"
    }
    response = client.patch(f"{url}update/40", data=json.dumps(update_user), headers=headers)

    assert response.json['error'] == "You don't have permission on this functionality."
    assert response.status_code == 403

def test_update_user_success(client, logged_in_client):
    """
    1. Login;
    2. PATCH user data;
    3. Check message and status 200.
    """

    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    headers['Authorization'] = f"Bearer {logged_in_client}"

    update_user = {
        "name": "Luis Lopes",
        "email": "luislopesssss@gmail.com",
        "password": "123Mudar!"
    }
    response = client.patch(f"{url}update/40", data=json.dumps(update_user), headers=headers)

    assert response.json["message"] == "User successfully updated."
    assert response.status_code == 200

def test_update_user_not_found(client, logged_in_client):
    """
    1. Login;
    2. PATCH user with impossible query param;
    3. Check error message and status 404.
    """

    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    headers['Authorization'] = f"Bearer {logged_in_client}"

    update_user = {
        "name": "Luis Lopes",
        "email": "luislopesssss@gmail.com",
        "password": "123Mudar!"
    }
    response = client.patch(f"{url}update/5050505050", data=json.dumps(update_user), headers=headers)

    assert response.json["error"] == "User not found."
    assert response.status_code == 404

def test_update_user_qparam_not_int(client, logged_in_client):
    """
    1. Login;
    2. PATCH user with string query param;
    3. Check status 404.
    """

    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    headers['Authorization'] = f"Bearer {logged_in_client}"

    update_user = {
        "name": "Luis Lopes",
        "email": "luislopesssss@gmail.com",
        "password": "123Mudar!"
    }
    response = client.patch(f"{url}update/g", data=json.dumps(update_user), headers=headers)

    assert response.status_code == 404

def test_update_user_email_exists(client, logged_in_client):
    """
    1. Login;
    2. Try to PATCH user data with an existent email;
    3. Check error message and status 409.
    """

    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    headers['Authorization'] = f"Bearer {logged_in_client}"

    update_user = {
        "name": "Luis Lopes",
        "email": "gui.ferreira@example.com",
        "password": "123Mudar!"
    }

    response = client.patch(f"{url}update/40", data=json.dumps(update_user), headers=headers)

    assert response.json["error"] == "Email already exists."
    assert response.status_code == 409

def test_update_user_invalid_field(client, logged_in_client):
    """
    1. Login;
    2. Try to PATCH user data with invalid email and phone number;
    3. Check error messages and status 400.
    """

    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    headers['Authorization'] = f"Bearer {logged_in_client}"

    update_user = {
        "name": "Luis Lopes",
        "email": "luislopesexample.com",
        "password": "123Mudar!",
        "phone":''
    }
    response = client.patch(f"{url}update/40", data=json.dumps(update_user), headers=headers)

    assert response.json["email"] == ["Invalid email."]
    assert response.json["phone"] == ["Invalid phone number."]
    assert response.status_code == 400