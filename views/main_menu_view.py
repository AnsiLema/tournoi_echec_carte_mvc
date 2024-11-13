import re
from datetime import datetime


class MainMenuView:
    @staticmethod
    def display_main_menu():
        print("\n=== Menu Principal ===")
        print("1. Commencer un nouveau tournoi")
        print("2. Charger un tournoi existant")
        print("3. Quitter")
        choice = input("Veuillez choisir une option : ")
        return choice

    @staticmethod
    def prompt_date(prompt_message, optional=False):
        """Prompt for a date in the format JJ/MM/AAAA, validate the format, and allow empty input if optional."""
        date_pattern = r"^\d{2}/\d{2}/\d{4}$"  # Pattern for DD/MM/YYYY format
        while True:
            date_str = input(prompt_message).strip()

            # If the date is optional and the user leaves it empty, return None
            if optional and date_str == "":
                return None

            # Validate the date format
            if re.match(date_pattern, date_str):
                try:
                    # Check if it's a valid calendar date
                    datetime.strptime(date_str, "%d/%m/%Y")
                    return date_str
                except ValueError:
                    print("Date invalide. Assurez-vous d'entrer une date réelle.")
            else:
                print("Format invalide. La date doit être au format JJ/MM/AAAA.")

    @staticmethod
    def get_tournament_details():
        print("\n=== Démarrage d'un nouveau tournoi ===")
        name = input("Nom du tournoi : ")
        location = input("Lieu du tournoi : ")

        # Using prompt_date to ensure valid format for the start date
        start_date = MainMenuView.prompt_date("Date de début (JJ/MM/AAAA) : ")
        # Using prompt_date with optional=True for the end date
        end_date = MainMenuView.prompt_date("Date de fin (JJ/MM/AAAA, "
                                            "laissez vide si non définie) : ", optional=True)

        description = input("Description du tournoi : ")
        number_of_rounds = int(input("Nombre de rounds : "))
        return name, location, start_date, end_date, description, number_of_rounds

    @staticmethod
    def display_load_tournament():
        filename = input("Nom du fichier du tournoi à charger : ")
        return filename

    @staticmethod
    def display_quit_message():
        print("Merci d'avoir utilisé l'application. À bientôt!")
