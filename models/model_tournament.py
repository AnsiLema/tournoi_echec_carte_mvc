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
        """Generates unique pairs for matches
        based on the absence of previous encounters first,
        and then on scores.
        """
        sorted_players = sorted(self.players, key=lambda p: p.score, reverse=True)
        pairs = []
        used_players = set()

        for player1 in sorted_players:
            if player1 in used_players:
                continue

            found_pair = False
            for player2 in sorted_players:
                if (player2 not in used_players and
                        player2.national_id not in player1.opponents):
                    pairs.append((player1, player2))
                    used_players.add(player1)
                    used_players.add(player2)
                    found_pair = True
                    break

            if not found_pair:
                for player2 in sorted_players:
                    if player2 not in used_players:
                        pairs.append((player1, player2))
                        used_players.add(player1)
                        used_players.add(player2)
                        break

        return pairs

    def to_dict(self):
        """Convert the tournament instance to a
        dictionary for JSON serialization.
        """
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
                    **player.to_dict(),
                    "score": getattr(player, "score", 0),
                    "opponents": getattr(player, "opponents", [])
                }
                for player in self.players
            ],
            "rounds": [round.to_dict() for round in self.rounds]
        }

    @classmethod
    def from_dict(cls, data):
        tournament = cls(
            data["name"], data["location"], data["start_date"],
            data["end_date"], data["description"], data["number_of_rounds"]
        )
        tournament.id = data["id"]
        tournament.completed = data["completed"]
        # Load players with tournament-specific attributes
        tournament.players = []
        for p_data in data["players"]:
            player = Player.from_dict(p_data)
            player.score = p_data.get("score", 0)
            player.opponents = p_data.get("opponents", [])
            tournament.players.append(player)

        tournament.rounds = [Round.from_dict(r_data, tournament)
                             for r_data in data["rounds"]]
        return tournament

    def __repr__(self):
        return (f"Tournament(id={self.id},"
                f" name={self.name},"
                f" location={self.location})")
