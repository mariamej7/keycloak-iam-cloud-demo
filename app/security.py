"""Autorisation explicite côté serveur, indépendante de l'affichage des boutons."""
from collections.abc import Mapping
from typing import Any

KNOWN_ROLES = frozenset({'ETUDIANT', 'PROFESSEUR', 'ADMIN'})


def roles_from_claims(claims: Mapping[str, Any]) -> list[str]:
    """Lire la revendication de rôle issue d'un ID token OIDC vérifié par Authlib.

    Le mapping Keycloak inclus dans le realm émet une revendication `roles`.
    Le support `realm_access.roles` rend l'exemple plus tolérant aux variations.
    """
    raw = claims.get('roles', [])
    if not raw:
        realm_access = claims.get('realm_access') or {}
        raw = realm_access.get('roles', []) if isinstance(realm_access, Mapping) else []
    if isinstance(raw, str):
        raw = [raw]
    if not isinstance(raw, (tuple, list)):
        return []
    return sorted(set(r for r in raw if isinstance(r, str) and r in KNOWN_ROLES))


def is_authorized(user: Mapping[str, Any] | None, allowed_roles: set[str]) -> bool:
    return bool(user and allowed_roles.intersection(set(user.get('roles', []))))
