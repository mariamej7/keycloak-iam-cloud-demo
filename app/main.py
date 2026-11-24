"""Deux portails FastAPI reliés au même Keycloak via OIDC (Authorization Code + PKCE)."""
from __future__ import annotations

import logging
import os
from pathlib import Path
from urllib.parse import urlencode

import httpx

from authlib.integrations.starlette_client import OAuth, OAuthError
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from starlette.staticfiles import StaticFiles

from app.security import is_authorized, roles_from_claims

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / '.env')
VARIANT = os.getenv('APP_VARIANT', 'universite').strip().lower()
if VARIANT not in ('universite', 'bibliotheque'):
    raise ValueError('APP_VARIANT doit être universite ou bibliotheque.')
CONFIG = {
    'universite': {'name': 'CampusCloud', 'port': 8000, 'client_id': 'portail-universite',
                   'subtitle': 'Portail universitaire sécurisé'},
    'bibliotheque': {'name': 'BiblioCloud', 'port': 8001, 'client_id': 'portail-bibliotheque',
                     'subtitle': 'Bibliothèque numérique du campus'},
}[VARIANT]
# Mode local par defaut, HTTPS public sur Render.
PUBLIC_HOST = os.getenv('RENDER_EXTERNAL_HOSTNAME', '').strip()
BASE_URL = os.getenv('APP_BASE_URL') or (f'https://{PUBLIC_HOST}' if PUBLIC_HOST else f"http://localhost:{CONFIG['port']}")
BASE_URL = BASE_URL.rstrip('/')
KEYCLOAK_HOST = os.getenv('KEYCLOAK_EXTERNAL_HOSTNAME', '').strip()
KEYCLOAK_URL = (os.getenv('KEYCLOAK_URL') or (f'https://{KEYCLOAK_HOST}' if KEYCLOAK_HOST else 'http://localhost:8080')).rstrip('/')
OTHER_HOST = os.getenv('OTHER_APP_HOSTNAME', '').strip()
OTHER_URL = f'https://{OTHER_HOST}' if OTHER_HOST else f"http://localhost:{8001 if VARIANT == 'universite' else 8000}"
REALM = os.getenv('KEYCLOAK_REALM', 'universite')
SESSION_SECRET = os.getenv('SESSION_SECRET')
if not SESSION_SECRET:
    # Lancer l'appli via le guide : il crée un .env dédié.
    raise RuntimeError('SESSION_SECRET manquant. Copiez .env.example vers .env et définissez un secret.')

app = FastAPI(title=f"{CONFIG['name']} — Keycloak IAM", docs_url=None, redoc_url=None)
app.add_middleware(
    SessionMiddleware,
    secret_key=f'{SESSION_SECRET}-{VARIANT}',
    session_cookie=f'session_keycloak_{VARIANT}',
    max_age=3600,
    same_site='lax',
    https_only=BASE_URL.startswith('https://'),  # Cookie Secure sur Render et HTTP local.
)
app.mount('/static', StaticFiles(directory=ROOT / 'app' / 'static'), name='static')
templates = Jinja2Templates(directory=ROOT / 'app' / 'templates')

# Endpoints OIDC declares explicitement pour eviter la requete de discovery
# pendant le premier clic de connexion. Sur Render Free, Keycloak peut dormir;
# une redirection navigateur le reveille, contrairement a la requete interne.
# La validation de l'ID token continue via l'issuer et les cles JWKS publiques.
OIDC_ISSUER = f'{KEYCLOAK_URL}/realms/{REALM}'
OIDC_PROTOCOL = f'{OIDC_ISSUER}/protocol/openid-connect'
oauth = OAuth()
oauth.register(
    name='keycloak',
    client_id=CONFIG['client_id'],
    authorize_url=f'{OIDC_PROTOCOL}/auth',
    access_token_url=f'{OIDC_PROTOCOL}/token',
    jwks_uri=f'{OIDC_PROTOCOL}/certs',
    issuer=OIDC_ISSUER,
    client_kwargs={
        'scope': 'openid profile email',
        'code_challenge_method': 'S256',
        'token_endpoint_auth_method': 'none',
    },
)


def view(request: Request, name: str, status_code: int = 200, **context):
    user = request.session.get('user')
    return templates.TemplateResponse(request=request, name=name, context={
        'user': user, 'config': CONFIG, 'variant': VARIANT,
        'other_port': 8001 if VARIANT == 'universite' else 8000,
        'other_name': 'BiblioCloud' if VARIANT == 'universite' else 'CampusCloud',
        'other_url': OTHER_URL, 'cloud_mode': BASE_URL.startswith('https://'),
        **context,
    }, status_code=status_code)


