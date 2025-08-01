                                             -*  PipouBlog *-

-- Description --

PipouBlog est une application web développée avec Django, conçue pour créer, éditer et gérer des posts de blog. Elle offre des fonctionnalités d'authentification (inscription, connexion, déconnexion), de gestion de profils utilisateur avec photos, une interface responsive compatible mobile et desktop, et un bouton flottant pour créer rapidement des posts. Le projet utilise une base de données PostgreSQL et inclut une suite de tests automatisés (96% de couverture) ainsi qu'une configuration CI/CD via GitHub Actions.

Pour des informations détaillées, consultez les notices suivantes :

- <b>NOTICE.docker.md</b> : Instructions pour construire, exécuter et déployer avec Docker.
- <b>NOTICE.Init.md</b> : Guide pour l'initialisation et la configuration du projet.
- <b>NOTICE.test.md</b> : Instructions pour exécuter les tests.



-- Prérequis --

- Git
- Docker
- Docker Compose



-- Cloner le projet --

Clonez le dépôt et accédez au répertoire du projet :

``` git clone git@github.com:adatechschool/pipou-blog.git ```</br>
<code> cd PipouBlog/pipou-blog </code>



-- Construire et exécuter avec Docker --

1 - Assurez-vous que Docker et Docker Compose sont installés et en cours d'exécution.


2 - Construisez et lancez les services (incluant la base de données PostgreSQL) :

``` docker-compose up --build ```


3 - Appliquez les migrations pour configurer la base de données :

``` docker-compose exec server python manage.py migrate ```


4 - (Optionnel) Créez un superutilisateur pour accéder à l'interface d'administration :

``` docker-compose exec server python manage.py createsuperuser ```


5 - (Optionnel) Chargez les données de démonstration :

``` docker-compose exec server python manage.py loaddata fixtures/all_data.json ```


6 - L'application est accessible à : http://localhost:8000.


7 - L'interface d'administration est disponible à : http://localhost:8000/admin.

<i> Pour des instructions détaillées sur la configuration Docker, consultez <b>NOTICE.docker.md</b> et <b> NOTICE.Init.md</b> </i>.



-- Déploiement sur le cloud --


1 - Construisez l'image Docker :

``` docker build -t pipoublog ```

Si votre cloud utilise une architecture différente (par exemple, amd64 pour un Mac M1) :

``` docker build --platform=linux/amd64 -t pipoublog ```


2 - Poussez l'image vers votre registre :

``` docker push myregistry.com/pipoublog ```

Pour plus de détails, consultez <b>NOTICE.docker.md</b> ou la documentation officielle de Docker.



-- Tests --

Le projet inclut une suite de tests automatisés avec une couverture de 96%. Pour exécuter les tests localement ou configurer l'intégration continue avec GitHub Actions, consultez <b>NOTICE.test.md.</b>

-- Structure du projet

pipou-blog/</br>
├── pipou_blog/           # Configuration Django</br>
├── blog/                 # Application blog</br>
├── authentication/       # Application authentification</br>
├── user_profile/         # Application profils utilisateur</br>
├── static/               # Fichiers statiques (CSS, JS, images)</br>
├── templates/            # Templates HTML</br>
├── fixtures/             # Données de démonstration</br>
├── requirements.txt      # Dépendances Python</br>
├── compose.yaml          # Configuration Docker</br>
└── manage.py             # Script de gestion Django</br>

-- Fonctionnalités principales --

- Authentification : Inscription, connexion, déconnexion.
- Blog : Création, édition, suppression de posts.
- Profils utilisateur : Gestion des profils avec photos.
- Interface responsive : Compatible mobile et desktop.
- Bouton flottant : Création rapide de posts.
- Tests automatisés : Couverture de 96%.
- CI/CD : Configuré avec GitHub Actions.


-- Contribution --

1 - Forkez le projet.</br>
2 - Créez une branche pour votre fonctionnalité.</br>
3 - Committez vos changements.</br>
4 - Poussez vers la branche.</br>
5 - Ouvrez une Pull Request.</br>

Pour plus de détails, consultez <b>NOTICE.Init.md</b>.




