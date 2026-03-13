from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.canonical_integrity_manifest import compute_constraint_signature_sha256

SCRIPT = Path('scripts/build_memory_overlay_registry.py')


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')


class MemoryOverlayRegistryBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.bridge = self.root / 'bridge'
        self.registry = self.root / 'registry'

        prov = {'schemaVersion': 'lrq-v0.1', 'producerCommits': ['lrq123'], 'sourceMode': 'fixture'}
        write_json(self.bridge / 'phase_lineage_registry.json', {'provenance': prov, 'entries': [{'reviewId': 'm-1'}]})
        write_json(self.bridge / 'phase_glossary.json', {'provenance': prov, 'entries': [{'reviewId': 'm-1'}]})
        write_json(self.bridge / 'coherence_memory_trace.json', {'provenance': prov, 'entries': [
            {'phaseId': 'm-1', 'donorPatternsApplied': ['pattern:a'], 'unresolvedTensions': ['tension:x']},
            {'phaseId': 'm-2', 'donorPatternsApplied': ['pattern:b'], 'unresolvedTensions': []},
        ]})
        write_json(self.bridge / 'governance_action_ledger.json', {'provenance': prov, 'recommendations': [{'reviewId': 'm-1'}]})
        write_json(self.bridge / 'audit_lineage_registry.json', {'provenance': prov, 'audits': [{'reviewId': 'm-1'}]})

        reg_prov = {'provenance': {'schemaVersions': {'x': '1'}, 'producerCommits': ['abc'], 'derivedFromFixtures': True}}
        write_json(self.registry / 'civilizational_memory_dashboard.json', {**reg_prov, 'entries': [
            {'memoryId': 'mem-1', 'phaseId': 'm-1', 'memoryTier': 'hot', 'preservationCriticality': 'critical', 'invariantHash': 'sig:same', 'reuseFrequency': 7, 'sourceSignalId': 'source:A', 'compressedAt': '2026-03-10T00:00:00+00:00', 'linkedTargetIds': ['x', 'y']},
            {'memoryId': 'mem-2', 'phaseId': 'm-2', 'memoryTier': 'warm', 'preservationCriticality': 'bounded', 'invariantHash': 'sig:same', 'reuseFrequency': 3, 'sourceSignalId': 'source:B', 'compressedAt': '2026-03-11T00:00:00+00:00', 'linkedTargetIds': ['z']},
            {'memoryId': 'mem-3', 'phaseId': 'm-3', 'memoryTier': 'cold', 'preservationCriticality': 'low', 'invariantHash': 'sig:other', 'reuseFrequency': 'not-a-number', 'sourceSignalId': 'source:C', 'compressedAt': '2026-03-09T00:00:00+00:00', 'linkedTargetIds': []},
        ]})
        write_json(self.registry / 'phase_lineage_dashboard.json', {**reg_prov, 'entries': []})

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
            '--civilizational-memory-dashboard', str(self.registry / 'civilizational_memory_dashboard.json'),
            '--phase-lineage-dashboard', str(self.registry / 'phase_lineage_dashboard.json'),
            '--bridge-canonical-integrity-manifest', str(self.bridge / 'canonical_integrity_manifest.json'),
            '--registry-canonical-integrity-manifest', str(self.registry / 'canonical_integrity_manifest.json'),
            '--out-memory-overlay', str(self.registry / 'memory_overlay.json'),
            '--out-memory-dashboard', str(self.registry / 'memory_dashboard.json'),
        ]
        return subprocess.run(cmd, text=True, capture_output=True)

    def test_outputs_and_navigation_links(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        overlay = json.loads((self.registry / 'memory_overlay.json').read_text(encoding='utf-8'))
        self.assertEqual(len(overlay['entries']), 3)
        first = overlay['entries'][0]
        self.assertIn('navigationLinks', first)
        self.assertIn('lineageOverlay', first['navigationLinks'])
        self.assertEqual(first['reversibilityNotice'], '(compressed, reversible – audit-only)')

    def test_dashboard_stats(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dash = json.loads((self.registry / 'memory_dashboard.json').read_text(encoding='utf-8'))
        self.assertEqual(dash['countsByTier']['hot'], 1)
        self.assertEqual(dash['countsByTier']['warm'], 1)
        self.assertEqual(dash['countsByTier']['cold'], 1)
        self.assertEqual(dash['topReusedFragments'][0]['memoryId'], 'mem-1')
        self.assertEqual(dash['lineageCollisions'][0]['compressedSignature'], 'sig:same')

    def test_dashboard_includes_navigation_links_and_notices(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dash = json.loads((self.registry / 'memory_dashboard.json').read_text(encoding='utf-8'))
        self.assertIn('tierEncodings', dash)
        self.assertIn('hot', dash['tierEncodings'])
        self.assertEqual(dash['topReusedFragments'][0]['reversibilityNotice'], '(compressed, reversible – audit-only)')
        self.assertIn('memoryOverlay', dash['topReusedFragments'][0]['navigationLinks'])
        self.assertEqual(dash['recentlyCompressedPathways'][0]['reversibilityNotice'], '(compressed, reversible – audit-only)')
        self.assertTrue(dash['noCompressionAuthorityGain'])
        self.assertTrue(dash['noMinorityVoiceEliminationClaim'])

    def test_provenance_failure(self) -> None:
        payload = json.loads((self.bridge / 'phase_lineage_registry.json').read_text(encoding='utf-8'))
        payload['provenance']['producerCommits'] = []
        write_json(self.bridge / 'phase_lineage_registry.json', payload)
        result = self.run_builder()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('must be a non-empty list of non-empty strings', result.stdout + result.stderr)

    def test_numeric_fallback(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        overlay = json.loads((self.registry / 'memory_overlay.json').read_text(encoding='utf-8'))
        mem3 = next(e for e in overlay['entries'] if e['memoryId'] == 'mem-3')
        self.assertEqual(mem3['reuseFrequency'], 0)

    def test_canonical_integrity_propagation(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dash = json.loads((self.registry / 'memory_dashboard.json').read_text(encoding='utf-8'))
        self.assertTrue(dash['canonicalIntegrityVerified'])
        self.assertFalse(dash['modificationDisclosureMissing'])
        self.assertFalse(dash['trustPresentationDegraded'])

    def test_sync_helper_exists_and_lists_bridge_files(self) -> None:
        helper = Path('tools/sync_bridge_from_coherencelattice.py').read_text(encoding='utf-8')
        self.assertIn('phase_lineage_registry.json', helper)
        self.assertIn('civilizational_delta_map.json', helper)
        self.assertIn('rupture_map.json', helper)
        self.assertIn('navigation_state.json', helper)

    def test_optional_registry_provenance_accepts_schema_version(self) -> None:
        payload = json.loads((self.registry / 'phase_lineage_dashboard.json').read_text(encoding='utf-8'))
        payload['provenance'] = {
            'schemaVersion': 'phase-lineage-v1',
            'producerCommits': ['def456'],
            'derivedFromFixtures': False,
        }
        write_json(self.registry / 'phase_lineage_dashboard.json', payload)

        result = self.run_builder()
        self.assertEqual(result.returncode, 0)

        overlay = json.loads((self.registry / 'memory_overlay.json').read_text(encoding='utf-8'))
        self.assertIn('phase_lineage_dashboard', overlay['provenance']['schemaVersions'])
        self.assertEqual(overlay['provenance']['schemaVersions']['phase_lineage_dashboard'], 'phase-lineage-v1')

    def test_deployment_profiles_yaml_exists_with_federation_examples(self) -> None:
        cfg = Path('config/deployment_profiles.yaml').read_text(encoding='utf-8')
        self.assertIn('local_single_node', cfg)
        self.assertIn('local_plus_dashboard', cfg)
        self.assertIn('federated_two_node', cfg)
        self.assertIn('federated_mesh', cfg)
        self.assertIn('artifact_repos', cfg)



    def test_publish_telemetry_generates_manifest_fields(self) -> None:
        publish = Path('tools/publish_telemetry.py')
        self.assertTrue(publish.exists())

        artifact = self.root / 'telemetry.json'
        artifact.write_text(json.dumps({'events': [{'agentId': 'a1', 'score': 0.8}]}, sort_keys=True), encoding='utf-8')
        pubkey = self.root / 'mypub.key'
        pubkey.write_text('PUBKEY_PLACEHOLDER', encoding='utf-8')
        output = self.root / 'telemetry_manifest.json'

        result = subprocess.run([
            'python3', str(publish),
            '--artifact', str(artifact),
            '--pubkey', str(pubkey),
            '--output', str(output),
        ], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0)

        manifest = json.loads(output.read_text(encoding='utf-8'))
        self.assertEqual(manifest['artifact'], str(artifact))
        self.assertIn('hash', manifest)
        self.assertEqual(manifest['signature'], 'TODO_GENERATE_SIGNATURE')
        self.assertEqual(manifest['origin'], 'node_local_001')
        self.assertEqual(manifest['canonicalPhaselock'], 'local')
    def test_deployment_profiles_yaml_exists_with_federation_examples(self) -> None:
        cfg = Path('config/deployment_profiles.yaml').read_text(encoding='utf-8')
        self.assertIn('local_single_node', cfg)
        self.assertIn('local_plus_dashboard', cfg)
        self.assertIn('federated_two_node', cfg)
        self.assertIn('federated_mesh', cfg)
        self.assertIn('artifact_repos', cfg)



    def test_publish_telemetry_generates_manifest_fields(self) -> None:
        publish = Path('tools/publish_telemetry.py')
        self.assertTrue(publish.exists())

        artifact = self.root / 'telemetry.json'
        artifact.write_text(json.dumps({'events': [{'agentId': 'a1', 'score': 0.8}]}, sort_keys=True), encoding='utf-8')
        pubkey = self.root / 'mypub.key'
        pubkey.write_text('PUBKEY_PLACEHOLDER', encoding='utf-8')
        output = self.root / 'telemetry_manifest.json'

        result = subprocess.run([
            'python3', str(publish),
            '--artifact', str(artifact),
            '--pubkey', str(pubkey),
            '--output', str(output),
        ], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0)

        manifest = json.loads(output.read_text(encoding='utf-8'))
        self.assertEqual(manifest['artifact'], str(artifact))
        self.assertIn('hash', manifest)
        self.assertEqual(manifest['signature'], 'TODO_GENERATE_SIGNATURE')
        self.assertEqual(manifest['origin'], 'node_local_001')
        self.assertEqual(manifest['canonicalPhaselock'], 'local')
    def test_deployment_profiles_yaml_exists_with_federation_examples(self) -> None:
        cfg = Path('config/deployment_profiles.yaml').read_text(encoding='utf-8')
        self.assertIn('local_single_node', cfg)
        self.assertIn('local_plus_dashboard', cfg)
        self.assertIn('federated_two_node', cfg)
        self.assertIn('federated_mesh', cfg)
        self.assertIn('artifact_repos', cfg)



    def test_publish_telemetry_generates_manifest_fields(self) -> None:
        publish = Path('tools/publish_telemetry.py')
        self.assertTrue(publish.exists())

        artifact = self.root / 'telemetry.json'
        artifact.write_text(json.dumps({'events': [{'agentId': 'a1', 'score': 0.8}]}, sort_keys=True), encoding='utf-8')
        pubkey = self.root / 'mypub.key'
        pubkey.write_text('PUBKEY_PLACEHOLDER', encoding='utf-8')
        output = self.root / 'telemetry_manifest.json'

        result = subprocess.run([
            'python3', str(publish),
            '--artifact', str(artifact),
            '--pubkey', str(pubkey),
            '--output', str(output),
        ], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0)

        manifest = json.loads(output.read_text(encoding='utf-8'))
        self.assertEqual(manifest['artifact'], str(artifact))
        self.assertIn('hash', manifest)
        self.assertEqual(manifest['signature'], 'TODO_GENERATE_SIGNATURE')
        self.assertEqual(manifest['origin'], 'node_local_001')
        self.assertEqual(manifest['canonicalPhaselock'], 'local')
    def test_deployment_profiles_yaml_exists_with_federation_examples(self) -> None:
        cfg = Path('config/deployment_profiles.yaml').read_text(encoding='utf-8')
        self.assertIn('local_single_node', cfg)
        self.assertIn('local_plus_dashboard', cfg)
        self.assertIn('federated_two_node', cfg)
        self.assertIn('federated_mesh', cfg)
        self.assertIn('artifact_repos', cfg)



    def test_publish_telemetry_generates_manifest_fields(self) -> None:
        publish = Path('tools/publish_telemetry.py')
        self.assertTrue(publish.exists())

        artifact = self.root / 'telemetry.json'
        artifact.write_text(json.dumps({'events': [{'agentId': 'a1', 'score': 0.8}]}, sort_keys=True), encoding='utf-8')
        pubkey = self.root / 'mypub.key'
        pubkey.write_text('PUBKEY_PLACEHOLDER', encoding='utf-8')
        output = self.root / 'telemetry_manifest.json'

        result = subprocess.run([
            'python3', str(publish),
            '--artifact', str(artifact),
            '--pubkey', str(pubkey),
            '--output', str(output),
        ], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0)

        manifest = json.loads(output.read_text(encoding='utf-8'))
        self.assertEqual(manifest['artifact'], str(artifact))
        self.assertIn('hash', manifest)
        self.assertEqual(manifest['signature'], 'TODO_GENERATE_SIGNATURE')
        self.assertEqual(manifest['origin'], 'node_local_001')
        self.assertEqual(manifest['canonicalPhaselock'], 'local')
    def test_deployment_profiles_yaml_exists_with_federation_examples(self) -> None:
        cfg = Path('config/deployment_profiles.yaml').read_text(encoding='utf-8')
        self.assertIn('local_single_node', cfg)
        self.assertIn('local_plus_dashboard', cfg)
        self.assertIn('federated_two_node', cfg)
        self.assertIn('federated_mesh', cfg)
        self.assertIn('artifact_repos', cfg)



    def test_publish_telemetry_generates_manifest_fields(self) -> None:
        publish = Path('tools/publish_telemetry.py')
        self.assertTrue(publish.exists())

        artifact = self.root / 'telemetry.json'
        artifact.write_text(json.dumps({'events': [{'agentId': 'a1', 'score': 0.8}]}, sort_keys=True), encoding='utf-8')
        pubkey = self.root / 'mypub.key'
        pubkey.write_text('PUBKEY_PLACEHOLDER', encoding='utf-8')
        output = self.root / 'telemetry_manifest.json'

        result = subprocess.run([
            'python3', str(publish),
            '--artifact', str(artifact),
            '--pubkey', str(pubkey),
            '--output', str(output),
        ], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0)

        manifest = json.loads(output.read_text(encoding='utf-8'))
        self.assertEqual(manifest['artifact'], str(artifact))
        self.assertIn('hash', manifest)
        self.assertEqual(manifest['signature'], 'TODO_GENERATE_SIGNATURE')
        self.assertEqual(manifest['origin'], 'node_local_001')
        self.assertEqual(manifest['canonicalPhaselock'], 'local')
    def test_deployment_profiles_yaml_exists_with_federation_examples(self) -> None:
        cfg = Path('config/deployment_profiles.yaml').read_text(encoding='utf-8')
        self.assertIn('local_single_node', cfg)
        self.assertIn('local_plus_dashboard', cfg)
        self.assertIn('federated_two_node', cfg)
        self.assertIn('federated_mesh', cfg)
        self.assertIn('artifact_repos', cfg)



    def test_publish_telemetry_generates_manifest_fields(self) -> None:
        publish = Path('tools/publish_telemetry.py')
        self.assertTrue(publish.exists())

        artifact = self.root / 'telemetry.json'
        artifact.write_text(json.dumps({'events': [{'agentId': 'a1', 'score': 0.8}]}, sort_keys=True), encoding='utf-8')
        pubkey = self.root / 'mypub.key'
        pubkey.write_text('PUBKEY_PLACEHOLDER', encoding='utf-8')
        output = self.root / 'telemetry_manifest.json'

        result = subprocess.run([
            'python3', str(publish),
            '--artifact', str(artifact),
            '--pubkey', str(pubkey),
            '--output', str(output),
        ], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0)

        manifest = json.loads(output.read_text(encoding='utf-8'))
        self.assertEqual(manifest['artifact'], str(artifact))
        self.assertIn('hash', manifest)
        self.assertEqual(manifest['signature'], 'TODO_GENERATE_SIGNATURE')
        self.assertEqual(manifest['origin'], 'node_local_001')
        self.assertEqual(manifest['canonicalPhaselock'], 'local')
    def test_deployment_profiles_yaml_exists_with_federation_examples(self) -> None:
        cfg = Path('config/deployment_profiles.yaml').read_text(encoding='utf-8')
        self.assertIn('local_single_node', cfg)
        self.assertIn('local_plus_dashboard', cfg)
        self.assertIn('federated_two_node', cfg)
        self.assertIn('federated_mesh', cfg)
        self.assertIn('artifact_repos', cfg)



    def test_publish_telemetry_generates_manifest_fields(self) -> None:
        publish = Path('tools/publish_telemetry.py')
        self.assertTrue(publish.exists())

        artifact = self.root / 'telemetry.json'
        artifact.write_text(json.dumps({'events': [{'agentId': 'a1', 'score': 0.8}]}, sort_keys=True), encoding='utf-8')
        pubkey = self.root / 'mypub.key'
        pubkey.write_text('PUBKEY_PLACEHOLDER', encoding='utf-8')
        output = self.root / 'telemetry_manifest.json'

        result = subprocess.run([
            'python3', str(publish),
            '--artifact', str(artifact),
            '--pubkey', str(pubkey),
            '--output', str(output),
        ], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0)

        manifest = json.loads(output.read_text(encoding='utf-8'))
        self.assertEqual(manifest['artifact'], str(artifact))
        self.assertIn('hash', manifest)
        self.assertEqual(manifest['signature'], 'TODO_GENERATE_SIGNATURE')
        self.assertEqual(manifest['origin'], 'node_local_001')
        self.assertEqual(manifest['canonicalPhaselock'], 'local')
    def test_deployment_profiles_yaml_exists_with_federation_examples(self) -> None:
        cfg = Path('config/deployment_profiles.yaml').read_text(encoding='utf-8')
        self.assertIn('local_single_node', cfg)
        self.assertIn('local_plus_dashboard', cfg)
        self.assertIn('federated_two_node', cfg)
        self.assertIn('federated_mesh', cfg)
        self.assertIn('artifact_repos', cfg)



    def test_publish_telemetry_generates_manifest_fields(self) -> None:
        publish = Path('tools/publish_telemetry.py')
        self.assertTrue(publish.exists())

        artifact = self.root / 'telemetry.json'
        artifact.write_text(json.dumps({'events': [{'agentId': 'a1', 'score': 0.8}]}, sort_keys=True), encoding='utf-8')
        pubkey = self.root / 'mypub.key'
        pubkey.write_text('PUBKEY_PLACEHOLDER', encoding='utf-8')
        output = self.root / 'telemetry_manifest.json'

        result = subprocess.run([
            'python3', str(publish),
            '--artifact', str(artifact),
            '--pubkey', str(pubkey),
            '--output', str(output),
        ], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0)

        manifest = json.loads(output.read_text(encoding='utf-8'))
        self.assertEqual(manifest['artifact'], str(artifact))
        self.assertIn('hash', manifest)
        self.assertEqual(manifest['signature'], 'TODO_GENERATE_SIGNATURE')
        self.assertEqual(manifest['origin'], 'node_local_001')
        self.assertEqual(manifest['canonicalPhaselock'], 'local')
    def test_deployment_profiles_yaml_exists_with_federation_examples(self) -> None:
        cfg = Path('config/deployment_profiles.yaml').read_text(encoding='utf-8')
        self.assertIn('local_single_node', cfg)
        self.assertIn('local_plus_dashboard', cfg)
        self.assertIn('federated_two_node', cfg)
        self.assertIn('federated_mesh', cfg)
        self.assertIn('artifact_repos', cfg)



    def test_publish_telemetry_generates_manifest_fields(self) -> None:
        publish = Path('tools/publish_telemetry.py')
        self.assertTrue(publish.exists())

        artifact = self.root / 'telemetry.json'
        artifact.write_text(json.dumps({'events': [{'agentId': 'a1', 'score': 0.8}]}, sort_keys=True), encoding='utf-8')
        pubkey = self.root / 'mypub.key'
        pubkey.write_text('PUBKEY_PLACEHOLDER', encoding='utf-8')
        output = self.root / 'telemetry_manifest.json'

        result = subprocess.run([
            'python3', str(publish),
            '--artifact', str(artifact),
            '--pubkey', str(pubkey),
            '--output', str(output),
        ], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0)

        manifest = json.loads(output.read_text(encoding='utf-8'))
        self.assertEqual(manifest['artifact'], str(artifact))
        self.assertIn('hash', manifest)
        self.assertEqual(manifest['signature'], 'TODO_GENERATE_SIGNATURE')
        self.assertEqual(manifest['origin'], 'node_local_001')
        self.assertEqual(manifest['canonicalPhaselock'], 'local')
    def test_deployment_profiles_yaml_exists_with_federation_examples(self) -> None:
        cfg = Path('config/deployment_profiles.yaml').read_text(encoding='utf-8')
        self.assertIn('local_single_node', cfg)
        self.assertIn('local_plus_dashboard', cfg)
        self.assertIn('federated_two_node', cfg)
        self.assertIn('federated_mesh', cfg)
        self.assertIn('artifact_repos', cfg)



    def test_publish_telemetry_generates_manifest_fields(self) -> None:
        publish = Path('tools/publish_telemetry.py')
        self.assertTrue(publish.exists())

        artifact = self.root / 'telemetry.json'
        artifact.write_text(json.dumps({'events': [{'agentId': 'a1', 'score': 0.8}]}, sort_keys=True), encoding='utf-8')
        pubkey = self.root / 'mypub.key'
        pubkey.write_text('PUBKEY_PLACEHOLDER', encoding='utf-8')
        output = self.root / 'telemetry_manifest.json'

        result = subprocess.run([
            'python3', str(publish),
            '--artifact', str(artifact),
            '--pubkey', str(pubkey),
            '--output', str(output),
        ], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0)

        manifest = json.loads(output.read_text(encoding='utf-8'))
        self.assertEqual(manifest['artifact'], str(artifact))
        self.assertIn('hash', manifest)
        self.assertEqual(manifest['signature'], 'TODO_GENERATE_SIGNATURE')
        self.assertEqual(manifest['origin'], 'node_local_001')
        self.assertEqual(manifest['canonicalPhaselock'], 'local')
    def test_deployment_profiles_yaml_exists_with_federation_examples(self) -> None:
        cfg = Path('config/deployment_profiles.yaml').read_text(encoding='utf-8')
        self.assertIn('local_single_node', cfg)
        self.assertIn('local_plus_dashboard', cfg)
        self.assertIn('federated_two_node', cfg)
        self.assertIn('federated_mesh', cfg)
        self.assertIn('artifact_repos', cfg)



    def test_publish_telemetry_generates_manifest_fields(self) -> None:
        publish = Path('tools/publish_telemetry.py')
        self.assertTrue(publish.exists())

        artifact = self.root / 'telemetry.json'
        artifact.write_text(json.dumps({'events': [{'agentId': 'a1', 'score': 0.8}]}, sort_keys=True), encoding='utf-8')
        pubkey = self.root / 'mypub.key'
        pubkey.write_text('PUBKEY_PLACEHOLDER', encoding='utf-8')
        output = self.root / 'telemetry_manifest.json'

        result = subprocess.run([
            'python3', str(publish),
            '--artifact', str(artifact),
            '--pubkey', str(pubkey),
            '--output', str(output),
        ], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0)

        manifest = json.loads(output.read_text(encoding='utf-8'))
        self.assertEqual(manifest['artifact'], str(artifact))
        self.assertIn('hash', manifest)
        self.assertEqual(manifest['signature'], 'TODO_GENERATE_SIGNATURE')
        self.assertEqual(manifest['origin'], 'node_local_001')
        self.assertEqual(manifest['canonicalPhaselock'], 'local')
    def test_deployment_profiles_yaml_exists_with_federation_examples(self) -> None:
        cfg = Path('config/deployment_profiles.yaml').read_text(encoding='utf-8')
        self.assertIn('local_single_node', cfg)
        self.assertIn('local_plus_dashboard', cfg)
        self.assertIn('federated_two_node', cfg)
        self.assertIn('federated_mesh', cfg)
        self.assertIn('artifact_repos', cfg)



    def test_publish_telemetry_generates_manifest_fields(self) -> None:
        publish = Path('tools/publish_telemetry.py')
        self.assertTrue(publish.exists())

        artifact = self.root / 'telemetry.json'
        artifact.write_text(json.dumps({'events': [{'agentId': 'a1', 'score': 0.8}]}, sort_keys=True), encoding='utf-8')
        pubkey = self.root / 'mypub.key'
        pubkey.write_text('PUBKEY_PLACEHOLDER', encoding='utf-8')
        output = self.root / 'telemetry_manifest.json'

        result = subprocess.run([
            'python3', str(publish),
            '--artifact', str(artifact),
            '--pubkey', str(pubkey),
            '--output', str(output),
        ], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0)

        manifest = json.loads(output.read_text(encoding='utf-8'))
        self.assertEqual(manifest['artifact'], str(artifact))
        self.assertIn('hash', manifest)
        self.assertEqual(manifest['signature'], 'TODO_GENERATE_SIGNATURE')
        self.assertEqual(manifest['origin'], 'node_local_001')
        self.assertEqual(manifest['canonicalPhaselock'], 'local')
    def test_deployment_profiles_yaml_exists_with_federation_examples(self) -> None:
        cfg = Path('config/deployment_profiles.yaml').read_text(encoding='utf-8')
        self.assertIn('local_single_node', cfg)
        self.assertIn('local_plus_dashboard', cfg)
        self.assertIn('federated_two_node', cfg)
        self.assertIn('federated_mesh', cfg)
        self.assertIn('artifact_repos', cfg)



    def test_publish_telemetry_generates_manifest_fields(self) -> None:
        publish = Path('tools/publish_telemetry.py')
        self.assertTrue(publish.exists())

        artifact = self.root / 'telemetry.json'
        artifact.write_text(json.dumps({'events': [{'agentId': 'a1', 'score': 0.8}]}, sort_keys=True), encoding='utf-8')
        pubkey = self.root / 'mypub.key'
        pubkey.write_text('PUBKEY_PLACEHOLDER', encoding='utf-8')
        output = self.root / 'telemetry_manifest.json'

        result = subprocess.run([
            'python3', str(publish),
            '--artifact', str(artifact),
            '--pubkey', str(pubkey),
            '--output', str(output),
        ], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0)

        manifest = json.loads(output.read_text(encoding='utf-8'))
        self.assertEqual(manifest['artifact'], str(artifact))
        self.assertIn('hash', manifest)
        self.assertEqual(manifest['signature'], 'TODO_GENERATE_SIGNATURE')
        self.assertEqual(manifest['origin'], 'node_local_001')
        self.assertEqual(manifest['canonicalPhaselock'], 'local')
    def test_deployment_profiles_yaml_exists_with_federation_examples(self) -> None:
        cfg = Path('config/deployment_profiles.yaml').read_text(encoding='utf-8')
        self.assertIn('local_single_node', cfg)
        self.assertIn('local_plus_dashboard', cfg)
        self.assertIn('federated_two_node', cfg)
        self.assertIn('federated_mesh', cfg)
        self.assertIn('artifact_repos', cfg)



    def test_publish_telemetry_generates_manifest_fields(self) -> None:
        publish = Path('tools/publish_telemetry.py')
        self.assertTrue(publish.exists())

        artifact = self.root / 'telemetry.json'
        artifact.write_text(json.dumps({'events': [{'agentId': 'a1', 'score': 0.8}]}, sort_keys=True), encoding='utf-8')
        pubkey = self.root / 'mypub.key'
        pubkey.write_text('PUBKEY_PLACEHOLDER', encoding='utf-8')
        output = self.root / 'telemetry_manifest.json'

        result = subprocess.run([
            'python3', str(publish),
            '--artifact', str(artifact),
            '--pubkey', str(pubkey),
            '--output', str(output),
        ], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0)

        manifest = json.loads(output.read_text(encoding='utf-8'))
        self.assertEqual(manifest['artifact'], str(artifact))
        self.assertIn('hash', manifest)
        self.assertEqual(manifest['signature'], 'TODO_GENERATE_SIGNATURE')
        self.assertEqual(manifest['origin'], 'node_local_001')
        self.assertEqual(manifest['canonicalPhaselock'], 'local')
    def test_deployment_profiles_yaml_exists_with_federation_examples(self) -> None:
        cfg = Path('config/deployment_profiles.yaml').read_text(encoding='utf-8')
        self.assertIn('local_single_node', cfg)
        self.assertIn('local_plus_dashboard', cfg)
        self.assertIn('federated_two_node', cfg)
        self.assertIn('federated_mesh', cfg)
        self.assertIn('artifact_repos', cfg)



    def test_publish_telemetry_generates_manifest_fields(self) -> None:
        publish = Path('tools/publish_telemetry.py')
        self.assertTrue(publish.exists())

        artifact = self.root / 'telemetry.json'
        artifact.write_text(json.dumps({'events': [{'agentId': 'a1', 'score': 0.8}]}, sort_keys=True), encoding='utf-8')
        pubkey = self.root / 'mypub.key'
        pubkey.write_text('PUBKEY_PLACEHOLDER', encoding='utf-8')
        output = self.root / 'telemetry_manifest.json'

        result = subprocess.run([
            'python3', str(publish),
            '--artifact', str(artifact),
            '--pubkey', str(pubkey),
            '--output', str(output),
        ], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0)

        manifest = json.loads(output.read_text(encoding='utf-8'))
        self.assertEqual(manifest['artifact'], str(artifact))
        self.assertIn('hash', manifest)
        self.assertEqual(manifest['signature'], 'TODO_GENERATE_SIGNATURE')
        self.assertEqual(manifest['origin'], 'node_local_001')
        self.assertEqual(manifest['canonicalPhaselock'], 'local')
    def test_deployment_profiles_yaml_exists_with_federation_examples(self) -> None:
        cfg = Path('config/deployment_profiles.yaml').read_text(encoding='utf-8')
        self.assertIn('local_single_node', cfg)
        self.assertIn('local_plus_dashboard', cfg)
        self.assertIn('federated_two_node', cfg)
        self.assertIn('federated_mesh', cfg)
        self.assertIn('artifact_repos', cfg)



if __name__ == '__main__':
    unittest.main()
