from marshmallow import Schema, fields,validate

class AISchema(Schema):
    query = fields.String(required=True,validate=validate.Length(max=1000))
