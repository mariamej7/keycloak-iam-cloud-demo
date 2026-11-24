# Démonstration Keycloak dans le Cloud avec Render

Ce fichier décrit une **architecture de démonstration**, sans infrastructure PFA partagée.

- Trois Web Services **free** : Keycloak, CampusCloud, BiblioCloud.
- Un nouveau PostgreSQL **free** : `iam2026-keycloak-pg`, inaccessible depuis Internet (autorisation IP externe vide).
- URL HTTPS des clients et mots de passe générés automatiquement par Render grâce à des références Blueprint.
- Les secrets ne doivent jamais être ajoutés au dépôt GitHub. Pour un test, consulter les variables `DEMO_ETUDIANT_PASSWORD`, `DEMO_PROFESSEUR_PASSWORD`, `DEMO_ADMIN_PASSWORD` et `KC_BOOTSTRAP_ADMIN_PASSWORD` dans l'espace Environment du **nouveau service Keycloak uniquement**.
- Le serveur importe une variante Cloud du Realm avec variables `${...}` au premier démarrage ; le Realm local n'est pas modifié.
- Les applications conservent leur exécution locale inchangée ; en Cloud elles utilisent HTTPS, cookies Secure et URLs publiques.

**Attention :** Render gratuit limite chaque service Web à 512 Mo RAM et met les applications en veille en cas d'inactivité. Keycloak peut manquer de mémoire. Le PostgreSQL gratuit expire 30 jours après création. Ne pas annoncer la démo comme opérationnelle en ligne avant d'avoir vérifié le login OIDC et le contrôle HTTP 403.

## Isolement de la PFA

Le Blueprint doit être déployé avec `existingResources: create_new`. Ne jamais utiliser l'option `adopt`. Vérifier dans le plan qu'il propose **uniquement quatre nouvelles ressources** et aucune modification ni redéploiement de `pfa-fleet-platform`.
