import datetime
from models.model_match import Match


class Round:
    def __init__(self, name):
        self.name = name
        self.matches = []
        self.start_date = datetime.datetime.now()
        self.end_date = None

    def add_match(self, match):
        """Adds a match to the round."""
        self.matches.append(match)

    def finish_round(self):
        """Marks the round as finished and records the end date."""
        self.end_date = datetime.datetime.now()

    def to_dict(self):
        return {
            "name": self.name,
            "matches": [match.to_dict() for match in self.matches]
        }

    @classmethod
    def from_dict(cls, data, tournament):
        round_instance = cls(name=data["name"])
        round_instance.matches = [Match.from_dict(m_data, tournament)
                                  for m_data in data["matches"]]
        return round_instance

    def __repr__(self):
        return (f"{self.name} - Début: {self.start_date},"
                f" Fin: {self.end_date} "
                f"- Matches: {len(self.matches)}")
