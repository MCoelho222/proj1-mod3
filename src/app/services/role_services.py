from src.app.models.role import Role
from src.app.models.permission import Permission
from flask import json

def create_role(name, description, permissions):
    
    permissions_seed = Permission.query.filter(Permission.id.in_(permissions)).all()
    Role.seed(
        description=description,
        name=name,
        permissions=permissions_seed
    )
    return True