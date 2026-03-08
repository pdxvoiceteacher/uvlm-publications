from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path('scripts/build_review_packet_overlay.py')


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')


class ReviewPacketOverlayBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.bridge = self.root / 'bridge'
        self.registry = self.root / 'registry'

        prov = {'schemaVersion': 'phase-y.0', 'producerCommits': ['y123'], 'sourceMode': 'fixture'}
        write_json(self.bridge / 'review_packet_audit.json', {
            'provenance': prov,
            'audits': [{'reviewId': 'rp-1', 'reviewPacketAuditState': 'verified'}],
        })
        write_json(self.bridge / 'review_packet_recommendations.json', {
            'provenance': prov,
            'recommendations': [
                {'reviewId': 'rp-1', 'targetPublisherAction': 'docket', 'linkedTargetIds': ['concept:x']},
                {'reviewId': 'rp-2', 'targetPublisherAction': 'watch', 'linkedTargetIds': ['concept:y']},
                {'reviewId': 'rp-3', 'targetPublisherAction': 'suppressed', 'linkedTargetIds': ['concept:z']},
            ],
        })
        write_json(self.bridge / 'review_packet_map.json', {
            'provenance': prov,
            'entries': [{'reviewId': 'rp-1', 'packetStatus': 'ready-for-human-review'}],
        })
        write_json(self.bridge / 'review_packet_summary.json', {
            'provenance': prov,
            'entries': [{'reviewId': 'rp-1', 'maturityCeiling': 'bounded-public-summary', 'ambiguityLevel': 'medium'}],
        })
        write_json(self.bridge / 'narrative_synthesis_map.json', {
            'provenance': prov,
            'entries': [{'reviewId': 'rp-1', 'synthesisStatus': 'bounded', 'excludedConclusions': ['identity-attribution']}],
        })
        write_json(self.bridge / 'uncertainty_disclosure_report.json', {
            'provenance': prov,
            'entries': [{'reviewId': 'rp-1', 'uncertaintyDisclosures': ['causal-direction-underdetermined']}],
        })

        reg_prov = {'provenance': {'schemaVersions': {'x': '1'}, 'producerCommits': ['abc'], 'derivedFromFixtures': True}}
        write_json(self.registry / 'investigation_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'public_record_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'authority_gate_dashboard.json', {**reg_prov, 'entries': []})

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_builder(self, extra: list[str] | None = None) -> subprocess.CompletedProcess[str]:
        cmd = [
            'python3', str(SCRIPT),
            '--review-packet-audit', str(self.bridge / 'review_packet_audit.json'),
            '--review-packet-recommendations', str(self.bridge / 'review_packet_recommendations.json'),
            '--review-packet-map', str(self.bridge / 'review_packet_map.json'),
            '--review-packet-summary', str(self.bridge / 'review_packet_summary.json'),
            '--narrative-synthesis-map', str(self.bridge / 'narrative_synthesis_map.json'),
            '--uncertainty-disclosure-report', str(self.bridge / 'uncertainty_disclosure_report.json'),
            '--investigation-dashboard', str(self.registry / 'investigation_dashboard.json'),
            '--public-record-dashboard', str(self.registry / 'public_record_dashboard.json'),
            '--authority-gate-dashboard', str(self.registry / 'authority_gate_dashboard.json'),
            '--out-review-packet-dashboard', str(self.registry / 'review_packet_dashboard.json'),
            '--out-review-packet-registry', str(self.registry / 'review_packet_registry.json'),
            '--out-uncertainty-watchlist', str(self.registry / 'uncertainty_watchlist.json'),
            '--out-review-packet-annotations', str(self.registry / 'review_packet_annotations.json'),
        ]
        if extra:
            cmd.extend(extra)
        return subprocess.run(cmd, text=True, capture_output=True)

    def test_canonical_artifact_name_usage(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)

    def test_deprecated_name_rejection(self) -> None:
        result = self.run_builder(['--review-packet-snapshot', str(self.bridge / 'old.json')])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Deprecated artifact alias', result.stdout + result.stderr)

    def test_action_filters(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        dashboard = json.loads((self.registry / 'review_packet_dashboard.json').read_text(encoding='utf-8'))
        watchlist = json.loads((self.registry / 'uncertainty_watchlist.json').read_text(encoding='utf-8'))
        self.assertEqual([e['reviewId'] for e in dashboard['entries']], ['rp-1'])
        self.assertEqual([e['reviewId'] for e in watchlist['entries']], ['rp-2'])

    def test_output_contract_validation(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        for name in [
            'review_packet_dashboard.json',
            'review_packet_registry.json',
            'uncertainty_watchlist.json',
            'review_packet_annotations.json',
        ]:
            payload = json.loads((self.registry / name).read_text(encoding='utf-8'))
            self.assertIsInstance(payload, dict)
            self.assertIn('provenance', payload)

    def test_non_mutation_guarantee_preserved(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        payload = json.loads((self.registry / 'review_packet_annotations.json').read_text(encoding='utf-8'))
        self.assertTrue(payload.get('noCanonicalMutation'))
        self.assertTrue(payload.get('noAutomaticAccusation'))
        self.assertTrue(payload.get('noAutomaticPublication'))


if __name__ == '__main__':
    unittest.main()
