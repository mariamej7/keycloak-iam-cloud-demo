# Compte rendu — Démonstration de gestion des identités et des accès dans le Cloud avec Keycloak

**Projet réalisé en binôme. Date de réalisation : 24 novembre 2026.**

## 1. Objectif

Mettre en place une solution pédagogique IAM capable de centraliser l'authentification, distribuer les rôles et démontrer une connexion unique (SSO) entre plusieurs applications universitaires.

## 2. Environnement technique

- **Keycloak 26.8.2** : authentification centralisée, gestion des utilisateurs et rôles.
- **FastAPI** : deux applications indépendantes, CampusCloud et BiblioCloud.
- **PostgreSQL 17** : conservation des informations du Realm et des utilisateurs.
- **Render** : hébergement Cloud dédié, accessible en HTTPS.
- **OpenID Connect** avec Authorization Code + PKCE S256.

Les trois ressources Web et la base de données sont séparées d'autres projets.

## 3. Comptes et droits

| Compte fictif | Rôle | Étudiant | Professeur | Admin | Bibliothèque |
|---|---|:---:|:---:|:---:|:---:|
| `etudiant` | ETUDIANT | 200 | 403 | 403 | 200 |
| `professeur` | PROFESSEUR | 403 | 200 | 403 | 200 |
| `admin.universite` | ADMIN | 200 | 200 | 200 | 200 |

La matrice décrit les droits implémentés dans le code. Des tests réels ont confirmé notamment l'authentification des trois comptes et le refus HTTP 403 pour l'étudiant dans l'administration.

## 4. Déroulement de démonstration

1. Afficher l'accueil du portail https://iam2026-campus-mariam-riad-ufwv.onrender.com.
2. Cliquer sur **Se connecter avec Keycloak** et saisir le compte fictif `etudiant` (mot de passe temporaire pédagogique `123`).
3. Montrer que l'identité et le rôle `ETUDIANT` sont reconnus.
4. Montrer **Espace étudiant** : autorisation **HTTP 200**.
5. Montrer **Administration** : refus **HTTP 403**, contrôlé par FastAPI côté serveur.
6. Passer vers https://iam2026-biblio-mariam-riad-ufwv.onrender.com, puis cliquer sur **Se connecter** afin d'illustrer le SSO avec le même Keycloak.
7. Utiliser **Déconnexion complète** puis, si l'écran Keycloak apparaît, confirmer **Logout** ; ensuite se connecter avec un autre profil pour observer ses droits.

## 5. Résultats

- Les trois comptes fictifs se sont connectés avec succès lors des essais Cloud.
- Le refus HTTP 403 a été observé pour le compte étudiant sur la route d'administration.
- Les portails partagent un serveur Keycloak et des clients OIDC distincts.
- Le bouton de déconnexion complète a été déployé sur les deux portails ; son scénario utilisateur final après mise à jour doit être vérifié manuellement.

## 6. Conclusion

La preuve de concept illustre l'authentification centralisée, la séparation authentification/autorisation, le RBAC et le principe du SSO. Les comptes sont fictifs ; la configuration est volontairement simplifiée et ne convient pas à la production.

**Captures d'écran :** la version PDF du compte rendu remise dans la conversation comprend une capture réelle de la page Keycloak et des illustrations des autres vues reproduites à partir du code. Cette version Markdown est destinée au suivi du projet et ne présente aucune reconstruction comme une capture réelle.
