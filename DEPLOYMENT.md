# Guide de déploiement sur Vercel - PipouBlog

## Prérequis

1. Compte Vercel (gratuit)
2. Base de données PostgreSQL (recommandé : Neon, Supabase, ou Railway)
3. Compte GitHub pour connecter votre repository

## Étapes de déploiement

### 1. Préparer la base de données

Créez une base de données PostgreSQL sur un service cloud :
- **Neon** (recommandé) : https://neon.tech/
- **Supabase** : https://supabase.com/
- **Railway** : https://railway.app/

Récupérez l'URL de connexion au format :
```
postgresql://username:password@hostname:port/database_name
```

### 2. Configurer les variables d'environnement sur Vercel

Dans votre dashboard Vercel, allez dans Settings > Environment Variables et ajoutez :

```
SECRET_KEY=votre-clé-secrète-django-très-longue-et-sécurisée
DEBUG=False
DATABASE_URL=postgresql://username:password@hostname:port/database_name
```

**Important** : Générez une nouvelle SECRET_KEY pour la production !

### 3. Déployer sur Vercel

1. Connectez votre repository GitHub à Vercel
2. Vercel détectera automatiquement le fichier `vercel.json`
3. Le déploiement se lancera automatiquement

### 4. Migrations de base de données

Après le premier déploiement, vous devrez exécuter les migrations :

1. Installez Vercel CLI : `npm i -g vercel`
2. Connectez-vous : `vercel login`
3. Liez votre projet : `vercel link`
4. Exécutez les migrations :
   ```bash
   vercel exec -- python manage.py migrate
   vercel exec -- python manage.py createsuperuser
   ```

## Structure des fichiers ajoutés

- `vercel.json` : Configuration Vercel
- `build_files.sh` : Script de build pour collecter les fichiers statiques
- `.env.example` : Exemple des variables d'environnement
- `requirements.txt` : Mis à jour avec whitenoise et gunicorn

## Modifications apportées

### settings.py
- Configuration pour production/développement
- Ajout de WhiteNoise pour les fichiers statiques
- Configuration flexible de la base de données
- Variables d'environnement sécurisées

### Gestion des fichiers statiques
- `STATIC_ROOT` configuré pour Vercel
- WhiteNoise pour servir les fichiers statiques
- Compression automatique des assets

## Troubleshooting

### Problème de fichiers statiques
Si les CSS/JS ne se chargent pas :
1. Vérifiez que `python manage.py collectstatic` s'exécute sans erreur
2. Vérifiez les chemins dans vos templates

### Problème de base de données
Si la connexion à la base de données échoue :
1. Vérifiez l'URL `DATABASE_URL` dans les variables d'environnement
2. Assurez-vous que la base de données accepte les connexions externes

### Erreur 500
Consultez les logs Vercel pour identifier le problème :
```bash
vercel logs
```

## Commandes utiles

```bash
# Voir les logs en temps réel
vercel logs --follow

# Exécuter des commandes Django sur Vercel
vercel exec -- python manage.py shell
vercel exec -- python manage.py dbshell

# Redéployer
vercel --prod
```
