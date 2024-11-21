# Chess Tournament Application
![Capture d’écran 2024-11-21 à 16 53 17](https://github.com/user-attachments/assets/2c23489a-2f34-4e7b-acb5-564d8dcc0872)


## Description

Cette application permet de gérer un tournoi d'échecs en utilisant Python. Elle suit le schéma MVC (Model-View-Controller) afin de structurer le code de manière claire et séparée. Le but de l'application est de faciliter la gestion des joueurs, des tournois, ainsi que des scores et des rencontres entre les joueurs. L'application fonctionne hors-ligne, et utilise des fichiers JSON pour la persistance des données.

## Fonctionnalités
- Gestion des joueurs : ajout, modification et suppression des joueurs.
- Gestion des tournois : création, planification, et mise à jour des informations du tournoi.
- Gestion des matchs : couplage des joueurs pour les matchs, saisie des scores.
- Persistance des données : enregistrement des joueurs, des tournois et des matchs dans des fichiers JSON.
- Interface utilisateur en ligne de commande.

## Arborescence des Fichiers
Voici une présentation des fichiers principaux de l'application :

```
|-- controllers
|   |-- __init__.py
|   |-- application_controller.py
|   |-- tournament_controller.py
|
|-- data
|   |-- players.json
|   |-- tournaments.json
|
|-- flake8-html
|   |-- back.svg
|   |-- file.svg
|   |-- index.html
|   |-- styles.css
|
|-- models
|   |-- __init__.py
|   |-- model_match.py
|   |-- model_player.py
|   |-- model_round.py
|   |-- model_tournament.py
|
|-- views
|   |-- __init__.py
|   |-- main_menu_view.py
|   |-- player_view.py
|   |-- tournament_view.py
|
|-- config.py
|-- main.py
|-- README.md
|-- requirements.txt
```

- **controllers/** : Contient les contrôleurs qui gèrent la logique de l'application.
  - **application_controller.py** : Point d'entrée principal de l'application, qui gère les interactions entre l'utilisateur et les différents contrôleurs.
  - **tournament_controller.py** : Contrôleur gérant la logique des tournois, incluant la gestion des matchs et la coordination des différentes vues.

- **data/** : Contient les fichiers JSON pour la persistance des données.
  - **players.json** : Fichier contenant les données des joueurs.
  - **tournaments.json** : Fichier contenant les données des tournois.

- **flake8-html/** : Contient le rapport flake8 généré en HTML pour la qualité du code.

- **models/** : Contient les modèles de données utilisés dans l'application.
  - **model_match.py** : Modèle représentant un match.
  - **model_player.py** : Modèle représentant un joueur.
  - **model_round.py** : Modèle représentant un round de tournoi.
  - **model_tournament.py** : Modèle représentant un tournoi.

- **views/** : Contient les vues qui gèrent l'interface utilisateur.
  - **main_menu_view.py** : Vue présentant le menu principal, offrant des options pour accéder à différentes fonctionnalités.
  - **player_view.py** : Vue gérant les interactions utilisateur pour la gestion des joueurs.
  - **tournament_view.py** : Vue gérant les interactions utilisateur pour la gestion des tournois.

- **config.py** : Fichier de configuration de l'application.
- **main.py** : Point d'entrée principal pour lancer l'application.
- **requirements.txt** : Fichier listant les dépendances requises pour le projet.

## Prérequis
- Python 3.8+
- Aucune autre dépendance externe n'est requise.

## Installation
1. Clonez le dépôt :
   ```
   git clone https://github.com/AnsiLema/tournoi_echec_v2.git
   ```
2. Accédez au dossier du projet :
   ```
   cd tournoi_echec_v2
   ```

## Mise en place de l'environnement virtuel
Il est recommandé d'utiliser un environnement virtuel pour isoler les dépendances du projet. Voici comment le mettre en place :

1. Créez un environnement virtuel :
   ```
   python -m venv venv
   ```
2. Activez l'environnement virtuel :
   - Sous Windows :
     ```
     venv\Scripts\activate
     ```
   - Sous macOS/Linux :
     ```
     source venv/bin/activate
     ```
3. Installez les dépendances requises (s'il y en a) :
   ```
   pip install -r requirements.txt
   ```

## Lancer l'application
Une fois l'environnement virtuel activé, lancez l'application :
``` 
python main.py
```

## Générer un rapport flake8 en HTML
Pour s'assurer de la qualité du code, vous pouvez utiliser flake8 pour générer un rapport en HTML. Voici comment procéder :

1. Installez flake8 et le plugin flake8-html :
   ```
   pip install flake8 flake8-html
   ```
2. Générez le rapport HTML :
   ```
   flake8 --format=html --htmldir=flake8-html
   ```
3. Le rapport sera généré dans le dossier `flake8-html` et vous pourrez ouvrir le fichier `index.html` dans votre navigateur pour voir les détails des erreurs et avertissements.

## Utilisation
L'application est utilisée via une interface en ligne de commande.
- Depuis le menu principal, vous pouvez choisir d'ajouter des joueurs, de créer un nouveau tournoi, ou de consulter les informations sur un tournoi existant.
- Les contrôleurs gèrent la logique des tournois et des joueurs, tandis que les vues affichent les informations et permettent à l'utilisateur de naviguer entre les options.

## Exemple d'utilisation
1. Démarrez l'application.
2. Choisissez l'option pour créer un nouveau tournoi.
3. Ajoutez des joueurs au tournoi.
4. Démarrez le tournoi et entrez les scores des matchs à chaque tour.

## Auteur
Développé par A'nsi.

