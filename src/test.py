# exec(open("./valid-book-object.py").read())
from validBookObject import *

valid_object = {
    'name': 'BookName',
    'price': 5.66,
    'isbn': 12345678
}

missing_name = {
    'price': 5.66,
    'isbn': 12345678
}

missing_price  = {
    'name': 'BookName',
    'isbn': 12345678
}

missing_isbn = {
    'name': 'BookName',
    'price': 5.66
}

empty_dictionary = {}

if validBookObject(valid_object) == True:
    print("validBookObject(valid_object) passed")
else:
    print("validBookObject(valid_object) failed")

if validBookObject(missing_name) == False:
    print("validBookObject(missing_name) passed")
else:
    print("validBookObject(missing_name) failed")

if validBookObject(missing_price) == False:
    print("validBookObject(missing_price) passed")
else:
    print("validBookObject(missing_price) failed")

if validBookObject(missing_isbn) == False:
    print("validBookObject(missing_isbn) passed")
else:
    print("validBookObject(missing_isbn) failed")