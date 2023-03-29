# OpenClassrooms_Projet_2

Instruction de création et d'exécution de l'environnement virtuel via le terminal :

- python -m venv [nom de l'environnement]
- aller dans le dossier "Scripts" via le chemin suivant : venv\Scripts
- Lancer le fichier "activate".

Dans le cas où l'environnement ne se lance pas (problème possible avec PowerShell sous Windows):
- Executez la commande : Get-ExecutionPolicy. Si la réponse est "Restricted" vous devrez modifier cette politique.
- Executez la commande suivante : Set-ExecutionPolicy RemoteSigned -Scope CurrentUser.
- Retournez dans le dossier et recommencer à lancer le fichier via la commande .\activate

Execution de l'application :
- lancer le programme en l'appelant; Exemple : dossier_application\book_to_scrap.py

