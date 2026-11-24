# Déploiement Keycloak IAM dans le Cloud — état réalisé et améliorations

## Architecture effectivement mise en place

Le 24 novembre 2026, **quatre ressources dédiées** ont été créées dans Render : Keycloak, CampusCloud, BiblioCloud et PostgreSQL 17. Les applications sont accessibles par les URLs HTTPS documentées dans [cloud/README_CLOUD.md](cloud/README_CLOUD.md).

- Keycloak 26.8.2 en mode de production (derrière le proxy HTTPS Render) et hostname externe configuré.
- PostgreSQL hébergé séparément, avec persistance dédiée.
- Deux portails FastAPI utilisant OpenID Connect Authorization Code + PKCE (clients indépendants).
- Un Realm Cloud `universite-demo-123` comprenant trois rôles et trois comptes fictifs.
- Contrôles d'autorisation appliqués dans FastAPI ; accès interdit retournant HTTP 403.
- Déconnexion OIDC demandée par le bouton `Déconnexion complète`; Keycloak peut demander confirmation.

## Sécurité : limites du prototype

**Ce projet est une démonstration et n'est pas une infrastructure IAM de production.**

1. Le mot de passe `123` des trois utilisateurs fictifs doit être remplacé par des mots de passe longs et distincts avant toute ouverture à de vrais utilisateurs.
2. Activer MFA pour les administrateurs techniques, désactiver les comptes de démonstration et durcir les droits d'administration.
3. Protéger les secrets Render, les faire tourner périodiquement et éviter toute copie dans Git.
4. Mettre en place sauvegardes automatiques et monitoring de PostgreSQL et de Keycloak.
5. Pour une déconnexion globale stricte entre plusieurs applications, ajouter la propagation de session (front/back-channel logout) ou des sessions serveur invalidables ; le bouton actuel lance le logout SSO et efface la session du portail courant.
6. Prévoir une offre Cloud adaptée en RAM, en disponibilité et en temps de démarrage (Render gratuit met les services en veille).

## Durée de vie et conservation

La base PostgreSQL gratuite de démonstration a été créée le 24 novembre 2026 ; son expiration est signalée au 24 décembre 2026. Ne pas attendre la date limite pour une sauvegarde ou une migration.

## Indépendance

Toute action de déploiement et tous les fichiers de ce dépôt sont propres à **ce projet Keycloak uniquement**. Ne pas adopter, supprimer, relancer, mettre à jour ou synchroniser les ressources d'un autre projet.

Documentation complémentaire : [README.md](README.md), [GUIDE_DEMONSTRATION.md](GUIDE_DEMONSTRATION.md), [CHECKLIST_INDEPENDANCE.md](CHECKLIST_INDEPENDANCE.md).
