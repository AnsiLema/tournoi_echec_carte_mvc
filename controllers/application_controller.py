from controllers.tournament_controller import TournamentController
from views.main_menu_view import MainMenuView
from views.tournament_view import TournamentView


class ApplicationController:
    """Main application controller."""
    def __init__(self):
        self.tournament_controller = TournamentController()

    def run(self):
        """Main program loop."""
        while True:
            choice = MainMenuView.display_main_menu()
            if choice == "1":
                self.start_new_tournament()
            elif choice == "2":
                self.load_existing_tournament()
            elif choice == "3":
                self.show_reports()
            elif choice == "4":
                MainMenuView.display_quit_message()
                break
            else:
                MainMenuView.display_invalid_choice()

    def show_reports(self):
        """Display the reports menu and handle the selected report."""
        while True:
            report_choice = MainMenuView.display_reports_menu()
            if report_choice in ["3", "4", "5"]:
                search_str = MainMenuView.get_tournament_search_input()
                filtered_tournaments = self.tournament_controller.search_tournaments_by_name(search_str)

                if not filtered_tournaments:
                    TournamentView.display_no_matching_tournaments()
                    continue

                TournamentView.display_matching_tournaments(filtered_tournaments)
                selected_index = MainMenuView.get_tournament_selection(len(filtered_tournaments))
                if selected_index is None:
                    continue

                selected_tournament = filtered_tournaments[selected_index]
                tournament_id = selected_tournament['id']
                tournament = self.tournament_controller.load_tournament_by_id(tournament_id)

                if not tournament:
                    TournamentView.display_loading_error()
                    continue

                if report_choice == "3":
                    details = self.tournament_controller.get_tournament_details(tournament_id)
                    if details:
                        TournamentView.display_tournament_details(*details)
                    else:
                        TournamentView.display_tournament_not_found()
                elif report_choice == "4":
                    # Show players sorted alphabetically for a given tournament
                    players_sorted = self.tournament_controller.get_tournament_players_sorted(tournament_id)
                    TournamentView.display_tournament_players(players_sorted)
                elif report_choice == "5":
                    # Show rounds and matches for a given tournament
                    rounds = self.tournament_controller.get_tournament_rounds_and_matches(tournament_id)
                    prepared_rounds = TournamentController.prepare_rounds_and_matches(rounds, tournament)
                    TournamentView.display_tournament_rounds_and_matches(prepared_rounds)
            elif report_choice == "1":
                # Display players from the database
                players = self.tournament_controller.get_all_players_sorted()
                TournamentView.display_all_players(players)
            elif report_choice == "2":
                # Display all tournaments
                tournaments = self.tournament_controller.get_all_tournaments()
                TournamentView.display_all_tournaments(tournaments)
            elif report_choice == "6":
                break
            else:
                MainMenuView.display_invalid_choice()

    def start_new_tournament(self):
        """Initialize and start a new tournament."""
        tournament_details = MainMenuView.get_tournament_details()
        self.tournament_controller.create_tournament(*tournament_details)
        self.tournament_controller.add_players()
        self.tournament_controller.start_tournament()

    def load_existing_tournament(self):
        """Loads an existing tournament by displaying available tournaments for selection."""
        search_str = MainMenuView.get_tournament_search_input()
        filtered_tournaments = self.tournament_controller.search_tournaments_by_name(search_str)

        if not filtered_tournaments:
            TournamentView.display_no_matching_tournaments()
            return

        TournamentView.display_matching_tournaments(filtered_tournaments)
        selected_index = MainMenuView.get_tournament_selection(len(filtered_tournaments))
        if selected_index is None:
            return

        selected_tournament = filtered_tournaments[selected_index]
        tournament_id = selected_tournament['id']

        if self.tournament_controller.load_tournament_by_id(tournament_id):
            TournamentView.display_tournament_loaded_success()

            if self.tournament_controller.can_resume_tournament():
                resume_choice = MainMenuView.get_resume_choice()
                if resume_choice == "o":
                    self.tournament_controller.start_tournament()
                else:
                    MainMenuView.display_return_to_main_menu()
            else:
                TournamentView.display_tournament_already_completed()
        else:
            TournamentView.display_loading_error()
