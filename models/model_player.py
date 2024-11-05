class Player:
    def __init__(self, last_name, first_name, date_of_birth, national_id):
        self.last_name = last_name
        self.first_name = first_name
        self.date_of_birth = date_of_birth
        self.national_id = national_id

    def __str__(self):
        return f" {self.last_name} {self.first_name}"


    def to_dict(self):
        return {
            "last_name": self.last_name,
            "first_name": self.first_name,
            "date_of_birth": self.date_of_birth,
            "national_id": self.national_id
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            last_name=data["last_name"],
            first_name=data["first_name"],
            date_of_birth=data["date_of_birth"],
            national_id=data["national_id"]
        )


