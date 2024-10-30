class Tournament:
    def __init__(self, name, location, start_date, end_date, description, number_of_rounds):
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        self.number_of_rounds = number_of_rounds
        self.current_round = 1
        self.rounds = []
        self.players = []

    def add_round(self, round):
        """
        :param round: The 'round' parameter represents an instance of a round to be added to the rounds list.
        :return: None
        """
        self.rounds.append(round)

    def add_player(self, player):
        player.score = 0
        player.opponents = []
        self.players.append(player)

    def __repr__(self):
        return (f"Tournament(name={self.name},"
                f" location={self.location}, "
                f"start_date={self.start_date})")