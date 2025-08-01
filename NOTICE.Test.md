# Tests pour PipouBlog

Ce document explique comment nous avons implémenté les tests pour le projet PipouBlog, comment les exécuter localement et comment fonctionne l'intégration continue (CI) pour les tests.

## 🗂️ Architecture des tests

### Framework de test

Nous utilisons le framework de test intégré de Django, qui est basé sur `unittest` de Python. Cette approche a été choisie pour sa simplicité et sa compatibilité directe avec Django, sans besoin de dépendances supplémentaires complexes.

### Structure des tests

- Les tests sont organisés dans les fichiers `tests.py` de chaque application Django
- Actuellement, nous avons des tests basiques pour vérifier le bon fonctionnement des vues principales

### Configuration spéciale pour les tests

Nous avons créé un fichier de configuration spécifique pour les tests qui offre deux options :

- `pipou_blog/pipou_blog/test_settings.py` : Ce fichier contient une configuration Django complète qui :
  - Détecte automatiquement la disponibilité de PostgreSQL/Neon via la variable d'environnement `DATABASE_URL`
  - Si `DATABASE_URL` est valide, utilise PostgreSQL/Neon avec un préfixe `test_` pour la base de données
  - Sinon, utilise SQLite en mémoire (plus simple pour le développement local)
  - Désactive les migrations pour accélérer les tests
  - Conserve toutes les autres configurations nécessaires (authentification personnalisée, etc.)

## 🚀 Exécution des tests localement

### Exécuter les tests avec SQLite (par défaut)

Pour lancer les tests localement avec SQLite (plus simple pour le développement rapide), exécutez :

```bash
cd pipou_blog
python manage.py test --settings=pipou_blog.test_settings
```

Cette commande :

- Crée automatiquement une base de données SQLite en mémoire temporaire
- Exécute tous les tests trouvés dans l'application `blog`

### Exécuter les tests avec PostgreSQL/Neon

Pour exécuter les tests avec votre base de données PostgreSQL/Neon (identique à la production) :

```bash
# Définir la variable d'environnement DATABASE_URL
# Sous Windows PowerShell
$env:DATABASE_URL="postgresql://username:password@hostname:5432/dbname"

# Ou sous Bash/Linux/Mac
export DATABASE_URL="postgresql://username:password@hostname:5432/dbname"

# Exécuter les tests avec l'option --keepdb pour éviter les erreurs de suppression de base
cd pipou_blog
python manage.py test blog --settings=pipou_blog.test_settings --keepdb
```

L'option `--keepdb` est importante car elle permet d'éviter les erreurs lors de la tentative de suppression de la base de données de test, qui peut être utilisée par d'autres connexions avec Neon.

### Mesurer la couverture de code

Pour mesurer la couverture de code, nous utilisons l'outil `coverage` :

1. Exécuter les tests avec mesure de couverture :

```bash
cd pipou_blog
coverage run manage.py test --settings=pipou_blog.test_settings
```

2. Afficher le rapport de couverture en console :

```bash
coverage report
```

3. Générer un rapport HTML interactif (plus détaillé) :

```bash
coverage html
```

Puis ouvrez le fichier `htmlcov/index.html` dans votre navigateur.

## 🔄 Intégration Continue (CI)

### Configuration GitHub Actions

Nous avons configuré GitHub Actions pour exécuter automatiquement les tests à chaque push sur les branches `main` et `dev`. Le workflow est défini dans le fichier `.github/workflows/tests.yml` et il :

1. Configure l'environnement Python
2. Installe les dépendances du projet
3. **Utilise la base de données PostgreSQL/Neon** via la variable d'environnement `DATABASE_URL`
4. Exécute les tests avec mesure de couverture et l'option `--keepdb`
5. Génère un rapport de couverture
6. Publie le rapport comme un artefact de build

### Configuration du secret DATABASE_URL

Pour que les tests CI fonctionnent avec PostgreSQL/Neon, vous devez configurer un secret GitHub :

1. Allez dans les paramètres de votre dépôt GitHub
2. Sélectionnez "Secrets and variables" > "Actions"
3. Cliquez sur "New repository secret"
4. Nommez-le `DATABASE_URL` et entrez votre URL de connexion Neon

### Consulter les résultats des tests CI

Après chaque exécution du workflow GitHub Actions :

1. Allez dans l'onglet "Actions" du dépôt GitHub
2. Sélectionnez l'exécution de workflow que vous souhaitez consulter
3. Dans la section "Artifacts", vous pouvez télécharger le rapport de couverture XML

## 📝 Écrire de nouveaux tests

### Créer un test simple

Pour ajouter un nouveau test, modifiez ou créez un fichier `tests.py` dans votre application Django :

```python
from django.test import TestCase
from django.urls import reverse

class VotreTestCase(TestCase):
    def setUp(self):
        # Code exécuté avant chaque test
        pass

    def test_exemple(self):
        # Votre test ici
        response = self.client.get(reverse('nom-de-la-vue'))
        self.assertEqual(response.status_code, 200)
```

### Bonnes pratiques pour les tests

1. **Isolation** : Chaque test doit être indépendant des autres
2. **Nommage clair** : Nommez vos tests de façon descriptive (`test_user_can_login` plutôt que `test1`)
3. **Tests atomiques** : Chaque test ne doit vérifier qu'un seul comportement
4. **Fixtures** : Utilisez `setUp()` pour préparer les données de test
5. **Couverture complète** : Testez les cas de succès ET d'erreur

## 🔍 Dépannage

### Problèmes courants

- **ImportError** : Vérifiez que les imports correspondent à la structure du projet
- **Erreurs de base de données** : Assurez-vous d'utiliser `--settings=pipou_blog.test_settings`
- **Échecs de test** : Vérifiez les messages d'erreur et assurez-vous que les conditions testées sont correctes

## 📈 Évolution future des tests

À mesure que le projet évolue, nous prévoyons d'ajouter :

1. **Tests unitaires** pour tous les modèles et fonctions
2. **Tests d'intégration** pour vérifier les interactions entre composants
3. **Tests fonctionnels** pour simuler des scénarios utilisateur complets
4. **Tests de performance** pour vérifier la rapidité de l'application sous charge

---
