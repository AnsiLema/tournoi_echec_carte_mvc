import random
from models.model_match import Match
from models.model_round import Round
from models.model_player import Player  # Assuming Player has a from_dict method

class Tournament:
    def __init__(self, name, location, start_date, end_date, description, number_of_rounds):
        self.id = str(random.randint(1000, 9999))  # Generate a unique 4-digit ID
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        self.number_of_rounds = number_of_rounds
        self.current_round = []
        self.rounds = []
        self.players = []

    def add_player(self, player):
        """Adds a player to the tournament and initializes their score and opponent list."""
        player.score = 0
        player.opponents = []  # Track opponents each player has faced
        self.players.append(player)

    def add_round(self):
        """Adds a new round to the tournament."""
        round_number = len(self.rounds) + 1
        round_name = f"Round {round_number}"
        new_round = Round(name=round_name)
        self.rounds.append(new_round)

    def start_new_round(self):
        """Starts a new round and generates unique pairs of matches."""
        round_name = f"Round {len(self.rounds) + 1}"
        new_round = Round(name=round_name)
        self.rounds.append(new_round)

        # Generate unique pairs for the matches
        pairs = self.generate_pairs()
        for player1, player2 in pairs:
            match = Match(player1, player2)
            new_round.add_match(match)
            # Update each player's opponent list
            player1.opponents.append(player2)
            player2.opponents.append(player1)

    def generate_pairs(self):
        """Generates unique pairs for the matches based on player scores and previous opponents."""
        sorted_players = sorted(self.players, key=lambda p: p.score, reverse=True)
        pairs = []
        used_players = set()  # Track players already paired in this round

        for i, player1 in enumerate(sorted_players):
            if player1 in used_players:
                continue

            # Find the first available player who hasn't played against player1
            for player2 in sorted_players[i + 1:]:
                if player2 not in used_players and player2 not in player1.opponents:
                    pairs.append((player1, player2))
                    used_players.add(player1)
                    used_players.add(player2)
                    break  # Move on to the next player1

        return pairs

    def to_dict(self):
        """Converts the tournament instance to a dictionary for JSON serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "description": self.description,
            "number_of_rounds": self.number_of_rounds,
            "players": [player.to_dict() for player in self.players],
            "rounds": [round.to_dict() for round in self.rounds]
        }

    @classmethod
    def from_dict(cls, data):
        """Creates a Tournament instance from a dictionary and loads players and rounds if needed."""
        # Initialize the tournament with basic details
        tournament = cls(
            data["name"],
            data["location"],
            data["start_date"],
            data["end_date"],
            data["description"],
            data["number_of_rounds"]
        )
        tournament.id = data["id"]  # Restore tournament's ID

        # Load players
        tournament.players = [Player.from_dict(player_data) for player_data in data.get("players", [])]

        # Load rounds and matches
        tournament.rounds = []
        for round_data in data.get("rounds", []):
            round_instance = Round.from_dict(round_data)
            tournament.rounds.append(round_instance)

        return tournament

    def __repr__(self):
        return (f"Tournament(id={self.id}, name={self.name}, location={self.location}, "
                f"start_date={self.start_date})")

    def __str__(self):
        return (f"{self.name} - {self.location} - {self.start_date}")
