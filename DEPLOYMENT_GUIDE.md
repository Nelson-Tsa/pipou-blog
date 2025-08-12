# 🚀 Guide de Déploiement PipouBlog sur Vercel

## 📋 Checklist Pré-Déploiement

### ✅ Fichiers de Configuration
- [x] `vercel.json` - Configuration Vercel
- [x] `index.py` - Point d'entrée WSGI
- [x] `build_files.sh` - Script de build
- [x] `requirements.txt` - Dépendances Python
- [x] `settings.py` - Configuration Django mise à jour
- [x] `.env.example` - Template variables d'environnement

## 🔧 Variables d'Environnement Vercel

Configurer ces variables dans le dashboard Vercel :

```bash
DATABASE_URL=postgresql://[votre-url-neon-complete]
SECRET_KEY=[votre-clé-secrète-django]
DEBUG=False
```

## 🗄️ Base de Données Neon

La base de données PostgreSQL Neon est déjà configurée et contient :
- ✅ Superuser : admin / admin123
- ✅ Données de test
- ✅ Tables migrées

## 🚀 Étapes de Déploiement

### 1. Créer une branche de restauration
```bash
git checkout -b restore-working-version
```

### 2. Appliquer les modifications proposées
- Accepter toutes les modifications de fichiers proposées
- Vérifier que tous les fichiers sont créés/modifiés

### 3. Commit et push
```bash
git add .
git commit -m "Restore working version with Vercel and Neon config"
git push origin restore-working-version
```

### 4. Déployer sur Vercel
- Connecter le repository GitHub à Vercel
- Configurer les variables d'environnement
- Déployer automatiquement

## 🔍 Fonctionnalités à Tester

Après déploiement, vérifier :
- [ ] Page d'accueil accessible
- [ ] Connexion utilisateur (`/login/`)
- [ ] Inscription (`/register/`)
- [ ] Admin accessible (`/admin/`)
- [ ] CSS chargé correctement
- [ ] Base de données Neon connectée

## 🛠️ Configuration d'Authentification

**URLs correctes** (basé sur les mémoires) :
- Connexion : `/login/` (PAS `/authentication/login/`)
- Déconnexion : `/logout/`
- Inscription : `/register/`

**Backend d'authentification :**
- Authentification par email activée
- Backend personnalisé `EmailBackend` configuré

## 📞 Support

Si des problèmes surviennent :
1. Vérifier les logs Vercel
2. Confirmer les variables d'environnement
3. Tester les URLs d'authentification
4. Vérifier la connexion base de données
