from src.novapost.dao.transfer_dao import TransferDao
import datetime

class TransferService:
    def __init__(self, transfer_dao: TransferDao):
        self.transfer_dao = transfer_dao

    def create_transfer(self, sender_id: int, reciever_id: int, parcel_id: int, date: str | None = None):
        """Create a new transfer. If date is missing, use today's date. Date should be ISO YYYY-MM-DD."""
        if date is None:
            date_obj = datetime.date.today()
        else:
            try:
                # support full ISO date strings like 'YYYY-MM-DD'
                date_obj = datetime.date.fromisoformat(date)
            except Exception:
                raise ValueError('Invalid date format; expected ISO YYYY-MM-DD')

        return self.transfer_dao.create_transfer(sender_id, reciever_id, parcel_id, date_obj)

    def get_all_transfers(self):
        """Retrieve all transfers."""
        return self.transfer_dao.get_all_transfers()

    def get_transfer(self, id: int):
        """Retrieve a transfer by ID."""
        return self.transfer_dao.get_transfer(id)

    def update_transfer(self, id: int, **kwargs):
        """Update a transfer's details."""
        return self.transfer_dao.update_transfer(id, **kwargs)

    def delete_transfer(self, id: int):
        """Delete a transfer by ID."""
        return self.transfer_dao.delete_transfer(id)