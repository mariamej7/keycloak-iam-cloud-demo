# Déploiement Cloud actuel — Render

**État documenté au 24 novembre 2026 :** déploiement effectif, distinct de tous les autres projets. Les trois services Web ont été observés en état `live` après les changements et la base PostgreSQL a été créée.

| Ressource | URL ou identifiant | Fonction |
|---|---|---|
| CampusCloud | https://iam2026-campus-mariam-riad-ufwv.onrender.com | Client OIDC `portail-universite` |
| BiblioCloud | https://iam2026-biblio-mariam-riad-ufwv.onrender.com | Client OIDC `portail-bibliotheque` |
| Keycloak | https://iam2026-keycloak-mariam-riad-ufwv.onrender.com | IAM, Realm `universite-demo-123` |
| PostgreSQL | `iam2026-keycloak-pg-ufwv` | Stockage privé Keycloak |

- Image Keycloak : `26.8.2` et démarrage `start --optimized --import-realm`.
- Application FastAPI déployée séparément pour chaque portail.
- HTTPS sur les trois adresses publiques Render.
- Base Render PostgreSQL 17, instance gratuite dédiée.
- Code Cloud Realm : `cloud/keycloak/universite-realm.json`.
- Import Keycloak : `universite-demo-123-realm.json` dans le conteneur ; l'ancien Realm `universite` demeure dans la base et n'est pas utilisé par les portails Cloud.
- Valeurs `KEYCLOAK_REALM=universite-demo-123` sur les deux portails.
- Variables `KC_HOSTNAME`, `KEYCLOAK_EXTERNAL_HOSTNAME`, `CAMPUS_EXTERNAL_HOSTNAME`, `BIBLIO_EXTERNAL_HOSTNAME`, `OTHER_APP_HOSTNAME` : noms d'hôte publics exacts.
- `render.yaml` est un modèle actualisé pour ce déploiement. Toute synchronisation Blueprint est une action explicite, non effectuée ici.

## Comptes pour la démonstration seulement

| Profil | Utilisateur | Mot de passe |
|---|---|---|
| Étudiant | `etudiant` | `123` |
| Professeur | `professeur` | `123` |
| Administrateur des applications | `admin.universite` | `123` |

Le véritable compte technique Keycloak `kcadmin` reste protégé par un **secret Render distinct** ; ne pas le mettre dans GitHub. Le mot de passe `123` est volontairement faible pour les comptes fictifs et **ne doit pas être utilisé en production**.

## Ce qui a été vérifié

- Accès HTTPS aux deux portails et à la configuration OpenID Connect Keycloak.
- Connexion réelle avec les trois comptes fictifs dans le Realm `universite-demo-123`.
- Vérification du rôle `ETUDIANT` et du refus HTTP 403 sur l'URL `/espace/admin`.
- Test du principe de SSO et de l'endpoint Keycloak de déconnexion avec confirmation ; après ajout du bouton `Déconnexion complète`, les deux portails ont été redéployés `live`. **Le scénario complet de changement d'utilisateur après ce déploiement reste à vérifier sur le navigateur de présentation.**

## Coûts et limites de l'offre gratuite

- Les services Render peuvent se mettre en veille ; au premier accès ils peuvent mettre plusieurs minutes à se réveiller.
- PostgreSQL gratuit créé le 24/11/2026 : expiration indiquée le **24/12/2026**. Préparer une solution durable avant la date.
- Aucun dispositif haute disponibilité ni sauvegarde garantie n'a été configuré.
- Le déploiement est destiné aux *comptes fictifs* et non à des données personnelles réelles.

## Isolement du projet

Aucune ressource d'une autre application, dépôt GitHub, service ou base existants n'est adoptée ni modifiée. Trois nouveaux Web Services et un PostgreSQL ont été créés **uniquement** pour cette démo.
