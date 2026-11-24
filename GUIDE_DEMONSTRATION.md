# Guide de démonstration Keycloak — Version Cloud (8 à 10 minutes)

**Projet** : mise en place d'une solution de gestion des identités et des accès dans le Cloud avec Keycloak.

**Démarrage** : ouvrir https://iam2026-campus-mariam-riad-ufwv.onrender.com ; attendre le réveil éventuel de Render gratuit. Le serveur Keycloak peut mettre plusieurs minutes à démarrer après une période d'inactivité.

**Comptes fictifs** : `etudiant / 123`, `professeur / 123`, `admin.universite / 123`. **Ne jamais montrer ni communiquer les véritables secrets Render ou de l'administrateur technique Keycloak.**

## 0:00–1:00 — Présentation (personne 1)

**À faire** : afficher la page d'accueil CampusCloud.

**À dire** : « Notre objectif est de centraliser la gestion des identités et des accès d'une université. Nous avons créé deux applications indépendantes, CampusCloud et BiblioCloud, connectées à un serveur Keycloak commun et déployées sur Render. »

## 1:00–2:00 — Authentification Keycloak (personne 1)

**À faire** : cliquer sur **Se connecter avec Keycloak** et observer le changement d'adresse vers le serveur Keycloak. Se connecter avec `etudiant / 123`.

**À dire** : « CampusCloud ne vérifie pas lui-même le mot de passe. Il délègue l'authentification à Keycloak via OpenID Connect. L'application reçoit ensuite l'identité et les rôles vérifiés de l'utilisateur. »

**Résultat attendu** : utilisateur `etudiant`, rôle `ETUDIANT` affiché.

## 2:00–3:30 — Autorisation RBAC (personne 2)

**À faire** : ouvrir **Espace étudiant**, voir `HTTP 200` ; revenir à l'accueil, ouvrir **Administration**, voir `HTTP 403`.

**À dire** : « L'authentification répond à *Qui êtes-vous ?* ; l'autorisation répond à *Qu'avez-vous le droit de faire ?* Le rôle ETUDIANT n'autorise pas l'administration. La vérification est réalisée côté serveur, même si l'URL est saisie directement. »

## 3:30–5:00 — Single Sign-On (personne 2)

**À faire** : sans se déconnecter, cliquer sur **BiblioCloud** ; puis **Se connecter**. Ne pas ouvrir de navigation privée, car le SSO dépend de la session existante.

**À dire** : « Les deux applications ont des clients OpenID Connect différents mais partagent le même fournisseur d'identité. Keycloak réutilise la session existante : nous n'avons pas besoin de ressaisir notre mot de passe. »

**Résultat attendu** : BiblioCloud reconnaît le compte ; **Bibliothèque numérique** est accessible (HTTP 200).

## 5:00–6:30 — Déconnexion et changement d'utilisateur (personne 1)

**À faire** : sur l'application, cliquer sur **Déconnexion complète**. Si Keycloak présente l'écran « Do you want to log out? », cliquer sur **Logout**. Revenir sur CampusCloud. Cliquer sur **Se connecter**, saisir `admin.universite / 123`, puis ouvrir **Administration**.

**À dire** : « Contrairement à une simple déconnexion locale, ce bouton lance la fin de la session centrale Keycloak. Nous pouvons ensuite nous authentifier avec un autre profil et constater que ses permissions sont différentes. »

**Attention** : les sessions de l'autre application, si déjà établies, ne sont pas forcément invalidées immédiatement. Pour un scénario sans ambiguïté, repartir de CampusCloud et vérifier quel compte est affiché.

## 6:30–8:00 — Architecture Cloud (personne 2)

**À montrer** : l'architecture dans `README.md` ou `docs/COMPTE_RENDU_DEMONSTRATION.md`.

**À dire** : « Trois services Web sont déployés sur Render : Keycloak, CampusCloud et BiblioCloud. PostgreSQL conserve les utilisateurs et la configuration du serveur IAM. L'authentification utilise OpenID Connect avec PKCE et les connexions publiques sont en HTTPS. »

## 8:00–9:00 — Conclusion (les deux)

**À dire** : « Nous avons démontré l'authentification centralisée, le contrôle d'accès RBAC et le Single Sign-On entre deux applications distinctes. Keycloak simplifie la gestion des identités, tandis que les applications appliquent leurs propres règles d'autorisation. »

## Questions possibles

**Pourquoi deux applications ?** Pour démontrer le SSO, qui concerne plusieurs applications indépendantes.

**Pourquoi HTTP 403 ?** L'identité est reconnue, mais le rôle ne permet pas l'accès.

**Keycloak autorise-t-il toutes les pages ?** Non. Keycloak fournit les rôles ; FastAPI vérifie les permissions sur les routes protégées.

**Quelle différence entre `admin.universite` et `kcadmin` ?** Le premier est un utilisateur fictif ayant le rôle ADMIN dans les portails ; le second administre réellement le serveur Keycloak.

**Pourquoi le mot de passe `123` ?** Uniquement pour faciliter la démonstration pédagogique avec des comptes fictifs. C'est insuffisant pour des utilisateurs réels.

**SSO vs déconnexion complète ?** Le SSO réutilise une session centrale Keycloak ; la déconnexion complète demande à Keycloak de fermer cette session, avec confirmation éventuelle.

**Limites ?** Hébergement gratuit Render sujet aux démarrages lents ; base gratuite temporaire ; configuration de comptes fictifs non adaptée à la production.
