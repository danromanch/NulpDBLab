from flask import request
from flask_restx import Namespace, Resource, fields
from src.novapost.service.department_service import DepartmentService
from src.novapost.dao.department_dao import DepartmentDao
from src import db

api = Namespace('departments', description='Department operations')

department_dao = DepartmentDao(db.session)
department_service = DepartmentService(department_dao)

# Define models for Swagger documentation
department_model = api.model('Department', {
    'id': fields.Integer(readonly=True, description='The department unique identifier'),
    'email': fields.String(required=True, description='Department email'),
    'phone': fields.String(required=True, description='Department phone number')
})

department_input = api.model('DepartmentInput', {
    'email': fields.String(required=True, description='Department email'),
    'phone': fields.String(required=True, description='Department phone number')
})

@api.route('')
class DepartmentList(Resource):
    @api.doc('list_departments')
    @api.response(200, 'Success', [department_model])
    def get(self):
        '''Get all departments'''
        departments = department_service.get_all_departments()
        return [department.serialize() for department in departments]

    @api.doc('create_department')
    @api.expect(department_input)
    @api.response(201, 'Created', department_model)
    def post(self):
        '''Create a new department'''
        data = request.get_json()
        new_department = department_service.create_department(data['email'], data['phone'])
        return new_department.serialize(), 201

@api.route('/<int:id>')
@api.param('id', 'The department identifier')
class Department(Resource):
    @api.doc('get_department')
    @api.response(200, 'Success', department_model)
    def get(self, id):
        '''Get a specific department by ID'''
        department = department_service.get_department(id)
        return department.serialize()

    @api.doc('update_department')
    @api.expect(department_input)
    @api.response(200, 'Success', department_model)
    def put(self, id):
        '''Update a department'''
        data = request.get_json()
        department = department_service.update_department(id, data['email'], data['phone'])
        return department.serialize()
