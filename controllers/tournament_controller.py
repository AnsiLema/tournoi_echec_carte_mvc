from config import (load_players, save_players,
                    load_all_tournaments, save_tournament)
from models.model_player import Player
from models.model_match import Match
from models.model_tournament import Tournament
from views.tournament_view import TournamentView
from views.player_view import PlayerMenuView


class TournamentController:
    def __init__(self):
        self.tournament = None
        self.players = load_players()

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
        if number_of_rounds is None:
            number_of_rounds = 4

        self.tournament = Tournament(name, location, start_date, end_date, description, number_of_rounds)
        self.tournament.id = self._get_next_id()
        TournamentView.display_tournament_info(self.tournament)
        self._save_current_tournament()

    def load_all_players(self):
        """Load all players from players.json and return a dictionary with national_id as the key."""
        players_data = load_players()
        all_players = {p["national_id"]: Player.from_dict(p) for p in players_data}
        return all_players

    def load_tournament_by_id(self, tournament_id):
        """Load a tournament by its ID and return the tournament object."""
        tournaments = load_all_tournaments()
        tournament_data = next((t for t in tournaments if t['id'] == tournament_id), None)

        if tournament_data:
            all_players = self.load_all_players()
            self.tournament = Tournament.from_dict(tournament_data, all_players)
            return self.tournament
        else:
            TournamentView.display_tournament_not_found()
            return None

    def can_resume_tournament(self):
        """Check if there are any remaining rounds to play."""
        if self.tournament and len(self.tournament.rounds) < self.tournament.number_of_rounds:
            return True
        return False

    def add_players(self):
        """
        Method to add players required for a tournament.

        This method ensures that the number of players is equal to double
        the number of rounds in the tournament. It prompts the user to either
        add a new player or select an existing one until the necessary number
        of players is reached, then saves the tournament state and notifies
        that the tournament is ready to start.
        """
        required_players = self.tournament.number_of_rounds * 2

        while len(self.tournament.players) < required_players:
            PlayerMenuView.display_player_count(len(self.tournament.players), required_players)
            add_choice = PlayerMenuView.get_add_choice()

            if add_choice == '1':
                self._add_new_player(self.players)
            elif add_choice == '2':
                self._select_player(self.players)
            else:
                PlayerMenuView.display_invalid_option()

            self._save_current_tournament()

        PlayerMenuView.display_ready_to_start()

    def _is_player_already_added(self, national_id):
        """Check if a player with the given national_id is already in the tournament."""
        return any(player.national_id == national_id for player in self.tournament.players)

    def _add_new_player(self, players):
        """
        Adds a new player to the list of players and the current tournament if they are not
        already added.
        """
        last_name, first_name, date_of_birth, national_id = PlayerMenuView.display_add_player_menu()

        if self._is_player_already_added(national_id):
            PlayerMenuView.display_player_already_added()
            return

        new_player = {
            "last_name": last_name,
            "first_name": first_name,
            "date_of_birth": date_of_birth,
            "national_id": national_id
        }
        players.append(new_player)
        save_players(players)

        player = Player(last_name, first_name, date_of_birth, national_id)
        self.tournament.add_player(player)
        PlayerMenuView.display_add_player_success_menu()

    def _select_player(self, players):
        """
        Select a player from a list of players based on user input, apply a filter, and add the selected player to the
        tournament if not already added.

        Summary:
            This method provides a menu to filter and select players in a tournament. If the player is
            already added, it notifies the user. The process involves continuously prompting the user to
            filter the list and select a player until a valid selection is made. The selected player is
            then added to the tournament and the current state is saved.

        Args:
            players (list[dict]): List of player information dictionaries, where each dictionary contains player details
                                  such as 'last_name', 'first_name', 'date_of_birth', and 'national_id'.
        """
        while True:
            filter_str = PlayerMenuView.get_player_filter()
            filtered_players = [p for p in players if p["last_name"].lower().startswith(filter_str)]

            if not filtered_players:
                PlayerMenuView.display_no_matching_players()
                continue

            PlayerMenuView.display_filtered_players(filtered_players)
            input_str = PlayerMenuView.get_player_selection()

            if input_str.isdigit():
                choice = int(input_str) - 1
                if 0 <= choice < len(filtered_players):
                    selected_player = filtered_players[choice]

                    if self._is_player_already_added(selected_player["national_id"]):
                        PlayerMenuView.display_player_already_added()
                        continue

                    player = Player(
                        selected_player["last_name"],
                        selected_player["first_name"],
                        selected_player["date_of_birth"],
                        selected_player["national_id"]
                    )
                    self.tournament.add_player(player)
                    PlayerMenuView.display_player_added(player)
                    self._save_current_tournament()
                    return
                else:
                    PlayerMenuView.display_invalid_number()
            elif input_str.lower() == 'r':
                continue
            else:
                PlayerMenuView.display_invalid_entry()

    def start_tournament(self):
        """Start the tournament by iterating through rounds and matches."""
        if not self.tournament or len(self.tournament.players) < 2:
            TournamentView.display_insufficient_players()
            return

        starting_round = len(self.tournament.rounds) + 1
        for round_num in range(starting_round, self.tournament.number_of_rounds + 1):
            self.tournament.start_new_round()
            current_round = self.tournament.rounds[-1]
            TournamentView.display_round_info(round_num, current_round.matches)

            for match in current_round.matches:
                result = TournamentView.get_match_result(match.match[0][0], match.match[1][0])
                match.add_points(result)
                TournamentView.display_match_result(match)

            current_round.finish_round()
            self._save_current_tournament()

            # Display rankings only for intermediate rounds
            if round_num < self.tournament.number_of_rounds:
                TournamentView.display_rankings(self.tournament.players)

            # Do not ask to continue if it's the last round
            if round_num == self.tournament.number_of_rounds:
                break

            # Ask user if he wants to continue the tournament
            continue_choice = TournamentView.ask_to_continue_after_round()
            if continue_choice != "o":
                TournamentView.display_tournament_paused()
                break

        # Check if the tournament is completed
        if len(self.tournament.rounds) == self.tournament.number_of_rounds:
            self.tournament.mark_as_completed()
            self._save_current_tournament()
            TournamentView.display_final_results(self.tournament.players)

    def _save_current_tournament(self):
        """ Saves the current tournament to tournaments.json."""
        if self.tournament:
            tournament_data = self.tournament.to_dict()
            save_tournament(tournament_data)

    def get_all_players_sorted(self):
        """Return a list of all players in alphabetical order."""
        players = load_players()
        return sorted(players, key=lambda p: p['last_name'])

    def get_all_tournaments(self):
        """Return a list of all tournaments."""
        return load_all_tournaments()

    def search_tournaments_by_name(self, search_str):
        """Search for tournaments whose names contain the given letters, case-insensitive."""
        tournaments = load_all_tournaments()
        return [t for t in tournaments
                if search_str.lower() in t['name'].lower()]

    def get_tournament_details(self, tournament_id):
        """Return the name and dates of a specific tournament."""
        tournaments = load_all_tournaments()
        tournament = next((t for t in tournaments if t['id']
                           == tournament_id), None)
        if tournament:
            return (tournament['name'],
                    tournament['start_date'],
                    tournament['end_date'])
        return None

    def get_tournament_players_sorted(self, tournament_id):
        """Return a list of players in a tournament, sorted alphabetically."""
        # Load tournament data and find the matching tournament
        tournaments = load_all_tournaments()
        tournament = next((t for t in tournaments if t['id'] == tournament_id), None)

        if tournament:
            # Load all players from players.json
            all_players = self.load_all_players()

            # Retrieve full Player objects using national_id
            players = [
                all_players[player_data['national_id']]
                for player_data in tournament.get('players', [])
                if player_data['national_id'] in all_players
            ]

            # Sort players by "last_name" (alphabetical order)
            sorted_players = sorted(players, key=lambda p: p.last_name)
            return sorted_players

        return []

    def get_tournament_rounds_and_matches(self, tournament_id):
        """Return a list of rounds and matches for a tournament."""
        tournaments = load_all_tournaments()
        tournament = next((t for t in tournaments if t['id']
                           == tournament_id), None)
        if tournament:
            return tournament.get('rounds', [])
        return []

    @staticmethod
    def prepare_rounds_and_matches(rounds, tournament):
        """Transform rounds and matches into a format suitable for the view."""
        prepared_rounds = []
        for round_info in rounds:
            prepared_matches = []
            for match_data in round_info.get('matches', []):
                match = Match.from_dict(match_data, tournament)
                if match:
                    prepared_matches.append({
                        'player1_name': str(match.match[0][0]),
                        'player2_name': str(match.match[1][0]),
                        'score1': match.match_score1,
                        'score2': match.match_score2
                    })
                else:
                    prepared_matches.append({'error': "Match invalide ou joueurs introuvables"})

            prepared_rounds.append({
                'name': round_info['name'],
                'start_date': round_info.get('start_date', 'Date de début non définie'),
                'end_date': round_info.get('end_date', 'Date de fin non définie'),
                'matches': prepared_matches
            })
        return prepared_rounds
