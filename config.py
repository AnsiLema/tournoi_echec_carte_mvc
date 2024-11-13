import json
from pathlib import Path

# Define the main data directory path
DATA_DIR = Path("data")

# Paths for specific JSON files and directories
PLAYERS_JSON_PATH = DATA_DIR / "players.json"
TOURNAMENTS_JSON_PATH = DATA_DIR / "tournaments.json"

# Ensure the main data directory exists
DATA_DIR.mkdir(exist_ok=True)


# Utility function to load JSON data from a file
def load_json_data(file_path):
    """Load JSON data from a file."""
    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    return []  # Return an empty list if the file doesn't exist


# Utility function to save JSON data to a file
def save_json_data(data, file_path):
    """Save data to a JSON file."""
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


# Load players from players.json
def load_players():
    return load_json_data(PLAYERS_JSON_PATH)


# Save players to players.json
def save_players(players):
    save_json_data(players, PLAYERS_JSON_PATH)


# Load all tournaments from tournaments.json
def load_all_tournaments():
    return load_json_data(TOURNAMENTS_JSON_PATH)


# Save all tournaments to tournaments.json
def save_all_tournaments(tournaments):
    save_json_data(tournaments, TOURNAMENTS_JSON_PATH)


# Save or update a single tournament in tournaments.json
def save_tournament(tournament_data):
    """Save or update a single tournament in tournaments.json."""
    tournaments = load_all_tournaments()

    # Update if tournament exists, otherwise append
    for i, tournament in enumerate(tournaments):
        if tournament["id"] == tournament_data["id"]:
            tournaments[i] = tournament_data
            break
    else:
        tournaments.append(tournament_data)  # Add new tournament if not found

    # Save updated list of tournaments back to file
    save_all_tournaments(tournaments)
