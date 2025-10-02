from src.novapost.domain.models import Parcel, Department, Transfer, Delivery
from sqlalchemy.exc import IntegrityError

class ParcelDao:
    def __init__(self, session):
        self.session = session

    def create_parcel(self, item, weight, size, is_paid, department_id):
        new_parcel = Parcel(item=item, weight=weight, size=size, is_paid=is_paid, department_id=department_id)
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
        if not parcel:
            return None

        # Check for related deliveries or transfers to avoid FK constraint errors
        related_delivery = self.session.query(Delivery).filter(Delivery.parcel_id == id).first()
        related_transfer = self.session.query(Transfer).filter(Transfer.parcel_id == id).first()
        if related_delivery or related_transfer:
            # Raise a clear Python exception the controller can catch and convert to a 409
            raise ValueError('Parcel cannot be deleted because related deliveries or transfers exist')

        self.session.delete(parcel)
        try:
            self.session.commit()
        except IntegrityError:
            # Convert DB integrity errors into a clear application error
            self.session.rollback()
            raise ValueError('Parcel cannot be deleted due to existing related records (FK constraint)')
        return parcel

    def get_parcels_by_sender_department(self, id):
        departments = (self.session.query(Department)
                       .join(Transfer, (Transfer.sender_id == Department.id))
                       .filter(Transfer.parcel_id == id)
                       .all())
        return departments