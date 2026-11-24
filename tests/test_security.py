from app.security import is_authorized, roles_from_claims


def test_roles_oidc_custom_claim():
    assert roles_from_claims({'roles': ['ADMIN', 'PROFESSEUR', 'ignored']}) == ['ADMIN', 'PROFESSEUR']


def test_roles_oidc_realm_access():
    assert roles_from_claims({'realm_access': {'roles': ['ETUDIANT', 'offline_access']}}) == ['ETUDIANT']


def test_deny_student_admin():
    assert not is_authorized({'roles': ['ETUDIANT']}, {'ADMIN'})


def test_allow_admin():
    assert is_authorized({'roles': ['ADMIN']}, {'ADMIN'})


def test_deny_anonymous():
    assert not is_authorized(None, {'ETUDIANT'})
