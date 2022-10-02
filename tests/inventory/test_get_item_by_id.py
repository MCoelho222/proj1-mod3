from flask import json
from src.app.models.inventory import Inventory
from src.app.services.queries_services import queries


mimetype = 'application/json'
url = "/inventory/item/"


def test_get_item_by_id_no_auth(client):
    """
    1. GET item with invalid token;
    2. Check status 403 and error message.
    """

    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    headers['Authorization'] = f"Bearer {''}"
    response = client.get(f"{url}4", headers=headers)

    assert response.json['error'] == "Invalid token."
    assert response.status_code == 403


def test_get_items_by_id_no_permission(client, logged_in_client):
    """
    1. POST user without role_id (no permission);
    2. Login;
    3. Try GET item;
    4. Check status 403 and error message.
    """

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
    response = client.get(f"{url}4", headers=headers)

    assert response.json['error'] == "You don't have permission on this functionality."
    assert response.status_code == 403


def test_get_item_by_id_success(client, logged_in_client):
    """
    1. Login;
    2. GET item;
    3. Check if response has all required keys;
    4. Check status 200.
    """

    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    headers['Authorization'] = f"Bearer {logged_in_client}"
    data = {
        "product_category_id": 2,
        "product_code": 12345678,
        "title": "Tablet", 
        "value": 2555.50, 
        "brand": "Apple", 
        "template": "TEX FOX 2000", 
        "description": "Produto novo, comprado em 2022." 
    }
    response = client.post('inventory/create', data=json.dumps(data), headers=headers)

    prod = Inventory.query.filter_by(product_code=data['product_code']).first()
    prod_id = prod.id
   
    response = client.get(f"{url}{prod_id}", headers=headers)
    item = response.json
    print(item.keys())
    keys = ['id', 'product_category_id', 'user_id', 'title', 'product_code']
    check_keys = []
    for key in keys:
        check_keys.append(key in item.keys())
        
    all_keys_confirm = all(check_keys)

    assert all_keys_confirm
    assert response.status_code == 200
   

def test_get_item_by_id_not_found(client, logged_in_client):
    """
    1. Login;
    2. GET item with impossible query param;
    3. Check error message and status 204.
    """

    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    headers['Authorization'] = f"Bearer {logged_in_client}"
    response = client.get(f"{url}505050", headers=headers)
    
    assert response.json['error'] == "Item not found."
    assert response.status_code == 404


