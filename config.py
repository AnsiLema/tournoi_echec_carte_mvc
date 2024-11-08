import json
from pathlib import Path

# Define the path for data files
DATA_DIR = Path("data")
PLAYERS_JSON_PATH = DATA_DIR/"players.json"
TOURNAMENTS_JSON_PATH = DATA_DIR/"tournaments.json"

# Ensure directories exists
DATA_DIR.mkdir(exist_ok=True)

# Loading data functions
def load_json_data(file_path):
    """Load JSON data from a file."""
    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    else:
        return {}

# Saving data function
def save_json_data(data, file_path):
    """Save data to a JSON file, ensuring the file is updated"""
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

#load players data
def load_players():
    return load_json_data(PLAYERS_JSON_PATH)

# Save players data
def save_players(players):
    save_json_data(players, PLAYERS_JSON_PATH)

#load tournament data
def load_tournament():
    return load_json_data(TOURNAMENTS_JSON_PATH)

#save tournament data
def save_tournaments(tournament):
    save_json_data(tournament, TOURNAMENTS_JSON_PATH)
