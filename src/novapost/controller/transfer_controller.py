from flask import Blueprint, request, jsonify
from src.novapost.service.transfer_service import TransferService
from src.novapost.dao.transfer_dao import TransferDao
from src import db

transfer_bp = Blueprint('transfer_bp', __name__)
transfer_dao = TransferDao(db.session)
transfer_service = TransferService(transfer_dao)

@transfer_bp.route('/transfers', methods=['POST'])
def create_transfer_route():
    data = request.get_json()
    new_transfer = transfer_service.create_transfer(data['sender_id'], data['reciever_id'], data['parcel_id'], data['date'])
    return jsonify(new_transfer.serialize()), 201

@transfer_bp.route('/transfers', methods=['GET'])
def get_all_transfers_route():
    transfers = transfer_service.get_all_transfers()
    return jsonify([transfer.serialize() for transfer in transfers])

@transfer_bp.route('/transfers/<int:id>', methods=['GET'])
def get_transfer_route(id):
    transfer = transfer_service.get_transfer(id)
    return jsonify(transfer.serialize())

@transfer_bp.route('/transfers/<int:id>', methods=['PUT'])
def update_transfer_route(id):
    data = request.get_json()
    transfer = transfer_service.update_transfer(id, **data)
    return jsonify(transfer.serialize())

@transfer_bp.route('/transfers/<int:id>', methods=['DELETE'])
def delete_transfer_route(id):
    transfer_service.delete_transfer(id)
    return '', 204