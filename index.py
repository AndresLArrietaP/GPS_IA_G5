from flask import Flask

def crear_app():
    app = Flask(__name__)
    from pdf import bp  as pdf_bp
    app.register_blueprint(pdf_bp)

    return app