from src.novapost.dao.transfer_dao import TransferDao

class TransferService:
    def __init__(self, transfer_dao: TransferDao):
        self.transfer_dao = transfer_dao

    def create_transfer(self, sender_id: int, reciever_id: int, parcel_id: int, date: str):
        """Create a new transfer."""
        return self.transfer_dao.create_transfer(sender_id, reciever_id, parcel_id, date)

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