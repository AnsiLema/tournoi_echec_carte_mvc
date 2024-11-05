from faker import Faker
from models.model_player import Player
from models.model_tournament import Tournament

def get_tournaments():
    # Initialisation du tournoi
    tournament = Tournament("Chess Championship", "Paris", "2023-10-01",
                            "2023-10-15", "Annual Chess Tournament", 4)
    fake = Faker('fr_FR')

    # Création et ajout de 8 joueurs fictifs
    for _ in range(8):
        firstname = fake.first_name()
        lastname = fake.last_name()
        birthdate = fake.date_of_birth(minimum_age=18, maximum_age=60).strftime("%d/%m/%Y")
        national_id = fake.unique.bothify(text='??#####')
        player = Player(firstname, lastname, birthdate, national_id)
        tournament.add_player(player)

    # Boucle pour chaque round
    for round_num in range(1, tournament.number_of_rounds + 1):
        print(f"\n=== Début du {round_num}e Round ===")

        # Démarre un nouveau round et génère les paires de matchs
        tournament.start_new_round()
        current_round = tournament.rounds[-1]  # Le dernier round ajouté

        # Affiche les paires de matchs
        print(f"{current_round.name} - Oppositions :")
        for match in current_round.matches:
            print(match)

        # Saisie des résultats des matchs
        for match in current_round.matches:
            match.add_points(match)

        # Fin du round
        current_round.finish_round()

        # Affichage des classements
        print("\nClassement après ce round :")
        sorted_players = sorted(tournament.players, key=lambda p: p.score, reverse=True)
        for rank, player in enumerate(sorted_players, start=1):
            print(f"{rank}. {player} - Score: {player.score}")

    # Résultats finaux
    print("\n=== Résultats finaux du tournoi ===")
    sorted_players = sorted(tournament.players, key=lambda p: p.score, reverse=True)
    for rank, player in enumerate(sorted_players, start=1):
        print(f"{rank}. {player} - Score: {player.score}")

    print("\n=== Le tournoi est terminé ===")

# Appel de la fonction pour démarrer le processus du tournoi
get_tournaments()
