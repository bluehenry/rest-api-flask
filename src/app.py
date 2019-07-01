from flask import Flask, jsonify, request
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
        return "True"
    else:
        return "False"

app.run(port=8080)
