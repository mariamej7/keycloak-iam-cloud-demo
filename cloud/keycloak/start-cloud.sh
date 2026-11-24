#!/bin/sh
# Configure uniquement les mots de passe des 3 comptes fictifs Keycloak.
# L'administrateur technique du realm master n'est jamais modifie.
set -eu

if [ -z "${DEMO_SHARED_PASSWORD:-}" ]; then
  exec /opt/keycloak/bin/kc.sh start --optimized --import-realm
fi

/opt/keycloak/bin/kc.sh start --optimized --import-realm &
KEYCLOAK_PID=$!

(
  # Sur Render gratuit, Keycloak peut necessiter plusieurs minutes au demarrage.
  # Ne pas lancer la CLI Java en boucle pendant l'initialisation lourde.
  sleep 75
  tries=0
  until /opt/keycloak/bin/kcadm.sh config credentials \
    --server http://127.0.0.1:10000 \
    --realm master \
    --user "$KC_BOOTSTRAP_ADMIN_USERNAME" \
    --password "$KC_BOOTSTRAP_ADMIN_PASSWORD" >/dev/null 2>&1; do
    tries=$((tries + 1))
    if [ "$tries" -ge 20 ] || ! kill -0 "$KEYCLOAK_PID" 2>/dev/null; then
      echo 'ERROR: impossible d appliquer les mots de passe de demonstration' >&2
      exit 1
    fi
    sleep 20
  done

  for username in etudiant professeur admin.universite; do
    if /opt/keycloak/bin/kcadm.sh set-password \
      --realm universite --username "$username" \
      --new-password "$DEMO_SHARED_PASSWORD" >/dev/null 2>&1; then
      echo "Mot de passe du compte demo $username configure"
    else
      echo "ERROR: echec configuration du compte demo $username" >&2
    fi
  done
) &

wait "$KEYCLOAK_PID"
