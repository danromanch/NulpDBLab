from src.novapost.domain.models import Operator
from src import db

class OperatorDao:
    def __init__(self, session):
        self.session = session

    def create_operator(self, name, surname, gender, birth_date, department_id):
        new_operator = Operator(name=name, surname=surname, gender=gender, birth_date=birth_date, department_id=department_id)
        self.session.add(new_operator)
        self.session.commit()
        return new_operator

    def get_all_operators(self):
        return self.session.query(Operator).all()

    def get_operator(self, id):
        return self.session.query(Operator).get(id)

    def update_operator(self, id, **kwargs):
        operator = self.session.query(Operator).get(id)
        if operator:
            for key, value in kwargs.items():
                setattr(operator, key, value)
            self.session.commit()
        return operator

    def delete_operator(self, id):
        operator = self.session.query(Operator).get(id)
        if operator:
            self.session.delete(operator)
            self.session.commit()
        return operator