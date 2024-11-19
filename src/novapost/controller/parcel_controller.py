from flask import Blueprint, request, jsonify
from src.novapost.service.parcel_service import ParcelService
from src.novapost.dao.parcel_dao import ParcelDao
from src import db

parcel_bp = Blueprint('parcel_bp', __name__)
parcel_dao = ParcelDao(db.session)
parcel_service = ParcelService(parcel_dao)

@parcel_bp.route('/parcels', methods=['POST'])
def create_parcel_route():
    data = request.get_json()
    new_parcel = parcel_service.create_parcel(data['item'], data['weight'], data['size'], data['is_paid'])
    return jsonify(new_parcel.serialize()), 201

@parcel_bp.route('/parcels', methods=['GET'])
def get_all_parcels_route():
    parcels = parcel_service.get_all_parcels()
    return jsonify([parcel.serialize() for parcel in parcels])

@parcel_bp.route('/parcels/<int:id>', methods=['GET'])
def get_parcel_route(id):
    parcel = parcel_service.get_parcel(id)
    return jsonify(parcel.serialize())

@parcel_bp.route('/parcels/<int:id>', methods=['PUT'])
def update_parcel_route(id):
    data = request.get_json()
    parcel = parcel_service.update_parcel(id, **data)
    return jsonify(parcel.serialize())

@parcel_bp.route('/parcels/<int:id>', methods=['DELETE'])
def delete_parcel_route(id):
    parcel_service.delete_parcel(id)
    return '', 204

@parcel_bp.route('/parcels/department/<int:id>', methods=['GET'])
def get_parcels_by_sender_department_route(id):
    departments = parcel_service.get_parcels_by_sender_department(id)
    return jsonify([department.serialize() for department in departments])
