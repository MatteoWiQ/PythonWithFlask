from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from app.database.database import dbConnection
from app.models.product import Product

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

    if name and price and quantity:
        product = Product(name, price, quantity)
        products.insert_one(product.toDBCollection())
        return redirect(url_for('product.index'))
    else:
        return notFound()

@product_bp.route('/delete/<string:product_name>')
def delete(product_name):
    products = db['products']
    products.delete_one({'name': product_name})
    return redirect(url_for('product.index'))

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

@product_bp.errorhandler(404)
def notFound(error=None):
    message = {
        'message': 'No encontrado ' + request.url,
        'status': '404 Not Found'
    }
    response = jsonify(message)
    response.status_code = 404
    return response
