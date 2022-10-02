from flask import json
from src.app.models.inventory import Inventory
import time


cod = str(round(time.time() * 1000))
cod_split = cod[7:]

mimetype = 'application/json'
url = "/inventory/update/"


def test_update_item_no_auth(client, logged_in_client):

    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    headers['Authorization'] = f"Bearer {logged_in_client}"
    data = {
        "product_category_id": 1,
        "product_code": 12345678,
        "title": "Tablet", 
        "value": 2555.50, 
        "brand": "Apple", 
        "template": "TEX FOX 2000", 
        "description": "Produto novo, comprado em 2022." 
    }
    response = client.post('inventory/create', data=json.dumps(data), headers=headers)
    prod = Inventory.query.filter_by(product_code=data['product_code']).first_or_404()
    prod_id = prod.id
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    headers['Authorization'] = f"Bearer {''}"
    data = {
        "product_category_id": 1,
        "product_code": 12345678,
        "title": "Tablet Smart", 
        "value": 2555.50, 
        "brand": "Apple", 
        "template": "TEX FOX 2000", 
        "description": "Produto novo, comprado em 2022." 
    }
    response = client.patch(f'{url}{prod_id}', data=json.dumps(data), headers=headers)

    assert response.json["error"] == "Invalid token."
    assert response.status_code == 403


def test_update_item_no_permission(client, logged_in_client):

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
    data = {
        "product_category_id": 2,
        "product_code": 6789,
        "title": "Tablet", 
        "value": 2555.50, 
        "brand": "Apple", 
        "template": "TEX FOX 2000", 
        "description": "Produto novo, comprado em 2022." 
    }
    response = client.post('inventory/create', data=json.dumps(data), headers=headers)
    prod = Inventory.query.filter_by(product_code=data['product_code']).first_or_404()
    prod_id = prod.id
    data = {
        "title": "Tablet Smart", 
        "value": 2555.50, 
        "brand": "Apple", 
        "template": "TEX FOX 2000", 
        "description": "Produto novo, comprado em 2022." 
    }
    response = client.patch(f'{url}{prod_id}', data=json.dumps(data), headers=headers)

    assert response.json['error'] == "You don't have permission on this functionality."
    assert response.status_code == 403

def test_update_item_success(client, logged_in_client):

    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    headers['Authorization'] = f"Bearer {logged_in_client}"
    data = {
        "product_category_id": 2,
        "product_code": 6789,
        "title": "Tablet", 
        "value": 2555.50, 
        "brand": "Apple", 
        "template": "TEX FOX 2000", 
        "description": "Produto novo, comprado em 2022." 
    }
    response = client.post('inventory/create', data=json.dumps(data), headers=headers)
    prod = Inventory.query.filter_by(product_code=data['product_code']).first_or_404()
    prod_id = prod.id
    data = {
        "title": "Tablet Smart", 
        "value": 2555.50, 
        "brand": "Apple", 
        "template": "TEX FOX 2000", 
        "description": "Produto novo, comprado em 2022." 
    }
    response = client.patch(f'{url}{prod_id}', data=json.dumps(data), headers=headers)
    
    assert response.status_code == 204


def test_update_item_invalid_field(client, logged_in_client):

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
    prod = Inventory.query.filter_by(product_code=data['product_code']).first_or_404()
    prod_id = prod.id
    data = {
        "title": "", 
        "value": -2555.50, 
        "brand": "", 
        "template": "", 
        "description": "" 
    }
    response = client.patch(f'{url}{prod_id}', data=json.dumps(data), headers=headers)

    assert response.json['value'] == ["Value must be higher than zero."]
    assert response.json['title'] == ["Title field cannot be empty."]
    assert response.json['brand'] == ["Brand field cannot be empty."]
    assert response.json['template'] == ["Template field cannot be empty."]
    assert response.json['description'] == ["Description field cannot be empty."]
    assert response.status_code == 400


def test_update_item_missing_field(client, logged_in_client):

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
    prod = Inventory.query.filter_by(product_code=data['product_code']).first_or_404()
    prod_id = prod.id
    data = {
        
        "value": 2555.50, 
        "brand": "Apple", 
        "template": "TEX FOX 2000", 
        "description": "Produto novo, comprado em 2022." 
    }
    response = client.patch(f'{url}{prod_id}', data=json.dumps(data), headers=headers)
    
    assert response.status_code == 204


def test_update_item_forbidden_fields(client, logged_in_client):

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
    prod = Inventory.query.filter_by(product_code=data['product_code']).first_or_404()
    prod_id = prod.id
    data = {
        "product_category_id": 2,
        "product_code": 12345678,
        "value": 2555.50, 
        "brand": "Apple", 
        "template": "TEX FOX 2000", 
        "description": "Produto novo, comprado em 2022." 
    }
    response = client.patch(f'{url}{prod_id}', data=json.dumps(data), headers=headers)
    
    assert response.json['product_category_id'] == ["Unknown field."]
    assert response.json['product_code'] == ["Unknown field."]
    assert response.status_code == 400