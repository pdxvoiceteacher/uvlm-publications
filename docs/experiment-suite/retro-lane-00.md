# RETRO-LANE-00

Purpose: inspect retrosynthesis admission lanes without executing retrosynthesis.

Run command: `python -m pytest -q python/tests/integration/test_retro_lane_00_acceptance.py`.

Evidence: `retrosynthesis_admission_packet.json`, `retrosynthesis_admission_review_packet.json`, `retro_lane_00_acceptance_receipt.json`.

Lane definitions: sandbox_auto, review_required, blocked.

Claim allowed: admission lane posture can be reviewed.

Claims blocked: Retrosynthesis admission is not retrosynthesis execution; hallucination is telemetry not evidence.

Caution: admission is not execution.
