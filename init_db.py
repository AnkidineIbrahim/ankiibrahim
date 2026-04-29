"""
init_db.py — Initialise la base de données et crée le premier admin
Usage : python init_db.py
"""
from app import init_db
if __name__ == '__main__':
    init_db()
    print("✅ Base de données initialisée avec succès !")
    print("🔑 Identifiants admin par défaut :")
    print("   Utilisateur : admin")
    print("   Mot de passe : admin123")
    print("⚠️  Changez le mot de passe après votre première connexion !")
