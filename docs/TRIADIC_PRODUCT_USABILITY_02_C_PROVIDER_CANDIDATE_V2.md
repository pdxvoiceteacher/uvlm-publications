# Universal provider candidate v2 compatibility

Atlas accepts existing candidate v1 sealed runs and candidate v2 runs produced through Sonya. V2 provider execution context is presentation-only: provider/model identity establishes execution provenance, not candidate correctness or authority.

For v2, Atlas validates the provider/profile/endpoint hashes, request/provider match, nonlocal egress consent, identity assurance, normalized completion, and existing Sophia digest closure. It never renders endpoint URLs, credentials, authorization material, or raw provider request IDs.

The human review page presents provider ID, trust and data-egress class, adapter/protocol, requested/observed model IDs, and assurance limits. The explanation engine remains posture-neutral: provider prestige, availability, cost, or model size does not change retention or publication posture. Receipts bind the safe provider evidence object for v2 only; v1 receipts remain compatible.

No provider call, network access, model output, repair, memory/PMR action, publication, deployment, or release occurs in Atlas.
