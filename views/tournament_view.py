class TournamentView:
    @staticmethod
    def display_tournament_info(tournament):
        """Affiche les informations générales du tournoi."""
        print("\n=== Informations sur le tournoi ===")
        print(f"Nom du tournoi : {tournament.name}")
        print(f"Lieu : {tournament.location}")
        print(f"Date de début : {tournament.start_date}")
        print(f"Date de fin : {tournament.end_date}")
        print(f"Description : {tournament.description}")
        print(f"Nombre de rounds : {tournament.number_of_rounds}")

    @staticmethod
    def display_round_info(round_number, matches):
        """Affiche les informations sur les matchs d'un round."""
        print(f"\n=== Début du Round {round_number} ===")
        print("Oppositions :")
        for match in matches:
            print(f"{match.match[0][0]} vs {match.match[1][0]}")  # Accès correct aux joueurs


    @staticmethod
    def display_match_result(match):
        """Shows the result of the specific match only, not cumulative scores."""
        print(f"Match : {match.match[0][0]} vs {match.match[1][0]}")
        print(
            f"Score du match : {match.match[0][0]} - {match.match_score1} | {match.match[1][0]} - {match.match_score2}")

    @staticmethod
    def display_rankings(players):
        """Affiche le classement actuel des joueurs."""
        print("\n=== Classement des joueurs ===")
        sorted_players = sorted(players, key=lambda p: p.score, reverse=True)
        for rank, player in enumerate(sorted_players, start=1):
            print(f"{rank}. {player} - Point(s): {player.score}")

    @staticmethod
    def display_final_results(players):
        """Affiche le classement final des joueurs après la fin du tournoi."""
        print("\n=== Résultats finaux du tournoi ===")
        sorted_players = sorted(players, key=lambda p: p.score, reverse=True)
        for rank, player in enumerate(sorted_players, start=1):
            print(f"{rank}. {player} - Score: {player.score}")
