#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def build_manifest(artifact_path: Path, pubkey_path: Path) -> dict:
    data = json.loads(artifact_path.read_text(encoding='utf-8'))
    digest = hashlib.sha256(json.dumps(data, sort_keys=True).encode('utf-8')).hexdigest()
    return {
        'artifact': str(artifact_path),
        'hash': digest,
        'signature': 'TODO_GENERATE_SIGNATURE',
        'origin': 'node_local_001',
        'canonicalPhaselock': 'local',
        'pubkey': str(pubkey_path),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description='Publish telemetry artifact with signature.')
    parser.add_argument('--artifact', required=True, help='Path to telemetry.json')
    parser.add_argument('--pubkey', required=True, help='Path to public key for signing')
    parser.add_argument('--output', required=True, help='Signed manifest output path')
    args = parser.parse_args()

    artifact_path = Path(args.artifact)
    pubkey_path = Path(args.pubkey)
    output_path = Path(args.output)

    manifest = build_manifest(artifact_path, pubkey_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n', encoding='utf-8')

    print(f'Published manifest to {output_path}')


if __name__ == '__main__':
    main()
