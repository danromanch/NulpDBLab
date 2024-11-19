from flask import Blueprint, request, jsonify
from src.novapost.service.department_service import DepartmentService
from src.novapost.dao.department_dao import DepartmentDao
from src import db

department_bp = Blueprint('department_bp', __name__)
department_dao = DepartmentDao(db.session)
department_service = DepartmentService(department_dao)

@department_bp.route('/departments', methods=['POST'])
def create_department_route():
    data = request.get_json()
    new_department = department_service.create_department(data['email'], data['phone'])
    return jsonify(new_department.serialize()), 201

@department_bp.route('/departments', methods=['GET'])
def get_all_departments_route():
    departments = department_service.get_all_departments()
    return jsonify([department.serialize() for department in departments])

@department_bp.route('/departments/<int:id>', methods=['GET'])
def get_department_route(id):
    department = department_service.get_department(id)
    return jsonify(department.serialize())

@department_bp.route('/departments/<int:id>', methods=['PUT'])
def update_department_route(id):
    data = request.get_json()
    department = department_service.update_department(id, data['email'], data['phone'])
    return jsonify(department.serialize())

@department_bp.route('/departments/<int:id>', methods=['DELETE'])
def delete_department_route(id):
    department_service.delete_department(id)
    return '', 204

@department_bp.route('/departments/operators/<int:id>', methods=['GET'])
def get_operators_by_department_route(id):
    operators = department_service.get_operators_by_department(id)
    return jsonify([operator.serialize() for operator in operators])

@department_bp.route('/departments/parcel/<int:id>', methods=['GET'])
def get_parcels_by_departments_route(id):
    parcels = department_service.get_parcels_by_departments(id)
    return jsonify([parcel.serialize() for parcel in parcels])