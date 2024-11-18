# Application pour les tournois d'échec

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
|-- tournament_controller.py
|-- application_controller.py
|-- main_menu_view.py
|-- player_view.py
|-- tournament_view.py
```

- **tournament_controller.py** : Contrôleur gérant la logique des tournois, incluant la gestion des matchs et la coordination des différentes vues.
- **application_controller.py** : Point d'entrée principal de l'application, qui gère les interactions entre l'utilisateur et les différents contrôleurs.
- **main_menu_view.py** : Vue présentant le menu principal, offrant des options pour accéder à différentes fonctionnalités.
- **player_view.py** : Vue gérant les interactions utilisateur pour la gestion des joueurs.
- **tournament_view.py** : Vue gérant les interactions utilisateur pour la gestion des tournois.

## Prérequis
- Python 3.8+

## Installation
1. Clonez le dépôt :
   ```
   git clone https://github.com/username/chess-tournament.git
   ```
2. Accédez au dossier du projet :
   ```
   cd chess-tournament
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
3. Installez les dépendances requises :
   ```
   pip install -r requirements.txt
   ```

## Lancer l'application
Une fois l'environnement virtuel activé, lancez l'application :
``` 
python application_controller.py
```

## Utilisation
L'application est utilisée via une interface en ligne de commande.
- Depuis le menu principal, vous pouvez choisir d'ajouter des joueurs, de créer un nouveau tournoi, ou de consulter les informations sur un tournoi existant.
- Les contrôleurs gèrent la logique des tournois et des joueurs, tandis que les vues affichent les informations et permettent à l'utilisateur de naviguer entre les options.

## Exemple d'utilisation
1. Démarrez l'application.
2. Choisissez l'option pour créer un nouveau tournoi.
3. Ajoutez des joueurs au tournoi.
4. Démarrez le tournoi et entrez les scores des matchs à chaque tour.

## Contribution
Les contributions sont les bienvenues ! Pour proposer des modifications :
1. Forkez le projet.
2. Créez une branche pour votre fonctionnalité : `git checkout -b nouvelle-fonctionnalite`.
3. Commitez vos modifications : `git commit -m 'Ajout d'une nouvelle fonctionnalité'`.
4. Poussez sur la branche : `git push origin nouvelle-fonctionnalite`.
5. Ouvrez une Pull Request.

## Auteur
Développé par A'nsi Lema.
