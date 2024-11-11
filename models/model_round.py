import datetime
from models.model_match import Match  # Import Match if you have a Match class with to_dict/from_dict methods

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
        """Converts the Round instance to a dictionary for JSON serialization."""
        return {
            "name": self.name,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "matches": [match.to_dict() for match in self.matches]
        }

    @classmethod
    def from_dict(cls, data):
        """Creates a Round instance from a dictionary."""
        round_instance = cls(data["name"])
        round_instance.start_date = datetime.datetime.fromisoformat(data["start_date"])
        round_instance.end_date = datetime.datetime.fromisoformat(data["end_date"]) if data["end_date"] else None
        round_instance.matches = [Match.from_dict(m) for m in data["matches"]]
        return round_instance

    def __repr__(self):
        return (f"{self.name} - Début: {self.start_date}, Fin: {self.end_date} "
                f"- Matches: {len(self.matches)}")
