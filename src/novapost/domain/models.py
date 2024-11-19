from sqlalchemy import BigInteger, Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

class Courier(Base):
    __tablename__ = 'courier'

    id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False, index=True)
    surname = Column(String(45), nullable=False, index=True)
    phone_number = Column(String(45), nullable=False, unique=True)
    email = Column(String(45), nullable=False, unique=True)


class Department(Base):
    __tablename__ = 'department'

    id = Column(Integer, primary_key=True)
    phone = Column(String(45), nullable=False, unique=True)
    email = Column(String(45), nullable=False, unique=True)

    def serialize(self):
        return {
            'id': self.id,
            'phone': self.phone,
            'email': self.email
        }


class DepartmentLocation(Department):
    __tablename__ = 'department_location'

    number = Column(String(45), nullable=False)
    street = Column(String(45), nullable=False)
    city = Column(String(45), nullable=False)
    region = Column(String(45), nullable=False, index=True)
    country = Column(String(45), nullable=False)
    department_id = Column(ForeignKey('department.id'), primary_key=True)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False, index=True)
    surname = Column(String(45), nullable=False, index=True)
    gender = Column(String(45), nullable=False)
    phone = Column(String(45), nullable=False, unique=True)
    email = Column(String(45), nullable=False, unique=True)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'surname': self.surname,
            'gender': self.gender,
            'phone': self.phone,
            'email': self.email
        }


class CreditCard(User):
    __tablename__ = 'credit_card'

    user_id = Column(ForeignKey('user.id'), primary_key=True)
    number = Column(BigInteger, nullable=False, unique=True)
    cvv = Column(Integer, nullable=False)
    expration_date = Column(Date, nullable=False)


class UserLocation(User):
    __tablename__ = 'user_location'

    room_number = Column(Integer)
    number = Column(Integer, nullable=False)
    street = Column(String(45), nullable=False)
    city = Column(String(45), nullable=False, index=True)
    region = Column(String(45), nullable=False)
    country = Column(String(45), nullable=False)
    user_id = Column(ForeignKey('user.id'), primary_key=True)
    user = relationship('User')

    def serialize(self):
        return {
            'user_id': self.user_id,
            'room_number': self.room_number,
            'number': self.number,
            'street': self.street,
            'city': self.city,
            'region': self.region,
            'country': self.country
        }


class Operator(Base):
    __tablename__ = 'operator'

    id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False, index=True)
    surname = Column(String(45), nullable=False, index=True)
    gender = Column(String(45), nullable=False)
    birth_date = Column(Date, nullable=False)
    department_id = Column(ForeignKey('department.id'), nullable=False, index=True)

    department = relationship('Department')
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'surname': self.surname,
            'birth_date': self.birth_date
        }


class Parcel(Base):
    __tablename__ = 'parcel'

    id = Column(Integer, primary_key=True)
    item = Column(String(45), nullable=False, index=True)
    weight = Column(Integer, nullable=False)
    size = Column(Integer, nullable=False)
    is_paid = Column(TINYINT, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'item': self.item,
            'weight': self.weight,
            'size': self.size,
            'is_paid': self.is_paid,
        }


class Delivery(Base):
    __tablename__ = 'delivery'

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    is_fast = Column(TINYINT, nullable=False)
    parcel_id = Column(ForeignKey('parcel.id'), nullable=False, index=True)
    courier_id = Column(ForeignKey('courier.id'), nullable=False, index=True)
    user_id = Column(ForeignKey('user.id'), nullable=False, index=True)
    department_id = Column(ForeignKey('department.id'), nullable=False, index=True)

    courier = relationship('Courier')
    department = relationship('Department')
    parcel = relationship('Parcel')
    user = relationship('User')


class Transfer(Base):
    __tablename__ = 'transfer'

    id = Column(Integer, primary_key=True)
    sender_id = Column(ForeignKey('department.id'), nullable=False, index=True)
    reciever_id = Column(ForeignKey('department.id'), nullable=False, index=True)
    parcel_id = Column(ForeignKey('parcel.id'), nullable=False, index=True)
    date = Column(Date, nullable=False)

    parcel = relationship('Parcel')
    reciever = relationship('Department', primaryjoin='Transfer.reciever_id == Department.id')
    sender = relationship('Department', primaryjoin='Transfer.sender_id == Department.id')

    def serialize(self):
        return {
            'id': self.id,
            'sender_id': self.sender_id,
            'reciever_id': self.reciever_id,
            'parcel_id': self.parcel_id,
            'date': self.date.isoformat()
        }
