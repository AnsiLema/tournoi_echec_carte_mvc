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

        # Option pour rechercher par nom de tournoi
        search_choice = input("Souhaitez-vous rechercher un tournoi par nom ? (o/n) : ").strip().lower()
        if search_choice == 'o':
            search_name = input("Entrez le nom ou une partie du nom du tournoi : ").strip().lower()
            filtered_tournaments = [
                t for t in tournaments if search_name in t['name'].lower()
            ]

            if not filtered_tournaments:
                print("Aucun tournoi ne correspond à ce nom.")
                return

            print("=== Tournois correspondants ===")
            for idx, tournament in enumerate(filtered_tournaments, start=1):
                print(f"{idx}. ID: {tournament['id']}, Nom: {tournament['name']}")

            selected_id = input("Veuillez entrer l'ID du tournoi à charger : ").strip()
        else:
            selected_id = input("Veuillez entrer l'ID du tournoi à charger : ").strip()

        if self.tournament_controller.load_tournament_by_id(selected_id):
            print("Tournoi chargé avec succès.")

            # Check if the loaded tournament can be resumed
            if self.tournament_controller.can_resume_tournament():
                resume_choice = input("Souhaitez-vous reprendre le tournoi ? (o/n) : ").strip().lower()
                if resume_choice == "o":
                    self.tournament_controller.start_tournament()
                else:
                    print("Retour au menu principal.")
            else:
                print("Ce tournoi est déjà terminé.")
        else:
            print("ID du tournoi invalide ou tournoi introuvable.")

