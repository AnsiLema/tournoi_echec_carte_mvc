import json
from faker import Faker
from pathlib import Path

# Définition de la classe Player
class Player:
    def __init__(self, last_name, first_name, date_of_birth, national_id):
        self.last_name = last_name
        self.first_name = first_name
        self.date_of_birth = date_of_birth
        self.national_id = national_id

    def to_dict(self):
        """Convertit l'instance de Player en dictionnaire pour la sauvegarde JSON."""
        return {
            "last_name": self.last_name,
            "first_name": self.first_name,
            "date_of_birth": self.date_of_birth,
            "national_id": self.national_id
        }

# Initialisation de Faker
fake = Faker('fr_FR')

# Création de 30 joueurs
players = []
for _ in range(30):
    last_name = fake.last_name()
    first_name = fake.first_name()
    date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=60).strftime("%d/%m/%Y")
    national_id = fake.unique.bothify(text='??#####')
    player = Player(last_name, first_name, date_of_birth, national_id)
    players.append(player.to_dict())

# Define the path to the data folder and the JSON file
data_folder = Path("data")
data_folder.mkdir(exist_ok=True)  # Create the folder if it doesn't exist
file_path = data_folder / "players.json"

# Save players data to the JSON file
with open(file_path, "w", encoding="utf-8") as file:
    json.dump(players, file, indent=4, ensure_ascii=False)

print("Fichier 'players.json' créé avec succès avec 30 joueurs.")
