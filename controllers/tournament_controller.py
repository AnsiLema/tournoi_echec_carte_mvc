import json
from typing import List, Dict
from config import PLAYERS_JSON_PATH, TOURNAMENTS_DIR
from models.model_player import Player
from models.model_tournament import Tournament
from views.tournament_view import TournamentView
from views.player_view import PlayerMenuView
from pathlib import Path

class TournamentController:
    def __init__(self):
        self.tournament = None
        self.players = self._load_players()

    def _get_next_id(self):
        """Retrieve the next available 4-digit tournament ID."""
        tournaments = self._load_tournaments()

        # Find the maximum existing ID
        if tournaments:
            max_id = max(int(t["id"]) for t in tournaments if "id" in t)
            next_id = max_id + 1
        else:
            next_id = 1  # Start with ID 0001 if no tournaments exist

        return f"{next_id:04d}"

    def create_tournament(self, name, location, start_date, end_date, description, number_of_rounds):
        """Initializes a new tournament with a unique 4-digit ID."""
        self.tournament = Tournament(name, location, start_date, end_date, description, number_of_rounds)
        self.tournament.id = self._get_next_id()  # Assign a sequential 4-digit ID to the tournament

        TournamentView.display_tournament_info(self.tournament)
        self._save_tournament()  # Save the new tournament with ID

    def get_all_tournaments(self):
        """Retrieve all available tournaments with their IDs and names from the directory."""
        tournaments = []
        for file_path in TOURNAMENTS_DIR.glob("tournament_*.json"):
            with open(file_path, "r", encoding="utf-8") as file:
                tournament_data = json.load(file)
                tournaments.append(tournament_data)
        return tournaments

    def load_tournament_by_id(self, tournament_id):
        """Load a tournament by its unique ID from a single JSON file."""
        tournament_file = Path(TOURNAMENTS_DIR) / f"tournament_{tournament_id}.json"
        try:
            with open(tournament_file, "r", encoding="utf-8") as file:
                tournament_data = json.load(file)
                self.tournament = Tournament.from_dict(tournament_data)  # Assuming from_dict deserializes full details
                return True
        except FileNotFoundError:
            print("Tournoi introuvable.")
            return False

    def can_resume_tournament(self):
        """Check if there are any remaining rounds to play."""
        if self.tournament and len(self.tournament.rounds) < self.tournament.number_of_rounds:
            return True
        return False

    def add_players(self):
        """Handles adding players until the user decides to start the tournament."""
        while True:
            choice = input("Sélectionnez une option :\n1. Ajouter un joueur\n2. Commencer le tournoi\n> ")
            if choice == '1':
                add_choice = input("Voulez-vous :\n1. Créer un nouveau joueur\n2. Sélectionner un joueur existant\n> ")
                if add_choice == '1':
                    self._add_new_player(self.players)
                elif add_choice == '2':
                    self._select_player(self.players)
                else:
                    print("Option non valide, veuillez réessayer.")
                print(f"Nombre de joueurs enregistrés: {len(self.tournament.players)}")
            elif choice == '2' and len(self.tournament.players) >= 2:
                break
            else:
                print("Au moins 2 joueurs sont requis pour démarrer le tournoi.")

    def _add_new_player(self, players):
        last_name, first_name, date_of_birth, national_id = PlayerMenuView.display_add_player_menu()
        new_player = {"last_name": last_name, "first_name": first_name, "date_of_birth": date_of_birth,
                      "national_id": national_id}
        players.append(new_player)
        self._save_players(players)
        player = Player(last_name, first_name, date_of_birth, national_id)
        self.tournament.add_player(player)
        PlayerMenuView.display_add_player_success_menu()

    def _select_player(self, players):
        filter_str = ""
        while True:
            filtered_players = [p for p in players if
                                filter_str.lower() in p["last_name"].lower() or filter_str.lower() in p[
                                    "first_name"].lower()]
            if not filtered_players:
                print("Aucun joueur ne correspond à ce filtre.")
                return

            for i, player in enumerate(filtered_players, start=1):
                print(f"{i}. {player['first_name']} {player['last_name']} (ID: {player['national_id']})")

            input_str = input("Entrez une lettre pour filtrer ou un numéro pour sélectionner un joueur : ")
            if input_str.isdigit():
                choice = int(input_str) - 1
                if 0 <= choice < len(filtered_players):
                    selected_player = filtered_players[choice]
                    player = Player(selected_player["last_name"], selected_player["first_name"],
                                    selected_player["date_of_birth"], selected_player["national_id"])
                    self.tournament.add_player(player)
                    print(f"{player.first_name} {player.last_name} a été ajouté au tournoi.")
                    return
                else:
                    print("Numéro invalide, veuillez réessayer.")
            else:
                filter_str += input_str

    def _load_players(self):
        try:
            with open(PLAYERS_JSON_PATH, 'r', encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print("Fichier du joueur introuvable.")
            return []

    def _save_players(self, players: List[Dict[str, str]]):
        PLAYERS_JSON_PATH.parent.mkdir(exist_ok=True)
        with open(PLAYERS_JSON_PATH, 'w', encoding="utf-8") as f:
            json.dump(players, f, indent=4, ensure_ascii=False)

    def start_tournament(self):
        if not self.tournament or len(self.tournament.players) < 2:
            print("Au moins 2 joueurs sont requis pour démarrer le tournoi.")
            return

        # Start from the next round if there are unfinished rounds
        starting_round = len(self.tournament.rounds) + 1

        for round_num in range(starting_round, self.tournament.number_of_rounds + 1):
            self.tournament.start_new_round()
            current_round = self.tournament.rounds[-1]
            TournamentView.display_round_info(round_num, current_round.matches)

            for match in current_round.matches:
                match.add_points()
                TournamentView.display_match_result(match)

            current_round.finish_round()
            # Save the entire tournament after each round
            self._save_tournament()
            TournamentView.display_rankings(self.tournament.players)

        TournamentView.display_final_results(self.tournament.players)
        print("\n=== Le tournoi est terminé ===")

    def _load_tournaments(self):
        """Load all tournaments by reading each JSON file in the tournaments directory."""
        tournaments = []
        for file_path in Path(TOURNAMENTS_DIR).glob("tournament_*.json"):
            with open(file_path, "r", encoding="utf-8") as file:
                tournament_data = json.load(file)
                tournaments.append(tournament_data)
        return tournaments

    def _save_tournament(self):
        """Save the entire tournament, including players and rounds, to a single JSON file."""
        tournament_data = self.tournament.to_dict()  # Convert tournament to a dictionary
        tournament_file = Path(TOURNAMENTS_DIR) / f"tournament_{self.tournament.id}.json"

        tournament_file.parent.mkdir(parents=True, exist_ok=True)  # Ensure directory exists

        try:
            with open(tournament_file, "w", encoding="utf-8") as file:
                json.dump(tournament_data, file, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving tournament data: {e}")

