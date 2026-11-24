# Contrôle de séparation — Démo Keycloak Cloud

## Ressources de démonstration indépendantes

- [x] Dépôt GitHub dédié `mariamej7/keycloak-iam-cloud-demo`.
- [x] Deux applications propres au projet : CampusCloud et BiblioCloud.
- [x] Service Cloud Keycloak distinct, hébergé sur Render.
- [x] Base PostgreSQL Render gratuite **dédiée** à ce projet.
- [x] Realm Cloud `universite-demo-123`, trois rôles, trois comptes fictifs.
- [x] Deux clients OpenID Connect indépendants.
- [x] Déploiements des portails `live` après ajout du bouton `Déconnexion complète`.
- [x] Connexion et autorisations testées pour les trois profils fictifs.
- [x] Aucun code opérationnel n'utilise des données d'un autre projet.
- [x] Aucun service GitHub, Render, Vercel ou base d'un autre projet n'a été modifié pour la démo.
- [ ] Tester le changement complet d'identité `etudiant` → `admin.universite` dans la fenêtre de démonstration après le dernier déploiement.
- [ ] Prévoir une migration ou une sauvegarde de la base gratuite avant le 24 décembre 2026.
- [ ] Remplacer les identifiants de démonstration si le projet est destiné à de vrais utilisateurs.

## Environnement local distinct

- [x] Projet Docker local `keycloak-demo-universite-2026` indépendant.
- [x] Realm local `universite` conservé séparément du Realm Cloud.
- [x] `compose.yaml` utilise ses propres ports, volumes et réseau.

**Règle permanente** : jamais de partage de secrets, de bases de données ou de fichiers avec une autre application.
