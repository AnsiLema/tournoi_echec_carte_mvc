from models.model_match import Match
from models.model_round import Round


class Tournament:
    def __init__(self, name, location, start_date, end_date, description, number_of_rounds):
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
        player.score = 0
        player.opponents = []
        self.players.append(player)

    def add_round(self):
        round_number = len(self.rounds) + 1
        round_name = f"Round {round_number}"
        new_round = Round(name=round_name)
        self.rounds.append(new_round)


    def start_new_round(self):
        """Démarre un nouveau round et génère les paires de matchs."""
        round_name = f"Round {len(self.rounds) + 1}"
        new_round = Round(name=round_name)
        self.rounds.append(new_round)

        # Appairage des joueurs
        pairs = self.generate_pairs()
        for player1, player2 in pairs:
            match = Match(player1, player2)
            new_round.add_match(match)

    def generate_pairs(self):
        """Génère les paires pour les matchs en fonction du score des joueurs."""
        # Tri des joueurs par score, puis appairage par ordre
        sorted_players = sorted(self.players, key=lambda p: p.score, reverse=True)
        pairs = [(sorted_players[i], sorted_players[i + 1]) for i in range(0, len(sorted_players) - 1, 2)]
        return pairs

    def __repr__(self):
        return (f"Tournament(name={self.name},"
                f" location={self.location}, "
                f"start_date={self.start_date})")

    def __str__(self):
        return (f"{self.name} - "
                f"{self.location} - "
                f"{self.start_date}")