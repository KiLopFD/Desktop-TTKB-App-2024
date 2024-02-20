class Person:
    def __init__(self, name, address, cmnd, birth_day):
        self.name = name
        self.address = address
        self.cmnd = cmnd
        self.birth_day = birth_day

    def __str__(self):
        return f"{self.name} - {self.address} - {self.cmnd} - {self.birth_day}"