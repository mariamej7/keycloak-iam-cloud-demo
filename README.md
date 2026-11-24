# Démo Keycloak — Gestion des identités et des accès dans le Cloud

**Projet pédagogique indépendant**, conçu pour une présentation en binôme. **Il ne lit et ne modifie aucun fichier, service, compte ou base de données d'un autre projet.** Le code est conservé dans un dépôt GitHub privé dédié. Aucun service Render ou Vercel existant n'a été modifié.

## Objectif

Mettre en place une preuve de concept IAM avec **Keycloak**, une base **PostgreSQL**, et **deux applications web indépendantes en FastAPI** :

- **CampusCloud** : `http://localhost:8000`
- **BiblioCloud** : `http://localhost:8001`
- **Keycloak** : `http://localhost:8080`

Les deux applications font confiance au **même Realm `universite`**, mais possèdent **deux clients OIDC différents**. L'identité est authentifiée par Keycloak. Les applications vérifient ensuite **côté serveur** les rôles de chaque utilisateur.

```text
                       Navigateur (localhost)
                              │
               ┌──────────────┴──────────────┐
               ▼                             ▼
     CampusCloud :8000               BiblioCloud :8001
       Client OIDC A                   Client OIDC B
               │                             │
               └──────────────┬──────────────┘
                              ▼
                  Keycloak :8080 (Docker)
                         Realm universite
                       /               \
               Identités & rôles      SSO / OIDC
                              │
                              ▼
                    PostgreSQL (Docker)
                   (réseau Docker privé)
```

**Important — vocabulaire :** Keycloak assure l'authentification centralisée et émet les informations d'identité et de rôles. Chaque application **applique elle-même** les contrôles d'autorisation sur ses routes. Le SSO est observable entre les deux applications si la session Keycloak est active.

## Pré-requis

- **Docker Desktop** installé, moteur Docker démarré, `docker compose` disponible.
- **Python 3.11 ou plus récent** installé, `python` accessible en ligne de commande.
- Connexion Internet **au premier lancement** pour télécharger Keycloak, PostgreSQL et les dépendances Python.
- Ports `8080`, `8000`, `8001` libres sur **ton propre ordinateur**.

> Ce projet est destiné à un environnement de **démonstration locale**. Le seul service Docker exposé à l'hôte est Keycloak, lié à `127.0.0.1`. PostgreSQL n'est pas exposé. **Ne pas exposer le projet tel quel à Internet** : il emploie `start-dev`, HTTP local et des comptes fictifs avec des mots de passe connus.

## Démarrage sur Windows (PowerShell)

1. Extraire l'archive ZIP dans un nouveau dossier indépendant, par exemple `Documents\demo-keycloak-universite`.
2. Ouvrir PowerShell dans ce dossier.
3. S'assurer que Docker Desktop est lancé.
4. Exécuter les commandes :

```powershell
Copy-Item .env.example .env
# Facultatif mais recommandé : remplacer les secrets de .env par de vraies valeurs aléatoires
powershell -ExecutionPolicy Bypass -File .\scripts\start-demo.ps1
```

Le script crée un environnement Python virtuel **dans ce nouveau dossier**, installe ses dépendances et lance les deux applications. Laisse cette fenêtre ouverte pendant toute la démo. Au premier démarrage, attendre que Keycloak soit prêt (60 à 120 secondes parfois).

Si le script Windows est bloqué, alternative manuelle :

```powershell
docker compose -f compose.yaml up -d
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r app\requirements.txt
.\.venv\Scripts\python.exe scripts\run_apps.py
```

## Démarrage Linux / macOS

```bash
cp .env.example .env
bash scripts/start-demo.sh
```

## Comptes de test (fictifs)

**Ces mots de passe sont uniquement destinés à la démo locale et figurent volontairement dans l'import de Realm. Ne jamais réutiliser ou déployer publiquement ces comptes.**

| Rôle | Identifiant | Mot de passe |
|---|---|---|
| Étudiant | `etudiant` | `Etudiant2026!` |
| Professeur | `professeur` | `Professeur2026!` |
| Administrateur applicatif | `admin.universite` | `AdminUniv2026!` |

Pour ouvrir la **console d'administration Keycloak** : `http://localhost:8080/admin/`. Identifiant bootstrap : `kcadmin`. Son mot de passe est dans ton fichier `.env` sous `KEYCLOAK_ADMIN_PASSWORD`. **Ce compte technique Keycloak est distinct de l'administrateur applicatif** `admin.universite`.

## Scénario de démonstration

