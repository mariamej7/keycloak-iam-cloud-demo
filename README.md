# Keycloak IAM Cloud — Démonstration universitaire

Projet pédagogique indépendant réalisé en binôme, intitulé **« Mise en place d'une solution de gestion des identités et des accès dans le Cloud avec Keycloak »**.

> **Version principale : déployée sur Render (24 novembre 2026).** L'ancienne version Docker locale est conservée pour travailler hors ligne. Ce dépôt est entièrement distinct de tout autre projet.

## Accès aux trois services Cloud

| Service | URL publique | Rôle |
|---|---|---|
| CampusCloud | https://iam2026-campus-mariam-riad-ufwv.onrender.com | Application universitaire FastAPI |
| BiblioCloud | https://iam2026-biblio-mariam-riad-ufwv.onrender.com | Application de bibliothèque FastAPI |
| Keycloak | https://iam2026-keycloak-mariam-riad-ufwv.onrender.com | Serveur central IAM / fournisseur OIDC |

La console de gestion technique Keycloak est accessible sous https://iam2026-keycloak-mariam-riad-ufwv.onrender.com/admin/ avec le **compte technique séparé** `kcadmin` et son secret conservé dans les variables Render, jamais dans Git.

## Démonstration : comptes **fictifs** uniquement

Dans le Realm Cloud `universite-demo-123` :

| Rôle | Utilisateur | Mot de passe de démonstration |
|---|---|---|
| ETUDIANT | `etudiant` | `123` |
| PROFESSEUR | `professeur` | `123` |
| ADMIN (applicatif) | `admin.universite` | `123` |

**Avertissement de sécurité :** `123` est volontairement faible, demandé uniquement pour une présentation de comptes fictifs. **Ce déploiement n'est pas adapté à de véritables comptes, données ou usages de production.** Le compte `admin.universite` n'est pas l'administrateur technique de Keycloak.

## But du projet

1. **Authentification centralisée** : CampusCloud et BiblioCloud délèguent la vérification des identités à Keycloak, au lieu de conserver les mots de passe dans leurs applications.
2. **Contrôle d'accès par rôles (RBAC)** : les deux applications vérifient les rôles `ETUDIANT`, `PROFESSEUR` et `ADMIN` **côté serveur**. Un étudiant obtient HTTP 200 pour l'espace étudiant, mais HTTP 403 pour l'administration.
3. **Single Sign-On (SSO)** : une session Keycloak active peut être réutilisée pour s'authentifier dans les deux applications sans ressaisir les identifiants.
4. **Déconnexion complète** : le bouton du portail efface sa session locale, appelle l'endpoint OIDC de fin de session Keycloak et peut afficher une confirmation Keycloak. La déconnexion des autres sessions applicatives déjà ouvertes n'est **pas** automatiquement garantie.

## Architecture Cloud

```text
                          Navigateur HTTPS
                           /           \
                  CampusCloud        BiblioCloud
                FastAPI, client A   FastAPI, client B
                           \           /
                         OpenID Connect + PKCE
                                  |
                            Keycloak IAM
                     Realm: universite-demo-123
                                  |
                           PostgreSQL privé
                 (3 services Web + 1 base sur Render)
```

- Protocole : **OpenID Connect**, Authorization Code Flow et PKCE S256.
- Applications : deux clients OIDC distincts, `portail-universite` et `portail-bibliotheque`.
- Sessions applicatives : cookies signés avec attribut `Secure` en HTTPS.
- Déploiement : instances Render distinctes, hébergement gratuit ; les services peuvent se mettre en veille après inactivité.
- Persistance : PostgreSQL dédié à ce projet.
- Import : le nouveau Realm Cloud est défini dans `cloud/keycloak/universite-realm.json` ; l'ancien Realm local est conservé séparément.

## Déroulement recommandé de la démo

1. Ouvrir CampusCloud, cliquer sur **Se connecter avec Keycloak**, saisir `etudiant / 123`.
2. Montrer le rôle ETUDIANT et l'accès à **Espace étudiant** (HTTP 200).
3. Tenter **Administration** : le serveur renvoie **HTTP 403 — Accès refusé**.
4. Ouvrir **BiblioCloud**, cliquer sur **Se connecter** : observer le SSO, si la session du navigateur est conservée.
5. Cliquer sur **Déconnexion complète** puis, **si Keycloak le demande**, confirmer **Logout**.
6. Se reconnecter avec `admin.universite / 123` et montrer l'accès à **Administration** (HTTP 200).

Voir [GUIDE_DEMONSTRATION.md](GUIDE_DEMONSTRATION.md) pour les phrases à dire à l'oral, et [docs/COMPTE_RENDU_DEMONSTRATION.md](docs/COMPTE_RENDU_DEMONSTRATION.md) pour le compte rendu.

## Version locale facultative

L'exécution locale est indépendante du Cloud et utilise le Realm `universite`, ainsi que les mots de passe locaux historiques, **différents de `123`** :

| Application | URL locale |
|---|---|
| CampusCloud | http://localhost:8000 |
| BiblioCloud | http://localhost:8001 |
| Keycloak | http://localhost:8080 |

1. Installer Docker Desktop et Python 3.11+.
2. Copier `.env.example` en `.env` et définir un secret `SESSION_SECRET` unique.
3. Sous Windows : `powershell -ExecutionPolicy Bypass -File .\scripts\start-demo.ps1`.
4. Sous Linux/macOS : `bash scripts/start-demo.sh`.
5. Le fichier `realm/universite-realm.json` donne les comptes et rôles **locaux**, jamais ceux du Cloud.

La configuration locale n'expose Keycloak que sur `127.0.0.1`. Ne pas ouvrir cette version à Internet.

## Déploiement, sécurité et tests

- `render.yaml` : définition des ressources propres à ce projet ; le Blueprint **ne synchronise pas automatiquement** (`autoDeployTrigger: off`).
- `cloud/keycloak/Dockerfile` : Keycloak en mode production derrière HTTPS Render.
- `app/main.py` : intégration OIDC, espaces protégés, déconnexion complète.
- `app/security.py` : RBAC et vérification des permissions.
- `tests/` : tests automatisés locaux (exécuter `python -m pytest -q tests`).
- [cloud/README_CLOUD.md](cloud/README_CLOUD.md) : configuration Render et limites.
- [DEPLOIEMENT_CLOUD.md](DEPLOIEMENT_CLOUD.md) : déploiement et recommandations de durcissement.
- [CHECKLIST_INDEPENDANCE.md](CHECKLIST_INDEPENDANCE.md) : séparation des ressources.

**Attention** : le PostgreSQL gratuit Render créé le 24 novembre 2026 est une ressource temporaire dont l'expiration est annoncée au **24 décembre 2026**. Prévoir une sauvegarde/migration avant cette échéance pour conserver le projet.

**Aucun autre dépôt, base de données ou service externe au projet Keycloak n'a été modifié dans le cadre de ces mises à jour.**
