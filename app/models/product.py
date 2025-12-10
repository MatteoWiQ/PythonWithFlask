# app/models/product.py

from bson import ObjectId

class Product:
    def __init__(self, name, description, price, stock, category, image_filename=None):
        """
        Inicializa un producto con los campos requeridos.
        
        Args:
            name (str): Nombre del producto
            description (str): Descripción del producto
            price (float): Precio del producto
            stock (int): Stock disponible
            category (str): Categoría del producto
            image_filename (str, optional): Nombre del archivo de imagen
        """
        self.name = name
        self.description = description
        self.price = float(price)
        self.stock = int(stock)
        self.category = category
        self.image_filename = image_filename or "default.png"
        
    def toDBCollection(self):
        """Convierte el producto a diccionario para guardar en MongoDB."""
        return {
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'stock': self.stock,
            'category': self.category,
            'image_filename': self.image_filename
        }
    
    @staticmethod
    def from_db(doc):
        """Crea un objeto Product desde un documento de MongoDB."""
        if not doc:
            return None
        
        product = Product(
            name=doc.get('name', ''),
            description=doc.get('description', ''),
            price=doc.get('price', 0.0),
            stock=doc.get('stock', 0),
            category=doc.get('category', ''),
            image_filename=doc.get('image_filename', 'default.png')
        )
        product._id = doc.get('_id')
        return product