#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
docker compose -f compose.yaml down
echo 'Conteneurs de la démo arrêtés. Volume conservé.'
