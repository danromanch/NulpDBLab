from src.novapost.domain.models import Parcel, Department, Transfer
from src import db

class ParcelDao:
    def __init__(self, session):
        self.session = session

    def create_parcel(self, item, weight, size, is_paid, department_id):
        new_parcel = Parcel(item=item, weight=weight, size=size, is_paid=is_paid)
        self.session.add(new_parcel)
        self.session.commit()
        return new_parcel

    def get_all_parcels(self):
        return self.session.query(Parcel).all()

    def get_parcel(self, id):
        return self.session.query(Parcel).get(id)

    def update_parcel(self, id, **kwargs):
        parcel = self.session.query(Parcel).get(id)
        if parcel:
            for key, value in kwargs.items():
                setattr(parcel, key, value)
            self.session.commit()
        return parcel

    def delete_parcel(self, id):
        parcel = self.session.query(Parcel).get(id)
        if parcel:
            self.session.delete(parcel)
            self.session.commit()
        return parcel

    def get_parcels_by_sender_department(self, id):
        departments = (self.session.query(Department)
                       .join(Transfer, (Transfer.sender_id == Department.id))
                       .filter(Transfer.parcel_id == id)
                       .all())
        return departments