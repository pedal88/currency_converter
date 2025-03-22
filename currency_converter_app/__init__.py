from flask import Flask
from currency_converter_app.config import Config
import os

def create_app(config_class=Config):
    # Try both absolute and relative paths
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'app', 'templates'))
    relative_template_dir = 'app/templates'
    
    print(f"Absolute template directory path: {template_dir}")  # Debug log
    print(f"Relative template directory path: {relative_template_dir}")  # Debug log
    print(f"Current working directory: {os.getcwd()}")  # Debug log
    print(f"Directory exists (absolute): {os.path.exists(template_dir)}")  # Debug log
    print(f"Directory exists (relative): {os.path.exists(relative_template_dir)}")  # Debug log
    
    # Try using relative path instead
    app = Flask(__name__, template_folder=relative_template_dir)
    app.config.from_object(config_class)

    # Register blueprints
    from currency_converter_app.app.routes.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app 