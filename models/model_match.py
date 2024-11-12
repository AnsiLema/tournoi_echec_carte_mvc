class Match:
    """
    Class Match

    Represents a game match between two players.

    Attributes:
    MATCH_SCORE : list
        Pre-defined score outcomes for a match.

    Methods:
    __init__(player1, player2)
        Initializes the match with two players
        and sets their initial scores to zero.
    """
    MATCH_SCORE = [(1, 0), (0.5, 0.5), (0, 1)]

    def __init__(self, player1, player2):
        self.match = [
            (player1, 0),
            (player2, 0)
        ]
        self.score1 = 0
        self.score2 = 0

    def add_points(self):
        """Assigns points based on match result input."""
        while True:
            result = input(
                f"Entrez le résultat pour le match entre {self.match[0][0]} "
                f"et {self.match[1][0]} (1 pour {self.match[0][0]}, N pour nul, 2 pour {self.match[1][0]}): "
            ).strip()
            if result == "1":
                self.match[0][0].score += self.MATCH_SCORE[0][0]
                self.match[1][0].score += self.MATCH_SCORE[0][1]
                break
            elif result in ["N", "n"]:
                self.match[0][0].score += self.MATCH_SCORE[1][0]
                self.match[1][0].score += self.MATCH_SCORE[1][1]
                break
            elif result == "2":
                self.match[0][0].score += self.MATCH_SCORE[2][0]
                self.match[1][0].score += self.MATCH_SCORE[2][1]
                break
            else:
                print("Entrée invalide. Veuillez entrer '1', 'N' ou '2'.")

        self.score1 = self.match[0][0].score
        self.score2 = self.match[1][0].score

    def to_dict(self):
        return {
            "player1_id": self.match[0][0].national_id,
            "player2_id": self.match[1][0].national_id,
            "score1": self.score1,
            "score2": self.score2
        }

    @classmethod
    def from_dict(cls, data, tournament):
        player1 = next((p for p in tournament.players if p.national_id == data["player1_id"]), None)
        player2 = next((p for p in tournament.players if p.national_id == data["player2_id"]), None)
        if player1 and player2:
            match_instance = cls(player1, player2)
            match_instance.score1 = data["score1"]
            match_instance.score2 = data["score2"]
            return match_instance
        print(f"Error: Could not find players with IDs {data['player1_id']} and {data['player2_id']}")
        return None

    def __str__(self):
        return f"Match entre {self.match[0][0]} et {self.match[1][0]}"

    def __repr__(self):
        return str(self)
