from flask import Flask, jsonify, request, Response
import json
from validBookObject import *

app = Flask(__name__)

books = [
    {
        'name': 'Green Eggs and Ham',
        'price': 7.99,
        'isbn': 97803400165
    },
    {
        'name': 'The Cat In The Hat',
        'price': 6.99,
        'isbn': 97803400193
    },
    {
        'name': 'The Odyssey',
        'price': 0.01,
        'isbn': 888
    }
]

# Get /books
@app.route('/books')
def get_books():
    return jsonify({'books': books})

@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
    return_val = {}
    for book in books:
        if book["isbn"] == isbn:
            return_val = {
                'name': book["name"],
                'price': book["price"],
                'isbn': book["isbn"]
            }
    return jsonify(return_val)

# Post /books
# {
#     'name': 'BookName',
#     'price': 8.88,
#     'isbn': 123456
# }

@app.route('/books', methods=['POST'])
def add_book():
    request_data = request.get_json()
    if(validBookObject(request_data)):
        new_book = {
            "name": request_data['name'],
            "price": request_data['price'],
            "isbn": request_data['isbn']
        }
        books.insert(0, request_data)
        response = Response("", 201, mimetype='application/json')
        response.headers['Location'] = "/books/" + str(new_book['isbn'])
        return response
    else:
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
def replace_book(isbn):
    request_data = request.get_json()
    new_book = {
        'name': request_data['name'],
        'price': request_data['price'],
        'isbn': isbn
    }
    i = 0;
    for book in books:
        currentIsbn = book["isbn"]
        if currentIsbn == isbn:
            books[i] = new_book
        i += 1
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
def update_book(isbn):
    request_data = request.get_json()
    updated_book = {}
    if("name" in request_data):
        updated_book["name"] = request_data['name']
    if("price" in request_data):
        updated_book["price"] = request_data['price']
    for book in books:
        if book["isbn"] == isbn:
            book.update(updated_book)
    response = Response("", status=204)
    response.headers['Location'] = "/books/" + str(isbn)
    return response

# DELETE /books/888

@app.route('/books/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
    i = 0;
    for book in books:
        if book["isbn"] == isbn:
            books.pop(i)
            response = Response("", status=204)
            return response
        i += 1
    invalidBookObjectErrorMsg = {
        "error": "Book with the ISBN number that was provide was not found."
    }
    response = Response(json.dumps(invalidBookObjectErrorMsg), status=404, mimetype='application/json')
    return response;

app.run(port=8080)
