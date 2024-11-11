import json
from typing import List, Dict
from config import PLAYERS_JSON_PATH, TOURNAMENTS_JSON_PATH, ROUNDS_DIR
from models.model_player import Player
from models.model_tournament import Tournament
from models.model_round import Round
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
        self._save_tournaments([self.tournament])  # Save the new tournament with ID

    def get_all_tournaments(self):
        """Retrieve all available tournaments with their IDs and names."""
        try:
            with open(TOURNAMENTS_JSON_PATH, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def load_tournament_by_id(self, tournament_id):
        """Load a specific tournament by its unique 4-digit ID."""
        tournaments = self.get_all_tournaments()
        selected_tournament = next((t for t in tournaments if t['id'] == tournament_id), None)

        if selected_tournament:
            self.tournament = Tournament.from_dict(selected_tournament)
        else:
            raise FileNotFoundError("Tournoi avec cet ID introuvable.")

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

        for round_num in range(1, self.tournament.number_of_rounds + 1):
            self.tournament.start_new_round()
            current_round = self.tournament.rounds[-1]
            TournamentView.display_round_info(round_num, current_round.matches)

            for match in current_round.matches:
                match.add_points()
                TournamentView.display_match_result(match)

            current_round.finish_round()
            current_round_dict = current_round.to_dict()
            self.save_round(current_round_dict, round_num)
            TournamentView.display_rankings(self.tournament.players)

        TournamentView.display_final_results(self.tournament.players)
        print("\n=== Le tournoi est terminé ===")

    def _load_tournaments(self):
        try:
            with open(TOURNAMENTS_JSON_PATH, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def _save_tournaments(self, tournaments: List[Tournament]):
        TOURNAMENTS_JSON_PATH.parent.mkdir(exist_ok=True)
        with open(TOURNAMENTS_JSON_PATH, "w", encoding="utf-8") as file:
            json.dump([tournament.to_dict() for tournament in tournaments], file, indent=4, ensure_ascii=False)

    def save_round(self, round_data, round_number):
        round_file = ROUNDS_DIR / f"round_{round_number}.json"
        round_file.parent.mkdir(exist_ok=True)
        with open(round_file, "w", encoding="utf-8") as f:
            json.dump(round_data, f, indent=4, ensure_ascii=False)

    def load_round(self, round_number):
        round_file = ROUNDS_DIR / f"round_{round_number}.json"
        try:
            with open(round_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Le fichier pour le Round {round_number} est introuvable.")
            return None
