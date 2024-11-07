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
            choice = PlayerMenuView.display_player_menu()
            if choice == '1':
                self._add_new_player(players)
                # Show the updated player count after each new addition
                print(f"Total players registered: {len(self.tournament.players)}")
            elif choice == '2':
                self._select_player(players)
                # Show the updated player count after each selection
                print(f"Total players registered: {len(self.tournament.players)}")
            else:
                print("Invalid option.")

            # Confirm if the user wants to start the tournament
            confirmation = PlayerMenuView.display_start_tournament_confirmation()
            if confirmation == '':
                if len(self.tournament.players) >= 2:
                    break  # Start the tournament
                else:
                    print("At least 2 players are required to start the tournament.")
            elif confirmation.lower() == 'return':
                continue  # Return to menu

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
        """Allows selecting an existing player by filtering based on the beginning of the last name."""
        filter_str = ""
        while True:
            # Display players filtered by the beginning of last_name
            filtered_players = [p for p in players if p["last_name"].lower().startswith(filter_str.lower())]

            if not filtered_players:
                print("No players match this filter.")
                return  # Return to main menu if no matches

            # Display filtered players with their full information
            print("\nMatching Players:")
            for i, player in enumerate(filtered_players, start=1):
                print(f"{i}. {player['first_name']} {player['last_name']} (ID: {player['national_id']})")

            # User input to continue filtering or to select a player
            input_str = input("Enter a letter to filter by last name or a number to select a player: ")
            if input_str.isdigit():  # Check if input is a number
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
                    print(f"{player.first_name} {player.last_name} has been added to the tournament.")
                    return
                else:
                    print("Invalid number, please try again.")
            else:
                # Add the input to filter_str to refine the search by the beginning of last_name
                filter_str += input_str

    def _load_players(self):
        """Loads players from the consistent JSON file path."""
        try:
            with open(PLAYERS_JSON_PATH, 'r', encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print("Player file not found.")
            return []

    def _save_players(self, players: List[Dict[str, str]]):
        """Saves players to the consistent JSON file path."""
        PLAYERS_JSON_PATH.parent.mkdir(exist_ok=True)  # Ensure the 'data' directory exists
        with open(PLAYERS_JSON_PATH, 'w', encoding="utf-8") as f:
            json.dump(players, f, indent=4, ensure_ascii=False)


    def start_tournament(self):
        """Starts the tournament if the conditions are met."""
        if not self.tournament or len(self.tournament.players) < 2:
            print("At least 2 players are required to start the tournament.")
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
        print("\n=== The tournament is over ===")

    def load_tournament(self, filename):
        """Loads a tournament from a JSON file."""
        with open(filename, "r") as file:
            tournament_data = json.load(file)
            self.tournament = Tournament.from_dict(tournament_data)
            TournamentView.display_tournament_info(self.tournament)
