from sophia.audit_civilization import audit_civilization


def test_civilization_instability_watch():
    artifact = {"psi_vector": [0.05, 0.95, 0.2]}

    findings = audit_civilization(artifact)

    assert findings
    assert findings[0]["law"] == "civilizational_instability"
    assert findings[0]["semanticMode"] == "non-executive"


def test_civilization_stable_no_findings():
    artifact = {"psi_vector": [0.2, 0.5, 0.7]}

    findings = audit_civilization(artifact)

    assert findings == []
