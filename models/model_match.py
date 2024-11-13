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
        """Converts the Match instance to a dictionary for JSON serialization."""
        return {
            "player1_id": self.match[0][0].id,  # Assuming Player has an `id` attribute
            "player2_id": self.match[1][0].id,
            "score1": self.match[0][0].score,
            "score2": self.match[1][0].score
        }

    @classmethod
    def from_dict(cls, data, tournament):
        """
        Creates a Match instance from a dictionary.

        Args:
        - data (dict): Dictionary with match data.
        - player_lookup (dict): Dictionary or function to find player objects by ID.
        """
        player1_id = data["player1_id"]
        player2_id = data["player2_id"]

        # Find players by ID in the tournament
        player1 = next((p for p in tournament.players if p.national_id == player1_id), None)
        player2 = next((p for p in tournament.players if p.national_id == player2_id), None)

        if player1 and player2:
            return cls(player1, player2)
        else:
            # Handle case where players are not found (e.g., raise an error or return None)
            print(f"Error: Could not find players with IDs {player1_id} and {player2_id} in the tournament.")
            return None

    def __str__(self):
        return f"Match entre {self.match[0][0]} et {self.match[1][0]}"

    def __repr__(self):
        return str(self)
