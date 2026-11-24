#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
if [ ! -f .env ]; then
  cp .env.example .env
  echo "[ATTENTION] .env créé : remplacez les secrets avant toute exposition externe."
fi
echo 'Démarrage Keycloak + PostgreSQL dédiés au projet...'
docker compose -f compose.yaml up -d
python3 -m venv .venv
.venv/bin/python -m pip install -r app/requirements.txt
echo 'CampusCloud : http://localhost:8000'
echo 'BiblioCloud: http://localhost:8001'
echo 'Keycloak peut prendre une ou deux minutes au premier démarrage.'
.venv/bin/python scripts/run_apps.py
