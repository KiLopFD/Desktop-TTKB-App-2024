from app.db.entity.Person import Person

class Student(Person):

    def __init__(self, name, address, cmnd, birth_day):
        super().__init__(name, address, cmnd, birth_day)
        self.role = "student"
        self.grade = None
    
    def __str__(self):
        return f"{self.name} - {self.address} - {self.cmnd} - {self.birth_day} - {self.role} - {self.grade}"