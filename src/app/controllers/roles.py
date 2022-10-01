import requests
from flask import Blueprint, jsonify, request, current_app
from flask import json
from sqlalchemy.exc import IntegrityError
from flask.wrappers import Response
from werkzeug.utils import redirect
from flask.globals import session
from src.app import db
from src.app.middlewares.auth import requires_access_level
from src.app.models.permission import Permission
from src.app.utils.decorators import validate_body
from src.app.schemas.role_schema import CreateRoleBodySchema
from src.app.services.role_services import create_role

role = Blueprint('role', __name__, url_prefix='/role')

@role.route("/create", methods=['POST'])
@requires_access_level(["READ", "WRITE", "DELETE", "UPDATE"])
@validate_body(CreateRoleBodySchema())
def create_new_role(body):

    for permission in body['permissions']:
        try:
            Permission.query.filter_by(id=permission).first_or_404()
        except:
            return jsonify({'error': f"Permission {permission} does not exist."}), 400
    
    try:
        create_role(**body)
        return jsonify({'message': 'Role successfully created.'}), 201
    except:
        return jsonify({'error': 'Oops! Something went wrong...'}), 400


