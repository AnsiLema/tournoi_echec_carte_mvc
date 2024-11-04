class TournamentView:
    """Manages the menu and interaction views
     for the chess tournament."""
    def __init__(self, active_view, views):
        """Initializes the active view (for user input)
        and passive views."""
        self.active_view = active_view
        self.views = views

    def start_tournament(self):
        name=self.active_view.get_name()
        location=self.active_view.get_location()
        date=self.active_view.get_date()
        description=self.active_view.get_description()
        number_of_rounds=self.active_view.get_number_of_rounds()
        self.views['tournament'].create_tournament(name, location,
                                                   date,
                                                   description,
                                                   number_of_rounds)
        return name, location, date, description, number_of_rounds

