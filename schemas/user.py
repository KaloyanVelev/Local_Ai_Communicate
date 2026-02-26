from marshmallow import Schema, fields, validate

class BaseUserSchema(Schema):
    username = fields.String(required=True, validate=validate.Length(min=4, max=40))

class UserCreationSchema(BaseUserSchema):
    email = fields.Email(required=True, validate=validate.Length(min=5, max=40))
    password = fields.String(required=True, validate=validate.Length(min=5, max=255))

class UserLogInSchema(BaseUserSchema):
    password = fields.String(required=True, validate=validate.Length(min=5, max=255))