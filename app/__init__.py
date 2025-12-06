from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    from .routes.product_routes import product_bp
    app.register_blueprint(product_bp)
    return app
