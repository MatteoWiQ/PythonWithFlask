# app/routes/product_routes.py

from flask import Blueprint, render_template, request, redirect, url_for, current_app, flash
from werkzeug.utils import secure_filename
from bson import ObjectId
import os
import uuid
from app.database.database import dbConnection
from app.models.product import Product

ALLOWED_EXTS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    """Verifica si el archivo tiene extensión permitida."""
    return ('.' in filename) and (filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTS)

def unique_filename(filename):
    """Genera un nombre único para el archivo."""
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    base = uuid.uuid4().hex
    return f"{base}.{ext}" if ext else base

def save_product_image(image_file):
    """Guarda la imagen del producto y retorna el nombre del archivo."""
    if not image_file or not image_file.filename:
        return None
    
    if not allowed_file(image_file.filename):
        return None
    
    secure_name = secure_filename(image_file.filename)
    image_filename = unique_filename(secure_name)
    save_path = os.path.join(current_app.root_path, 'static/uploads', image_filename)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    image_file.save(save_path)
    return image_filename

def delete_product_image(image_filename):
    """Elimina la imagen del servidor si existe."""
    if not image_filename or image_filename == 'default.png':
        return
    path = os.path.join(current_app.root_path, 'static/uploads', image_filename)
    if os.path.exists(path):
        try:
            os.remove(path)
        except Exception as e:
            print(f"Error al eliminar imagen: {e}")

product_bp = Blueprint('product', __name__, url_prefix='/products')
db = dbConnection()

# ============ LISTAR PRODUCTOS ============
@product_bp.route('/', methods=['GET'])
def index():
    """Lista todos los productos con filtros opcionales."""
    products_collection = db['products']
    
    # Obtener parámetros de filtro
    search = request.args.get('search', '').strip()
    category = request.args.get('category', '').strip()
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    
    # Construir filtro
    filters = {}
    
    if search:
        filters['name'] = {'$regex': search, '$options': 'i'}  # Case-insensitive
    
    if category:
        filters['category'] = {'$regex': category, '$options': 'i'}
    
    if min_price is not None or max_price is not None:
        filters['price'] = {}
        if min_price is not None:
            filters['price']['$gte'] = min_price
        if max_price is not None:
            filters['price']['$lte'] = max_price
    
    # Ejecutar búsqueda
    products = list(products_collection.find(filters))
    
    return render_template('products/index.html', 
                         products=products,
                         search=search,
                         category=category,
                         min_price=min_price,
                         max_price=max_price)

# ============ CREAR PRODUCTO - GET (FORMULARIO) ============
@product_bp.route('/new', methods=['GET'])
def create_get():
    """Muestra el formulario para crear un nuevo producto."""
    return render_template('products/create.html')

# ============ CREAR PRODUCTO - POST (GUARDAR) ============
@product_bp.route('/', methods=['POST'])
def create():
    """Crea un nuevo producto."""
    try:
        # Obtener datos del formulario
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        price = request.form.get('price', type=float)
        stock = request.form.get('stock', type=int)
        category = request.form.get('category', '').strip()
        
        # Validaciones
        if not name or not category or price is None or stock is None:
            flash('Todos los campos son requeridos', 'danger')
            return render_template('products/create.html', form_data=request.form)
        
        if price < 0:
            flash('El precio no puede ser negativo', 'danger')
            return render_template('products/create.html', form_data=request.form)
        
        if stock < 0:
            flash('El stock no puede ser negativo', 'danger')
            return render_template('products/create.html', form_data=request.form)
        
        # Procesar imagen
        image_filename = None
        if 'image' in request.files:
            image_filename = save_product_image(request.files['image'])
        
        # Crear producto
        product = Product(name, description, price, stock, category, image_filename)
        
        # Guardar en BD
        products_collection = db['products']
        result = products_collection.insert_one(product.toDBCollection())
        
        flash(f'Producto "{name}" creado exitosamente', 'success')
        return redirect(url_for('product.index'))
        
    except Exception as e:
        flash(f'Error al crear producto: {str(e)}', 'danger')
        return render_template('products/create.html', form_data=request.form)

# ============ VER DETALLE DEL PRODUCTO ============
@product_bp.route('/<product_id>', methods=['GET'])
def detail(product_id):
    """Muestra los detalles de un producto."""
    try:
        products_collection = db['products']
        product = products_collection.find_one({'_id': ObjectId(product_id)})
        
        if not product:
            flash('Producto no encontrado', 'warning')
            return redirect(url_for('product.index'))
        
        return render_template('products/detail.html', product=product)
        
    except Exception as e:
        flash(f'Error al obtener producto: {str(e)}', 'danger')
        return redirect(url_for('product.index'))

