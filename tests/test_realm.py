import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
REALM = json.loads((ROOT / 'realm' / 'universite-realm.json').read_text(encoding='utf8'))


def test_name_and_clients():
    assert REALM['realm'] == 'universite'
    assert {c['clientId'] for c in REALM['clients']} == {'portail-universite', 'portail-bibliotheque'}


def test_redirects():
    for client in REALM['clients']:
        assert all(uri.startswith('http://localhost:') for uri in client['redirectUris'])
        assert client['attributes']['pkce.code.challenge.method'] == 'S256'


def test_roles_users():
    roles = {r['name'] for r in REALM['roles']['realm']}
    assert roles == {'ADMIN', 'ETUDIANT', 'PROFESSEUR'}
    assert len(REALM['users']) == 3
    assert all(set(u['realmRoles']) <= roles for u in REALM['users'])


def test_id_token_roles_mapper():
    for client in REALM['clients']:
        mapper = client['protocolMappers'][0]
        assert mapper['config']['claim.name'] == 'roles'
        assert mapper['config']['id.token.claim'] == 'true'
