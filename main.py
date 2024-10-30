from models.model_player import Player
from models.model_tournament import Tournament

tournament = Tournament("Chess Championship", "Paris", "2023-10-01",
                        "2023-10-15", "Annual Chess Tournament",
                        5)

player1 = Player("Lema", "A'nsi", "02/03/1984", "DE15557")
tournament.add_player(player1)

# Afficher les joueurs pour vérifier
for player in tournament.players:
    print(vars(player))