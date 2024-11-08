import json
from config import PLAYERS_JSON_PATH


class Player:
    def __init__(self, last_name, first_name, date_of_birth, national_id):
        self.last_name = last_name
        self.first_name = first_name
        self.date_of_birth = date_of_birth
        self.national_id = national_id

    def __repr__(self):
        return (f"Player(last_name={self.last_name}, "
                f"first_name={self.first_name})")

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    def to_dict(self):
        """Converts the Player instance to a dictionary for JSON storage."""
        return {
            "last_name": self.last_name,
            "first_name": self.first_name,
            "date_of_birth": self.date_of_birth,
            "national_id": self.national_id
        }

    @classmethod
    def from_dict(cls, data):
        """Creates a Player instance from a dictionary."""
        return cls(
            last_name=data["last_name"],
            first_name=data["first_name"],
            date_of_birth=data["date_of_birth"],
            national_id=data["national_id"]
        )

    @staticmethod
    def load_players():
        """Loads players from the JSON file."""
        try:
            with open(PLAYERS_JSON_PATH, "r", encoding="utf-8") as file:
                player_data = json.load(file)
                return [Player.from_dict(p) for p in player_data]
        except FileNotFoundError:
            return []

    @staticmethod
    def save_players(players):
        """Saves the player list to the JSON file."""
        with open(PLAYERS_JSON_PATH, "w", encoding="utf-8") as file:
            json.dump([player.to_dict() for player in players], file,
                      indent=4,
                      ensure_ascii=False)
