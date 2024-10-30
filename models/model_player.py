class Player:
    def __init__(self, lastname, firstname, birthdate, national_id):
        self.lastname = lastname
        self.firstname = firstname
        self.birthdate = birthdate
        self.national_id = national_id

    def __str__(self):
        return f"{self.lastname} {self.firstname}"



