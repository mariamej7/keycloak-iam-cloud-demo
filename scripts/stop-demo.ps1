$ErrorActionPreference = 'Stop'
Set-Location (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Write-Host 'Arrêt uniquement des conteneurs dédiés à Keycloak Démo...' -ForegroundColor Cyan
docker compose -f compose.yaml down
Write-Host 'Données conservées dans le volume kc_demo_pg_data.'
