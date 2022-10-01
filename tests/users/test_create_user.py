from flask import json

mimetype = 'application/json'
url = "/user/create"

def test_create_user_unauthorized(client, logged_in_client):

    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    headers['Authorization'] = f"Bearer {logged_in_client}"

    data = {
        "role_id": 2,
        "name": "Marcelo Coelho",
        "email": "mcoelho2011@hotmail.com",
        "password": "mc5447#@T"
    }
   
    response = client.post(url, data=json.dumps(data), headers=headers)

    user = {
        "email": "mcoelho2011@hotmail.com",
        "password": "mc5447#@T"
    }

    login_response = client.post('/user/login', data=json.dumps(user), headers=headers)

    token = login_response.json['token']
    headers['Authorization'] = f"Bearer {token}"

    data = {
        "name": "Roger Cobalto",
        "email": "rogercobalto@gmail.com",
        "password": "1234567@#$"
    }
   
    response = client.post(url, data=json.dumps(data), headers=headers)

    assert response.json['error'] == "You don't have permission on this functionality."
    assert response.status_code == 403

def test_create_user_success(client, logged_in_client):

    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    headers['Authorization'] = f"Bearer {logged_in_client}"

    data = {
        "name": "Marcelo Coelho",
        "email": "mcoelho2011@hotmail.com",
        "password": "mc5447#@T"
    }
   
    response = client.post(url, data=json.dumps(data), headers=headers)

    user = {
        "email": "mcoelho2011@hotmail.com",
        "password": "mc5447#@T"
    }

    login_response = client.post('/user/login', data=json.dumps(user), headers=headers)

    assert response.status_code == 201
    assert response.json['message'] == "User created with success."
    assert login_response.status_code == 200



def test_create_user_missing_field(client, logged_in_client):

    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    headers['Authorization'] = f"Bearer {logged_in_client}"

    data = {
        "password": "mc5447#@T"
    }

    response = client.post(url, data=json.dumps(data), headers=headers)

    assert response.json['name'] == ['The field name is required.']
    assert response.json['email'] == ['The field email is required.']
    assert response.status_code == 400


def test_create_user_invalid_field(client, logged_in_client):

    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    headers['Authorization'] = f"Bearer {logged_in_client}"

    data = {
        "name": "Marcelo Coelho",
        "email": "mcoelhohotmail.com",
        "password": "12345678",
        "phone": "4199216640"
    }

    response = client.post(url, data=json.dumps(data), headers=headers)

    assert response.json['email'] == ['Invalid email.']
    assert response.json['password'] == ['Your password must have more 8 characters or more, and at least 1 special character.']
    assert response.json['phone'] == ['Invalid phone number.']
    assert response.status_code == 400


def test_create_user_email_exists(client, logged_in_client):

    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    headers['Authorization'] = f"Bearer {logged_in_client}"

    data = {
        "name": "Marcelo Coelho",
        "email": "luislopes@gmail.com",
        "password": "mc5447#@T"
    }

    response = client.post(url, data=json.dumps(data), headers=headers)

    assert response.json['error'] == "User not created. Email already exists."
    assert response.status_code == 400
    
    

