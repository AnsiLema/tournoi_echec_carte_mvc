import re
from datetime import datetime


class MainMenuView:
    """Class for displaying the main menu and handling user input."""
    @staticmethod
    def display_main_menu():
        """Display the main menu and return the user's choice."""
        print("\n=== Menu Principal ===")
        print("1. Commencer un nouveau tournoi")
        print("2. Continuer un tournoi")
        print("3. Rapports")
        print("4. Quitter")
        return input("Veuillez choisir une option : ")

    @staticmethod
    def display_quit_message():
        """Display a quit message."""
        print("Merci d'avoir utilisé l'application. À bientôt!")

    @staticmethod
    def display_invalid_choice():
        """Display a message when the user makes an invalid choice."""
        print("Choix non valide, veuillez réessayer.")

    @staticmethod
    def display_reports_menu():
        """Display the reports menu and return the user's choice."""
        print("\n=== Menu des Rapports ===")
        print("1. Liste de tous les joueurs par ordre alphabétique")
        print("2. Liste de tous les tournois")
        print("3. Nom et dates d’un tournoi donné")
        print("4. Liste des joueurs du tournoi par ordre alphabétique")
        print("5. Liste de tous les tours du tournoi et de tous les matchs du tour")
        print("6. Retour au menu principal")
        return input("Veuillez choisir une option : ")

    @staticmethod
    def get_tournament_search_input():
        """Get input from the user for tournament search."""
        return input("Entrez les lettres présentes dans le nom du tournoi : ").strip().lower()

    @staticmethod
    def get_tournament_selection(max_index):
        """Get the tournament selection from the user and validate it."""
        try:
            selection = int(input("Veuillez entrer le numéro du tournoi choisi : ").strip()) - 1
            if 0 <= selection < max_index:
                return selection
            else:
                print("Numéro de tournoi invalide.")
                return None
        except ValueError:
            print("Entrée invalide. Veuillez entrer un numéro.")
            return None

    @staticmethod
    def get_resume_choice():
        """Ask the user if they want to resume the tournament."""
        return input("Souhaitez-vous reprendre le tournoi ? (o/n) : ").strip().lower()

    @staticmethod
    def display_return_to_main_menu():
        """Display a message to return to the main menu."""
        print("Retour au menu principal.")

    @staticmethod
    def prompt_date(prompt_message, optional=False):
        """Prompt for a date in the format DD/MM/YYYY."""
        date_pattern = r"^\d{2}/\d{2}/\d{4}$"
        while True:
            date_str = input(prompt_message).strip()
            if optional and date_str == "":
                return None
            if re.match(date_pattern, date_str):
                try:
                    datetime.strptime(date_str, "%d/%m/%Y")
                    return date_str
                except ValueError:
                    print("Date invalide. Assurez-vous d'entrer une vraie date.")
            else:
                print("Format invalide. La date doit être au format JJ/MM/AAAA.")

    @staticmethod
    def get_tournament_details():
        """Get tournament details from the user."""
        print("\n=== Démarrage d'un nouveau tournoi ===")
        name = input("Nom du tournoi : ")
        location = input("Lieu du tournoi : ")
        start_date = MainMenuView.prompt_date("Date de début (JJ/MM/AAAA) : ")
        end_date = MainMenuView.prompt_date("Date de fin (JJ/MM/AAAA, laissez vide si non définie) : ",
                                            optional=True)
        description = input("Description du tournoi : ")

        # Handling empty input for number_of_rounds
        while True:
            number_of_rounds_input = input("Nombre de rounds (appuyez sur Entrée pour 4) : ").strip()
            if number_of_rounds_input == "":
                number_of_rounds = 4  # Default value
                break
            elif number_of_rounds_input.isdigit() and 1 <= int(number_of_rounds_input) <= 20:
                number_of_rounds = int(number_of_rounds_input)
                break
            else:
                print(
                    "Veuillez entrer un nombre valide entre 1 et 20, "
                    "ou appuyez sur Entrée pour utiliser la valeur par défaut (4).")

        return name, location, start_date, end_date, description, number_of_rounds
