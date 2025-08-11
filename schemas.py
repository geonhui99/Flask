# schemas.py
from marshmallow import Schema, fields

class BookBase(Schema):
    title = fields.String(required=True)
    author = fields.String(required=True)

class BookSchema(BookBase):
    id = fields.Int(dump_only=True)

# (선택) PATCH용: 부분 업데이트에서 모든 필드를 선택적으로
class BookUpdateSchema(Schema):
    title = fields.String()
    author = fields.String()
