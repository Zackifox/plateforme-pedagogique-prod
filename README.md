# Plateforme Pédagogique

Plateforme de ressources pédagogiques (cours et sujets en PDF) organisées par Institut, Filière, Niveau et Matière.

---

## Stack technique

- **Backend** : Python 3.11 + Django 4.2 + Django REST Framework + JWT
- **Frontend** : Vue.js 3 + Vite + Pinia + Tailwind CSS + PWA
- **Base de données** : PostgreSQL (prod) / SQLite (dev)
- **Serveur** : Gunicorn + Nginx

---

## Installation en développement

### 1. Prérequis
```bash
python3.11 --version   # >= 3.11
node --version         # >= 18
```

### 2. Backend Django
```bash
cd backend

# Environnement virtuel
python3 -m venv venv
source venv/bin/activate       # Linux/Mac
# venv\Scripts\activate        # Windows

# Dépendances
pip install -r requirements.txt

# Variables d'environnement
cp .env.example .env
# Éditez .env : SECRET_KEY, DB_*, etc.

# Base de données (SQLite en dev)
python manage.py migrate --settings=config.settings.development
python manage.py createsuperuser --settings=config.settings.development

# Lancer le serveur
python manage.py runserver --settings=config.settings.development
# API disponible sur http://127.0.0.1:8000
```

### 3. Frontend Vue.js
```bash
cd frontend

npm install

cp .env.example .env
# VITE_API_URL= (laisser vide en dev, le proxy Vite redirige vers :8000)

npm run dev
# Application disponible sur http://localhost:5173
```

---

## Déploiement en production (Ubuntu 22.04)

### 1. Installer les dépendances système
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3.11 python3.11-venv python3-pip \
    postgresql postgresql-contrib nginx nodejs npm certbot python3-certbot-nginx
```

### 2. Base de données PostgreSQL
```bash
sudo -u postgres psql

CREATE DATABASE plateforme_db;
CREATE USER plateforme_user WITH PASSWORD 'motdepasse_securise';
GRANT ALL PRIVILEGES ON DATABASE plateforme_db TO plateforme_user;
\q
```

### 3. Cloner le projet
```bash
cd /home/ubuntu
git clone https://github.com/votre-repo/plateforme-pedagogique.git
cd plateforme-pedagogique
```

### 4. Backend
```bash
cd backend
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configurer .env (production)
cp .env.example .env
nano .env
# SECRET_KEY=<clé longue et aléatoire>
# DEBUG=False
# ALLOWED_HOSTS=mondomaine.com,www.mondomaine.com
# DB_NAME=plateforme_db
# DB_USER=plateforme_user
# DB_PASSWORD=motdepasse_securise

python manage.py migrate --settings=config.settings.production
python manage.py collectstatic --settings=config.settings.production
python manage.py createsuperuser --settings=config.settings.production
```

### 5. Gunicorn en service systemd
```bash
sudo mkdir -p /var/log/gunicorn
sudo chown ubuntu:ubuntu /var/log/gunicorn

sudo nano /etc/systemd/system/gunicorn.service
```

Contenu du fichier service :
```ini
[Unit]
Description=Gunicorn — Plateforme Pédagogique
After=network.target

[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu/plateforme-pedagogique/backend
Environment="DJANGO_SETTINGS_MODULE=config.settings.production"
ExecStart=/home/ubuntu/plateforme-pedagogique/backend/venv/bin/gunicorn \
    -c gunicorn.conf.py config.wsgi:application
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable gunicorn
sudo systemctl start gunicorn
sudo systemctl status gunicorn
```

### 6. Frontend — build
```bash
cd /home/ubuntu/plateforme-pedagogique/frontend
npm install

# Configurer .env
echo "VITE_API_URL=https://mondomaine.com" > .env

npm run build
# Les fichiers sont générés dans frontend/dist/
```

### 7. Nginx
```bash
sudo cp /home/ubuntu/plateforme-pedagogique/nginx/nginx.conf \
    /etc/nginx/sites-available/plateforme

# Remplacer mondomaine.com par votre domaine dans le fichier
sudo nano /etc/nginx/sites-available/plateforme

sudo ln -s /etc/nginx/sites-available/plateforme /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 8. SSL avec Let's Encrypt
```bash
sudo certbot --nginx -d mondomaine.com -d www.mondomaine.com
# Renouvellement automatique géré par certbot
```

---

## Commandes utiles

```bash
# Redémarrer Gunicorn après modification du code
sudo systemctl restart gunicorn

# Voir les logs
sudo journalctl -u gunicorn -f
tail -f /var/log/gunicorn/error.log

# Rebuild frontend après modification
cd frontend && npm run build

# Créer un administrateur
cd backend && source venv/bin/activate
python manage.py createsuperuser --settings=config.settings.production

# Mettre à jour (git pull + migrate + collectstatic + restart)
git pull
cd backend && source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate --settings=config.settings.production
python manage.py collectstatic --no-input --settings=config.settings.production
sudo systemctl restart gunicorn
cd ../frontend && npm install && npm run build
```



---
Demarer les serveurs
backend python manage.py runserver --settings=config.settings.development
Frontend npm run dev
---

## Structure des URL API

| Méthode | URL | Description |
|---|---|---|
| POST | /api/auth/login/ | Connexion admin |
| POST | /api/auth/refresh/ | Rafraîchir le token |
| GET | /api/catalogue/instituts/ | Liste des instituts |
| GET | /api/catalogue/instituts/{id}/filieres/ | Filières d'un institut |
| GET | /api/catalogue/filieres/{id}/niveaux/ | Niveaux d'une filière |
| GET | /api/catalogue/niveaux/{id}/matieres/ | Matières d'un niveau |
| GET | /api/ressources/ | Liste des ressources (filtrable) |
| GET | /api/ressources/{id}/telecharger/ | Télécharger un PDF |
| GET | /api/ressources/{id}/apercu/ | Aperçu inline du PDF |
| POST | /api/ressources/ | Uploader une ressource (admin) |
| DELETE | /api/ressources/{id}/ | Supprimer (admin) |
