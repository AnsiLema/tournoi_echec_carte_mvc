import json
from typing import List, Dict
from config import PLAYERS_JSON_PATH  # Import the path constant
from models.model_player import Player
from models.model_tournament import Tournament
from views.tournament_view import TournamentView
from views.player_view import PlayerMenuView


class TournamentController:
    def __init__(self):
        self.tournament = None

    def create_tournament(self, name, location, start_date, end_date, description, number_of_rounds):
        """Initializes a new tournament with the provided information."""
        self.tournament = Tournament(name, location, start_date, end_date, description, number_of_rounds)
        TournamentView.display_tournament_info(self.tournament)

    def add_players(self):
        """Handles adding players until the user decides to start the tournament."""
        players = self._load_players()

        while True:
            # Prompt the user to add a new player or start the tournament
            choice = input("Sélectionnez une option :\n1. Ajouter un joueur\n2. Commencer le tournoi\n> ")

            if choice == '1':
                # Prompt to either create a new player or select from the existing players
                add_choice = input("Voulez-vous :\n1. Créer un nouveau joueur\n2. Sélectionner un joueur existant\n> ")

                if add_choice == '1':
                    # Create a new player
                    self._add_new_player(players)
                elif add_choice == '2':
                    # Select an existing player
                    self._select_player(players)
                else:
                    print("Option non valide, veuillez réessayer.")
                    continue

                print(f"Nombre de joueurs enregistrés: {len(self.tournament.players)}")  # Show player count

            elif choice == '2':
                if len(self.tournament.players) >= 2:
                    break  # Start the tournament if there are at least 2 players
                else:
                    print("Au moins 2 joueurs sont requis pour démarrer le tournoi.")
            else:
                print("Option non valide, veuillez réessayer.")

    def _add_new_player(self, players):
        """Internal logic to add a new player and save to JSON file."""
        last_name, first_name, date_of_birth, national_id = PlayerMenuView.display_add_player_menu()
        new_player = {
            "last_name": last_name,
            "first_name": first_name,
            "date_of_birth": date_of_birth,
            "national_id": national_id
        }
        players.append(new_player)  # Add player to the list
        self._save_players(players)  # Save to JSON
        player = Player(last_name, first_name, date_of_birth, national_id)
        self.tournament.add_player(player)
        PlayerMenuView.display_add_player_success_menu()

    def _select_player(self, players):
        """Allows selecting an existing player with dynamic filtering."""
        filter_str = ""
        filtered_players = players
        while True:
            # Display filtered list of players
            filtered_players = [p for p in players if
                                filter_str.lower() in p["last_name"].lower() or filter_str.lower() in p[
                                    "first_name"].lower()]
            if not filtered_players:
                print("Aucun joueur ne correspond à ce filtre.")
                return  # Return to main menu

            # Display filtered players
            for i, player in enumerate(filtered_players, start=1):
                print(f"{i}. {player['first_name']} {player['last_name']} (ID: {player['national_id']})")

            # User input to filter or select a player
            input_str = input("Entrez une lettre pour filtrer ou un numéro pour sélectionner un joueur : ")
            if input_str.isdigit():  # If a number is entered
                choice = int(input_str) - 1
                if 0 <= choice < len(filtered_players):
                    selected_player = filtered_players[choice]
                    player = Player(
                        selected_player["last_name"],
                        selected_player["first_name"],
                        selected_player["date_of_birth"],
                        selected_player["national_id"]
                    )
                    self.tournament.add_player(player)
                    print(f"{player.first_name} {player.last_name} a été ajouté au tournoi.")
                    return
                else:
                    print("Numéro invalide, veuillez réessayer.")
            else:
                filter_str += input_str  # Add letter to filter to refine results

    def _load_players(self):
        """Loads players from the consistent JSON file path."""
        try:
            with open(PLAYERS_JSON_PATH, 'r', encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print("Fichier du joueur introuvable.")
            return []

    def _save_players(self, players: List[Dict[str, str]]):
        """Saves players to the consistent JSON file path."""
        PLAYERS_JSON_PATH.parent.mkdir(exist_ok=True)  # Ensure the 'data' directory exists
        with open(PLAYERS_JSON_PATH, 'w', encoding="utf-8") as f:
            json.dump(players, f, indent=4, ensure_ascii=False)


    def start_tournament(self):
        """Starts the tournament if the conditions are met."""
        if not self.tournament or len(self.tournament.players) < 2:
            print("Au moins 2 joueurs sont requis pour démarrer le tournoi.")
            return

        for round_num in range(1, self.tournament.number_of_rounds + 1):
            self.tournament.start_new_round()
            current_round = self.tournament.rounds[-1]
            TournamentView.display_round_info(round_num, current_round.matches)

            # Enter match results
            for match in current_round.matches:
                match.add_points()
                TournamentView.display_match_result(match)

            current_round.finish_round()
            TournamentView.display_rankings(self.tournament.players)

        TournamentView.display_final_results(self.tournament.players)
        print("\n=== Le tournoi est terminé ===")

    def load_tournament(self, filename):
        """Loads a tournament from a JSON file."""
        with open(filename, "r") as file:
            tournament_data = json.load(file)
            self.tournament = Tournament.from_dict(tournament_data)
            TournamentView.display_tournament_info(self.tournament)
