# app/models/product.py

class Product:
    def __init__(self, name, price, quantity, image_filename=None):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.image_filename = image_filename or "default.png"
        
    def toDBCollection(self):
        return{
            'name': self.name,
            'price': self.price,
            'quantity': self.quantity,
            'image_filename': self.image_filename
        }