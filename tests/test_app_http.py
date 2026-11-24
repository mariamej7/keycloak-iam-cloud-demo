"""Tests HTTP limités à l'application, sans Keycloak lancé.

Ces tests ne remplacent PAS une validation OpenID Connect réelle dans le navigateur.
"""
import base64
import json
import os

import pytest

pytest.importorskip('authlib')

from itsdangerous import TimestampSigner
from fastapi.testclient import TestClient

os.environ['SESSION_SECRET'] = 'only-test-secret-not-for-production'
os.environ['APP_VARIANT'] = 'universite'
from app.main import app  # noqa: E402


def session_cookie(user):
    payload = json.dumps({'user': user}).encode('utf8')
    signer = TimestampSigner('only-test-secret-not-for-production-universite')
    return signer.sign(base64.b64encode(payload)).decode('utf8')


def test_home_and_health():
    with TestClient(app) as client:
        assert client.get('/').status_code == 200
        assert client.get('/health').json()['status'] == 'ok'


def test_redirect_anonymous_to_login():
    with TestClient(app) as client:
        res = client.get('/espace/admin', follow_redirects=False)
        assert res.status_code == 303
        assert res.headers['location'] == '/login'


def test_student_admin_is_http_403():
    with TestClient(app) as client:
        client.cookies.set('session_keycloak_universite', session_cookie({'username': 'etudiant', 'roles': ['ETUDIANT']}))
        assert client.get('/espace/etudiant').status_code == 200
        response = client.get('/espace/admin')
        assert response.status_code == 403
        assert 'Accès refusé' in response.text

def test_complete_logout_redirects_to_keycloak_and_clears_session():
    from urllib.parse import parse_qs, urlsplit

    with TestClient(app, base_url='http://localhost:8000') as client:
        client.cookies.set('session_keycloak_universite', session_cookie({
            'username': 'etudiant', 'roles': ['ETUDIANT']
        }))
        response = client.post('/logout', follow_redirects=False)
        assert response.status_code == 303
        url = urlsplit(response.headers['location'])
        assert url.path.endswith('/realms/universite/protocol/openid-connect/logout')
        query = parse_qs(url.query)
        assert query['client_id'] == ['portail-universite']
        assert query['post_logout_redirect_uri'] == ['http://localhost:8000/auth/callback']
        assert query['state'] == ['logout-complete']
        assert 'session_keycloak_universite' in response.headers.get('set-cookie', '')
        assert client.get('/').status_code == 200


def test_logout_callback_returns_to_public_home():
    with TestClient(app) as client:
        response = client.get('/auth/callback?state=logout-complete', follow_redirects=False)
        assert response.status_code == 303
        assert response.headers['location'] == '/'


def test_home_displays_complete_logout_control_after_authentication():
    with TestClient(app) as client:
        client.cookies.set('session_keycloak_universite', session_cookie({
            'username': 'etudiant', 'roles': ['ETUDIANT']
        }))
        response = client.get('/')
        assert response.status_code == 200
        assert 'Déconnexion complète' in response.text
