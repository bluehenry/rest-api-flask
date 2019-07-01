def validBookObject(bookObject):
    if ("name" in bookObject
            and "price" in bookObject
            and "isbn" in bookObject):
        return True
    else:
        return False
