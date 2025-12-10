from flask import Flask
import os
# Constante de tamaño máximo de imagen en bytes
MAX_IMAGE_SIZE = 6 * 1024 * 1024  # 6 MB

def create_app():
    app = Flask(__name__)
    # app.config.from_object('config')
    
    # Configuracion para subir imagenes
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = MAX_IMAGE_SIZE
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    from .routes.product_routes import product_bp
    app.register_blueprint(product_bp)
    return app
