# Guide d'Installation et de Configuration - PipouBlog 📝

## Prérequis

Avant de commencer, assurez-vous que votre machine répond aux exigences suivantes :

- **Système d'exploitation** : Windows, macOS ou Linux
- **Python** : Version 3.8 ou supérieure
- **PostgreSQL** : Version 13 ou supérieure
- **Git** : Pour cloner le projet
- **Docker** : (Optionnel) Pour utiliser l'environnement containerisé

## Étape 1 : 📚 Cloner le Projet

1. **Ouvrir un terminal** : Sur votre machine, ouvrez un terminal ou une invite de commande.

2. **Cloner le dépôt** : Utilisez Git pour cloner le dépôt du projet.

```bash
git clone https://github.com/votre-utilisateur/PipouBlog.git
cd PipouBlog/pipou-blog
```

## Étape 2 : 🐍 Configurer l'Environnement Python

1. **Créer un environnement virtuel** : Il est recommandé d'utiliser un environnement virtuel pour isoler les dépendances du projet.

```bash
python -m venv .venv
```

2. **Activer l'environnement virtuel** :

**Sur Windows :**

```bash
.venv\Scripts\activate
```

**Sur macOS/Linux :**

```bash
source .venv/bin/activate
```

## Étape 3 : 📦 Installer les Dépendances

Installer les paquets requis listés dans le fichier `requirements.txt` :

```bash
pip install -r requirements.txt
```

**Dépendances principales :**

- Django 5.2.4
- psycopg (PostgreSQL adapter)
- Pillow (gestion d'images)
- python-dotenv (variables d'environnement)

## Étape 4 : 🗃️ Configurer la Base de Données

### Option A : Configuration manuelle PostgreSQL

1. **Installer PostgreSQL** : Si ce n'est pas déjà fait, installez PostgreSQL sur votre machine.

2. **Créer une base de données** :

```sql
sudo -u postgres psql
CREATE DATABASE pipoubdd;
CREATE USER pipou WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE pipoubdd TO pipou;
\q
```

3. **Configurer les variables d'environnement** :
   - Copiez le fichier `exemple.env` vers `.env`
   - Modifiez le fichier `.env` :

```env
DATABASE_URL=postgres://pipou:password@localhost:5432/pipoubdd
```

### Option B : Utiliser Docker (Recommandé)

```bash
docker-compose up -d db
```

## Étape 5 : 📚 Appliquer les Migrations

Configurez la structure de la base de données :

```bash
python manage.py migrate
```

## Étape 6 : 👤 Créer un Superutilisateur

Créez un compte administrateur pour accéder à l'interface d'administration :

```bash
python manage.py createsuperuser
```

## Étape 7 : 📦 Charger les Fixtures (Optionnel)

Le projet inclut des données de démonstration. Pour les charger :

```bash
python manage.py loaddata fixtures/all_data.json
```

**Note :** Consultez `fixtures/README.fixture.md` pour plus de détails sur les données incluses.

## Étape 8 : 🚀 Lancer le Serveur de Développement

1. **Démarrer le serveur** :

```bash
python manage.py runserver
```

2. **Accéder à l'application** : Ouvrez un navigateur web et accédez à :

```
http://127.0.0.1:8000/
```

3. **Interface d'administration** : Accédez à l'admin Django :

```
http://127.0.0.1:8000/admin/
```

## Étape 9 : 🐳 Utiliser Docker (Alternative complète)

Si vous préférez utiliser Docker pour tout l'environnement :

1. **Construire et lancer tous les services** :

```bash
docker-compose up --build
```

2. **Appliquer les migrations dans le conteneur** :

```bash
docker-compose exec server python manage.py migrate
```

3. **Créer un superutilisateur dans le conteneur** :

```bash
docker-compose exec server python manage.py createsuperuser
```

## Étape 10 : 🧪 Lancer les Tests

Le projet inclut une suite de tests complète :

```bash
# Tests avec coverage
python manage.py test --settings=pipou_blog.test_settings

```

**Note :** Consultez `README.Test.md` pour plus de détails sur les tests.

## Structure du Projet

```
pipou-blog/
├── pipou_blog/           # Configuration Django
├── blog/                 # Application blog
├── authentication/      # Application authentification
├── user_profile/        # Application profils utilisateur
├── static/              # Fichiers statiques (CSS, JS, images)
├── templates/           # Templates HTML
├── fixtures/            # Données de démonstration
├── requirements.txt     # Dépendances Python
├── compose.yaml         # Configuration Docker
└── manage.py           # Script de gestion Django
```

## Fonctionnalités Principales

- ✅ **Authentification** : Inscription, connexion, déconnexion
- ✅ **Blog** : Création, édition, suppression de posts
- ✅ **Profils utilisateur** : Gestion des profils avec photos
- ✅ **Interface responsive** : Compatible mobile et desktop
- ✅ **Bouton flottant** : Création rapide de posts
- ✅ **Tests automatisés** : Coverage de 96%
- ✅ **CI/CD** : GitHub Actions configuré

## Dépannage

### Problèmes courants

1. **Erreur de base de données** : Vérifiez que PostgreSQL est démarré et que les credentials sont corrects
2. **Erreur de migration** : Supprimez les fichiers de migration et recréez-les avec `makemigrations`
3. **Erreur de dépendances** : Vérifiez que l'environnement virtuel est activé

### Support

- Consultez les logs avec `python manage.py runserver --verbosity=2`
- Vérifiez la configuration dans `pipou_blog/settings.py`
- Consultez la documentation Django : https://docs.djangoproject.com/

## Contribution

1. Forkez le projet
2. Créez une branche pour votre fonctionnalité
3. Committez vos changements
4. Poussez vers la branche
5. Ouvrez une Pull Request

---

**Bon développement avec PipouBlog ! 🚀**
