from models.model_match import Match


class TournamentView:
    @staticmethod
    def display_tournament_info(tournament):
        """Display general information about the tournament."""
        print("\n=== Informations sur le tournoi ===")
        print(f"Nom du tournoi : {tournament.name}")
        print(f"Lieu : {tournament.location}")
        print(f"Date de début : {tournament.start_date}")
        print(f"Date de fin : {tournament.end_date}")
        print(f"Description : {tournament.description}")
        print(f"Nombre de rounds : {tournament.number_of_rounds}")

    @staticmethod
    def display_no_matching_tournaments():
        """Display a message when no matching tournaments are found."""
        print("Aucun tournoi ne correspond à ces lettres.")

    @staticmethod
    def display_matching_tournaments(tournaments):
        """Display a list of matching tournaments."""
        print("\n=== Tournois correspondants ===")
        for idx, tournament in enumerate(tournaments, start=1):
            print(f"{idx}: {tournament['name']}")

    @staticmethod
    def display_round_info(round_number, matches):
        """Display the round information and the matches for that round."""
        print(f"\n=== Début du Round {round_number} ===")
        print("Oppositions :")
        for match in matches:
            # Access players correctly from the match object
            player1 = match.match[0][0]
            player2 = match.match[1][0]
            print(f"{player1.first_name} {player1.last_name} (ID: {player1.national_id}) "
                  f"vs {player2.first_name} {player2.last_name} (ID: {player2.national_id})")

    @staticmethod
    def get_match_result(player1, player2):
        while True:
            result = input(
                f"Entrez le résultat pour le match entre {player1} et {player2} "
                f"(1 pour {player1}, N pour nul, 2 pour {player2}): "
            ).strip()
            if result in ["1", "N", "n", "2"]:
                return result
            print("Entrée invalide. Veuillez entrer '1', 'N', ou '2'.")

    @staticmethod
    def display_match_result(match):
        """Display the result of a match."""
        # Access players correctly from the match object
        player1 = match.match[0][0]
        player2 = match.match[1][0]
        print(f"Match : {player1.first_name} {player1.last_name} (ID: {player1.national_id}) "
              f"vs {player2.first_name} {player2.last_name} (ID: {player2.national_id})")
        print(f"Score : {player1.first_name} {player1.last_name} - {match.match_score1} | "
              f"{player2.first_name} {player2.last_name} - {match.match_score2}")

    @staticmethod
    def display_loading_error():
        """Display an error message if the tournament cannot be loaded."""
        print("Erreur lors du chargement du tournoi.")

    @staticmethod
    def display_tournament_loaded_success():
        """Display a success message when a tournament is loaded."""
        print("Tournoi chargé avec succès.")

    @staticmethod
    def display_tournament_already_completed():
        """Display a message when the tournament is already completed."""
        print("Ce tournoi est déjà terminé.")

    @staticmethod
    def display_tournament_details(name, start_date, end_date):
        """Display the details of a tournament."""
        print("\n=== Détails du Tournoi ===")
        print(f"Nom: {name}")
        print(f"Date de début: {start_date}")
        print(f"Date de fin: {end_date if end_date else 'Non définie'}")

    @staticmethod
    def display_tournament_players(players):
        print("\n=== Joueurs du Tournoi (ordre alphabétique) ===")
        for player in players:
            print(f"{player.last_name} {player.first_name} (ID: {player.national_id})")
        print("\n")

    @staticmethod
    def display_all_players(players):
        """Display all players in alphabetical order."""
        print("\n=== Liste de tous les joueurs ===")
        for index, player in enumerate(players, start=1):
            print(f"{index}. {player['last_name']} {player['first_name']} (ID: {player['national_id']})")
        print(f"\nNombre total de joueurs : {len(players)}\n")

    @staticmethod
    def display_all_tournaments(tournaments):
        """Display all tournaments."""
        print("\n=== Liste de tous les tournois ===")
        for tournament in tournaments:
            print(f"Nom: {tournament['name']}, Lieu: {tournament['location']},"
                  f" Date de début: {tournament['start_date']}")

    @staticmethod
    def display_tournament_rounds_and_matches(rounds, tournament):
        """Display all rounds and matches of a tournament."""
        print("\n=== Tours et Matchs du Tournoi ===")
        for round_info in rounds:
            start_date = round_info.get("start_date", "Date de début non définie")
            end_date = round_info.get("end_date", "Date de fin non définie")
            print(f"Tour: {round_info['name']}")
            print(f"  Date de début: {start_date}")
            print(f"  Date de fin: {end_date}")

            for match_data in round_info.get('matches', []):
                match = Match.from_dict(match_data, tournament)
                if match:
                    player1_name = match.match[0][0].__str__()
                    player2_name = match.match[1][0].__str__()
                    score1 = match.match_score1
                    score2 = match.match_score2
                    print(f"  Match: {player1_name} vs {player2_name} - Résultat: {score1} - {score2}")
                else:
                    print("  Erreur: Match invalide ou joueurs introuvables.")

    @staticmethod
    def display_rankings(players):
        """Display the current player rankings."""
        print("\n=== Classement des joueurs ===")
        sorted_players = sorted(players, key=lambda p: p.score, reverse=True)
        for rank, player in enumerate(sorted_players, start=1):
            print(f"{rank}. {player} - Point(s): {player.score}")

    @staticmethod
    def display_final_results(players):
        """Display the final results of the tournament."""
        print("\n=== Résultats finaux du tournoi ===")
        sorted_players = sorted(players, key=lambda p: p.score, reverse=True)
        for rank, player in enumerate(sorted_players, start=1):
            print(f"{rank}. {player} - Score: {player.score}")

    @staticmethod
    def display_tournament_not_found():
        """Display a message when a tournament is not found."""
        print("Tournoi non trouvé ou déjà terminé.")

    @staticmethod
    def display_insufficient_players():
        """Display a message when there are not enough players to start the tournament."""
        print("Au moins 2 joueurs sont requis pour démarrer le tournoi.")

    @staticmethod
    def ask_to_continue_after_round():
        return input("Souhaitez-vous continuer le tournoi ? (o/n) : ").strip().lower()

    @staticmethod
    def display_tournament_paused():
        """Inform the user that the tournament is paused."""
        print("Le tournoi a été mis en pause. Vous pouvez le reprendre plus tard.")
