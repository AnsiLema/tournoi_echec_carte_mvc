from faker import Faker
from models.model_player import Player
from models.model_tournament import Tournament

def get_tournaments():
    pass


def get_players():
    pass

tournament = Tournament("Chess Championship", "Paris", "2023-10-01",
                        "2023-10-15", "Annual Chess Tournament",
                        5)

fake = Faker('fr_FR')
# Create and add 8 fictional players
for _ in range(8):
    firstname = fake.first_name()
    lastname = fake.last_name()
    birthdate = fake.date_of_birth(minimum_age=18, maximum_age=60).strftime("%d/%m/%Y")
    national_id = fake.unique.bothify(text='??#####')

    player = Player(firstname, lastname, birthdate, national_id)
    tournament.add_player(player)

# Show players for verification
for player in tournament.players:
    print(player)