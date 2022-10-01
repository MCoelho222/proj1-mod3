from marshmallow import Schema, fields, ValidationError, validates
from src.app.utils.error_messages import handle_error_messages

class CreateRoleBodySchema(Schema):
    
    name = fields.Str(required=True, error_messages=handle_error_messages('name'))
    description = fields.Str(required=True, error_messages=handle_error_messages('description'))
    permissions = fields.List(fields.Integer(), required=True, error_messages=handle_error_messages('permissions'))

    @validates('name')
    def validate_name(self, name):
        if len(name) == 0:
            raise ValidationError('The field name cannot be empty.')

    @validates('description')
    def validate_description(self, description):
        if len(description) == 0:
            raise ValidationError('The field description cannot be empty.')

    @validates('permissions')
    def validate_permissions(self, permissions):
        if len(permissions) == 0:
            raise ValidationError('The field permissions cannot be empty.')