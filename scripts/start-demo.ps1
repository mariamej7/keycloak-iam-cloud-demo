# Démo 100 % distincte. Ne supprime aucun volume/conteneur externe.
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $root
if (-not (Test-Path '.env')) {
  Copy-Item '.env.example' '.env'
  Write-Host 'Le fichier .env local vient d’être créé. Modifiez les secrets pour une meilleure sécurité.' -ForegroundColor Yellow
}
Write-Host 'Démarrage des conteneurs Keycloak et PostgreSQL dédiés...' -ForegroundColor Cyan
docker compose -f compose.yaml up -d
if ($LASTEXITCODE -ne 0) { throw 'Docker n’a pas démarré. Vérifiez Docker Desktop.' }
if (-not (Test-Path '.venv\Scripts\python.exe')) {
  python -m venv .venv
  if ($LASTEXITCODE -ne 0) { throw 'Impossible de créer le venv Python.' }
}
& '.\.venv\Scripts\python.exe' -m pip install -r app\requirements.txt
if ($LASTEXITCODE -ne 0) { throw 'Installation des dépendances Python échouée.' }
Write-Host 'Ouverture locale sur http://localhost:8000 et http://localhost:8001' -ForegroundColor Green
Write-Host 'Le premier lancement de Keycloak peut prendre une ou deux minutes.' -ForegroundColor Yellow
& '.\.venv\Scripts\python.exe' scripts\run_apps.py
