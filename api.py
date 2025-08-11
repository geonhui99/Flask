# api.py
from flask import url_for, make_response
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import BookSchema, BookBase, BookUpdateSchema

book_blp = Blueprint('books', 'books', url_prefix='/books', description='Operations on books')

# ---- In-memory store ----
_books = []
_next_id = 1

def _find(book_id):
    return next((b for b in _books if b['id'] == book_id), None)

def _create(data):
    global _next_id
    book = {"id": _next_id, **data}
    _books.append(book)
    _next_id += 1
    return book

def _replace(book, data):   # PUT: 전면 교체
    book.clear()
    book.update(data)

def _patch(book, data):     # PATCH: 부분 업데이트
    book.update(data)

def _delete(book_id):
    idx = next((i for i, b in enumerate(_books) if b['id'] == book_id), None)
    if idx is None:
        return False
    _books.pop(idx)
    return True

@book_blp.route('/')
class BookList(MethodView):
    @book_blp.response(200, BookSchema(many=True))
    def get(self):
        return _books

    @book_blp.arguments(BookBase)          # 입력 검증
    @book_blp.response(201, BookSchema)
    def post(self, new_data):
        created = _create(new_data)
        resp = make_response(created, 201)
        resp.headers['Location'] = url_for('books.Book', book_id=created['id'])
        return resp

@book_blp.route('/<int:book_id>')
class Book(MethodView):
    @book_blp.response(200, BookSchema)
    def get(self, book_id):
        book = _find(book_id)
        if not book:
            abort(404, message="Book not found.")
        return book

    # PUT: 모든 필드 필수(전면 교체)
    @book_blp.arguments(BookBase)
    @book_blp.response(200, BookSchema)
    def put(self, new_data, book_id):
        book = _find(book_id)
        if not book:
            abort(404, message="Book not found.")
        _replace(book, {"id": book_id, **new_data})
        return book

    # PATCH: 부분 업데이트(선택 기능)
    @book_blp.arguments(BookUpdateSchema)
    @book_blp.response(200, BookSchema)
    def patch(self, partial_data, book_id):
        book = _find(book_id)
        if not book:
            abort(404, message="Book not found.")
        _patch(book, partial_data)
        return book

    @book_blp.response(204)
    def delete(self, book_id):
        if not _delete(book_id):
            abort(404, message="Book not found.")
        return  # 204는 바디 없음
