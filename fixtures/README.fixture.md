# Utilisation des Fixtures de Données

Ce dossier contient des fixtures de données pour le projet PipouBlog, générées à partir de la base de données de production (Neon). Ces fixtures permettent de peupler rapidement une base de données de développement ou de test avec des données réalistes, sans avoir à les créer manuellement.

## Fichier de Fixture

-   `all_data.json`: Contient l'export complet de toutes les données des modèles Django (utilisateurs, articles de blog, etc.).

## Comment charger les données

Pour charger ces données dans votre base de données de développement (par exemple, celle de Docker Compose), suivez les étapes ci-dessous.

**Prérequis :**

1.  Assurez-vous que votre environnement Docker Compose est configuré et que les services `server` et `db` sont en cours d'exécution.
    ```bash
    docker compose up -d
    ```
2.  Assurez-vous que les migrations Django ont été appliquées à votre base de données cible. Si ce n'est pas le cas, exécutez :
    ```bash
    docker compose exec server python pipou_blog/manage.py migrate
    ```

**Étapes pour charger les données :**

1.  **Accédez au shell du conteneur Django :**
    Vous devez exécuter la commande `loaddata` à l'intérieur du conteneur `server`.
    ```bash
    docker compose exec server bash
    ```
    *(Vous serez alors dans le shell du conteneur, dans le répertoire `/pipou-blog`)*

2.  **Chargez la fixture :**
    Une fois dans le shell du conteneur, exécutez la commande `loaddata` en spécifiant le chemin vers le fichier de fixture.
    ```bash
    python pipou_blog/manage.py loaddata fixtures/all_data.json
    ```
    *(Attendez la fin du processus. Si des erreurs surviennent (par exemple, données dupliquées), elles seront affichées ici.)*

3.  **Quittez le shell du conteneur :**
    ```bash
    exit
    ```

Vos données devraient maintenant être chargées dans la base de données de votre environnement de développement.
