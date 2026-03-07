from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path('scripts/build_public_record_overlay.py')


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')


class PublicRecordOverlayBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.bridge = self.root / 'bridge'
        self.registry = self.root / 'registry'

        prov = {'schemaVersion': 'phase-v.0', 'producerCommits': ['v123'], 'sourceMode': 'fixture'}
        write_json(self.bridge / 'public_record_audit.json', {'provenance': prov, 'audits': [{'reviewId': 'prv-1', 'publicRecordAuditState': 'verified'}]})
        write_json(self.bridge / 'public_record_recommendations.json', {
            'provenance': prov,
            'recommendations': [{'reviewId': 'prv-1', 'targetPublisherAction': 'docket', 'linkedTargetIds': ['concept:x']}],
        })
        write_json(self.bridge / 'public_record_intake_map.json', {
            'provenance': prov,
            'entries': [{'reviewId': 'prv-1', 'recordType': 'court-filing', 'machineReadabilityScore': 0.8}],
        })
        write_json(self.bridge / 'entity_graph_map.json', {
            'provenance': prov,
            'entries': [{'reviewId': 'prv-1', 'entityGraphStatus': 'linked'}],
        })
        write_json(self.bridge / 'relationship_edge_map.json', {
            'provenance': prov,
            'entries': [{'reviewId': 'prv-1', 'relationshipAmbiguity': 'medium'}],
        })
        write_json(self.bridge / 'chain_of_custody_report.json', {
            'provenance': prov,
            'entries': [{'reviewId': 'prv-1', 'custodyIntegrityScore': 0.91, 'custodyState': 'traceable'}],
        })

        reg_prov = {'provenance': {'schemaVersions': {'x': '1'}, 'producerCommits': ['abc'], 'derivedFromFixtures': True}}
        write_json(self.registry / 'verification_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'claim_type_registry.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'entity_watchlist.json', {**reg_prov, 'entries': []})

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_builder(self, extra: list[str] | None = None) -> subprocess.CompletedProcess[str]:
        cmd = [
            'python3', str(SCRIPT),
            '--public-record-audit', str(self.bridge / 'public_record_audit.json'),
            '--public-record-recommendations', str(self.bridge / 'public_record_recommendations.json'),
            '--public-record-intake-map', str(self.bridge / 'public_record_intake_map.json'),
            '--entity-graph-map', str(self.bridge / 'entity_graph_map.json'),
            '--relationship-edge-map', str(self.bridge / 'relationship_edge_map.json'),
            '--chain-of-custody-report', str(self.bridge / 'chain_of_custody_report.json'),
            '--verification-dashboard', str(self.registry / 'verification_dashboard.json'),
            '--claim-type-registry', str(self.registry / 'claim_type_registry.json'),
            '--entity-watchlist', str(self.registry / 'entity_watchlist.json'),
            '--out-public-record-dashboard', str(self.registry / 'public_record_dashboard.json'),
            '--out-entity-graph-registry', str(self.registry / 'entity_graph_registry.json'),
            '--out-relationship-watchlist', str(self.registry / 'relationship_watchlist.json'),
            '--out-chain-of-custody-annotations', str(self.registry / 'chain_of_custody_annotations.json'),
        ]
        if extra:
            cmd.extend(extra)
        return subprocess.run(cmd, text=True, capture_output=True)

    def test_canonical_artifact_name_usage(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)

    def test_deprecated_name_rejection(self) -> None:
        result = self.run_builder(['--public-record-snapshot', str(self.bridge / 'public_record_snapshot.json')])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Deprecated artifact alias', result.stdout + result.stderr)

    def test_provenance_propagation(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        payload = json.loads((self.registry / 'public_record_dashboard.json').read_text(encoding='utf-8'))
        self.assertIn('schemaVersions', payload.get('provenance', {}))

    def test_missing_upstream_artifact_failure(self) -> None:
        (self.bridge / 'relationship_edge_map.json').unlink()
        result = self.run_builder()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Missing required canonical artifact', result.stdout + result.stderr)

    def test_non_mutation_guarantee_preserved(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        payload = json.loads((self.registry / 'chain_of_custody_annotations.json').read_text(encoding='utf-8'))
        self.assertTrue(payload.get('noCanonicalMutation'))
        self.assertTrue(payload.get('noAutomaticAccusation'))
        self.assertTrue(payload.get('noAutomaticGraphHardening'))
        self.assertTrue(payload.get('noAutomaticIdentityMutation'))


if __name__ == '__main__':
    unittest.main()
