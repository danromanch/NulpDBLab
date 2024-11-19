from src.novapost.domain.models import Department, Operator, Parcel, Transfer
from src import db

class DepartmentDao:
    def __init__(self, session):
        self.session = session

    def create_department(self, email, phone):
        new_department = Department(email=email, phone=phone)
        self.session.add(new_department)
        self.session.commit()
        return new_department

    def get_all_departments(self):
        return self.session.query(Department).all()

    def get_department(self, id):
        return self.session.query(Department).get(id)

    def update_department(self, id, email, phone):
        department = self.session.query(Department).get(id)
        if department:
            department.email = email
            department.phone = phone
            self.session.commit()
        return department

    def delete_department(self, id):
        department = self.session.query(Department).get(id)
        if department:
            self.session.delete(department)
            self.session.commit()
        return department

    def get_operators_by_department(self, id):
        return self.session.query(Operator).filter_by(department_id=id).all()

    def get_parcels_by_departments(self, id):
        return self.session.query(Parcel).join(Transfer, Transfer.parcel_id == Parcel.id).filter(Transfer.sender_id == id).all()