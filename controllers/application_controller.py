from controllers.tournament_controller import TournamentController
from views.main_menu_view import MainMenuView


class ApplicationController:
    def __init__(self):
        self.tournament_controller = TournamentController()

    def run(self):
        """Main program loop."""
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
        """Initialize and start a new tournament."""
        tournament_details = MainMenuView.get_tournament_details()
        self.tournament_controller.create_tournament(*tournament_details)
        self.tournament_controller.add_players()
        self.tournament_controller.start_tournament()

    def load_existing_tournament(self):
        """Loads an existing tournament by displaying available tournaments for selection."""
        tournaments = self.tournament_controller.get_all_tournaments()

        if not tournaments:
            print("Aucun tournoi disponible pour chargement.")
            return

        print("=== Tournois disponibles ===")
        for idx, tournament in enumerate(tournaments, start=1):
            print(f"{idx}. ID: {tournament['id']}, Nom: {tournament['name']}")

        # Prompt the user to select a tournament by its ID
        selected_id = input("Veuillez entrer l'ID du tournoi à charger : ").strip()
        selected_tournament = next((t for t in tournaments if t['id'] == selected_id), None)

        if selected_tournament:
            try:
                self.tournament_controller.load_tournament_by_id(selected_id)
                print("Tournoi chargé avec succès.")
                self.tournament_controller.add_players()
                self.tournament_controller.start_tournament()
            except FileNotFoundError:
                print("Erreur : tournoi introuvable.")
        else:
            print("ID du tournoi invalide, veuillez réessayer.")
