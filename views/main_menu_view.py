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
    def get_tournament_details():
        print("\n=== Démarrage d'un nouveau tournoi ===")
        name = input("Nom du tournoi : ")
        location = input("Lieu du tournoi : ")
        start_date = input("Date de début (YYYY-MM-DD) : ")
        end_date = input("Date de fin (YYYY-MM-DD) : ")
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