from src.novapost.domain.models import Transfer
from src import db

class TransferDao:
    def __init__(self, session):
        self.session = session

    def create_transfer(self, sender_id, reciever_id, parcel_id, date):
        new_transfer = Transfer(sender_id=sender_id, reciever_id=reciever_id, parcel_id=parcel_id, date=date)
        self.session.add(new_transfer)
        self.session.commit()
        return new_transfer

    def get_all_transfers(self):
        return self.session.query(Transfer).all()

    def get_transfer(self, id):
        return self.session.query(Transfer).get(id)

    def update_transfer(self, id, **kwargs):
        transfer = self.session.query(Transfer).get(id)
        if transfer:
            for key, value in kwargs.items():
                setattr(transfer, key, value)
            self.session.commit()
        return transfer

    def delete_transfer(self, id):
        transfer = self.session.query(Transfer).get(id)
        if transfer:
            self.session.delete(transfer)
            self.session.commit()
        return transfer