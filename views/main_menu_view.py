import re
from datetime import datetime


class MainMenuView:
    @staticmethod
    def display_main_menu():
        print("\n=== Menu Principal ===")
        print("1. Commencer un nouveau tournoi")
        print("2. Continuer un tournoi")
        print("3. Rapports")  # New option for reports
        print("4. Quitter")
        choice = input("Veuillez choisir une option : ")
        return choice

    @staticmethod
    def display_reports_menu():
        print("\n=== Menu des Rapports ===")
        print("1. Liste de tous les joueurs par ordre alphabétique")
        print("2. Liste de tous les tournois")
        print("3. Nom et dates d’un tournoi donné")
        print("4. Liste des joueurs du tournoi par ordre alphabétique")
        print("5. Liste de tous les tours du tournoi "
              "et de tous les matchs du tour")
        print("6. Retour au menu principal")
        choice = input("Veuillez choisir une option : ")
        return choice

    @staticmethod
    def prompt_date(prompt_message, optional=False):
        """Prompt for a date in the format JJ/MM/AAAA,
        validate the format, and allow empty input if optional."""
        date_pattern = r"^\d{2}/\d{2}/\d{4}$"
        while True:
            date_str = input(prompt_message).strip()

            if optional and date_str == "":
                return None

            # Validate the date format
            if re.match(date_pattern, date_str):
                try:
                    # Check if it's a valid calendar date
                    datetime.strptime(date_str, "%d/%m/%Y")
                    return date_str
                except ValueError:
                    print("Date invalide. "
                          "Assurez-vous d'entrer une vraie date.")
            else:
                print("Format invalide. "
                      "La date doit être au format JJ/MM/AAAA.")

    @staticmethod
    def get_tournament_details():
        print("\n=== Démarrage d'un nouveau tournoi ===")
        name = input("Nom du tournoi : ")
        location = input("Lieu du tournoi : ")

        # Using prompt_date to ensure valid format for the start date
        start_date = MainMenuView.prompt_date("Date de début (JJ/MM/AAAA) : ")
        # Using prompt_date with optional=True for the end date
        end_date = MainMenuView.prompt_date("Date de fin (JJ/MM/AAAA, "
                                            "laissez vide si non définie) : ",
                                            optional=True)

        description = input("Description du tournoi : ")
        number_of_rounds = int(input("Nombre de rounds : "))
        return (name, location,
                start_date,
                end_date,
                description,
                number_of_rounds)

    @staticmethod
    def display_load_tournament():
        filename = input("Nom du fichier du tournoi à charger : ")
        return filename

    @staticmethod
    def display_quit_message():
        print("Merci d'avoir utilisé l'application. À bientôt!")
