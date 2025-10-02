from src.novapost.dao.parcel_dao import ParcelDao

class ParcelService:
    def __init__(self, parcel_dao: ParcelDao):
        self.parcel_dao = parcel_dao

    def create_parcel(self, item: str, weight: int, size: int, is_paid: bool, department_id: int):
        """Create a new parcel with associated department."""
        return self.parcel_dao.create_parcel(item, weight, size, is_paid, department_id)

    def get_all_parcels(self):
        """Retrieve all parcels."""
        return self.parcel_dao.get_all_parcels()

    def get_parcel(self, id: int):
        """Retrieve a parcel by ID."""
        return self.parcel_dao.get_parcel(id)

    def update_parcel(self, id: int, **kwargs):
        """Update a parcel's details."""
        return self.parcel_dao.update_parcel(id, **kwargs)

    def delete_parcel(self, id: int):
        """Delete a parcel by ID."""
        return self.parcel_dao.delete_parcel(id)

    def get_parcels_by_sender_department(self, id: int):
        return self.parcel_dao.get_parcels_by_sender_department(id)
