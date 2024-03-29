from flask import Flask, jsonify, request, Response
import json
import jwt, datetime

from validBookObject import *
from settings import *
from BookModel import *
from UserModel import *
from functools import wraps

app.config['SECRET_KEY'] = 'jellyfish'

books = Book.get_all_books()

DEFAULT_PAGE_LIMIT = 3

def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args.get('token')
        try:
            jwt.decode(token, app.config['SECRET_KEY'])
            return f(*args, **kwargs)
        except:
            return jsonify({'error': 'Need a valid token to view this page'}), 401
    return wrapper


# Login /login
@app.route('/login', methods=['POST'])
def get_token():
    request_data = request.get_json()

    username = str(request_data['username'])
    password = str(request_data['password'])

    match = User.username_password_match(username, password)
    if match:
        expiration_date = datetime.datetime.utcnow() + datetime.timedelta(days=1)
        token = jwt.encode({'exp': expiration_date}, app.config['SECRET_KEY'], algorithm='HS256')
        return token
    else:
        return Response('', 401, mimetype='application/json')


# Get /books?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9
@app.route('/books')
@token_required
def get_books():
    return jsonify({'books': Book.get_all_books()})

@app.route('/books/<int:isbn>')
@token_required
def get_book_by_isbn(isbn):
    return_value = Book.get_book(isbn)
    return jsonify(return_value)

# GET /books/page/<int:page_number>
# /books/page/1?limit=100
@token_required
@app.route('/books/page/<int:page_number>')
def get_paginated_books(page_number):
    print(type(request.args.get('limit')))
    LIMIT = request.args.get('limit', DEFAULT_PAGE_LIMIT, int)
    startIndex = page_number * LIMIT - LIMIT
    endIndex = page_number * LIMIT
    print(startIndex)
    print(endIndex)
    return jsonify({'books': books[startIndex:endIndex]})


# Post /books
# {
#     'name': 'BookName',
#     'price': 8.88,
#     'isbn': 123456
# }
@app.route('/books', methods=['POST'])
@token_required
def add_book():
    request_data = request.get_json()
    if(validBookObject(request_data)):
        Book.add_book(request_data['name'], request_data['price'], request_data['isbn'])
        response = Response("", 201, mimetype='application/json')
        response.headers['Location'] = "/books/" + str(request_data['isbn'])
        return response

        invalidBookObjectErrorMsg = {
            "error": "Invalid book object passed in request",
            "helpString": "Data passed in similar to this {'name': 'bookname', 'price': 7.99, 'isbn': 123456}"
        }
        response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')
        return response

# PUT /books/888
# {
#   'name': 'The Odyssey'
#   'price': 9.99
# }
# (1) no valid book object from our client
#     -> not add the book to the store
# valid book object has name and price field
@app.route('/books/<int:isbn>', methods=['PUT'])
@token_required
def replace_book(isbn):
    request_data = request.get_json()
    if(not validBookObject(request_data)):
        invalidBookObjectErrorMsg = {
            "error": "Invalid book object passed in request",
            "helpString": "Data should be passed in simlar to this {'name': 'bookname', 'price': 7.99, 'isbn': 123456}"
        }
        response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')

    Book.replace_book(isbn, request_data['name'], request_data['price'])
    response = Response("", status=204)
    return response


# PATH /books/888
# {
#     'name': 'Harry Potter and the Chamber of Secrets'
# }

# PATH /books/888
# {
#     'price': 39.99
# }
@app.route('/books/<int:isbn>', methods=['PATCH'])
@token_required
def update_book(isbn):
    request_data = request.get_json()
    if(not validBookObject(request_data)):
        invalidBookObjectErrorMsg = {
            "error": "Invalid book object passed in request",
            "helpString": "Data should be passed in simlar to this {'name': 'bookname', 'price': 7.99, 'isbn': 123456}"
        }
        response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')

    if("name" in request_data):
        Book.update_book_name(isbn, request_data['name'])
    if("price" in request_data):
        Book.update_book_price(isbn, request_data['price'])

    response = Response("", status=204)
    response.headers['Location'] = "/books/" + str(isbn)
    return response

# DELETE /books/888
@app.route('/books/<int:isbn>', methods=['DELETE'])
@token_required
def delete_book(isbn):
    if(Book.delete_book(isbn)):
        response = Response("", status=204)
        return response

    invalidBookObjectErrorMsg = {
        "error": "Book with the ISBN number that was provide was not found."
    }
    response = Response(json.dumps(invalidBookObjectErrorMsg), status=404, mimetype='application/json')
    return response;

app.run(port=8080)
