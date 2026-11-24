# Démonstration Keycloak — script oral pour deux personnes (6 à 8 minutes)

## Avant de passer devant le professeur

- Docker Desktop en marche, deux serveurs FastAPI en marche, `http://localhost:8080` prêt.
- Utiliser des onglets distincts pour `http://localhost:8000` et `http://localhost:8001`.
- Prévoir les identifiants **fictifs** de `README.md`.
- Éviter de montrer des secrets de `.env` ou des informations personnelles.
- Tester l'authentification une fois au préalable, et savoir que les sessions SSO continuent après une déconnexion locale.

## Minute 0:00 – 0:50 — Lancement du scénario (personne 1)

**À dire :** « Notre objectif est de sécuriser l'accès à deux applications du campus grâce à un serveur centralisé de gestion des identités et des accès. Nous avons installé Keycloak avec PostgreSQL et intégré deux applications indépendantes à l'aide d'OpenID Connect. »

**À montrer :** la page d'accueil CampusCloud et le lien vers BiblioCloud. Souligner les deux adresses `localhost:8000` et `localhost:8001`.

## Minute 0:50 – 2:00 — Authentification centralisée (personne 1)

**À faire :** sur CampusCloud, cliquer sur « Se connecter avec Keycloak ». Le navigateur va vers Keycloak. Entrer les identifiants de l'étudiant.

**À dire :** « L'application ne stocke pas le mot de passe. Elle délègue la vérification de l'identité à Keycloak. Après authentification, Keycloak renvoie une preuve d'identité selon le protocole OpenID Connect. »

**Résultat attendu :** nom et rôle de l'étudiant visibles sur CampusCloud.

## Minute 2:00 – 3:30 — Autorisation basée sur les rôles (personne 2)

**À faire :** cliquer sur « Espace étudiant » (accès autorisé). Puis sur « Administration » (accès refusé).

**À dire :** « Authentification signifie : qui êtes-vous ? Autorisation signifie : qu'avez-vous le droit de faire ? Notre étudiant est bien connecté, mais il n'a pas le rôle ADMIN. Le serveur répond donc par un code HTTP 403. Cette vérification n'est pas seulement visuelle : elle est appliquée côté serveur, même si l'utilisateur saisit directement l'adresse. »

**Résultat attendu :** écran vert d'autorisation (HTTP 200), puis écran « Accès refusé » (HTTP 403).

## Minute 3:30 – 5:00 — Single Sign-On sur une deuxième application (personne 2)

**À faire :** sur CampusCloud, cliquer sur le lien BiblioCloud. Dans BiblioCloud, cliquer sur « Se connecter ».

**À dire :** « Les deux applications ont des clients OIDC différents, mais partagent le même serveur Keycloak. Tant que la session SSO de Keycloak reste active, la connexion à la deuxième application se fait sans ressaisir les identifiants. C'est le principe du Single Sign-On. »

**Résultat attendu :** connexion à BiblioCloud et accès à Bibliothèque numérique.

## Minute 5:00 – 6:00 — Montrer le Realm dans Keycloak (personne 1)

**À faire :** ouvrir `http://localhost:8080/admin/`, choisir le Realm `universite`, afficher les sections **Users**, **Realm roles**, **Clients**.

**À dire :** « Nous avons séparé la gestion des identités, des rôles et des applications clientes. Le même Realm contient trois utilisateurs fictifs, trois rôles et deux applications clientes indépendantes. »

## Minute 6:00 – 7:00 — Sécurité et limites (les deux)

**À dire :** « Nous utilisons l'Authorization Code Flow avec PKCE. L'application valide les informations OpenID Connect et contrôle les permissions sur ses routes. Notre environnement actuel est local pour la démonstration. Pour le Cloud public, nous utiliserions Keycloak en mode production, HTTPS, une base persistante et des secrets sécurisés. »

**Option MFA :** si testé avant, configurer OTP sur un compte et en montrer la connexion. Ne pas improviser la configuration en direct si le téléphone d'authentification n'est pas prêt.

## Questions probables du professeur

**Pourquoi Keycloak ?** Il centralise les identités et l'authentification, gère des rôles et supporte OIDC, SAML et SSO sans développer un système d'authentification à partir de zéro.

**IAM, c'est quoi ?** Identity and Access Management : identifier les utilisateurs, les authentifier et gérer leurs droits d'accès.

**Différence IAM et SSO ?** IAM est le système global de gestion des identités et permissions. SSO est l'une de ses fonctionnalités : une session d'authentification réutilisée entre plusieurs applications.

**Qui vérifie les permissions ?** Dans notre démonstration, Keycloak émet les rôles dans un ID token, mais **l'application vérifie les rôles côté serveur** pour les routes protégées.

**Que se passe-t-il avec un étudiant sur `/espace/admin` ?** HTTP 403 : connecté, mais insuffisamment autorisé.

**Quel est le rôle de PostgreSQL ?** Conserver durablement les données Keycloak (utilisateurs, Realm, clients, paramètres).

**Qu'est-ce qui est vraiment dans le Cloud ?** Dans la version présentée ici, Keycloak et PostgreSQL tournent en Docker **en local** ; c'est un prototype d'architecture cloud-ready. On ne doit pas prétendre avoir déjà déployé une instance publique sans l'avoir fait.