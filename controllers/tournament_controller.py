from config import (load_players, save_players,
                    load_all_tournaments,
                    save_tournament)
from models.model_player import Player
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

    def create_tournament(self, name,
                          location,
                          start_date,
                          end_date,
                          description,
                          number_of_rounds):
        """Initialize a new tournament with a unique 4-digit ID."""
        # Create the tournament, allowing end_date to be None
        self.tournament = Tournament(name,
                                     location,
                                     start_date,
                                     end_date,
                                     description,
                                     number_of_rounds)
        self.tournament.id = self._get_next_id()
        TournamentView.display_tournament_info(self.tournament)
        self._save_current_tournament()

    def load_all_players(self):
        """Load all players from players.json and return a dictionary with national_id as the key."""
        players_data = load_players()  # Charge les données des joueurs depuis un fichier
        all_players = {p["national_id"]: Player.from_dict(p) for p in players_data}
        return all_players

    def get_unfinished_tournaments(self):
        """Retrieve only incomplete tournaments from tournaments.json."""
        tournaments = load_all_tournaments()
        return [t for t in tournaments if not t.get("completed", False)]

    def load_tournament_by_id(self, tournament_id):
        """Load a tournament by its ID and return the tournament object, not a bool."""
        tournaments = load_all_tournaments()
        tournament_data = next((t for t in tournaments if t['id'] == tournament_id), None)

        if tournament_data:
            # Charger tous les joueurs avant de créer le tournoi
            all_players = self.load_all_players()  # Cette fonction doit retourner un dictionnaire de tous les joueurs

            # Passer all_players à from_dict
            self.tournament = Tournament.from_dict(tournament_data, all_players)
            return self.tournament  # Return the Tournament object
        else:
            print("Tournoi non trouvé ou déjà terminé.")
            return None  # Return None if not found

    def can_resume_tournament(self):
        """Check if there are any remaining rounds to play."""
        if (self.tournament and len(self.tournament.rounds)
                < self.tournament.number_of_rounds):
            return True
        return False

    def add_players(self):
        """Gère l'ajout de joueurs jusqu'à ce que le nombre requis de joueurs soit atteint."""
        # Calculer le nombre requis de joueurs en fonction du nombre de rounds
        required_players = self.tournament.number_of_rounds * 2

        while len(self.tournament.players) < required_players:
            print(f"Nombre de joueurs enregistrés : {len(self.tournament.players)}"
                  f" / {required_players} requis")

            add_choice = input("Voulez-vous :\n"
                               "1. Créer un nouveau joueur\n"
                               "2. Sélectionner un joueur existant\n> ")

            if add_choice == '1':
                self._add_new_player(self.players)
            elif add_choice == '2':
                self._select_player(self.players)
            else:
                print("Option non valide, veuillez réessayer.")

            self._save_current_tournament()

        print("Le nombre requis de joueurs a été atteint. Le tournoi peut commencer.")

    def _add_new_player(self, players):
        (last_name, first_name,
         date_of_birth,
         national_id) = PlayerMenuView.display_add_player_menu()
        new_player = {"last_name": last_name,
                      "first_name": first_name,
                      "date_of_birth": date_of_birth,
                      "national_id": national_id}
        players.append(new_player)
        save_players(players)
        player = Player(last_name,
                        first_name,
                        date_of_birth,
                        national_id)
        self.tournament.add_player(player)
        PlayerMenuView.display_add_player_success_menu()

    def _select_player(self, players):
        while True:
            filter_str = input(
                "Entrez une lettre ou plusieurs lettres pour filtrer"
                " les joueurs par nom de famille, "
                "puis un numéro pour sélectionner : ").strip().lower()

            filtered_players = [
                p for p in players if p["last_name"].lower().
                startswith(filter_str)
            ]

            if not filtered_players:
                print("Aucun joueur ne correspond à ce filtre.")
                continue  # Prompt the user for input again

            # Display filtered players with numbered list
            for i, player in enumerate(filtered_players, start=1):
                print(f"{i}. {player['first_name']} {player['last_name']}"
                      f" (ID: {player['national_id']})")

            input_str = input("Entrez le numéro pour sélectionner un joueur "
                              "ou 'r' pour réessayer le filtre : ").strip()

            if input_str.isdigit():
                choice = int(input_str) - 1
                if 0 <= choice < len(filtered_players):
                    selected_player = filtered_players[choice]
                    player = Player(selected_player["last_name"],
                                    selected_player["first_name"],
                                    selected_player["date_of_birth"],
                                    selected_player["national_id"])
                    self.tournament.add_player(player)
                    print(f"{player.first_name} {player.last_name}"
                          f" a été ajouté au tournoi.")
                    self._save_current_tournament()
                    return
                else:
                    print("Numéro invalide, veuillez réessayer.")
            elif input_str.lower() == 'r':
                # Allows the user to re-enter a filter string
                continue
            else:
                print("Entrée invalide, veuillez réessayer.")

    def start_tournament(self):
        """Begins the tournament,
        marking it as completed when finished.
        """
        if not self.tournament or len(self.tournament.players) < 2:
            print("Au moins 2 joueurs sont requis pour démarrer le tournoi.")
            return

        starting_round = len(self.tournament.rounds) + 1
        for round_num in range(starting_round,
                               self.tournament.number_of_rounds + 1):
            self.tournament.start_new_round()
            current_round = self.tournament.rounds[-1]
            TournamentView.display_round_info(round_num,
                                              current_round.matches)

            for match in current_round.matches:
                match.add_points()
                TournamentView.display_match_result(match)

            current_round.finish_round()
            # Save tournament state after each round
            self._save_current_tournament()
            TournamentView.display_rankings(self.tournament.players)

        if len(self.tournament.rounds) == self.tournament.number_of_rounds:
            self.tournament.mark_as_completed()
            self._save_current_tournament()
            TournamentView.display_final_results(self.tournament.players)
            print("\n=== Le tournoi est terminé ===")

    def _save_current_tournament(self):
        """Save or update the current tournament in tournaments.json."""
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
        """Search for tournaments whose names contain the given letters,
         case-insensitive.
         """
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
        """Return a list of players in a tournament,
         sorted alphabetically.
         """
        tournaments = load_all_tournaments()
        tournament = next((t for t in tournaments if t['id']
                           == tournament_id), None)
        if tournament:
            players = tournament.get('players', [])
            return sorted(players, key=lambda p: p['last_name'])
        return []

    def get_tournament_rounds_and_matches(self, tournament_id):
        """Return a list of rounds and matches for a tournament."""
        tournaments = load_all_tournaments()
        tournament = next((t for t in tournaments if t['id']
                           == tournament_id), None)
        if tournament:
            return tournament.get('rounds', [])
        return []