1. Ouvrir `http://localhost:8000`, cliquer sur **Se connecter avec Keycloak** et s'authentifier avec `etudiant`.
2. Ouvrir **Espace étudiant** : **HTTP 200, accès accepté**.
3. Ouvrir **Administration** : **HTTP 403, accès refusé**. Taper directement `/espace/admin` produit aussi un 403.
4. Ouvrir `http://localhost:8001` via le lien vers **BiblioCloud**. Cliquer sur **Se connecter**. Keycloak réutilise normalement la session SSO : pas de nouveau mot de passe demandé.
5. Ouvrir **Bibliothèque numérique** : **HTTP 200**. Expliquer que le SSO concerne l'authentification commune, pas la permission d'accéder à toutes les sections.
6. Pour tester les rôles `PROFESSEUR` et `ADMIN`, ouvrir une **fenêtre privée distincte**, ou terminer la session SSO Keycloak. Une simple déconnexion **locale** de l'application ne termine pas nécessairement la session SSO du serveur Keycloak.

Pour un script oral prêt à lire, voir [`GUIDE_DEMONSTRATION.md`](GUIDE_DEMONSTRATION.md).

## Matrice d'autorisation (attendue)

| Ressource | Étudiant | Professeur | Admin |
|---|:---:|:---:|:---:|
| Espace étudiant | ✅ | ❌ | ✅ |
| Espace professeur | ❌ | ✅ | ✅ |
| Administration | ❌ | ❌ | ✅ |
| Bibliothèque numérique | ✅ | ✅ | ✅ |

La logique est implémentée dans [`app/security.py`](app/security.py), et appliquée par les routes de [`app/main.py`](app/main.py). Un utilisateur non connecté est redirigé vers Keycloak au moment de l'authentification.

## Activer l'authentification multifacteur (MFA) pour la démo — facultatif

1. Connectez-vous à la **console d'administration Keycloak** avec le compte `kcadmin`.
2. Sélectionnez le Realm **universite** (et non `master`).
3. Ouvrez **Users**, puis sélectionnez `admin.universite`.
4. Dans **Required user actions**, ajoutez **Configure OTP** et sauvegardez (libellé exact variable selon la version).
5. Dans une fenêtre privée, connectez-vous à CampusCloud comme `admin.universite`. Keycloak propose alors la configuration d'un code OTP (application d'authentification compatible TOTP).

**Ne pas activer le MFA juste avant la présentation si vous n'avez pas un appareil d'authentification prêt.** Si la session Keycloak reste active, utiliser une navigation privée pour voir les étapes d'authentification.

## Configuration et portée du prototype

- Fichier `compose.yaml` : **projet Docker nommé explicitement** `keycloak-demo-universite-2026`, avec sa propre base et son réseau.
- `realm/universite-realm.json` : Realm, deux clients OIDC, trois utilisateurs et trois rôles. **Import uniquement au premier lancement** lorsque le Realm n'existe pas.
- `.env.example` : modèle des variables d'environnement. Le vrai `.env` est ignoré par Git.
- `app/main.py` : intégration **OIDC Authorization Code + PKCE** au moyen d'Authlib ; session locale signée ne conservant **ni access token, ni refresh token**.
- `app/security.py` : autorisation serveur selon les rôles fournis dans l'ID token OIDC validé.
- `scripts/run_apps.py` : lance **uniquement** les deux applications de cette démo et les arrête avec Ctrl+C.

### Pourquoi la démo n'est-elle pas encore un déploiement Cloud public ?

Le Cloud exige une **instance indépendante** avec nom de domaine, HTTPS, Keycloak en mode de production, une base PostgreSQL persistante sécurisée, des secrets réels et des redirect URIs publiques correctement configurées. Voir [`DEPLOIEMENT_CLOUD.md`](DEPLOIEMENT_CLOUD.md). **Aucun déploiement Cloud n'est exécuté automatiquement** et aucune ressource existante n'est réutilisée.

## Tests

Depuis la racine du projet :

```bash
python -m pytest -q tests
```

Ces tests vérifient les règles RBAC, la structure du Realm et les barrières contre les références à un autre projet. La validation **réelle** de la connexion SSO nécessite le lancement de Keycloak avec Docker et des essais dans le navigateur.

## Arrêt et conservation des données

- Ctrl+C dans la fenêtre Python : arrête uniquement les deux serveurs locaux.
- `docker compose -f compose.yaml down` : arrête uniquement les **services de CE projet Docker**, **sans supprimer son volume de base de données**.
- Ne jamais lancer une commande globale du type `docker system prune` dans le cadre de cette démo.
- Ne jamais exécuter `docker compose down -v` sans comprendre la suppression de la **base de données de ce projet démo**.

## Références officielles

- [Keycloak — démarrer avec Docker](https://www.keycloak.org/getting-started/getting-started-docker)
- [Keycloak — conteneurs et import Realm](https://www.keycloak.org/server/containers)
- [Keycloak — administration](https://www.keycloak.org/documentation)
- [Authlib — intégration FastAPI / Starlette](https://docs.authlib.org/en/v1.6.9/client/fastapi.html)

*Ce projet est un prototype pédagogique prêt à être lancé localement sur un ordinateur avec Docker et Python. Son exécution Keycloak en conditions réelles devra être validée sur cet ordinateur.*