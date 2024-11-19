from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import yaml

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    with open('config/app.yml', 'r') as config_file:
        config = yaml.safe_load(config_file)
    app.config['SQLALCHEMY_DATABASE_URI'] = config['database']['uri']

    db.init_app(app)

    from src.novapost.controller.parcel_controller import parcel_bp
    from src.novapost.controller.department_controller import department_bp
    from src.novapost.controller.transfer_controller import transfer_bp
    from src.novapost.controller.operator_controller import operator_bp
    app.register_blueprint(operator_bp)
    app.register_blueprint(transfer_bp)
    app.register_blueprint(parcel_bp)
    app.register_blueprint(department_bp)

    @app.route('/ping')
    def hello_world():
        return 'pong'

    return app
