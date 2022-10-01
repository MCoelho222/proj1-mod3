from flask import json
import time


cod = str(round(time.time() * 1000))
cod_split = cod[7:]

mimetype = 'application/json'
url = "/inventory/"


def test_get_item_no_auth(client):

    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    headers['Authorization'] = f"Bearer {''}"
    response = client.get(f"{url}?id=4", headers=headers)

    assert response.json['error'] == "Invalid token."
    assert response.status_code == 403


def test_get_items_by_id_no_permission(client, logged_in_client):

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
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    user = {
        "email": "mcoelho2011@hotmail.com",
        "password": "mc5447#@T"
    }
    response = client.post('/user/login', data=json.dumps(user), headers=headers)
    token = response.json['token']
    headers['Authorization'] = f"Bearer {token}"
    response = client.get(f"{url}?id=4", headers=headers)

    assert response.json['error'] == "You don't have permission on this functionality."
    assert response.status_code == 403


def test_get_item_by_id_success(client, logged_in_client):

    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    headers['Authorization'] = f"Bearer {logged_in_client}"
    qparam = 'mouse'
    response = client.get(f"{url}?name={qparam}", headers=headers)
    items_list = response.json
    check_all_names = all([qparam in item['title'].lower() for item in items_list])
    keys = ['id', 'product_category_id', 'user_id', 'title', 'product_code']
    check_keys = []
    for item in items_list:
        for key in keys:
            check_keys.append(key in item)
    all_keys_confirm = all(check_keys)

    assert check_all_names
    assert all_keys_confirm
    assert response.status_code == 200
   

def test_get_item_by_id_not_found(client, logged_in_client):
    
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    headers['Authorization'] = f"Bearer {logged_in_client}"
    response = client.get(f"{url}?id=505050", headers=headers)
    
    assert response.json['error'] == "Item not found."
    assert response.status_code == 404


def test_get_item_by_id_invalid_qparam(client, logged_in_client):
    
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    headers['Authorization'] = f"Bearer {logged_in_client}"
    response = client.get(f"{url}?id=mouse", headers=headers)
    
    assert response.status_code == 204


