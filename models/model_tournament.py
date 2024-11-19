from datetime import datetime
from models.model_match import Match
from models.model_round import Round
from models.model_player import Player


class Tournament:
    def __init__(self, name,
                 location,
                 start_date,
                 end_date=None,
                 description="",
                 number_of_rounds=1):
        self.id = None
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        self.number_of_rounds = number_of_rounds
        self.current_round = []
        self.rounds = []
        self.players = []
        self.completed = False

    def mark_as_completed(self):
        """Mark the tournament as completed."""
        self.completed = True
        self.end_date = datetime.now().strftime("%d/%m/%Y")

    def add_player(self, player):
        """Adds a player to the tournament
        and initializes their score and opponent list.
        """
        player.score = 0
        player.opponents = []
        self.players.append(player)

    def start_new_round(self):
        """Starts a new round and generates unique pairs of matches."""
        round_name = f"Round {len(self.rounds) + 1}"
        new_round = Round(name=round_name)
        self.rounds.append(new_round)

        pairs = self.generate_pairs()
        for player1, player2 in pairs:
            match = Match(player1, player2)
            new_round.add_match(match)
            player1.opponents.append(player2.national_id)
            player2.opponents.append(player1.national_id)

    def generate_pairs(self):
        """Generates unique pairs for the matches
        based on player scores and previous opponents.
        """
        sorted_players = sorted(self.players,
                                key=lambda p: p.score,
                                reverse=True)
        pairs = []
        used_players = set()

        for i, player1 in enumerate(sorted_players):
            if player1 in used_players:
                continue

            for player2 in sorted_players[i + 1:]:
                if (player2 not in used_players
                        and player2.national_id
                        not in player1.opponents):
                    pairs.append((player1, player2))
                    used_players.add(player1)
                    used_players.add(player2)
                    break

        return pairs

    def to_dict(self):
        """Convert the tournament instance to a dictionary for JSON serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "description": self.description,
            "number_of_rounds": self.number_of_rounds,
            "completed": self.completed,
            "players": [
                {
                    "national_id": player.national_id,
                    "score": player.score,
                    "opponents": player.opponents
                }
                for player in self.players
            ],
            "rounds": [round.to_dict() for round in self.rounds]
        }

    @classmethod
    def from_dict(cls, data, all_players):
        """Load a tournament from a dictionary and populate player details using national_id."""
        tournament = cls(
            data["name"], data["location"], data["start_date"],
            data["end_date"], data["description"], data["number_of_rounds"]
        )
        tournament.id = data["id"]
        tournament.completed = data["completed"]

        # Retrieve players using their national_id from all_players
        tournament.players = []
        for player_data in data["players"]:
            national_id = player_data["national_id"]
            if national_id in all_players:
                player = all_players[national_id]
                player.score = player_data["score"]
                player.opponents = player_data["opponents"]
                tournament.players.append(player)
            else:
                print(f"Avertissement: le joueur avec l'ID {national_id} n'a pas été trouvé dans all_players.")

        tournament.rounds = [Round.from_dict(r_data, tournament) for r_data in data["rounds"]]
        return tournament

    def __repr__(self):
        return (f"Tournament(id={self.id},"
                f" name={self.name},"
                f" location={self.location})")
