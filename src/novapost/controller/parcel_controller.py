from flask import request
from flask_restx import Namespace, Resource, fields
from src.novapost.service.parcel_service import ParcelService
from src.novapost.dao.parcel_dao import ParcelDao
from src.novapost.domain.models import Department
from src import db

api = Namespace('parcels', description='Parcel operations')

parcel_dao = ParcelDao(db.session)
parcel_service = ParcelService(parcel_dao)

# Define models for Swagger documentation
parcel_model = api.model('Parcel', {
    'id': fields.Integer(readonly=True, description='The parcel unique identifier'),
    'item': fields.String(required=True, description='Item description'),
    'weight': fields.Integer(required=True, description='Weight in grams'),
    'size': fields.Integer(required=True, description='Size in cubic centimeters'),
    'is_paid': fields.Boolean(required=True, description='Payment status'),
    'department_id': fields.Integer(required=True, description='Department id')
})

parcel_input = api.model('ParcelInput', {
    'item': fields.String(required=True, description='Item description'),
    'weight': fields.Integer(required=True, description='Weight in grams'),
    'size': fields.Integer(required=True, description='Size in cubic centimeters'),
    'is_paid': fields.Boolean(required=True, description='Payment status'),
    'department_id': fields.Integer(required=True, description='Department id')
})

@api.route('')
class ParcelList(Resource):
    @api.doc('list_parcels')
    @api.response(200, 'Success', parcel_model)
    def get(self):
        '''Get all parcels'''
        parcels = parcel_service.get_all_parcels()
        return [parcel.serialize() for parcel in parcels]

    @api.doc('create_parcel')
    @api.expect(parcel_input)
    @api.response(201, 'Created', parcel_model)
    def post(self):
        '''Create a new parcel'''
        data = request.get_json()
        # Validate required field
        if 'department_id' not in data:
            api.abort(400, 'department_id is required')

        # Ensure the department exists
        department = parcel_dao.session.query(Department).get(data['department_id'])
        if not department:
            api.abort(400, 'department not found')

        new_parcel = parcel_service.create_parcel(data['item'], data['weight'], data['size'], data['is_paid'], data['department_id'])
        return new_parcel.serialize(), 201

@api.route('/<int:id>')
@api.param('id', 'The parcel identifier')
class Parcel(Resource):
    @api.doc('get_parcel')
    @api.response(200, 'Success', parcel_model)
    def get(self, id):
        '''Get a specific parcel by ID'''
        parcel = parcel_service.get_parcel(id)
        return parcel.serialize()

    @api.doc('update_parcel')
    @api.expect(parcel_input)
    @api.response(200, 'Success', parcel_model)
    def put(self, id):
        '''Update a parcel'''
        data = request.get_json()
        parcel = parcel_service.update_parcel(id, **data)
        return parcel.serialize()

    @api.doc('delete_parcel')
    @api.response(204, 'Parcel deleted')
    def delete(self, id):
        '''Delete a parcel'''
        parcel = None
        try:
            parcel = parcel_service.delete_parcel(id)
        except ValueError as e:
            # Conflict due to related rows (deliveries/transfers)
            api.abort(409, str(e))

        if not parcel:
            api.abort(404, 'parcel not found')

        return '', 204

@api.route('/department/<int:id>')
@api.param('id', 'The department identifier')
class ParcelByDepartment(Resource):
    @api.doc('get_parcels_by_department')
    @api.response(200, 'Success', [parcel_model])
    def get(self, id):
        '''Get all parcels by sender department'''
        parcels = parcel_service.get_parcels_by_sender_department(id)
        return [parcel.serialize() for parcel in parcels]
