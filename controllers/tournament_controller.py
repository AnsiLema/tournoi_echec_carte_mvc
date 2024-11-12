import json
from typing import List, Dict
from config import load_players, save_players, load_all_tournaments, save_tournament
from models.model_player import Player
from models.model_tournament import Tournament
from views.tournament_view import TournamentView
from views.player_view import PlayerMenuView


class TournamentController:
    def __init__(self):
        self.tournament = None
        self.players = load_players()  # Load players from players.json

    def _get_next_id(self):
        """Retrieve the next available 4-digit tournament ID."""
        tournaments = load_all_tournaments()
        if tournaments:
            max_id = max(int(t["id"]) for t in tournaments if "id" in t)
            next_id = max_id + 1
        else:
            next_id = 1  # Start with ID 0001 if no tournaments exist
        return f"{next_id:04d}"

    def create_tournament(self, name, location, start_date, end_date, description, number_of_rounds):
        """Initialize a new tournament with a unique 4-digit ID."""
        self.tournament = Tournament(name, location, start_date, end_date, description, number_of_rounds)
        self.tournament.id = self._get_next_id()  # Assign a sequential 4-digit ID to the tournament

        TournamentView.display_tournament_info(self.tournament)
        self._save_current_tournament()  # Save the new tournament with ID

    def get_all_tournaments(self):
        """Retrieve all tournaments from tournaments.json."""
        return load_all_tournaments()

    def load_tournament_by_id(self, tournament_id):
        """Load a tournament by its unique ID from tournaments.json."""
        tournaments = load_all_tournaments()
        tournament_data = next((t for t in tournaments if t["id"] == tournament_id), None)
        if tournament_data:
            self.tournament = Tournament.from_dict(tournament_data)  # Assuming from_dict deserializes full details
            return True
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
                self._save_current_tournament()  # Save tournament state after each player addition
            elif choice == '2' and len(self.tournament.players) >= 2:
                break
            else:
                print("Au moins 2 joueurs sont requis pour démarrer le tournoi.")

    def _add_new_player(self, players):
        last_name, first_name, date_of_birth, national_id = PlayerMenuView.display_add_player_menu()
        new_player = {"last_name": last_name, "first_name": first_name, "date_of_birth": date_of_birth,
                      "national_id": national_id}
        players.append(new_player)
        save_players(players)  # Save all players to players.json
        player = Player(last_name, first_name, date_of_birth, national_id)
        self.tournament.add_player(player)
        PlayerMenuView.display_add_player_success_menu()

    def _select_player(self, players):
        filter_str = ""
        while True:
            filtered_players = [p for p in players if
                                filter_str.lower() in p["last_name"].lower() or filter_str.lower() in p["first_name"].lower()]
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
                    self._save_current_tournament()  # Save tournament after adding a player
                    return
                else:
                    print("Numéro invalide, veuillez réessayer.")
            else:
                filter_str += input_str

    def start_tournament(self):
        """Begins the tournament, saving after each round completes."""
        if not self.tournament or len(self.tournament.players) < 2:
            print("Au moins 2 joueurs sont requis pour démarrer le tournoi.")
            return

        starting_round = len(self.tournament.rounds) + 1
        for round_num in range(starting_round, self.tournament.number_of_rounds + 1):
            self.tournament.start_new_round()
            current_round = self.tournament.rounds[-1]
            TournamentView.display_round_info(round_num, current_round.matches)

            for match in current_round.matches:
                match.add_points()
                TournamentView.display_match_result(match)

            current_round.finish_round()
            # Save tournament state after each round
            self._save_current_tournament()
            TournamentView.display_rankings(self.tournament.players)

        TournamentView.display_final_results(self.tournament.players)
        print("\n=== Le tournoi est terminé ===")

    def _save_current_tournament(self):
        """Save or update the current tournament in tournaments.json."""
        if self.tournament:
            tournament_data = self.tournament.to_dict()
            save_tournament(tournament_data)  # Save using config function
