import json
from faker import Faker
from config import PLAYERS_JSON_PATH  # Import the path constant


# Define the Player class
class Player:
    def __init__(self, last_name, first_name, date_of_birth, national_id):
        self.last_name = last_name
        self.first_name = first_name
        self.date_of_birth = date_of_birth
        self.national_id = national_id

    def to_dict(self):
        """Converts the Player instance to a dictionary for JSON storage."""
        return {
            "last_name": self.last_name,
            "first_name": self.first_name,
            "date_of_birth": self.date_of_birth,
            "national_id": self.national_id
        }


# Initialize Faker
fake = Faker('fr_FR')


# Ensure the data folder exists
PLAYERS_JSON_PATH.parent.mkdir(exist_ok=True)

# Load existing players if the file exists
if PLAYERS_JSON_PATH.exists():
    with open(PLAYERS_JSON_PATH, "r", encoding="utf-8") as file:
        players = json.load(file)
else:
    players = []  # Start with an empty list if the file doesn't exist

# Generate additional players (e.g., 30 players) and add them to the list
for _ in range(30):
    last_name = fake.last_name()
    first_name = fake.first_name()
    date_of_birth = fake.date_of_birth(minimum_age=18,
                                       maximum_age=60).strftime("%d/%m/%Y")
    national_id = fake.unique.bothify(text='??#####')
    player = Player(last_name, first_name, date_of_birth, national_id)
    players.append(player.to_dict())

# Save the updated player list to the JSON file
with open(PLAYERS_JSON_PATH, "w", encoding="utf-8") as file:
    json.dump(players, file, indent=4, ensure_ascii=False)

print("The 'players.json' file was updated with 30 additional players.")
