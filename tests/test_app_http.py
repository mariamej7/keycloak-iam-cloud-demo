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
