# Contrôle de séparation — projet Keycloak

- [x] Nouveau dossier : `Keycloak_Demo_Universite_Independant`.
- [x] Nouveau projet Docker nommé `keycloak-demo-universite-2026`.
- [x] Base PostgreSQL et volume Docker dédiés à **cette démo seulement**.
- [x] Nouveau Realm `universite` et deux clients OIDC réservés à la démo.
- [x] Deux serveurs Python locaux uniquement, aux ports 8000 et 8001.
- [x] Aucune référence au dépôt ou à l'application PFA dans le code opérationnel.
- [x] Aucun script ne supprime des conteneurs, volumes ou bases de données existants.
- [x] Aucune création ou modification exécutée dans GitHub, Render, Vercel ou Supabase.
- [ ] Tests réels Docker + Keycloak sur l'ordinateur cible (à réaliser).
- [ ] Déploiement Cloud indépendant (en attente de demande explicite).

## Règles avant la démo

Le projet doit toujours être lancé dans **son propre dossier extrait**. Ne pas copier les fichiers de la démo dans un dépôt ou un répertoire d'un autre projet. Ne jamais réutiliser les variables d'environnement ni les identifiants d'une application existante.