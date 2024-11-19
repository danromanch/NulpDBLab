from src.novapost.dao.operator_dao import OperatorDao

class OperatorService:
    def __init__(self, operator_dao: OperatorDao):
        self.operator_dao = operator_dao

    def create_operator(self, name: str, surname: str, gender: str, birth_date: str, department_id: int):
        """Create a new operator."""
        return self.operator_dao.create_operator(name, surname, gender, birth_date, department_id)

    def get_all_operators(self):
        """Retrieve all operators."""
        return self.operator_dao.get_all_operators()

    def get_operator(self, id: int):
        """Retrieve an operator by ID."""
        return self.operator_dao.get_operator(id)

    def update_operator(self, id: int, **kwargs):
        """Update an operator's details."""
        return self.operator_dao.update_operator(id, **kwargs)

    def delete_operator(self, id: int):
        """Delete an operator by ID."""
        return self.operator_dao.delete_operator(id)