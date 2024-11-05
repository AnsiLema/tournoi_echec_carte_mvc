from controllers.tournament_controller import TournamentController
from views.main_menu_view import MainMenuView

class ApplicationController:
    def __init__(self):
        self.tournament_controller = TournamentController()

    def run(self):
        while True:
            choice = MainMenuView.display_main_menu()
            if choice == "1":
                # Créer un nouveau tournoi
                self.start_new_tournament()
            elif choice == "2":
                # Charger un tournoi existant
                self.load_tournament()
            elif choice == "3":
                MainMenuView.display_quit_message()
                break
            else:
                print("Choix non valide, veuillez réessayer.")

    def start_new_tournament(self):
        # Récupère les détails du tournoi via la vue
        name, location, start_date, end_date, description, number_of_rounds = MainMenuView.get_tournament_details()
        # Initialise un nouveau tournoi dans le contrôleur du tournoi
        self.tournament_controller.create_tournament(name, location, start_date, end_date, description, number_of_rounds)
        # Lance le tournoi avec la logique de gestion des joueurs, rounds, etc.
        self.tournament_controller.start_tournament()

    def load_tournament(self):
        # Demande le nom du fichier pour charger un tournoi
        filename = MainMenuView.display_load_tournament()
        try:
            # Charge le tournoi via le contrôleur du tournoi
            self.tournament_controller.load_tournament(filename)
            print("Tournoi chargé avec succès.")
            self.tournament_controller.start_tournament()
        except FileNotFoundError:
            print("Fichier de tournoi non trouvé. Veuillez vérifier le nom et réessayer.")
