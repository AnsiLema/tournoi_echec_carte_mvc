class Match:

    MATCH_SCORE = [(1.0, 0), (0.5, 0.5), (0, 1.0)]

    def __init__(self, player1, player2):
        self.match = [
            (player1, 0),
            (player2, 0)
        ]
        # Separate attributes for the current match score
        self.match_score1 = 0
        self.match_score2 = 0

    def add_points(self, result):
        """
        Assign points based on the match result.
        :param result: str, "1" (player1 wins), "2" (player2 wins), "N" (draw)
        :raises ValueError: if result is invalid
        """
        if result == "1":
            self.match_score1, self.match_score2 = self.MATCH_SCORE[0]
        elif result in ["N", "n"]:
            self.match_score1, self.match_score2 = self.MATCH_SCORE[1]
        elif result == "2":
            self.match_score1, self.match_score2 = self.MATCH_SCORE[2]
        else:
            raise ValueError("Résultat invalide. Utilisez '1', 'N', ou '2'.")

        # Update player scores
        self.match[0][0].score += self.match_score1
        self.match[1][0].score += self.match_score2

    def to_dict(self):
        """Converts the Match instance to a dictionary for JSON serialization."""
        return {
            "player1_id": self.match[0][0].id,
            "player2_id": self.match[1][0].id,
            "score1": self.match_score1,
            "score2": self.match_score2
        }

    @classmethod
    def from_dict(cls, data, tournament):
        """
        Creates a Match instance from a dictionary.
        :param data: dict, match data
        :param tournament: Tournament, containing player data
        :raises KeyError: if players are not found in the tournament
        """
        player1_id = data["player1_id"]
        player2_id = data["player2_id"]

        # Find players by ID in the tournament
        player1 = next((p for p in tournament.players if p.national_id == player1_id), None)
        player2 = next((p for p in tournament.players if p.national_id == player2_id), None)

        if not player1 or not player2:
            raise KeyError(f"Joueurs introuvables : {player1_id}, {player2_id}")

        match_instance = cls(player1, player2)
        match_instance.match_score1 = data.get("score1", 0)
        match_instance.match_score2 = data.get("score2", 0)
        return match_instance

    def __str__(self):
        return f"Match entre {self.match[0][0]} et {self.match[1][0]}"

    def __repr__(self):
        return str(self)
