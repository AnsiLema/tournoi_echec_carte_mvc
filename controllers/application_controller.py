from controllers.tournament_controller import TournamentController
from views.main_menu_view import MainMenuView


class ApplicationController:
    def __init__(self):
        self.tournament_controller = TournamentController()

    def run(self):
        """Boucle principale du programme."""
        while True:
            choice = MainMenuView.display_main_menu()
            if choice == "1":
                self.start_new_tournament()
            elif choice == "2":
                self.load_existing_tournament()
            elif choice == "3":
                MainMenuView.display_quit_message()
                break
            else:
                print("Choix non valide, veuillez réessayer.")

    def start_new_tournament(self):
        """Initialise et démarre un nouveau tournoi."""
        tournament_details = MainMenuView.get_tournament_details()
        self.tournament_controller.create_tournament(*tournament_details)
        self.tournament_controller.add_players()
        self.tournament_controller.start_tournament()

    def load_existing_tournament(self):
        """Charge un tournoi existant et le démarre."""
        filename = MainMenuView.display_load_tournament()
        try:
            self.tournament_controller.load_tournament(filename)
            print("Tournoi chargé avec succès.")
            self.tournament_controller.add_players()
            self.tournament_controller.start_tournament()
        except FileNotFoundError:
            print("Fichier de tournoi non trouvé. Veuillez vérifier le nom et réessayer.")