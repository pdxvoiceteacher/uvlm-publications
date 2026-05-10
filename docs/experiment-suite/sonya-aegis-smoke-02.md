# SONYA-AEGIS-SMOKE-02

Purpose: inspect a local Sonya membrane and direct-call blocking fixture.

Run command:

```powershell
.\experiments\Run-SONYA-AEGIS-SMOKE02-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\sonya_aegis_smoke_02_hardened `
  -LogDir C:\UVLM\run_artifacts\sonya_aegis_smoke_02_hardened_logs `
  -CiMode
```

Evidence: `sonya_aegis_smoke_02_acceptance_report.json`, human_review bundle, auto route bundle.

Claim allowed: local deterministic membrane evidence and direct-call blocking are reviewable.

Claims blocked: Sonya local membrane is not federation; candidate is not answer; local fixture only.

Inspect direct-call blocking and Sonya membrane evidence in the acceptance report and route bundles.