# ============ EDITAR PRODUCTO - GET (FORMULARIO) ============
@product_bp.route('/<product_id>/edit', methods=['GET'])
def edit_get(product_id):
    """Muestra el formulario para editar un producto."""
    try:
        products_collection = db['products']
        product = products_collection.find_one({'_id': ObjectId(product_id)})
        
        if not product:
            flash('Producto no encontrado', 'warning')
            return redirect(url_for('product.index'))
        
        return render_template('products/edit.html', product=product)
        
    except Exception as e:
        flash(f'Error al obtener producto: {str(e)}', 'danger')
        return redirect(url_for('product.index'))

# ============ EDITAR PRODUCTO - POST (ACTUALIZAR) ============
@product_bp.route('/<product_id>/edit', methods=['POST'])
def edit(product_id):
    """Actualiza un producto existente."""
    try:
        products_collection = db['products']
        product = products_collection.find_one({'_id': ObjectId(product_id)})
        
        if not product:
            flash('Producto no encontrado', 'warning')
            return redirect(url_for('product.index'))
        
        # Obtener datos del formulario
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        price = request.form.get('price', type=float)
        stock = request.form.get('stock', type=int)
        category = request.form.get('category', '').strip()
        
        # Validaciones
        if not name or not category or price is None or stock is None:
            flash('Todos los campos son requeridos', 'danger')
            # Merge original product with form data to preserve ID but show user inputs
            product.update({'name': name, 'description': description, 'price': price, 'stock': stock, 'category': category})
            return render_template('products/edit.html', product=product)
        
        if price < 0:
            flash('El precio no puede ser negativo', 'danger')
            product.update({'name': name, 'description': description, 'price': price, 'stock': stock, 'category': category})
            return render_template('products/edit.html', product=product)
        
        if stock < 0:
            flash('El stock no puede ser negativo', 'danger')
            product.update({'name': name, 'description': description, 'price': price, 'stock': stock, 'category': category})
            return render_template('products/edit.html', product=product)
        
        # Procesar imagen (si se carga una nueva)
        image_filename = product.get('image_filename', 'default.png')
        if 'image' in request.files and request.files['image'].filename:
            # Eliminar imagen antigua si existe
            delete_product_image(product.get('image_filename'))
            new_filename = save_product_image(request.files['image'])
            if new_filename:
                image_filename = new_filename
        
        # Actualizar en BD
        update_data = {
            'name': name,
            'description': description,
            'price': price,
            'stock': stock,
            'category': category,
            'image_filename': image_filename
        }
        
        products_collection.update_one(
            {'_id': ObjectId(product_id)},
            {'$set': update_data}
        )
        
        flash(f'Producto "{name}" actualizado exitosamente', 'success')
        return redirect(url_for('product.detail', product_id=product_id))
        
    except Exception as e:
        flash(f'Error al actualizar producto: {str(e)}', 'danger')
        # Try to preserve inputs if possible, though product might be stale
        return render_template('products/edit.html', product=product)

# ============ ELIMINAR PRODUCTO - GET (CONFIRMACIÓN) ============
@product_bp.route('/<product_id>/delete', methods=['GET'])
def delete_get(product_id):
    """Muestra la página de confirmación para eliminar."""
    try:
        products_collection = db['products']
        product = products_collection.find_one({'_id': ObjectId(product_id)})
        
        if not product:
            flash('Producto no encontrado', 'warning')
            return redirect(url_for('product.index'))
        
        return render_template('products/delete.html', product=product)
        
    except Exception as e:
        flash(f'Error al obtener producto: {str(e)}', 'danger')
        return redirect(url_for('product.index'))

# ============ ELIMINAR PRODUCTO - POST (EJECUTAR) ============
@product_bp.route('/<product_id>/delete', methods=['POST'])
def delete(product_id):
    """Elimina un producto."""
    try:
        products_collection = db['products']
        product = products_collection.find_one({'_id': ObjectId(product_id)})
        
        if not product:
            flash('Producto no encontrado', 'warning')
            return redirect(url_for('product.index'))
        
        # Eliminar imagen asociada
        image_filename = product.get('image_filename')
        if image_filename:
            delete_product_image(image_filename)
        
        # Eliminar producto de BD
        products_collection.delete_one({'_id': ObjectId(product_id)})
        
        flash(f'Producto "{product.get("name")}" eliminado exitosamente', 'success')
        return redirect(url_for('product.index'))
        
    except Exception as e:
        flash(f'Error al eliminar producto: {str(e)}', 'danger')
        return redirect(url_for('product.index'))
