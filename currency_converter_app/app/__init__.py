from flask import Flask
from currency_converter_app.config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Register blueprints
    from currency_converter_app.app.routes import main, info
    app.register_blueprint(main.bp)
    app.register_blueprint(info.bp)

    return app 