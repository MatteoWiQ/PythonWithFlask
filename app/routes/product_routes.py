# app/routes/product_routes.py

from flask import Blueprint, render_template, request, jsonify, redirect, url_for, current_app
from werkzeug.utils import secure_filename
import os
import uuid
from app.database.database import dbConnection
from app.models.product import Product

ALLOWED_EXTS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return ('.' in filename) and (filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTS)

def unique_filename(filename):
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    base = uuid.uuid4().hex
    return f"{base}.{ext}" if ext else base


product_bp = Blueprint('product', __name__)
db = dbConnection()

@product_bp.route('/')
def index():
    products = db['products']
    productsReceived = products.find()
    return render_template('index.html', products=productsReceived)


@product_bp.route('/products', methods=['POST'])
def addProduct():
    products = db['products']
    name = request.form['name']
    price = request.form['price']
    quantity = request.form['quantity']

    # Manejo de imagen
    image_file = request.files.get('image')  # <input type="file" name="image">
    image_filename = None

    if image_file and image_file.filename:
        if allowed_file(image_file.filename):
            secure_name = secure_filename(image_file.filename)
            image_filename = unique_filename(secure_name)
            save_path = os.path.join(current_app.root_path, 'static/uploads', image_filename)
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            image_file.save(save_path)

    if name and price and quantity:
        product = Product(name, price, quantity, image_filename=image_filename)
        products.insert_one(product.toDBCollection())
        return redirect(url_for('product.index'))
    else:
        return notFound()


@product_bp.route('/edit/<string:product_name>', methods=['POST'])
def edit(product_name):
    products = db['products']
    name = request.form['name']
    price = request.form['price']
    quantity = request.form['quantity']

    if name and price and quantity:
        products.update_one({'name': product_name}, {'$set': {'name': name, 'price': price, 'quantity': quantity}})
        return redirect(url_for('product.index'))
    else:
        return notFound()


@product_bp.route('/delete/<string:product_name>')
def delete(product_name):
    products = db['products']
    doc = products.find_one({'name': product_name})
    if doc:
        # Borrar imagen del servidor si existe
        image_filename = doc.get('image_filename')
        if image_filename:
            path = os.path.join(current_app.root_path, 'static/uploads', image_filename)
            if os.path.exists(path):
                os.remove(path)
        products.delete_one({'name': product_name})
    return redirect(url_for('product.index'))

@product_bp.errorhandler(404)
def notFound(error=None):
    message = {
        'message': 'No encontrado ' + request.url,
        'status': '404 Not Found'
    }
    response = jsonify(message)
    response.status_code = 404
    return response
