from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
import yaml

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    with open('config/app.yml', 'r') as config_file:
        config = yaml.safe_load(config_file)
    app.config['SQLALCHEMY_DATABASE_URI'] = config['database']['uri']

    # Initialize Swagger/OpenAPI documentation
    api = Api(
        app,
        version='1.0',
        title='NovaPost API',
        description='A REST API for NovaPost postal service management system',
        doc='/swagger/',
        prefix='/api/v1',
        mask=False  # Disable X-Fields header
    )

    db.init_app(app)

    # Import and register namespaces instead of blueprints
    from src.novapost.controller.parcel_controller import api as parcel_ns
    from src.novapost.controller.department_controller import api as department_ns
    from src.novapost.controller.transfer_controller import api as transfer_ns
    from src.novapost.controller.operator_controller import api as operator_ns

    api.add_namespace(parcel_ns)
    api.add_namespace(department_ns)
    api.add_namespace(transfer_ns)
    api.add_namespace(operator_ns)

    @app.route('/ping')
    def hello_world():
        return 'pong'

    return app
