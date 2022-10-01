from flask import json
import time

cod = str(round(time.time() * 1000))
cod_split = cod[7:]

mimetype = 'application/json'
url = "/inventory/"


def test_create_item_no_auth(client):

    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    headers['Authorization'] = f"Bearer {''}"
    data = {
        "product_category_id": 1,
        "product_code": cod_split,
        "title": "Tablet", 
        "value": 2555.50, 
        "brand": "Apple", 
        "template": "TEX FOX 2000", 
        "description": "Produto novo, comprado em 2022." 
    }
    response = client.post(f'{url}create', data=json.dumps(data), headers=headers)

    assert response.json["error"] == "Invalid token."
    assert response.status_code == 403


def test_create_item_no_permission(client, logged_in_client):

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
        "product_category_id": 1,
        "product_code": cod_split,
        "title": "Super Mouse", 
        "value": 546.50, 
        "brand": "Axterix", 
        "template": "5RTH7", 
        "description": "Mouse preto, perfeito estado, sem pilha."
    }
    response = client.post(f'{url}create', data=json.dumps(data), headers=headers)

    assert response.json['error'] == "You don't have permission on this functionality."
    assert response.status_code == 403


def test_create_item_success(client, logged_in_client):

    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    headers['Authorization'] = f"Bearer {logged_in_client}"
    data = {
        "product_category_id": 2,
        "product_code": cod_split,
        "title": "Tablet", 
        "value": 2555.50, 
        "brand": "Apple", 
        "template": "TEX FOX 2000", 
        "description": "Produto novo, comprado em 2022." 
    }
    response = client.post(f'{url}create', data=json.dumps(data), headers=headers)

    assert response.json["message"] == "Item successfully registered."
    assert response.status_code == 201


def test_create_item_missing_field(client, logged_in_client):

    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    headers['Authorization'] = f"Bearer {logged_in_client}"
    data = {
        "product_category_id": 1,
        "title": "Tablet", 
        "value": 2555.50, 
        "brand": "Apple", 
        "template": "TEX FOX 2000", 
        "description": "Produto novo, comprado em 2022." 
    }
    response = client.post(f'{url}create', data=json.dumps(data), headers=headers)

    assert response.json["product_code"] == ["The field product_code is required."]
    assert response.status_code == 400


def test_create_item_invalid_field(client, logged_in_client):

    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    headers['Authorization'] = f"Bearer {logged_in_client}"
    data = {
        "product_category_id": 1,
        "product_code": "12345ABC",
        "title": "Tablet", 
        "value": -2555.50, 
        "brand": "", 
        "template": "TEX FOX 2000", 
        "description": "Produto novo, comprado em 2022." 
    }
    response = client.post(f'{url}create', data=json.dumps(data), headers=headers)

    assert response.json["product_code"] == ["Invalid product_code."]
    assert response.json["value"] == ["Value must be higher than zero."]
    assert response.json["brand"] == ["Brand field cannot be empty."]
    assert response.status_code == 400


def test_create_item_short_prod_code(client, logged_in_client):

    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    headers['Authorization'] = f"Bearer {logged_in_client}"
    data = {
        "product_category_id": 2,
        "product_code": "123456789",
        "title": "Tablet", 
        "value": 2555.50, 
        "brand": "TexMax", 
        "template": "TEX FOX 2000", 
        "description": "Produto novo, comprado em 2022." 
    }
    response = client.post(f'{url}create', data=json.dumps(data), headers=headers)

    assert response.json["product_code"] == ["Product code must have from 1 to maximum 8 characters and must be positive."]
    assert response.status_code == 400


def test_create_item_negative_prod_code(client, logged_in_client):

    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    headers['Authorization'] = f"Bearer {logged_in_client}"
    data = {
        "product_category_id": 2,
        "product_code": -123456,
        "title": "Tablet", 
        "value": 2555.50, 
        "brand": "TexMax", 
        "template": "TEX FOX 2000", 
        "description": "Produto novo, comprado em 2022." 
    }
    response = client.post(f'{url}create', data=json.dumps(data), headers=headers)

    assert response.json["product_code"] == ["Product code must have from 1 to maximum 8 characters and must be positive."]
    assert response.status_code == 400


def test_create_item_prod_code_exists(client, logged_in_client):

    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    headers['Authorization'] = f"Bearer {logged_in_client}"
    prod1 = {
        "product_category_id": 2,
        "product_code": 12345678,
        "title": "Tablet", 
        "value": 2555.50, 
        "brand": "Apple", 
        "template": "TEX FOX 2000", 
        "description": "Produto novo, comprado em 2022." 
    }
    response = client.post(f'{url}create', data=json.dumps(prod1), headers=headers)
    prod2 = {
        "product_category_id": 3,
        "product_code": 12345678,
        "title": "Cadeira gamer", 
        "value": 1800.50, 
        "brand": "Asus", 
        "template": "F5GH78", 
        "description": "Cadeira preta, 4 rodinhas." 
    }
    response = client.post(f'{url}create', data=json.dumps(prod2), headers=headers)

    assert response.json["error"] == "Product code already exists."
    assert response.status_code == 400