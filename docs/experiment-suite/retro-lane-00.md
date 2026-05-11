# RETRO-LANE-00

Purpose: inspect retrosynthesis admission lanes without executing retrosynthesis.

Run command:

```powershell
.\experiments\Run-RETRO-LANE00-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\retro_lane_00 `
  -LogDir C:\UVLM\run_artifacts\retro_lane_00_logs `
  -CiMode
```

Evidence: `retrosynthesis_admission_packet.json`, `retrosynthesis_admission_review_packet.json`, `retro_lane_00_acceptance_receipt.json`.

Lane definitions: sandbox_auto, review_required, blocked.

Claim allowed: admission lane posture can be reviewed.

Claims blocked: Retrosynthesis admission is not retrosynthesis execution; hallucination is telemetry not evidence.

Caution: admission is not execution.
