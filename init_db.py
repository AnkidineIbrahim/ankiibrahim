"""
init_db.py — Initialise la base de données et crée le premier admin
Usage : python init_db.py
"""
from app import init_db, DEFAULT_ADMIN_USERNAME, DEFAULT_ADMIN_PASSWORD

if __name__ == '__main__':
    init_db(reset_admin=True)
    print("Base de donnees initialisee avec succes !")
    print("Identifiants admin par defaut :")
    print(f"   Utilisateur : {DEFAULT_ADMIN_USERNAME}")
    print(f"   Mot de passe : {DEFAULT_ADMIN_PASSWORD}")
    print("Changez le mot de passe apres votre premiere connexion !")
