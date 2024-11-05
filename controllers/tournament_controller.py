import json
from models.model_player import Player
from models.model_tournament import Tournament
from models.model_match import Match
from views.main_menu_view import MainMenuView
from views.tournament_view import TournamentView
from views.player_view import PlayerMenuView


class TournamentController:
    def __init__(self):
        self.tournament = None

    def create_tournament(self):
        # Demande des informations de tournoi à l'utilisateur via la vue
        name, location, start_date, end_date, description, number_of_rounds = MainMenuView.get_tournament_details()

        self.tournament = Tournament(name, location, start_date, end_date, description, number_of_rounds)
        TournamentView.display_tournament_info(self.tournament)
        return self.tournament

    def add_players(self):
        # Permet de gérer l'ajout de joueurs via un menu interactif
        while len(self.tournament.players) < 2:
            choice = PlayerMenuView.display_player_menu()
            if choice == '1':
                last_name, first_name, date_of_birth, national_id = PlayerMenuView.display_add_player_menu()
                player = Player(last_name, first_name, date_of_birth, national_id)
                self.tournament.add_player(player)
                PlayerMenuView.display_add_player_success_menu()
            elif choice == '2':
                PlayerMenuView.display_search_player_menu()
            else:
                print("Option invalide.")

            if len(self.tournament.players) >= 2:
                confirmation = PlayerMenuView.display_start_tournament_confirmation()
                if confirmation.lower() == 'retour':
                    continue
                break

    def start_tournament(self):
        # Vérifie que le tournoi existe et lance les rounds
        if not self.tournament or len(self.tournament.players) < 2:
            print("Il faut au moins 2 joueurs pour commencer le tournoi.")
            return

        # Boucle pour chaque round
        for round_num in range(1, self.tournament.number_of_rounds + 1):
            self.tournament.start_new_round()
            current_round = self.tournament.rounds[-1]  # Le dernier round ajouté

            TournamentView.display_round_info(round_num, current_round.matches)

            # Saisie des résultats des matchs
            for match in current_round.matches:
                match.add_points(match)
                TournamentView.display_match_result(match)

            current_round.finish_round()
            TournamentView.display_rankings(self.tournament.players)

        TournamentView.display_final_results(self.tournament.players)
        print("\n=== Le tournoi est terminé ===")

    def load_tournament(self, filename):
        # Charge un tournoi à partir d'un fichier JSON
        with open(filename, "r") as file:
            tournament_data = json.load(file)
            self.tournament = Tournament.from_dict(tournament_data)
            TournamentView.display_tournament_info(self.tournament)


def main_menu():
    controller = TournamentController()
    while True:
        choice = MainMenuView.display_main_menu()

        if choice == "1":
            controller.create_tournament()
            controller.add_players()
            controller.start_tournament()
        elif choice == "2":
            filename = MainMenuView.display_load_tournament()
            controller.load_tournament(filename)
            controller.add_players()
            controller.start_tournament()
        elif choice == "3":
            MainMenuView.display_quit_message()
            break
        else:
            print("Option invalide. Veuillez réessayer.")


# Appel de la fonction pour afficher le menu principal
main_menu()
