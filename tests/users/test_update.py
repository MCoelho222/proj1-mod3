from flask import json
import math as ma


mimetype = 'application/json'
url = "/user/"


def test_update_user_no_auth(client):

    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    user = {
        "email": "mcoelho2011@hotmail.com",
        "password": "mc5447#@T"
    }
    
    token = ''
    headers['Authorization'] = f"Bearer {token}"

    data = {
        "name": "Marcelo Coelho",
        "email": "mcoelho2011@hotmail.com",
        "password": "mc5447#@T"
    }
   
    response = client.patch(f'{url}update/5', data=json.dumps(data), headers=headers)


    assert response.json['error'] == "Invalid token."
    assert response.status_code == 403

def test_update_user_unauthorized(client, logged_in_client):

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
        "email": "janice.caldeira@hotmail.com",
    }

    response = client.patch(f"{url}update/5", data=json.dumps(update_user), headers=headers)

    assert response.json['error'] == "You don't have permission on this functionality."
    assert response.status_code == 403

def test_update_user_success(client, logged_in_client):

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

def test_update_user_success(client, logged_in_client):

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

    response = client.patch(f"{url}update/41", data=json.dumps(update_user), headers=headers)

    assert response.json["error"] == "User not found."
    assert response.status_code == 404

def test_update_user_email_exists(client, logged_in_client):

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