class TournamentView:
    def __init__(self, active_view, views):
        self.active_view = active_view
        self.views = views

    def start_tournament(self):
        self.active_view = self.views['tournament']
