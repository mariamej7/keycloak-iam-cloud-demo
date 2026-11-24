"""Lance deux applications dans deux processus séparés (sans toucher aux autres projets)."""
from __future__ import annotations
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent.parent
SERVICES = [('universite', 8000), ('bibliotheque', 8001)]
procs = []


def stop_all():
    for proc in procs:
        if proc.poll() is None:
            proc.terminate()
    for proc in procs:
        try:
            proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            proc.kill()


def main():
    try:
        for variant, port in SERVICES:
            env = os.environ.copy()
            env['APP_VARIANT'] = variant
            proc = subprocess.Popen(
                [sys.executable, '-m', 'uvicorn', 'app.main:app',
                 '--host', '127.0.0.1', '--port', str(port)],
                cwd=str(ROOT), env=env,
            )
            procs.append(proc)
        print('\n' + '=' * 60, flush=True)
        print('KEYCLOAK DEMO — applications locales en démarrage', flush=True)
        print('CampusCloud    : http://localhost:8000', flush=True)
        print('BiblioCloud   : http://localhost:8001', flush=True)
        print('Keycloak Admin: http://localhost:8080/admin/', flush=True)
        print('Arrêt des applications : Ctrl+C', flush=True)
        print('=' * 60 + '\n', flush=True)
        while True:
            for proc in procs:
                if proc.poll() is not None:
                    raise RuntimeError('Une application s’est arrêtée. Lire les erreurs ci-dessus.')
            time.sleep(0.8)
    except KeyboardInterrupt:
        print('\nArrêt des deux applications...', flush=True)
    finally:
        stop_all()

if __name__ == '__main__':
    main()
