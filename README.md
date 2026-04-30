# 🚀 Ibrahim Ankidine — Portfolio Flask v2

Portfolio professionnel avec panneau d'administration, construit avec **Python Flask**.
Bugs corrigés, compatible SQLAlchemy 2.0 + Python 3.13, prêt pour Vercel.

---

## ⚙️ Installation locale (Windows)

```bash
cd portfolio_flask

# Environnement virtuel (recommandé)
python -m venv venv
venv\Scripts\activate

# Dépendances
pip install -r requirements.txt

# Base de données
python init_db.py

# Lancer
python app.py
```
➡️ **http://localhost:5000** — Admin : **http://localhost:5000/admin**

**Identifiants admin :** `ankidine` / `ibrahim123`

---

## 🌐 Déploiement Vercel

### 1. Installer Vercel CLI
```bash
npm install -g vercel
```

### 2. Pousser sur GitHub
```bash
git init
git add .
git commit -m "Portfolio Flask v2"
git remote add origin https://github.com/AnkidineIbrahim/portfolio.git
git push -u origin main
```

### 3. Déployer
```bash
vercel login
vercel --prod
```

Ou via [vercel.com](https://vercel.com) :
1. **Add New Project** → importer depuis GitHub
2. **Framework** : Other
3. **Root Directory** : `./`
4. Cliquer **Deploy**

### 4. Variable d'environnement obligatoire
Dans Vercel → Settings → Environment Variables :
```
SECRET_KEY = <clé générée avec : python -c "import secrets; print(secrets.token_hex(32))">
```

> ⚠️ Sur Vercel, la DB SQLite est dans `/tmp` (temporaire, se réinitialise).
> Pour une DB persistante → utilisez **Render** ou **Railway** + PostgreSQL.

---

## 🔧 Bugs corrigés v2

| Bug | Correction |
|-----|-----------|
| `TypeError: fromisoformat` sur `/admin/stats` | Requête SQLite native avec `strftime` |
| `LegacyAPIWarning: Query.get()` | Remplacé par `db.session.get()` |
| `DeprecationWarning: utcnow()` | Remplacé par `datetime.now(timezone.utc)` |
| `favicon.ico 404` | Route `/favicon.ico` ajoutée |
| Chemin DB relatif cassé | Chemin absolu `os.path.join(app.root_path, ...)` |

---

## 🎛️ Fonctionnalités Admin

- **Dashboard** — KPIs, messages récents, stats de visites
- **Profil** — Photo, bio, CV PDF, réseaux sociaux
- **Projets** — CRUD complet (créer, modifier, supprimer)
- **Expériences** — CRUD avec bullet points dynamiques
- **Compétences** — CRUD par catégorie + icônes FontAwesome
- **Formation** — CRUD diplômes et établissements
- **Messages** — Lecture, réponse par email, suppression
- **Statistiques** — Graphique visites + répartition par page

---

*Ibrahim Ankidine · anki.ib.dev@gmail.com · 2025*
