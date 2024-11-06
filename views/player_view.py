class PlayerMenuView:
    @staticmethod
    def display_player_menu():
        print("\n=== Gestion des Joueurs ===")
        print("1. Ajouter un nouveau joueur")
        print("2. Rechercher un joueur dans la base de données JSON")
        choice = input("Veuillez choisir une option : ")
        return choice

    @staticmethod
    def display_add_player_menu():
        last_name = input("Nom :")
        first_name = input("Prénom :")
        date_of_birth = input("Date de naissance (format: JJ-MM-AAAA) :")
        national_id = input("ID National :")
        return last_name, first_name, date_of_birth, national_id

    @staticmethod
    def display_search_player_menu():
        pass

    @staticmethod
    def display_player_found_menu():
        pass

    @staticmethod
    def display_add_player_success_menu():
        print("\nJoueur ajouté avec succés.")
        input("Appuyez sur Entrée pour revenir au menu des joueurs.")

    @staticmethod
    def display_start_tournament_confirmation():
        return input("Appuyer sur 'Entrée' pour commencer le tournoi avec les joueurs actuels,"
                       " ou 'Retour' pour revenir au menu des joueurs :")