def protected(request: Request, allowed_roles: set[str], title: str, text: str):
    user = request.session.get('user')
    if not user:
        return RedirectResponse('/login', status_code=303)
    if not is_authorized(user, allowed_roles):
        return view(request, 'denied.html', title=title, status_code=403)
    return view(request, 'section.html', title=title, body=text)


@app.get('/', response_class=HTMLResponse)
async def home(request: Request):
    # Efface les paramètres de suivi ajoutés par des liens externes (ex. utm_source).
    # Ne touche jamais aux paramètres OIDC de /login et /auth/callback.
    if any(key.lower().startswith('utm_') for key in request.query_params.keys()):
        return RedirectResponse(url='/', status_code=302)
    return view(request, 'home.html')


@app.get('/login')
async def login(request: Request):
    # Authlib génère le state et le code_verifier PKCE, conservés en session.
    # Sur Render gratuit, Keycloak peut répondre 502 pendant son réveil.
    # Ne jamais exposer une erreur interne à l'utilisateur : proposer de réessayer.
    try:
        return await oauth.keycloak.authorize_redirect(request, f'{BASE_URL}/auth/callback')
    except httpx.HTTPError as exc:
        logging.getLogger(__name__).warning(
            'Keycloak indisponible durant le lancement OIDC (%s)', type(exc).__name__
        )
        return view(
            request, 'auth_wait.html', status_code=503,
        )


@app.get('/auth/callback')
async def auth_callback(request: Request):
    # Le client OIDC utilise le meme callback autorise pour la fin de deconnexion.
    # Le state de deconnexion est distinct du state aleatoire du login.
    if request.query_params.get('state') == 'logout-complete' and not request.query_params.get('code'):
        return RedirectResponse('/', status_code=303)
    try:
        token = await oauth.keycloak.authorize_access_token(request)
        # Authlib a validé l'ID token OIDC (signature / issuer / audience / nonce).
        claims = token.get('userinfo')
        if not claims or not claims.get('sub'):
            return view(request, 'error.html', message='Identité OIDC invalide.', status_code=401)
        request.session.clear()
        request.session['user'] = {
            'sub': claims['sub'],
            'username': claims.get('preferred_username', ''),
            'name': claims.get('name') or claims.get('preferred_username', 'Utilisateur'),
            'roles': roles_from_claims(claims),
        }
        return RedirectResponse('/', status_code=303)
    except OAuthError:
        return view(request, 'error.html', message='La connexion a échoué ou a été annulée.', status_code=401)
    except Exception:
        # Pas d'affichage de secrets, d'ID token ou de trace dans le navigateur.
        return view(request, 'error.html', message='Keycloak est peut-être indisponible. Vérifiez sa disponibilité.', status_code=503)


@app.post('/logout')
async def logout(request: Request):
    # Efface la session applicative, puis ferme la session SSO sur Keycloak.
    # Keycloak peut demander une confirmation avant de revenir au portail.
    request.session.clear()
    params = urlencode({
        'client_id': CONFIG['client_id'],
        'post_logout_redirect_uri': f'{BASE_URL}/auth/callback',
        'state': 'logout-complete',
    })
    end_session = f'{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/logout'
    return RedirectResponse(f'{end_session}?{params}', status_code=303)


@app.get('/espace/etudiant')
async def etudiant(request: Request):
    return protected(request, {'ETUDIANT', 'ADMIN'}, 'Espace étudiant',
                     'Cours disponibles, calendrier pédagogique et suivi de vos inscriptions.')


@app.get('/espace/professeur')
async def professeur(request: Request):
    return protected(request, {'PROFESSEUR', 'ADMIN'}, 'Espace professeur',
                     'Gestion des cours, ressources pédagogiques et espace des évaluations.')


@app.get('/espace/admin')
async def admin(request: Request):
    return protected(request, {'ADMIN'}, 'Administration',
                     'Gestion institutionnelle réservée aux administrateurs autorisés.')


@app.get('/espace/bibliotheque')
async def bibliotheque(request: Request):
    return protected(request, {'ETUDIANT', 'PROFESSEUR', 'ADMIN'}, 'Bibliothèque numérique',
                     'Catalogue des ouvrages, ressources scientifiques et accès documentaire.')


@app.get('/health')
async def health():
    return {'status': 'ok', 'application': CONFIG['name'], 'provider': 'Keycloak'}
