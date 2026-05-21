# Local Sonya path portability

Phase: `LOCAL-SONYA-PATH-PORTABILITY-00`

User path is not system path.
Example path is not runtime requirement.
Personal operator path is not package default.
Local Sonya node root must be user-defined.
Run artifact root must be configurable.
Shared source root must be configurable.
Local model root must be configurable.
PMR store root must be configurable.
TEL event sink root must be configurable.
Relative configured paths must fail closed.
Missing required root must fail closed.
Path portability audit is not deployment authority.
Path portability audit is not live node execution.
Localhost readiness is not LAN readiness.
LAN readiness is not federation authority.

```powershell
.\experiments\Run-LOCAL-SONYA-PATH-PORTABILITY00-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\local_sonya_path_portability_00 `
  -LogDir C:\UVLM\run_artifacts\local_sonya_path_portability_00_logs `
  -CiMode
```

- `local_sonya_path_portability_manifest.json`
- `local_sonya_node_environment_packet.json`
- `local_sonya_path_audit_rows.jsonl`
- `local_sonya_path_policy_packet.json`
- `local_sonya_path_portability_review_packet.json`
- `local_sonya_path_portability_summary.md`
- `artifact_inventory.json`
- `run_artifact_manifest.json`
- `export_bundle_manifest.json`
- `export_bundle_parity_report.json`
- `local_sonya_path_portability_00_acceptance_receipt.json`
