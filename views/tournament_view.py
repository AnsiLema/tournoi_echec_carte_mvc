from models.model_match import Match


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
            print(f"{match.match[0][0]} vs {match.match[1][0]}")

    @staticmethod
    def display_match_result(match):
        """Shows the result of the match"""
        print(f"Match : {match.match[0][0]} vs {match.match[1][0]}")
        print(
            f"Score du match : {match.match[0][0]} - {match.match_score1} |"
            f" {match.match[1][0]} - {match.match_score2}")

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
        sorted_players = sorted(players,
                                key=lambda p: p.score,
                                reverse=True)
        for rank, player in enumerate(sorted_players, start=1):
            print(f"{rank}. {player} - Score: {player.score}")

    @staticmethod
    def display_all_players(players):
        print("\n=== Liste de tous les joueurs ===")
        for index, player in enumerate(players, start=1):
            print(f"{index}. {player['last_name']} {player['first_name']}"
                  f" (ID: {player['national_id']})")
        print(f"\nNombre total de joueurs : {len(players)}\n")

    @staticmethod
    def display_all_tournaments(tournaments):
        print("\n=== Liste de tous les tournois ===")
        for tournament in tournaments:
            print(f"Nom: {tournament['name']},"
                  f" Lieu: {tournament['location']},"
                  f" Date de début: {tournament['start_date']}")
        print("\n")

    @staticmethod
    def display_tournament_details(name, start_date, end_date):
        print("\n=== Détails du Tournoi ===")
        print(f"Nom: {name}")
        print(f"Date de début: {start_date}")
        print(f"Date de fin: {end_date if end_date else 'Non définie'}")
        print("\n")

    @staticmethod
    def display_tournament_players(players):
        print("\n=== Joueurs du Tournoi ===")
        for player in players:
            print(f"{player['last_name']} {player['first_name']}"
                  f" (ID: {player['national_id']})")
        print("\n")

    @staticmethod
    def display_tournament_rounds_and_matches(rounds, tournament):
        print("\n=== Tours et Matchs du Tournoi ===")
        for round_info in rounds:
            print(f"Tour: {round_info['name']}")
            for match_data in round_info.get('matches', []):
                # Use the actual tournament object with players
                match = Match.from_dict(match_data, tournament)
                if match:
                    player1_name = match.match[0][0].__str__()
                    player2_name = match.match[1][0].__str__()
                    score1 = match.match_score1
                    score2 = match.match_score2
                    print(f"  Match: {player1_name} vs {player2_name} - "
                          f"Résultat: {score1} - {score2}")
                else:
                    print("  Erreur: Match invalide ou joueurs introuvables.")
        print("\n")
