from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent


def test_no_pfa_reference_in_operational_files():
    """Assurer l'absence de toute dépendance à l'ancienne plateforme."""
    for filename in ['compose.yaml', 'app/main.py', '.env.example', 'scripts/start-demo.ps1', 'scripts/start-demo.sh']:
        s=(ROOT / filename).read_text(encoding='utf-8').lower()
        assert 'pfa-fleet-platform' not in s
        assert 'oritech' not in s
        assert 'supabase' not in s


def test_docker_scopes_all_resources():
    s=(ROOT/'compose.yaml').read_text()
    assert 'name: keycloak-demo-universite-2026' in s
    assert '127.0.0.1:8080:8080' in s
    assert 'kc_demo_pg_data' in s
