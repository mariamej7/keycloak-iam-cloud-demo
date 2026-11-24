# Extension Cloud — plan de déploiement indépendant

> **À faire seulement avec accord explicite.** Ce document ne déploie rien et ne requiert aucun accès aux services existants.

## Architecture cible

1. Une **nouvelle instance Cloud dédiée à Keycloak**, distincte des environnements et services existants.
2. Un **nouveau PostgreSQL indépendant**, accessible uniquement depuis l'instance Keycloak, avec sauvegardes et restrictions réseau.
3. Un **nouveau nom de domaine / sous-domaine** et un **proxy HTTPS** (certificats TLS, en-têtes `X-Forwarded-*` de confiance).
4. Deux **nouveaux services applicatifs indépendants** (CampusCloud, BiblioCloud), avec clients OIDC séparés et leurs URLs HTTPS réelles.
5. Gestion des secrets via un **secret manager / variables secrètes de la plateforme** et comptes de test à mots de passe changés.

## Changements indispensables avant exposition à Internet

- Remplacer **`start-dev`** par le mode production `start`, configurer le hostname HTTPS, les proxys et les health checks selon la documentation officielle de la version utilisée.
- **Ne pas publier le fichier Realm contenant les identifiants démo** comme utilisateurs opérationnels. Créer des comptes de démonstration avec mots de passe nouveaux et/ou supprimer les utilisateurs du fichier d'import public.
- Définir des domaines HTTPS et actualiser `redirectUris` + `webOrigins` des deux clients.
- Dans FastAPI, passer les sessions à **Secure (`https_only=True`)** et à une gestion de session serveur adaptée à la production, avec rotation, expiration et révocation des sessions si nécessaire.
- Réévaluer l'authentification `client` public + PKCE selon l'architecture, l'hébergement et la politique de sécurité.
- Ajouter une vraie déconnexion globale OIDC (RP-Initiated Logout) si elle est exigée.
- Limiter l'accès à la console d'administration, activer MFA pour les administrateurs, sauvegarder PostgreSQL et surveiller les logs.
- Prévoir la disponibilité Keycloak / la connectivité à la base et vérifier les obligations de coût de la plateforme Cloud choisie.

## Séparation stricte

**Ne jamais réutiliser :** dépôt GitHub existant, service Render existant, projet Supabase existant, application Vercel existante, variables d'environnement d'un autre projet, ou secrets partagés.

Le **nouveau déploiement** devra être créé dans des ressources neuves et clairement identifiées. Il ne doit jamais invoquer une action de suppression, modification ou redéploiement d'une autre application.

## Références

- https://www.keycloak.org/server/configuration-production
- https://www.keycloak.org/server/reverseproxy
- https://www.keycloak.org/server/db
- https://www.keycloak.org/server/containers