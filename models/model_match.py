class Match:
    """
        Class Match

        Represents a game match between two players.

        Attributes:
        MATCH_SCORE : list
            Pre-defined score outcomes for a match.

        Methods:
        __init__(player1, player2)
            Initializes the match with two players and sets their initial scores to zero.
    """
    MATCH_SCORE = [(1, 0), (0.5, 0.5), (0, 1)]

    def __init__(self, player1, player2):
        self.match = (
            [player1, 0],
            [player2, 0]
        )

    def __str__(self):
        return f"Match entre {self.match[0][0]} et {self.match[1][0]}"

    def __repr__(self):
        return str(self)

    def add_points(self, result):
        """
        Adds points to layers based on the match result.

        Parameters:
        result : str
            The result of the match ('1' player 1 wins, 'N' for draw, '2' player 2 wins).
        """
        if result == '1':
            points = self.MATCH_SCORE[0]
        elif result == 'N':
            points = self.MATCH_SCORE[1]
        elif result == '2':
            points = self.MATCH_SCORE[2]
        else:
            raise ValueError("Le résultat du match doit être '1', 'N', ou '2'.")

        self.match[0][1] += points[0]
        self.match[1][1] += points[1]