from src.app.models.user import User
from flask import json

mimetype = 'application/json'
url = "/user/create"

def test_create_user_succes(client, logged_in_client):

    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    headers['Authorization'] = f"Bearer {logged_in_client}"

    user = {
        "name": "Marcelo Coelho",
        "email": "mcoelho2011@hotmail.com",
        "password": "mc5447#@T"
    }

    response = client.post(url, data=json.dumps(user), headers=headers)
    print(response)
    assert response.status_code == 201