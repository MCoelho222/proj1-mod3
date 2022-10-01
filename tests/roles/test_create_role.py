from flask import json

mimetype = 'application/json'
url = "/role/create"


def test_create_role_no_auth(client):

    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    token = ''
    headers['Authorization'] = f"Bearer {token}"
    data = {
        "name": "DevOps",
        "description": "Operator Developer",
        "permissions": [1, 2]
    }
    response = client.post(url, data=json.dumps(data), headers=headers)

    assert response.json['error'] == "Invalid token."
    assert response.status_code == 403


def test_create_role_no_permission(client, logged_in_client):

    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    headers['Authorization'] = f"Bearer {logged_in_client}"
    data = {
        "role_id": 3,
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

    data = {
        "name": "DevOps",
        "description": "Operator Developer",
        "permissions": [1, 2]
    }
    response = client.post(url, data=json.dumps(data), headers=headers)

    assert response.json['error'] == "You don't have permission on this functionality."
    assert response.status_code == 403


def test_create_role_success(client, logged_in_client):

    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    headers['Authorization'] = f"Bearer {logged_in_client}"
    data = {
        "name": "DevOps",
        "description": "Operator Developer",
        "permissions": [1, 2]
    }
    response = client.post(url, data=json.dumps(data), headers=headers)

    assert response.json['message'] == "Role successfully created."
    assert response.status_code == 201


def test_create_role_missing_field(client, logged_in_client):

    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    headers['Authorization'] = f"Bearer {logged_in_client}"
    data = {
        "name": "DevOps",
        "description": "Operator Developer",
    }
    response = client.post(url, data=json.dumps(data), headers=headers)

    assert response.json['permissions'] == ["The field permissions is required."]
    assert response.status_code == 400


def test_create_role_invalid_permission(client, logged_in_client):

    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    headers['Authorization'] = f"Bearer {logged_in_client}"
    data = {
        "name": "DevOps",
        "description": "Operator Developer",
        "permissions": [1, 2, 6]
    }
    response = client.post(url, data=json.dumps(data), headers=headers)

    assert response.json['error'] == "Permission 6 does not exist."
    assert response.status_code == 400


def test_create_role_permissions_not_list(client, logged_in_client):

    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    headers['Authorization'] = f"Bearer {logged_in_client}"
    data = {
        "name": "DevOps",
        "description": "Operator Developer",
        "permissions": 1
    }
    response = client.post(url, data=json.dumps(data), headers=headers)

    assert response.json['permissions'] == ["Invalid permissions."]
    assert response.status_code == 400


def test_create_role_invalid_field(client, logged_in_client):

    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    headers['Authorization'] = f"Bearer {logged_in_client}"
    data = {
        "name": "",
        "description": "Operator Developer",
        "permissions": [1, 2, 3]
    }
    response = client.post(url, data=json.dumps(data), headers=headers)

    assert response.json['name'] == ["The field name cannot be empty."]
    assert response.status_code == 400