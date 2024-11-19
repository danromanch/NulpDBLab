from flask import Blueprint, request, jsonify
from src.novapost.dao.operator_dao import OperatorDao
from src import db
from src.novapost.service.operator_service import OperatorService

operator_bp = Blueprint('operator_bp', __name__)
operator_dao = OperatorDao(db.session)
operator_service = OperatorService(operator_dao)

@operator_bp.route('/operators', methods=['POST'])
def create_operator_route():
    data = request.get_json()
    new_operator = operator_service.create_operator(
        name=data['name'],
        surname=data['surname'],
        gender=data['gender'],
        birth_date=data['birth_date'],
        department_id=data['department_id']
    )
    return jsonify(new_operator.serialize()), 201

@operator_bp.route('/operators', methods=['GET'])
def get_all_operators_route():
    operators = operator_service.get_all_operators()
    return jsonify([operator.serialize() for operator in operators])

@operator_bp.route('/operators/<int:id>', methods=['GET'])
def get_operator_route(id):
    operator = operator_service.get_operator(id)
    if operator is None:
        return jsonify({'error': 'Operator not found'}), 404
    return jsonify(operator.serialize())

@operator_bp.route('/operators/<int:id>', methods=['PUT'])
def update_operator_route(id):
    data = request.get_json()
    operator = operator_service.get_operator(id)
    if operator is None:
        return jsonify({'error': 'Operator not found'}), 404
    updated_operator = operator_dao.update_operator(id, **data)
    return jsonify(updated_operator.serialize())

@operator_bp.route('/operators/<int:id>', methods=['DELETE'])
def delete_operator_route(id):
    operator = operator_service.get_operator(id)
    if operator is None:
        return jsonify({'error': 'Operator not found'}), 404
    operator_dao.delete_operator(id)
    return '', 204
