from src.novapost.dao.department_dao import DepartmentDao

class DepartmentService:
    def __init__(self, department_dao: DepartmentDao):
        self.department_dao = department_dao

    def create_department(self, email: str, phone: str):
        """Create a new department."""
        return self.department_dao.create_department(email, phone)

    def get_all_departments(self):
        """Retrieve all departments."""
        return self.department_dao.get_all_departments()

    def get_department(self, id: int):
        """Retrieve a department by ID."""
        return self.department_dao.get_department(id)

    def update_department(self, id: int, email: str, phone: str):
        """Update a department's details."""
        return self.department_dao.update_department(id, email, phone)

    def delete_department(self, id: int):
        """Delete a department by ID."""
        return self.department_dao.delete_department(id)

    def get_operators_by_department(self, id: int):
        return self.department_dao.get_operators_by_department(id)

    def get_parcels_by_departments(self, id: int):
        return self.department_dao.get_parcels_by_departments(id)