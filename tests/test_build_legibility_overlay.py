from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.canonical_integrity_manifest import compute_constraint_signature_sha256

SCRIPT = Path('scripts/build_legibility_overlay.py')


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')


class LegibilityOverlayBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.bridge = self.root / 'bridge'
        self.registry = self.root / 'registry'

        prov = {'schemaVersion': 'lrq-v0.1', 'producerCommits': ['lrq123'], 'sourceMode': 'fixture'}
        write_json(self.bridge / 'phase_lineage_registry.json', {'provenance': prov, 'entries': [
            {'reviewId': 'lrq-1', 'phaseLineageVisibility': True},
            {'reviewId': 'lrq-2', 'phaseLineageVisibility': True},
        ]})
        write_json(self.bridge / 'phase_glossary.json', {'provenance': prov, 'entries': [
            {'reviewId': 'lrq-1', 'glossaryAvailability': True},
            {'reviewId': 'lrq-2', 'glossaryAvailability': True},
        ]})
        write_json(self.bridge / 'coherence_memory_trace.json', {'provenance': prov, 'entries': [
            {'reviewId': 'lrq-1', 'governanceBreadcrumbVisibility': True, 'operatorLegibilityFlags': ['needs-operator-bridge'], 'queryabilityReadiness': True, 'executiveReviewVisibility': True, 'pedagogyOrdinariness': 0.77, 'provenanceMarkers': ['prov:ok'], 'canonicalIntegrityMarkers': ['integrity:verified']},
            {'reviewId': 'lrq-2', 'governanceBreadcrumbVisibility': True, 'operatorLegibilityFlags': [], 'queryabilityReadiness': True, 'executiveReviewVisibility': False, 'pedagogyOrdinariness': 0.42, 'provenanceMarkers': ['prov:gap'], 'canonicalIntegrityMarkers': ['integrity:watch']},
            {'reviewId': 'lrq-3', 'governanceBreadcrumbVisibility': False, 'operatorLegibilityFlags': ['suppressed-note'], 'queryabilityReadiness': False, 'executiveReviewVisibility': False, 'pedagogyOrdinariness': 0.11},
        ]})
        write_json(self.bridge / 'governance_action_ledger.json', {'provenance': prov, 'recommendations': [
            {'reviewId': 'lrq-1', 'targetPublisherAction': 'docket'},
            {'reviewId': 'lrq-2', 'targetPublisherAction': 'watch'},
            {'reviewId': 'lrq-3', 'targetPublisherAction': 'suppressed', 'suppressedExplanatoryNote': 'suppressed pending bounded steward briefing'},
        ]})
        write_json(self.bridge / 'audit_lineage_registry.json', {'provenance': prov, 'audits': [
            {'reviewId': 'lrq-1', 'auditLineageState': 'verified'},
            {'reviewId': 'lrq-2', 'auditLineageState': 'watch'},
            {'reviewId': 'lrq-3', 'auditLineageState': 'suppressed-note-kept'},
        ]})

        reg_prov = {'provenance': {'schemaVersions': {'x': '1'}, 'producerCommits': ['abc'], 'derivedFromFixtures': True}}
        write_json(self.registry / 'background_coherence_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'living_terrace_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'epochal_surface_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'terrace_seed_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'new_delta_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'successor_crossing_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'terrace_health_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'delta_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'trust_surface_dashboard.json', {**reg_prov, 'entries': []})

        manifest = {
            'originProject': 'uvlm-publications',
            'canonicalPhaselock': 'lrq-v0.1-lock',
            'modificationDisclosureRequired': True,
            'ethicalBoundaryNotice': 'legibility bounded',
            'commonsIntegrityNotice': 'provenance required',
            'constraintSignatureVersion': 'lrq.integrity.v1',
        }
        manifest['constraintSignatureSha256'] = compute_constraint_signature_sha256(manifest)
        write_json(self.bridge / 'canonical_integrity_manifest.json', manifest)
        write_json(self.registry / 'canonical_integrity_manifest.json', manifest)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_builder(self) -> subprocess.CompletedProcess[str]:
        cmd = [
            'python3', str(SCRIPT),
            '--phase-lineage-registry', str(self.bridge / 'phase_lineage_registry.json'),
            '--phase-glossary', str(self.bridge / 'phase_glossary.json'),
            '--coherence-memory-trace', str(self.bridge / 'coherence_memory_trace.json'),
            '--governance-action-ledger', str(self.bridge / 'governance_action_ledger.json'),
            '--audit-lineage-registry', str(self.bridge / 'audit_lineage_registry.json'),
            '--background-coherence-dashboard', str(self.registry / 'background_coherence_dashboard.json'),
            '--living-terrace-dashboard', str(self.registry / 'living_terrace_dashboard.json'),
            '--epochal-surface-dashboard', str(self.registry / 'epochal_surface_dashboard.json'),
            '--terrace-seed-dashboard', str(self.registry / 'terrace_seed_dashboard.json'),
            '--new-delta-dashboard', str(self.registry / 'new_delta_dashboard.json'),
            '--successor-crossing-dashboard', str(self.registry / 'successor_crossing_dashboard.json'),
            '--terrace-health-dashboard', str(self.registry / 'terrace_health_dashboard.json'),
            '--delta-dashboard', str(self.registry / 'delta_dashboard.json'),
            '--trust-surface-dashboard', str(self.registry / 'trust_surface_dashboard.json'),
            '--bridge-canonical-integrity-manifest', str(self.bridge / 'canonical_integrity_manifest.json'),
            '--registry-canonical-integrity-manifest', str(self.registry / 'canonical_integrity_manifest.json'),
            '--out-phase-lineage-dashboard', str(self.registry / 'phase_lineage_dashboard.json'),
            '--out-operator-glossary-registry', str(self.registry / 'operator_glossary_registry.json'),
            '--out-governance-breadcrumb-watchlist', str(self.registry / 'governance_breadcrumb_watchlist.json'),
            '--out-legibility-annotations', str(self.registry / 'legibility_annotations.json'),
        ]
        return subprocess.run(cmd, text=True, capture_output=True)

    def test_routing_behavior(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'phase_lineage_dashboard.json').read_text(encoding='utf-8'))
        glossary = json.loads((self.registry / 'operator_glossary_registry.json').read_text(encoding='utf-8'))
        watch = json.loads((self.registry / 'governance_breadcrumb_watchlist.json').read_text(encoding='utf-8'))
        self.assertEqual([e['reviewId'] for e in dashboard['entries']], ['lrq-1'])
        self.assertEqual([e['reviewId'] for e in glossary['entries']], ['lrq-1'])
        self.assertEqual([e['reviewId'] for e in watch['entries']], ['lrq-2'])

    def test_safeguard_flags_present(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        ann = json.loads((self.registry / 'legibility_annotations.json').read_text(encoding='utf-8'))
        self.assertTrue(ann['noCanonMutation'])
        self.assertTrue(ann['noDeploymentExecution'])
        self.assertTrue(ann['noGovernanceRightMutation'])
        self.assertTrue(ann['noRankingOfPhasesCivilizationsFuturesInstitutions'])
        self.assertTrue(ann['lineageVisibilityNotSettlementAuthority'])
        self.assertTrue(ann['noTheoryCompetitionClosure'])
        self.assertTrue(ann['noFinalMapCompletePresentation'])

    def test_provenance_validation_failure(self) -> None:
        payload = json.loads((self.bridge / 'phase_lineage_registry.json').read_text(encoding='utf-8'))
        payload['provenance']['producerCommits'] = []
        write_json(self.bridge / 'phase_lineage_registry.json', payload)
        result = self.run_builder()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('must be a non-empty list of non-empty strings', result.stdout + result.stderr)

    def test_numeric_fallback(self) -> None:
        payload = json.loads((self.bridge / 'coherence_memory_trace.json').read_text(encoding='utf-8'))
        payload['entries'][0]['pedagogyOrdinariness'] = 'bad-number'
        write_json(self.bridge / 'coherence_memory_trace.json', payload)
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'phase_lineage_dashboard.json').read_text(encoding='utf-8'))
        self.assertEqual(dashboard['entries'][0]['pedagogyOrdinariness'], 0.0)

    def test_canonical_integrity_propagation(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'phase_lineage_dashboard.json').read_text(encoding='utf-8'))
        self.assertTrue(dashboard['canonicalIntegrityVerified'])
        self.assertFalse(dashboard['modificationDisclosureMissing'])
        self.assertFalse(dashboard['trustPresentationDegraded'])

    def test_glossary_lineage_visibility_presence(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'phase_lineage_dashboard.json').read_text(encoding='utf-8'))
        entry = dashboard['entries'][0]
        self.assertTrue(entry['phaseLineageVisibility'])
        self.assertTrue(entry['glossaryAvailability'])
        self.assertTrue(entry['governanceBreadcrumbVisibility'])
        self.assertTrue(entry['queryabilityReadiness'])
        self.assertTrue(entry['executiveReviewVisibility'])

    def test_reset_safe_atlas_classes_and_suppressed_note(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'phase_lineage_dashboard.json').read_text(encoding='utf-8'))
        annotations = json.loads((self.registry / 'legibility_annotations.json').read_text(encoding='utf-8'))

        classes = set(dashboard['entries'][0]['atlasClasses'])
        self.assertIn('lineage-visible', classes)
        self.assertIn('glossary-available', classes)
        self.assertIn('governance-breadcrumb-visible', classes)
        self.assertIn('operator-legibility-weak', classes)
        self.assertIn('queryability-ready', classes)

        self.assertEqual(set(annotations['atlasResetRemovesClasses']), {
            'lineage-visible',
            'glossary-available',
            'governance-breadcrumb-visible',
            'operator-legibility-weak',
            'queryability-ready',
            'legibility-trust-degraded',
        })

        suppressed = next(a for a in annotations['annotations'] if a['reviewId'] == 'lrq-3')
        self.assertEqual(suppressed['targetPublisherAction'], 'suppressed')
        self.assertEqual(suppressed['suppressedExplanatoryNote'], 'suppressed pending bounded steward briefing')


if __name__ == '__main__':
    unittest.main()
