import json
from models.model_player import Player
from models.model_tournament import Tournament
from views.main_menu_view import MainMenuView
from views.tournament_view import TournamentView
from views.player_view import PlayerMenuView


class TournamentController:
    def __init__(self):
        self.tournament = None

    def create_tournament(self, name, location, start_date, end_date, description, number_of_rounds):
        """Initialise un nouveau tournoi avec les informations fournies."""
        self.tournament = Tournament(name, location, start_date, end_date, description, number_of_rounds)
        TournamentView.display_tournament_info(self.tournament)

    def add_players(self):
        """Permet de gérer l'ajout de joueurs jusqu'à ce qu'il y ait suffisamment de participants pour commencer."""
        while len(self.tournament.players) < 2:
            choice = PlayerMenuView.display_player_menu()
            if choice == '1':
                self._add_new_player()
            elif choice == '2':
                PlayerMenuView.display_search_player_menu()
            else:
                print("Option invalide.")

            while True:
                confirmation = PlayerMenuView.display_start_tournament_confirmation()
                if confirmation.lower() in ['', 'retour']:
                    if confirmation == '':
                        break  # Start the tournament
                    else:
                        return self.add_players()  # Return to player menu
                else:
                    print("Option invalide, veuillez réessayer.")

    def _add_new_player(self):
        """Logique interne pour ajouter un nouveau joueur."""
        last_name, first_name, date_of_birth, national_id = PlayerMenuView.display_add_player_menu()
        player = Player(last_name, first_name, date_of_birth, national_id)
        self.tournament.add_player(player)
        PlayerMenuView.display_add_player_success_menu()

    def start_tournament(self):
        """Démarre le tournoi si les conditions sont remplies."""
        if not self.tournament or len(self.tournament.players) < 2:
            print("Il faut au moins 2 joueurs pour commencer le tournoi.")
            return

        for round_num in range(1, self.tournament.number_of_rounds + 1):
            self.tournament.start_new_round()
            current_round = self.tournament.rounds[-1]
            TournamentView.display_round_info(round_num, current_round.matches)

            # Entrée des résultats
            for match in current_round.matches:
                match.add_points()
                TournamentView.display_match_result(match)

            current_round.finish_round()
            TournamentView.display_rankings(self.tournament.players)

        TournamentView.display_final_results(self.tournament.players)
        print("\n=== Le tournoi est terminé ===")

    def load_tournament(self, filename):
        """Charge un tournoi depuis un fichier JSON."""
        with open(filename, "r") as file:
            tournament_data = json.load(file)
            self.tournament = Tournament.from_dict(tournament_data)
            TournamentView.display_tournament_info(self.tournament)
