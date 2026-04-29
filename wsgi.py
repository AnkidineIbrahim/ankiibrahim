"""
wsgi.py — Point d'entrée WSGI pour Vercel
"""
from app import app, init_db

# Initialiser la DB au démarrage
init_db()

# Vercel utilise 'app' comme handler
if __name__ == '__main__':
    app.run()
