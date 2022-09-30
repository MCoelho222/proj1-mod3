from marshmallow import Schema, fields, ValidationError, validates
from src.app.utils.error_messages import handle_error_messages


def validate_password(password):
    if len(password) < 8 or password.isalnum():
        raise ValidationError('Your password must have more 8 characters or more, and at least 1 special character.')


class LoginBodySchema(Schema):
    email = fields.Email(required=True, error_messages=handle_error_messages('email'))
    password = fields.Str(required=True, error_messages=handle_error_messages('password'))

    @validates('password')
    def validate(self, password):
        validate_password(password)


class CreateUserBodySchema(Schema):
    city_id = fields.Integer()
    gender_id = fields.Integer()
    role_id = fields.Integer()
    name = fields.Str(required=True, error_messages=handle_error_messages('name'))
    age = fields.Date(required=False, error_messages=handle_error_messages('age'))
    email = fields.Email(required=True, error_messages=handle_error_messages('email'))
    phone = fields.Str(required=False, error_messages=handle_error_messages('phone'))
    password = fields.Str(required=True, error_messages=handle_error_messages('password'))
    cep = fields.Str(required=False, error_messages=handle_error_messages('cep'))
    street = fields.Str(required=False, error_messages=handle_error_messages('street'))
    number_street = fields.Str(required=False, error_messages=handle_error_messages('number_street'))
    district = fields.Str(required=False, error_messages=handle_error_messages('district'))
    complement = fields.Str()
    landmark = fields.Str()

    @validates('password')
    def validate(self, password):
        validate_password(password)

    @validates('phone')
    def validate_phone(self, phone):
        if not phone.isnumeric() or len(phone) != 11:
            raise ValidationError('Invalid phone number.')

    @validates('cep')
    def validate_cep(self, cep):
        if not cep.isnumeric() or len(cep) != 8:
            raise ValidationError('Invalid CEP.')


class UpdateUserBodySchema(Schema):
    city_id = fields.Integer()
    gender_id = fields.Integer()
    role_id = fields.Integer()
    name = fields.Str(required=True, error_messages=handle_error_messages('name'))
    age = fields.Date()
    email = fields.Email(required=True, error_messages=handle_error_messages('email'))
    phone = fields.Str()
    password = fields.Str(required=True, error_messages=handle_error_messages('password'))
    cep = fields.Str()
    street = fields.Str()
    number_street = fields.Str()
    district = fields.Str()
    complement = fields.Str()
    landmark = fields.Str()

    @validates('password')
    def validate(self, password):
        validate_password(password)

    @validates('phone')
    def validate_phone(self, phone):
        if not phone.isnumeric() and len(phone) != 8:
            raise ValidationError('Invalid phone number.')

    @validates('cep')
    def validate_cep(self, cep):
        if not cep.isnumeric() and len(cep) != 8:
            raise ValidationError('Invalid CEP.')