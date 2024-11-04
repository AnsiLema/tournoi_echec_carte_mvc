class Player:
    def __init__(self, last_name, first_name, date_of_birth, national_id):
        self.last_name = last_name
        self.first_name = first_name
        self.date_of_birth = date_of_birth
        self.national_id = national_id

    def __str__(self):
        return f" {self.last_name} {self.first_name}"

    @staticmethod
    def from_json(data):
        """Create a Player instance from a JSON dictionary."""
        return Player(
            first_name=data['first_name'],
            last_name=data['last_name'],
            date_of_birth=data['date_of_birth'],
            national_id=data['national_id']
        )


