from flask import json
import math as ma


mimetype = 'application/json'
url = "/user/"


def test_get_user_unauthorized(client, logged_in_client):

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
   
    response = client.post('/user/create', data=json.dumps(data), headers=headers)

    user = {
        "email": "mcoelho2011@hotmail.com",
        "password": "mc5447#@T"
    }

    login_response = client.post('/user/login', data=json.dumps(user), headers=headers)

    token = login_response.json['token']
    headers['Authorization'] = f"Bearer {token}"

    response = client.get(url, headers=headers)

    assert response.json['error'] == "You don't have permission on this functionality."
    assert response.status_code == 403


def test_get_users_success(client, logged_in_client):

    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    headers['Authorization'] = f"Bearer {logged_in_client}"

    name = 'Luis'
    response = client.get(f"{url}?name={name}", headers=headers)
    users_list = response.json
    check = all([name in user['name'] for user in users_list])
    
    assert response.status_code == 200
    assert check

def test_get_specific_user_success(client, logged_in_client):

    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    headers['Authorization'] = f"Bearer {logged_in_client}"
    
    name = 'Luis Lopes'
    response = client.get(f"{url}?name={name}", headers=headers)
    users_list = response.json
    print(users_list)
    check_all_names = all([name in user['name'] for user in users_list])
    keys = ['id','name', 'email', 'phone', 'role.name']
    check_keys = []
    for user in users_list:
        for key in keys:
            check_keys.append(key in user)
    all_keys_confirm = all(check_keys)

    assert response.status_code == 200
    assert check_all_names
    assert all_keys_confirm

def test_get_all_users_per_page(client, logged_in_client):

    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    headers['Authorization'] = f"Bearer {logged_in_client}"

    response = client.get(url, headers=headers)

    assert response.status_code == 200
    assert len(response.json) == 20
    
   
def test_get_user_not_found(client, logged_in_client):
    
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    headers['Authorization'] = f"Bearer {logged_in_client}"

    response = client.get(f"{url}?name=4567", headers=headers)

    assert response.status_code == 204

def test_get_user_pagination(client, logged_in_client):

    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    headers['Authorization'] = f"Bearer {logged_in_client}"

    response1 = client.get(f"{url}", headers=headers)
    pages_float = len(response1.json)/20.
    pages_round_up = ma.ceil(pages_float)
    
    response2 = client.get(f"{url}?page={pages_round_up}", headers=headers)
    
    assert len(response2.json) > 0