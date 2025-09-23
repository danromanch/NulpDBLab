from flask import request
from flask_restx import Namespace, Resource, fields
from src.novapost.dao.operator_dao import OperatorDao
from src import db
from src.novapost.service.operator_service import OperatorService

api = Namespace('operators', description='Operator operations')

operator_dao = OperatorDao(db.session)
operator_service = OperatorService(operator_dao)

# Define models for Swagger documentation
operator_model = api.model('Operator', {
    'id': fields.Integer(readonly=True, description='The operator unique identifier'),
    'name': fields.String(required=True, description='Operator first name'),
    'surname': fields.String(required=True, description='Operator last name'),
    'birth_date': fields.String(required=True, description='Birth date (ISO format)'),
    'department_id': fields.Integer(required=True, description='Department ID where operator works')
})

operator_input = api.model('OperatorInput', {
    'name': fields.String(required=True, description='Operator first name'),
    'surname': fields.String(required=True, description='Operator last name'),
    'gender': fields.String(required=True, description='Operator gender'),
    'birth_date': fields.String(required=True, description='Birth date (ISO format)'),
    'department_id': fields.Integer(required=True, description='Department ID where operator works')
})

@api.route('')
class OperatorList(Resource):
    @api.doc('list_operators')
    @api.response(200, 'Success', [operator_model])
    def get(self):
        '''Get all operators'''
        operators = operator_service.get_all_operators()
        return [operator.serialize() for operator in operators]

    @api.doc('create_operator')
    @api.expect(operator_input)
    @api.response(201, 'Created', operator_model)
    def post(self):
        '''Create a new operator'''
        data = request.get_json()
        new_operator = operator_service.create_operator(
            name=data['name'],
            surname=data['surname'],
            gender=data['gender'],
            birth_date=data['birth_date'],
            department_id=data['department_id']
        )
        return new_operator.serialize(), 201

@api.route('/<int:id>')
@api.param('id', 'The operator identifier')
class Operator(Resource):
    @api.doc('get_operator')
    @api.response(200, 'Success', operator_model)
    @api.response(404, 'Operator not found')
    def get(self, id):
        '''Get a specific operator by ID'''
        operator = operator_service.get_operator(id)
        if operator is None:
            api.abort(404, 'Operator not found')
        return operator.serialize()

    @api.doc('update_operator')
    @api.expect(operator_input)
    @api.response(200, 'Success', operator_model)
    @api.response(404, 'Operator not found')
    def put(self, id):
        '''Update an operator'''
        data = request.get_json()
        operator = operator_service.get_operator(id)
        if operator is None:
            api.abort(404, 'Operator not found')
        updated_operator = operator_dao.update_operator(id, **data)
        return updated_operator.serialize()

    @api.doc('delete_operator')
    @api.response(204, 'Operator deleted')
    @api.response(404, 'Operator not found')
    def delete(self, id):
        '''Delete an operator'''
        operator = operator_service.get_operator(id)
        if operator is None:
            api.abort(404, 'Operator not found')
        operator_dao.delete_operator(id)
        return '', 204
