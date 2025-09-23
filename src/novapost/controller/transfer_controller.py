from flask import request
from flask_restx import Namespace, Resource, fields
from src.novapost.service.transfer_service import TransferService
from src.novapost.dao.transfer_dao import TransferDao
from src import db

api = Namespace('transfers', description='Transfer operations')

transfer_dao = TransferDao(db.session)
transfer_service = TransferService(transfer_dao)

# Define models for Swagger documentation
transfer_model = api.model('Transfer', {
    'id': fields.Integer(readonly=True, description='The transfer unique identifier'),
    'sender_id': fields.Integer(required=True, description='Sender department ID'),
    'reciever_id': fields.Integer(required=True, description='Receiver department ID'),
    'parcel_id': fields.Integer(required=True, description='Parcel ID'),
    'date': fields.String(required=True, description='Transfer date (ISO format)')
})

transfer_input = api.model('TransferInput', {
    'sender_id': fields.Integer(required=True, description='Sender department ID'),
    'reciever_id': fields.Integer(required=True, description='Receiver department ID'),
    'parcel_id': fields.Integer(required=True, description='Parcel ID'),
    'date': fields.String(required=True, description='Transfer date (ISO format)')
})

@api.route('')
class TransferList(Resource):
    @api.doc('list_transfers')
    @api.response(200, 'Success', [transfer_model])
    def get(self):
        '''Get all transfers'''
        transfers = transfer_service.get_all_transfers()
        return [transfer.serialize() for transfer in transfers]

    @api.doc('create_transfer')
    @api.expect(transfer_input)
    @api.response(201, 'Created', transfer_model)
    def post(self):
        '''Create a new transfer'''
        data = request.get_json()
        new_transfer = transfer_service.create_transfer(data['sender_id'], data['reciever_id'], data['parcel_id'], data['date'])
        return new_transfer.serialize(), 201

@api.route('/<int:id>')
@api.param('id', 'The transfer identifier')
class Transfer(Resource):
    @api.doc('get_transfer')
    @api.response(200, 'Success', transfer_model)
    def get(self, id):
        '''Get a specific transfer by ID'''
        transfer = transfer_service.get_transfer(id)
        return transfer.serialize()

    @api.doc('update_transfer')
    @api.expect(transfer_input)
    @api.response(200, 'Success', transfer_model)
    def put(self, id):
        '''Update a transfer'''
        data = request.get_json()
        transfer = transfer_service.update_transfer(id, **data)
        return transfer.serialize()

    @api.doc('delete_transfer')
    @api.response(204, 'Transfer deleted')
    def delete(self, id):
        '''Delete a transfer'''
        transfer_service.delete_transfer(id)
        return '', 204
