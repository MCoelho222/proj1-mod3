
from flask import json
from src.app.services.queries_services import queries
from src.app.models.inventory import Inventory

mimetype = 'application/json'
url = "/inventory/"


def test_get_item_results_no_auth(client):

    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    token = ''
    headers['Authorization'] = f"Bearer {token}"

    response = client.get(f"{url}results", headers=headers)

    assert response.json['error'] == "Invalid token."
    assert response.status_code == 403

def test_get_item_results_no_permission(client, logged_in_client):
    
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

    response = client.get(f"{url}results", headers=headers)
    
    assert response.json['error'] == "You don't have permission on this functionality."
    assert response.status_code == 403

def test_get_item_results_success(client, logged_in_client):
    
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    headers['Authorization'] = f"Bearer {logged_in_client}"
    
    response = client.get(f"{url}results", headers=headers)
    
    users_db_data = queries(model='user', type_request='all')
    inventory_db_data = queries(model='inventory', type_request='all', schema='inventories')

    total_items_price = 0
    total_items_loaned = 0
    for item in inventory_db_data:
        if item['user_id'] != None:
            total_items_loaned += 1
        if item['value'] > 0 and item['value'] != None:
            total_items_price += item['value']

    return_dados = {
        'total_items': len(inventory_db_data),
        'total_users': len(users_db_data),
        'total_items_loaned': total_items_loaned,
        'total_items_price': round(total_items_price, 2)
        }
    
    assert response.json['total_items'] == return_dados['total_items']
    assert response.json['total_users'] == return_dados['total_users']
    assert response.json['total_items_loaned'] == return_dados['total_items_loaned']
    assert response.json['total_items_price'] == return_dados['total_items_price']
    assert response.status_code == 200


def test_get_item_results_empty_db(client, logged_in_client):
    
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    headers['Authorization'] = f"Bearer {logged_in_client}"
    Inventory.query.delete()
    response = client.get(f"{url}results", headers=headers)
    
    assert response.json['total_items'] == 0
    assert response.json['total_items_loaned'] == 0
    assert response.json['total_items_price'] == 0.00
    assert response.status_code == 200
