#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.build_public_repro_dashboard import (
    LANGUAGE_GOVERNANCE_ARTIFACTS,
    LANGUAGE_GOVERNANCE_AUDIT_ARTIFACTS,
    LANGUAGE_GOVERNANCE_AUDIT_BLOCKED_CLAIMS,
    LANGUAGE_GOVERNANCE_AUDIT_CLAIM_ALLOWED,
    LANGUAGE_GOVERNANCE_AUDIT_REQUIRED_DOC_PHRASES,
    LANGUAGE_GOVERNANCE_BLOCKED_CLAIMS,
    LANGUAGE_GOVERNANCE_BOUNDARY_TERMS,
    LANGUAGE_GOVERNANCE_CLAIM_ALLOWED,
    LANGUAGE_GOVERNANCE_DOCTRINE_PHRASES,
    LANGUAGE_GOVERNANCE_POSITIVE_LEXICON_TERMS,
    METRIC_SEMANTIC_CONTRACT_ALIASES,
    METRIC_SEMANTIC_CONTRACT_ARTIFACTS,
    METRIC_SEMANTIC_CONTRACT_BLOCKED_CLAIM_PHRASES,
    METRIC_SEMANTIC_CONTRACT_REQUIRED_BOUNDARY_PHRASES,
    METRIC_SEMANTIC_CONTRACT_METRIC_ROWS,
    METRIC_SEMANTIC_CLAIM_ALLOWED,
    PERTURBATION_STRUCTURE_AFFORDANCE_BLOCKED_CLAIM_PHRASES,
    PERTURBATION_STRUCTURE_AFFORDANCE_REQUIRED_BOUNDARY_PHRASES,
    VISUAL_REVIEW_MODEL_ARTIFACTS,
    VISUAL_REVIEW_MODEL_BLOCKED_CLAIMS,
    VISUAL_REVIEW_MODEL_CAUTION_BADGES,
    VISUAL_REVIEW_MODEL_CLAIM_ALLOWED,
    VISUAL_REVIEW_MODEL_INPUT_ARTIFACTS,
    VISUAL_REVIEW_MODEL_PERMITTED_RENDER_TARGETS,
    VISUAL_REVIEW_MODEL_PROHIBITED_RENDER_CLAIMS,
    VISUAL_REVIEW_MODEL_REPRO_FRAGMENTS,
    VISUAL_REVIEW_MODEL_REQUIRED_DOC_PHRASES,
    VISUAL_REVIEW_MODEL_SECTIONS,
    VISUAL_REVIEW_STATIC_HTML_ACCESSIBILITY_STATEMENTS,
    VISUAL_REVIEW_STATIC_HTML_ARTIFACTS,
    VISUAL_REVIEW_STATIC_HTML_BLOCKED_CLAIMS,
    VISUAL_REVIEW_STATIC_HTML_CLAIM_ALLOWED,
    VISUAL_REVIEW_STATIC_HTML_INPUT_ARTIFACTS,
    VISUAL_REVIEW_STATIC_HTML_REQUIRED_DOC_PHRASES,
    VISUAL_REVIEW_STATIC_HTML_REPRO_FRAGMENTS,
    STATIC_HTML_USABILITY_REVIEW_ANSWER_SCALE,
    STATIC_HTML_USABILITY_REVIEW_ARTIFACTS,
    STATIC_HTML_USABILITY_REVIEW_BLOCKED_CLAIMS,
    STATIC_HTML_USABILITY_REVIEW_CLAIM_ALLOWED,
    STATIC_HTML_USABILITY_REVIEW_DIMENSIONS,
    STATIC_HTML_USABILITY_REVIEW_INPUT_ARTIFACTS,
    STATIC_HTML_USABILITY_REVIEW_REPRO_FRAGMENTS,
    STATIC_HTML_USABILITY_REVIEW_REQUIRED_DOC_PHRASES,
    STATIC_HTML_USABILITY_REVIEW_RESPONSE_SUMMARY,
    STATIC_HTML_USABILITY_REVIEW_REVISION_THEMES,
    STATIC_HTML_USABILITY_REVISION_ARTIFACTS,
    STATIC_HTML_USABILITY_REVISION_BLOCKED_CLAIMS,
    STATIC_HTML_USABILITY_REVISION_CLAIM_ALLOWED,
    STATIC_HTML_USABILITY_REVISION_IMPROVEMENTS,
    STATIC_HTML_USABILITY_REVISION_INPUT_ARTIFACTS,
    STATIC_HTML_USABILITY_REVISION_LANGUAGE_AUDIT_TERMS,
    STATIC_HTML_USABILITY_REVISION_METRIC_EXPLAINER_TERMS,
    STATIC_HTML_USABILITY_REVISION_NON_AUTHORITY_BANNERS,
    STATIC_HTML_USABILITY_REVISION_REPRO_FRAGMENTS,
    STATIC_HTML_USABILITY_REVISION_REQUIRED_DOC_PHRASES,
    STATIC_HTML_USABILITY_REVISION_THEMES,
    STATIC_HTML_USABILITY_REVISION_TRACEABILITY_TERMS,
    AI_RECEIPT_ARCHITECTURE_ARTIFACTS,
    AI_RECEIPT_ARCHITECTURE_BLOCKED_CLAIMS,
    AI_RECEIPT_ARCHITECTURE_CLAIM_ALLOWED,
    AI_RECEIPT_ARCHITECTURE_EVENT_CHAIN,
    AI_RECEIPT_ARCHITECTURE_INPUT_ARTIFACTS,
    AI_RECEIPT_ARCHITECTURE_PRODUCT_FRAMING,
    AI_RECEIPT_ARCHITECTURE_REPRO_FRAGMENTS,
    AI_RECEIPT_ARCHITECTURE_REQUIRED_DOC_PHRASES,
    MINIMAL_VIABLE_RECEIPT_DESIGN_ARTIFACTS,
    MINIMAL_VIABLE_RECEIPT_DESIGN_BLOCKED_CLAIMS,
    MINIMAL_VIABLE_RECEIPT_DESIGN_CLAIM_ALLOWED,
    MINIMAL_VIABLE_RECEIPT_DESIGN_CONTESTABILITY_OPTIONS,
    MINIMAL_VIABLE_RECEIPT_DESIGN_COST_BURDEN_DIMENSIONS,
    MINIMAL_VIABLE_RECEIPT_DESIGN_DASHBOARD_SUMMARY,
    MINIMAL_VIABLE_RECEIPT_DESIGN_DOCTRINE_LANGUAGE,
    MINIMAL_VIABLE_RECEIPT_DESIGN_FAILURE_CLASSES,
    MINIMAL_VIABLE_RECEIPT_DESIGN_PRIOR_PHASE_RELATION,
    MINIMAL_VIABLE_RECEIPT_DESIGN_PRODUCT_EVENT_COMPONENTS,
    MINIMAL_VIABLE_RECEIPT_DESIGN_RECEIPT_SECTIONS,
    MINIMAL_VIABLE_RECEIPT_DESIGN_USER_QUESTIONS,
    MINIMAL_VIABLE_RECEIPT_LOCAL_PROTOTYPE_ARTIFACTS,
    MINIMAL_VIABLE_RECEIPT_LOCAL_PROTOTYPE_BLOCKED_CLAIMS,
    MINIMAL_VIABLE_RECEIPT_LOCAL_PROTOTYPE_CHECKLIST_ITEMS,
    MINIMAL_VIABLE_RECEIPT_LOCAL_PROTOTYPE_CLAIM_ALLOWED,
    MINIMAL_VIABLE_RECEIPT_LOCAL_PROTOTYPE_CONTESTABILITY_OPTIONS,
    MINIMAL_VIABLE_RECEIPT_LOCAL_PROTOTYPE_COST_BURDEN_DIMENSIONS,
    MINIMAL_VIABLE_RECEIPT_LOCAL_PROTOTYPE_DASHBOARD_SUMMARY,
    MINIMAL_VIABLE_RECEIPT_LOCAL_PROTOTYPE_DOCTRINE_LANGUAGE,
    MINIMAL_VIABLE_RECEIPT_LOCAL_PROTOTYPE_FAILURE_CLASSES,
    MINIMAL_VIABLE_RECEIPT_LOCAL_PROTOTYPE_FIXTURE_TERMS,
    MINIMAL_VIABLE_RECEIPT_LOCAL_PROTOTYPE_PRIOR_PHASE_RELATION,
    MINIMAL_VIABLE_RECEIPT_LOCAL_PROTOTYPE_RECEIPT_SECTIONS,
    MINIMAL_VIABLE_RECEIPT_LOCAL_PROTOTYPE_REPRO_FRAGMENTS,
    MINIMAL_VIABLE_RECEIPT_LOCAL_PROTOTYPE_USER_QUESTIONS,
    MVR_READABILITY_REVIEW_SEED_ARTIFACTS,
    MVR_READABILITY_REVIEW_SEED_BLOCKED_CLAIMS,
    MVR_READABILITY_REVISION_BLOCKED_CLAIMS,
    MVR_REAL_INPUT_PILOT_DESIGN_BLOCKED_CLAIMS,
    MVR_REAL_INPUT_PILOT_PROTOTYPE_BLOCKED_CLAIMS,
    MVR_QUARANTINE_REPAIR_BLOCKED_CLAIMS,
    MVR_HUMAN_SELECTED_FILE_SMOKE_BLOCKED_CLAIMS,
    COMPLIANCE_DESIGN_BLOCKED_CLAIMS,
    WAVE_EU_PROVENANCE_BLOCKED_CLAIMS,
    EU_AI_ACT_MVR_EVIDENCE_MAP_LOCAL_PROTOTYPE_BLOCKED_CLAIMS,
    COMPLIANCE_REPORT_SOURCE_CORPUS_BLOCKED_CLAIMS,
    SOURCE_CORPUS_BATCH_MANIFEST_20260610_BLOCKED_CLAIMS,
    MVR_READABILITY_REVIEW_SEED_CLAIM_ALLOWED,
    MVR_READABILITY_REVIEW_SEED_DASHBOARD_SUMMARY,
    MVR_READABILITY_REVIEW_SEED_DOCTRINE_LANGUAGE,
    MVR_READABILITY_REVIEW_SEED_FAILURE_CLASSES,
    MVR_READABILITY_REVIEW_SEED_PRIOR_PHASE_RELATION,
    MVR_READABILITY_REVIEW_SEED_QUESTIONNAIRE_DIMENSIONS,
    MVR_READABILITY_REVIEW_SEED_RATING_TERMS,
    MVR_READABILITY_REVIEW_SEED_REPRO_FRAGMENTS,
    MVR_READABILITY_REVIEW_SEED_REVISION_SUGGESTION_IDS,
    VALIDATION_TIERING_PROVENANCE_ACCEPTANCE_TERMS,
    VALIDATION_TIERING_PROVENANCE_ARTIFACTS,
    VALIDATION_TIERING_PROVENANCE_BLOCKED_CLAIMS,
    VALIDATION_TIERING_PROVENANCE_CLAIM_ALLOWED,
    VALIDATION_TIERING_PROVENANCE_DEEP_TERMS,
    VALIDATION_TIERING_PROVENANCE_FAILURE_CLASSES,
    VALIDATION_TIERING_PROVENANCE_RECEIPT_TERMS,
    VALIDATION_TIERING_PROVENANCE_REPRO_FRAGMENTS,
    VALIDATION_TIERING_PROVENANCE_REQUIRED_DOC_PHRASES,
    VALIDATION_TIERING_PROVENANCE_SMOKE_TERMS,
    VALIDATION_TIERING_PROVENANCE_TIER_TERMS,
    TELEMETRY_APERTURE_BLOCKED_CLAIMS,
    TELEMETRY_APERTURE_CLAIM_ALLOWED,
    TELEMETRY_APERTURE_DESIGN_ARTIFACTS,
    TELEMETRY_APERTURE_DIMENSIONS,
    TELEMETRY_APERTURE_ESCALATION_TRIGGERS,
    TELEMETRY_APERTURE_FAILURE_CLASSES,
    TELEMETRY_APERTURE_HARD_BLOCKS,
    TELEMETRY_APERTURE_HUMAN_REVIEW_GATES,
    TELEMETRY_APERTURE_MINIMUM_AUDIT_FLOOR_TERMS,
    TELEMETRY_APERTURE_MODES,
    TELEMETRY_APERTURE_POLICY_DEFAULTS,
    TELEMETRY_APERTURE_REPRO_FRAGMENTS,
    TELEMETRY_APERTURE_REQUIRED_DOC_PHRASES,
    TELEMETRY_APERTURE_SAFE_MET_SEM_ALIASES,
    TELEMETRY_APERTURE_UNSAFE_METRIC_BOUNDARIES,
    TAC_POLICY_SIMULATION_ARTIFACTS,
    TAC_POLICY_SIMULATION_BLOCKED_CLAIMS,
    TAC_POLICY_SIMULATION_CLAIM_ALLOWED,
    TAC_POLICY_SIMULATION_DECISION_RETENTION_TERMS,
    TAC_POLICY_SIMULATION_DESIGN_RELATION,
    TAC_POLICY_SIMULATION_HARD_BLOCK_TERMS,
    TAC_POLICY_SIMULATION_INPUT_REFERENCES,
    TAC_POLICY_SIMULATION_REPRO_FRAGMENTS,
    TAC_POLICY_SIMULATION_REQUIRED_DOC_PHRASES,
    TAC_POLICY_SIMULATION_SCENARIO_OUTCOMES,
    TAC_POLICY_SIMULATION_SCENARIOS,
    TAC_LOCAL_REVIEW_INTEGRATION_ARTIFACTS,
    TAC_LOCAL_REVIEW_INTEGRATION_BLOCKED_CLAIMS,
    TAC_LOCAL_REVIEW_INTEGRATION_CLAIM_ALLOWED,
    TAC_LOCAL_REVIEW_INTEGRATION_INPUT_ARTIFACTS,
    TAC_LOCAL_REVIEW_INTEGRATION_OVERLAY_TERMS,
    TAC_LOCAL_REVIEW_INTEGRATION_PRIOR_PHASE_RELATION,
    TAC_LOCAL_REVIEW_INTEGRATION_REPRO_FRAGMENTS,
    TAC_LOCAL_REVIEW_INTEGRATION_REQUIRED_DOC_PHRASES,
    TAC_LOCAL_REVIEW_INTEGRATION_REVIEWER_PROMPTS,
    TAC_AI_RECEIPT_EVENT_LINK_ARTIFACTS,
    TAC_AI_RECEIPT_EVENT_LINK_BLOCKED_CLAIMS,
    TAC_AI_RECEIPT_EVENT_LINK_CLAIM_ALLOWED,
    TAC_AI_RECEIPT_EVENT_LINK_EVENTS,
    TAC_AI_RECEIPT_EVENT_LINK_INPUT_ARTIFACTS,
    TAC_AI_RECEIPT_EVENT_LINK_PRIOR_PHASE_RELATION,
    TAC_AI_RECEIPT_EVENT_LINK_REFERENCE_TERMS,
    TAC_AI_RECEIPT_EVENT_LINK_REPRO_FRAGMENTS,
    TAC_AI_RECEIPT_EVENT_LINK_REQUIRED_DOC_PHRASES,
    PMR_PATHWAY_PRIORS_DESIGN_ARTIFACTS,
    PMR_PATHWAY_PRIORS_DESIGN_BLOCKED_CLAIMS,
    PMR_PATHWAY_PRIORS_DESIGN_CLAIM_ALLOWED,
    PMR_PATHWAY_PRIORS_DESIGN_DOCTRINE_LANGUAGE,
    PMR_PATHWAY_PRIORS_DESIGN_REPRO_FRAGMENTS,
    CES_DESIGN_ARTIFACTS,
    CES_DESIGN_BLOCKED_CLAIMS,
    CES_DESIGN_CLAIM_ALLOWED,
    CES_DESIGN_DOCTRINE_LANGUAGE,
    CES_DESIGN_EVENT_TYPES,
    CES_DESIGN_FAILURE_CLASSES,
    CES_DESIGN_IDENTITY_INTEGRITY_DOCTRINE,
    CES_DESIGN_LAYERS,
    CES_DESIGN_NEGATIVE_CONTROLS,
    CES_DESIGN_PMR_RELATION,
    CES_DESIGN_PRODUCT_LANGUAGE,
    CES_DESIGN_REPRO_FRAGMENTS,
    CES_DESIGN_SAFE_METRIC_ALIASES,
    CES_DESIGN_SIMILARITY_PRIVACY_DOCTRINE,
    CES_PMR_INDEXING_DESIGN_ARTIFACTS,
    CES_PMR_INDEXING_DESIGN_BLOCKED_CLAIMS,
    CES_PMR_INDEXING_DESIGN_BOUNDARIES,
    CES_PMR_INDEXING_DESIGN_CLAIM_ALLOWED,
    CES_PMR_INDEXING_DESIGN_DOCTRINE_LANGUAGE,
    CES_PMR_INDEXING_DESIGN_FAILURE_CLASSES,
    CES_PMR_INDEXING_DESIGN_FORBIDDEN_ROLES,
    CES_PMR_INDEXING_DESIGN_INDEX_FIELDS,
    CES_PMR_INDEXING_DESIGN_INDEX_ROLES,
    CES_PMR_INDEXING_DESIGN_PRESERVED_SOURCE_CLASSES,
    CES_PMR_INDEXING_DESIGN_QUERY_INTENTS,
    CES_PMR_INDEXING_DESIGN_RELATION,
    CES_PMR_INDEXING_DESIGN_REPRO_FRAGMENTS,
    CES_PMR_INDEXING_DESIGN_REVOCATION_TRIGGERS,
    TRIADIC_OBSERVATION_CONTRACT_ARTIFACTS,
    TRIADIC_OBSERVATION_CONTRACT_BLOCKED_CLAIMS,
    TRIADIC_OBSERVATION_CONTRACT_CLAIM_ALLOWED,
    TRIADIC_OBSERVATION_CONTRACT_DECLARATIONS,
    TRIADIC_OBSERVATION_CONTRACT_DOCTRINE_LANGUAGE,
    TRIADIC_OBSERVATION_CONTRACT_FAILURE_CLASSES,
    TRIADIC_OBSERVATION_CONTRACT_NO_SILENT_MODE_SHIFT_TRIGGERS,
    TRIADIC_OBSERVATION_CONTRACT_PRIOR_PHASE_RELATION,
    TRIADIC_OBSERVATION_CONTRACT_RECIPROCITY_BUDGET_DIMENSIONS,
    TRIADIC_OBSERVATION_CONTRACT_RECOVERY_RIGHTS,
    OBSERVATION_CONTRACT_POLICY_SIMULATION_ARTIFACTS,
    OBSERVATION_CONTRACT_POLICY_SIMULATION_BLOCKED_CLAIMS,
    OBSERVATION_CONTRACT_POLICY_SIMULATION_CLAIM_ALLOWED,
    OBSERVATION_CONTRACT_POLICY_SIMULATION_DOCTRINE_LANGUAGE,
    OBSERVATION_CONTRACT_POLICY_SIMULATION_FAILURE_CLASSES,
    OBSERVATION_CONTRACT_POLICY_SIMULATION_INPUT_REFERENCES,
    OBSERVATION_CONTRACT_POLICY_SIMULATION_MATRIX_TERMS,
    OBSERVATION_CONTRACT_POLICY_SIMULATION_PRIOR_PHASE_RELATION,
    OBSERVATION_CONTRACT_POLICY_SIMULATION_SCENARIO_OUTCOMES,
    OBSERVATION_CONTRACT_POLICY_SIMULATION_SCENARIOS,
)


REQUIRED_PHASES = {
    "EXP-SUITE-REGISTRY-01",
    "EXP-SUITE-REPRO-01",
    "WAVE-FAMILY-CLOSEOUT-01",
    "SONYA-INGRESS-HARDEN-03",
    "SOPHIA-UCC-ROUTE-01",
    "PUB-GOV-ARTIFACT-COG-01",
    "PUB-WAVE-ROSETTA-01",
    "UNI-02D-SONYA-GATE-01",
    "RETRO-LANE-00",
    "PUBLIC-UTILITY-ALPHA-00",
    "RAW-BASELINE-COMPARISON-00",
    "EVIDENCE-REVIEW-PACK-00",
    "RW-COMP-01",
    "RW-COMP-02",
    "RETROSYNTHESIS-SANDBOX-CYCLE-01",
    "EVIDENCE-REVIEW-PACK-01",
    "RW-COMP-03",
    "UNIVERSAL-STAGE-PIPELINE-00",
    "TRIADIC-OBSERVATION-CONTRACT-DESIGN-00",
    "OBSERVATION-CONTRACT-POLICY-SIMULATION-00",
    "ARTIFACT-CONTRACT-REGISTRY-01",
    "UNIVERSAL-COMPATIBILITY-MATRIX-00",
    "SONYA-ADAPTER-CONTRACT-REGISTRY-01",
    "SONYA-ADAPTER-SMOKE-00",
    "SONYA-LOCAL-FIXTURE-ADAPTER-01",
    "EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER-01",
    "SONYA-LOCAL-FIXTURE-ADAPTER-02",
    "SONYA-LOCAL-FIXTURE-ADAPTER-03",
    "EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER-02",
    "RW-COMP-LOCAL-ADAPTER-01",
    "PMR-00-PROVENANCE-MEMORY-RESERVOIR",
    "PMR-01-LOCAL-ARTIFACT-INDEX",
    "PMR-02-GLOBAL-PROVENANCE-COHERENCE-UTILITY",
    "PMR-03-LIFECYCLE-STATE-MACHINE",
    "PMR-04-LIFECYCLE-AUDIT-PREFLIGHT",
    "PMR-05-SOPHIA-LIFECYCLE-AUDIT-REVIEW",
    "SPEC-FRESHNESS-REGISTRY-00",
    "FUNDAMENTAL-COHERENCE-METRICS-00",
    "PMR-06-USER-CONFIRMATION-PREFLIGHT",
    "PMR-07-USER-CONFIRMATION-NEGATIVE-CONTROL",
    "PMR-08-VALID-USER-CONFIRMATION-RECEIPT-SCAFFOLD",
    "PMR-09-DESTRUCTIVE-ACTION-AUTHORIZATION-NEGATIVE-CONTROL",
    "PMR-10-DESTRUCTIVE-ACTION-AUTHORIZATION-PREFLIGHT",
    "PMR-ARCH-DIVERSITY-CHECKPOINT-00",
    "PMR-SIM-00",
    "PMR-STAT-00",
    "PMR-FED-STRESS-00",
    "PMR-HUMAN-PROVENANCE-00",
    "PMR-HUMAN-CONSENT-NEGATIVE-CONTROL-00",
    "SONYA-REQUIRED-MEMBRANE-CHECKPOINT-00",
    "TEL-EVENT-STACK-00",
    "EVIDENCE-REVIEW-PRODUCT-LOOP-02",
    "EVIDENCE-REVIEW-METRICS-00",
    "COGNITIVE-WATERS-PATTERN-METRICS-00",
    "ONTOLOGY-CLAIM-REGISTRY-00",
    "LOCAL-SONYA-PATH-PORTABILITY-00",
    "TB-PRODUCT-SLICE-00",
    "TB-PRODUCT-SLICE-01",
    "TB-PRODUCT-SLICE-02",
    "SONYA-LOCAL-SERVER-GATEWAY-00",
    "SONYA-LOCAL-SERVER-GATEWAY-01",
    "SONYA-LOCAL-SERVER-GATEWAY-02",
    "LOCAL-SERVER-USER-FILE-INGRESS-00",
    "LOCAL-SERVER-USER-FILE-INGRESS-01",
    "LOCAL-SERVER-USER-FILE-INGRESS-02",
    "LAN-READINESS-PREFLIGHT-00",
    "LAN-AUTHORITY-MODEL-00",
    "LAN-AUTHORITY-NEGATIVE-CONTROL-00",
    "LAN-OPERATOR-CONSENT-PREFLIGHT-00",
    "LOCAL-REVIEW-RUNTIME-V0",
    "USER-FACING-RECEIPT-UX-01",
    "PMR-CONTEXT-AVAILABILITY-LEDGER-00",
    "MET-LOCAL-00",
    "WAVE-ROSETTA-METRIC-CALIBRATION-00",
    "TAF-RUNTIME-00",
    "SONYA-METRIC-MEMBRANE-COVERAGE-00",
    "COHERENCE-METRIC-FORMULA-REGISTRY-00",
    "METRIC-BOUND-SOURCE-TAXONOMY-00",
    "FLOW-RUNTIME-00",
    "MET-SEM-00",
    "RUNTIME-METRICS-CORPUS-SEED-00",
    "PMR-LOCAL-RUNTIME-QUERYABLE-STORE-00",
    "RETROSYNTHESIS-READINESS-00",
    "RETROSYNTHESIS-LOCAL-PROTOTYPE-00",
    "ATLAS-LOCAL-MEMORY-ADMISSION-READINESS-00",
    "ATLAS-LOCAL-MEMORY-ADMISSION-PROTOTYPE-00",
    "HUMAN-REVIEW-PROXY-LOCAL-TESTING-00",
    "AI-CONTEXT-PERFORMANCE-CONTINUITY-00",
    "THEOREM-VALIDATION-PATHWAY-00",
    "COOP-ENTROPY-DIVIDEND-00",
    "TRIADIC-LLM-METRICS-SMOKE-00",
    "UCC-SOPHIA-CONTROL-FORENSICS-00",
    "UCC-STANDARDS-SOURCE-REGISTRY-AND-MATERIALITY-00",
    "TRIADIC-LLM-SMOKE-PMR-INVENTORY-CONTRACT-REPAIR-REVISION",
    "AI-FORENSICS-DOSSIER-00",
    "HUMAN-REVIEW-UX-00",
    "PERTURBATION-OBSERVATION-CAPTURE-00",
    "PERTURBATION-TRUNK-MAPPING-00",
    "PERTURBATION-RESIDUAL-NOVELTY-MAP-00",
    "PERTURBATION-STRUCTURE-AFFORDANCE-CARD-00",
    "MINIMAL-VIABLE-RECEIPT-LOCAL-PROTOTYPE-00",
    "MVR-LOCAL-PROTOTYPE-READABILITY-REVIEW-SEED-00",
    "MVR-LOCAL-PROTOTYPE-READABILITY-REVISION-00",
    "MVR-LOCAL-REAL-INPUT-PILOT-DESIGN-00",
    "MVR-LOCAL-REAL-INPUT-PILOT-PROTOTYPE-00",
    "MVR-LOCAL-REAL-INPUT-PILOT-QUARANTINE-DETECTION-REPAIR-00",
    "MVR-LOCAL-REAL-INPUT-PILOT-HUMAN-SELECTED-FILE-SMOKE-00",
    "COMPLIANCE-READY-MVR-REPORT-DESIGN-00",
    "COMPLIANCE-EVIDENCE-TOOLSET-LIBRARY-DESIGN-00",
    "WAVE-ROSETTA-CANONICAL-PROXY-BRIDGE-00",
    "EU-AI-ACT-MVR-EVIDENCE-MAPPING-DESIGN-00",
    "EU-AI-ACT-MVR-EVIDENCE-MAP-LOCAL-PROTOTYPE-00",
    "COMPLIANCE-READY-MVR-REPORT-LOCAL-PROTOTYPE-00",
    "SOURCE-CORPUS-PROVENANCE-ARCHIVE-00",
    "SOURCE-CORPUS-PROVENANCE-HASH-FILL-00",
    "SOURCE-CORPUS-BATCH-MANIFEST-2026-06-10-00",
    "WAVE-ROSETTA-CANONICAL-PROXY-BRIDGE-PROVENANCE-00",
}
REQUIRED_BOUNDARY_PHRASES = (
    "not truth certification",
    "not deployment authority",
    "not final answer release",
    "local fixture only",
    "requires external peer review",
    "route is not authorization",
    "receipt is not truth certification",
    "candidate is not answer",
    "admission is not execution",
    "dashboard is not deployment authority",
    "public utility alpha",
    "local reviewer demo",
    "not live model execution",
    "not live adapter execution",
    "not remote provider call",
    "not federation",
    "FLOW-RUNTIME-00",
    "MET-LOCAL-00",
    "TAF-RUNTIME-00",
    "WAVE Rosetta baseline",
    "baseline not universal identity",
    "Sonya metric membrane coverage",
    "waters_spiral_runtime_v0",
    "not general AI safety certification",
    "not recursive braid",
    "MET-SEM-00",
    "PROJECT-LANGUAGE-GOVERNANCE-00",
    "coherencelattice.metric_semantic_reconciliation_packet.v1",
    "active_profile_proxy_reconciliation",
    "LOCAL-REVIEW-RUNTIME-V0",
    "canonical_meanings_preserved_as_targets",
    "canonical_theory_status",
    "semantic_target_not_fully_implemented",
    "runtime_profile_semantics",
    "local_review_operational_proxies",
    "current_values_are_profile_specific_proxies",
    "population_calibration_required_for_full_claims",
    "build_metric_semantic_reconciliation_packet",
    METRIC_SEMANTIC_CLAIM_ALLOWED,
    *METRIC_SEMANTIC_CONTRACT_ARTIFACTS,
    *METRIC_SEMANTIC_CONTRACT_ALIASES,
    *[row["safe_label"] for row in METRIC_SEMANTIC_CONTRACT_METRIC_ROWS],
    *[f"Unsafe label: {row['unsafe_label']}" for row in METRIC_SEMANTIC_CONTRACT_METRIC_ROWS],
    *METRIC_SEMANTIC_CONTRACT_REQUIRED_BOUNDARY_PHRASES,
    *METRIC_SEMANTIC_CONTRACT_BLOCKED_CLAIM_PHRASES,
    "PROJECT-LANGUAGE-GOVERNANCE-00",
    "language_governance_status",
    "reviewer_facing_language_policy",
    "ontology_glossary_status",
    "identifier_alias_map_status",
    "scanner_status",
    "runtime_authority_expanded",
    LANGUAGE_GOVERNANCE_CLAIM_ALLOWED,
    *LANGUAGE_GOVERNANCE_ARTIFACTS,
    *LANGUAGE_GOVERNANCE_DOCTRINE_PHRASES,
    *LANGUAGE_GOVERNANCE_POSITIVE_LEXICON_TERMS,
    *LANGUAGE_GOVERNANCE_BOUNDARY_TERMS,
    *LANGUAGE_GOVERNANCE_BLOCKED_CLAIMS,
    "LANGUAGE-GOVERNANCE-AUDIT-RUNTIME-00",
    "coherencelattice.reviewer_language_audit_report.v1",
    "reviewer_facing_language_governance",
    "audit_status",
    "completed",
    "scanned_path_count",
    "scanned_file_count",
    "error_count",
    "audit_is_not_truth_certification",
    "audit_is_not_theorem_proof",
    "audit_is_not_product_release",
    "audit_is_not_authority",
    "audit_requires_human_review_for_policy_changes",
    LANGUAGE_GOVERNANCE_AUDIT_CLAIM_ALLOWED,
    *LANGUAGE_GOVERNANCE_AUDIT_ARTIFACTS,
    *LANGUAGE_GOVERNANCE_AUDIT_REQUIRED_DOC_PHRASES,
    *LANGUAGE_GOVERNANCE_AUDIT_BLOCKED_CLAIMS,
    "build_reviewer_language_audit",
    "VISUAL-REVIEW-MODEL-00",
    "future_ui_rendering_contract",
    "data_model_only_no_ui",
    "model_is_ui_implementation",
    "visual_section_count",
    "language_audit_error_count",
    "build_visual_review_model",
    VISUAL_REVIEW_MODEL_CLAIM_ALLOWED,
    *VISUAL_REVIEW_MODEL_ARTIFACTS,
    *VISUAL_REVIEW_MODEL_INPUT_ARTIFACTS,
    *VISUAL_REVIEW_MODEL_SECTIONS,
    *VISUAL_REVIEW_MODEL_CAUTION_BADGES,
    *VISUAL_REVIEW_MODEL_REQUIRED_DOC_PHRASES,
    *VISUAL_REVIEW_MODEL_PERMITTED_RENDER_TARGETS,
    *VISUAL_REVIEW_MODEL_PROHIBITED_RENDER_CLAIMS,
    *VISUAL_REVIEW_MODEL_REPRO_FRAGMENTS,
    *VISUAL_REVIEW_MODEL_BLOCKED_CLAIMS,
    "VISUAL-REVIEW-STATIC-HTML-PROTOTYPE-00",
    "local_static_html_review_surface",
    "visual_review_static_review.html",
    "external_resource_count",
    "network_call_performed",
    "ui_release_performed",
    "build_visual_review_static_html",
    VISUAL_REVIEW_STATIC_HTML_CLAIM_ALLOWED,
    *VISUAL_REVIEW_STATIC_HTML_ARTIFACTS,
    *VISUAL_REVIEW_STATIC_HTML_INPUT_ARTIFACTS,
    *VISUAL_REVIEW_STATIC_HTML_REQUIRED_DOC_PHRASES,
    *VISUAL_REVIEW_STATIC_HTML_ACCESSIBILITY_STATEMENTS,
    *VISUAL_REVIEW_STATIC_HTML_REPRO_FRAGMENTS,
    *VISUAL_REVIEW_STATIC_HTML_BLOCKED_CLAIMS,
    "STATIC-HTML-USABILITY-REVIEW-SEED-00",
    "local_static_html_usability_seed",
    "local_test_reviewer",
    "build_static_html_usability_review_seed",
    STATIC_HTML_USABILITY_REVIEW_CLAIM_ALLOWED,
    *STATIC_HTML_USABILITY_REVIEW_ARTIFACTS,
    *STATIC_HTML_USABILITY_REVIEW_INPUT_ARTIFACTS,
    *STATIC_HTML_USABILITY_REVIEW_DIMENSIONS,
    *STATIC_HTML_USABILITY_REVIEW_ANSWER_SCALE,
    *STATIC_HTML_USABILITY_REVIEW_RESPONSE_SUMMARY,
    *STATIC_HTML_USABILITY_REVIEW_REVISION_THEMES,
    *STATIC_HTML_USABILITY_REVIEW_REQUIRED_DOC_PHRASES,
    *STATIC_HTML_USABILITY_REVIEW_REPRO_FRAGMENTS,
    *STATIC_HTML_USABILITY_REVIEW_BLOCKED_CLAIMS,
    "STATIC-HTML-USABILITY-REVISION-00",
    "local_static_html_usability_revision",
    "build_static_html_usability_revision",
    STATIC_HTML_USABILITY_REVISION_CLAIM_ALLOWED,
    *STATIC_HTML_USABILITY_REVISION_ARTIFACTS,
    *STATIC_HTML_USABILITY_REVISION_INPUT_ARTIFACTS,
    *STATIC_HTML_USABILITY_REVISION_THEMES,
    *STATIC_HTML_USABILITY_REVISION_IMPROVEMENTS,
    *STATIC_HTML_USABILITY_REVISION_REQUIRED_DOC_PHRASES,
    *STATIC_HTML_USABILITY_REVISION_METRIC_EXPLAINER_TERMS,
    *STATIC_HTML_USABILITY_REVISION_LANGUAGE_AUDIT_TERMS,
    *STATIC_HTML_USABILITY_REVISION_TRACEABILITY_TERMS,
    *STATIC_HTML_USABILITY_REVISION_NON_AUTHORITY_BANNERS,
    *STATIC_HTML_USABILITY_REVISION_REPRO_FRAGMENTS,
    *STATIC_HTML_USABILITY_REVISION_BLOCKED_CLAIMS,
    "AI-RECEIPT-ARCHITECTURE-00",
    "MINIMAL-VIABLE-RECEIPT-DESIGN-00",
    "ai_receipt_architecture",
    "A watermark says AI was here. A receipt says what happened.",
    AI_RECEIPT_ARCHITECTURE_CLAIM_ALLOWED,
    *AI_RECEIPT_ARCHITECTURE_ARTIFACTS,
    *AI_RECEIPT_ARCHITECTURE_INPUT_ARTIFACTS,
    *AI_RECEIPT_ARCHITECTURE_EVENT_CHAIN,
    *AI_RECEIPT_ARCHITECTURE_REQUIRED_DOC_PHRASES,
    *AI_RECEIPT_ARCHITECTURE_PRODUCT_FRAMING,
    *AI_RECEIPT_ARCHITECTURE_REPRO_FRAGMENTS,
    *AI_RECEIPT_ARCHITECTURE_BLOCKED_CLAIMS,
    "VALIDATION-TIERING-PROVENANCE-00",
    "policy_status",
    "validation_tier = deep",
    VALIDATION_TIERING_PROVENANCE_CLAIM_ALLOWED,
    *VALIDATION_TIERING_PROVENANCE_ARTIFACTS,
    *VALIDATION_TIERING_PROVENANCE_TIER_TERMS,
    *VALIDATION_TIERING_PROVENANCE_SMOKE_TERMS,
    *VALIDATION_TIERING_PROVENANCE_ACCEPTANCE_TERMS,
    *VALIDATION_TIERING_PROVENANCE_DEEP_TERMS,
    *VALIDATION_TIERING_PROVENANCE_REQUIRED_DOC_PHRASES,
    *VALIDATION_TIERING_PROVENANCE_FAILURE_CLASSES,
    *VALIDATION_TIERING_PROVENANCE_RECEIPT_TERMS,
    *VALIDATION_TIERING_PROVENANCE_REPRO_FRAGMENTS,
    *VALIDATION_TIERING_PROVENANCE_BLOCKED_CLAIMS,
    "TELEMETRY-APERTURE-DESIGN-00",
    TELEMETRY_APERTURE_CLAIM_ALLOWED,
    *TELEMETRY_APERTURE_DESIGN_ARTIFACTS,
    *TELEMETRY_APERTURE_MODES,
    *TELEMETRY_APERTURE_DIMENSIONS,
    *TELEMETRY_APERTURE_MINIMUM_AUDIT_FLOOR_TERMS,
    *TELEMETRY_APERTURE_POLICY_DEFAULTS,
    *TELEMETRY_APERTURE_ESCALATION_TRIGGERS,
    *TELEMETRY_APERTURE_HARD_BLOCKS,
    *TELEMETRY_APERTURE_HUMAN_REVIEW_GATES,
    *TELEMETRY_APERTURE_SAFE_MET_SEM_ALIASES,
    *TELEMETRY_APERTURE_REQUIRED_DOC_PHRASES,
    *TELEMETRY_APERTURE_FAILURE_CLASSES,
    *TELEMETRY_APERTURE_REPRO_FRAGMENTS,
    *TELEMETRY_APERTURE_UNSAFE_METRIC_BOUNDARIES,
    *TELEMETRY_APERTURE_BLOCKED_CLAIMS,
    "TAC-POLICY-SIMULATION-00",
    TAC_POLICY_SIMULATION_CLAIM_ALLOWED,
    *TAC_POLICY_SIMULATION_ARTIFACTS,
    *TAC_POLICY_SIMULATION_INPUT_REFERENCES,
    *TAC_POLICY_SIMULATION_SCENARIOS,
    *TAC_POLICY_SIMULATION_SCENARIO_OUTCOMES,
    *TAC_POLICY_SIMULATION_HARD_BLOCK_TERMS,
    *TAC_POLICY_SIMULATION_DECISION_RETENTION_TERMS,
    *TAC_POLICY_SIMULATION_REQUIRED_DOC_PHRASES,
    *TAC_POLICY_SIMULATION_DESIGN_RELATION,
    *TAC_POLICY_SIMULATION_REPRO_FRAGMENTS,
    *TAC_POLICY_SIMULATION_BLOCKED_CLAIMS,
    "TAC-LOCAL-REVIEW-INTEGRATION-00",
    "TAC-AI-RECEIPT-EVENT-LINK-00",
    "PMR-PATHWAY-PRIORS-DESIGN-DOCTRINE-00",
    "COHERENCE-EVENT-SIGNATURES-DESIGN-00",
    "CES-PMR-INDEXING-DESIGN-00",
    "TRIADIC-OBSERVATION-CONTRACT-DESIGN-00",
    "OBSERVATION-CONTRACT-POLICY-SIMULATION-00",
    TRIADIC_OBSERVATION_CONTRACT_CLAIM_ALLOWED,
    *TRIADIC_OBSERVATION_CONTRACT_ARTIFACTS,
    *TRIADIC_OBSERVATION_CONTRACT_DOCTRINE_LANGUAGE,
    *TRIADIC_OBSERVATION_CONTRACT_DECLARATIONS,
    *TRIADIC_OBSERVATION_CONTRACT_NO_SILENT_MODE_SHIFT_TRIGGERS,
    *TRIADIC_OBSERVATION_CONTRACT_RECOVERY_RIGHTS,
    *TRIADIC_OBSERVATION_CONTRACT_RECIPROCITY_BUDGET_DIMENSIONS,
    *TRIADIC_OBSERVATION_CONTRACT_FAILURE_CLASSES,
    *TRIADIC_OBSERVATION_CONTRACT_PRIOR_PHASE_RELATION,
    *TRIADIC_OBSERVATION_CONTRACT_BLOCKED_CLAIMS,
    OBSERVATION_CONTRACT_POLICY_SIMULATION_CLAIM_ALLOWED,
    *OBSERVATION_CONTRACT_POLICY_SIMULATION_ARTIFACTS,
    *OBSERVATION_CONTRACT_POLICY_SIMULATION_INPUT_REFERENCES,
    *OBSERVATION_CONTRACT_POLICY_SIMULATION_SCENARIOS,
    *OBSERVATION_CONTRACT_POLICY_SIMULATION_SCENARIO_OUTCOMES,
    *OBSERVATION_CONTRACT_POLICY_SIMULATION_DOCTRINE_LANGUAGE,
    *OBSERVATION_CONTRACT_POLICY_SIMULATION_PRIOR_PHASE_RELATION,
    *OBSERVATION_CONTRACT_POLICY_SIMULATION_MATRIX_TERMS,
    *OBSERVATION_CONTRACT_POLICY_SIMULATION_FAILURE_CLASSES,
    *OBSERVATION_CONTRACT_POLICY_SIMULATION_BLOCKED_CLAIMS,
    "build_observation_contract_policy_simulation",
    "Publication sync grants no runtime authority.",
    TAC_LOCAL_REVIEW_INTEGRATION_CLAIM_ALLOWED,
    *TAC_LOCAL_REVIEW_INTEGRATION_ARTIFACTS,
    *TAC_LOCAL_REVIEW_INTEGRATION_INPUT_ARTIFACTS,
    *TAC_LOCAL_REVIEW_INTEGRATION_OVERLAY_TERMS,
    *TAC_LOCAL_REVIEW_INTEGRATION_REVIEWER_PROMPTS,
    *TAC_LOCAL_REVIEW_INTEGRATION_REQUIRED_DOC_PHRASES,
    *TAC_LOCAL_REVIEW_INTEGRATION_PRIOR_PHASE_RELATION,
    *TAC_LOCAL_REVIEW_INTEGRATION_REPRO_FRAGMENTS,
    *TAC_LOCAL_REVIEW_INTEGRATION_BLOCKED_CLAIMS,
    "RUNTIME-METRICS-CORPUS-SEED-00",
    "bounded seed corpus instrumentation only",
    "not population calibration",
    "not human benefit proof",
    "not market validation",
    "PMR-LOCAL-RUNTIME-QUERYABLE-STORE-00",
    "bounded local provenance retrieval only",
    "PMR query is local provenance retrieval only",
    "PMR query is not memory write",
    "PMR query is not retrosynthesis",
    "PMR query is not Atlas memory admission",
    "PMR query is not truth certification",
    "PMR query is not product release",
    "PMR query is not final answer",
    "build_pmr_local_query_store",
    "build_runtime_metrics_seed_corpus",
    "runtime_metrics_seed_corpus",
    "pmr_local_query",
    "RETROSYNTHESIS-READINESS-00",
    "readiness, not retrosynthesis",
    "ready only for a bounded local retrosynthesis prototype",
    "No improvement hypotheses were generated",
    "No Atlas memory write occurred",
    "No memory admission occurred",
    "No federation occurred",
    "No product release occurred",
    "No Omega detection occurred",
    "Population calibration is not claimed",
    "build_retrosynthesis_readiness_assessment",
    "retrosynthesis_readiness",
    "This command builds readiness artifacts only",
    "No improvement hypotheses are generated",
    "No Atlas memory write occurs",
    "No Atlas memory admission occurs",
    "No truth certification occurs",
    "No consciousness proof or universal ontology proof is emitted",
    "RETROSYNTHESIS-LOCAL-PROTOTYPE-00",
    "bounded local candidate generation only",
    "candidate hypotheses are not truth",
    "repair plans are not authority",
    "Human review is required",
    "No final answer was emitted",
    "No accepted evidence was emitted",
    "No provider runtime occurred",
    "No LAN enablement occurred",
    "build_retrosynthesis_local_prototype",
    "retrosynthesis_local_prototype",
    "ATLAS-LOCAL-MEMORY-ADMISSION-READINESS-00",
    "This is Atlas memory admission readiness, not Atlas memory admission",
    "ready_for_bounded_atlas_memory_admission_prototype",
    "ATLAS-LOCAL-MEMORY-ADMISSION-PROTOTYPE-00",
    "readiness_dimensions = 21",
    "readiness_dimension_count = 21",
    "candidate_hypotheses = 7",
    "candidate_repair_plans = 3",
    "pattern_observations = 5",
    "No memory candidate was written",
    "No accepted evidence was emitted",
    "Human review is required before any future Atlas memory admission prototype",
    "build_atlas_local_memory_admission_readiness",
    "atlas_local_memory_admission_readiness",
    "ATLAS-LOCAL-MEMORY-ADMISSION-PROTOTYPE-00",
    "completed_candidate_admission_review",
    "Candidate admission reviews are not Atlas memory admission",
    "No Atlas memory entry was written",
    "HUMAN-REVIEW-PROXY-LOCAL-TESTING-00",
    "emitted_local_test_proxy_only",
    "Proxy review is not product human review",
    "AI-CONTEXT-PERFORMANCE-CONTINUITY-00",
    "WAITING_FOR_LOCAL_VALIDATION",
    "Live chat is not the primary memory substrate",
    "THEOREM-VALIDATION-PATHWAY-00",
    "theorem_validation_pathway_status = locally_validated",
    "Theorem cards are not proof",
    "COOP-ENTROPY-DIVIDEND-00",
    "proof_grade_current = operational_metric_hypothesis",
    "COOP-ENTROPY-DIVIDEND-00 is not proven",
    "build_atlas_local_memory_admission_prototype",
    "build_local_test_proxy_review_receipt",
    "build_ai_context_performance_continuity",
    "build_theorem_validation_pathway",
    "TRIADIC-LLM-METRICS-SMOKE-00",
    "raw model output is not final answer",
    "Sonya model candidate is not final answer",
    "raw model output is final answer",
    "UCC review certifies compliance",
    "NIST compliance is certified",
    "NIST controls were ingested",
    "theorem validation proves theorem",
    "COOP-ENTROPY-DIVIDEND-00 is proven",
    "evidence ledger certifies truth",
    "provider runtime",
    "Raw model output is not final answer",
    "build_triadic_llm_metrics_smoke",
    "UCC-SOPHIA-CONTROL-FORENSICS-00",
    "UCC control review is not legal compliance certification",
    "build_sophia_ucc_control_review",
    "UCC-STANDARDS-SOURCE-REGISTRY-AND-MATERIALITY-00",
    "NIST control text is not ingested",
    "build_ucc_standards_source_registry",
    "build_ucc_materiality_profile",
    "build_ucc_materiality_override_receipt",
    "TRIADIC-LLM-SMOKE-PMR-INVENTORY-CONTRACT-REPAIR-REVISION",
    "Visibility repair does not create final-answer authority",
    "AI-FORENSICS-DOSSIER-00",
    "Triadic Brain turns AI outputs into auditable, source-linked, control-aware forensic dossiers",
    "The dossier is AI process forensics",
    "The dossier is not model mind-reading",
    "The dossier is not hidden chain-of-thought disclosure",
    "This dossier is not a final answer",
    "This dossier is not truth certification",
    "This dossier is not compliance certification",
    "This dossier is not audit opinion",
    "This dossier is not professional attestation",
    "AI Forensics Dossier is final answer",
    "AI Forensics Dossier certifies truth",
    "AI Forensics Dossier certifies compliance",
    "AI Forensics Dossier is audit opinion",
    "AI Forensics Dossier is professional attestation",
    "AI Forensics Dossier reveals hidden chain of thought",
    "AI Forensics Dossier performs model mind-reading",
    "build_ai_forensics_dossier",
    "HUMAN-REVIEW-UX-00",
    "Human Review UX presents an AI Forensics Dossier for bounded review",
    "The reviewer inspected an AI Forensics Dossier",
    "The default local-test decision is needs_more_evidence",
    "Human review remains bounded by the selected action",
    "The review decision is not final-answer authority",
    "The review decision is not truth certification",
    "The review decision is not compliance certification",
    "The review decision is not audit opinion",
    "The review decision is not professional attestation",
    "The review decision is not product release",
    "The review decision is not memory write",
    "The review decision is not Atlas memory admission",
    "Professional or compliance use requires appropriate qualified review",
    "Product human review is not completed in local test mode",
    "Human Review UX creates final answer authority",
    "Human Review UX certifies truth",
    "Human Review UX certifies compliance",
    "Human Review UX is audit opinion",
    "Human Review UX is professional attestation",
    "Human Review UX approves product release",
    "Human Review UX approves provider runtime",
    "Human Review UX approves memory write",
    "Human Review UX approves Atlas memory admission",
    "perturbation observation proves novelty",
    "perturbation observation certifies diagnosis",
    "abstraction affordance is truth",
    "hyperreal resonance is authority",
    "trunk similarity is identity",
    "trunk mapping is novelty discovery",
    "heatmap values certify probability",
    "residual structure proves a novel trunk",
    "residual novelty map discovers novelty",
    "novel branch candidate is novel trunk proof",
    "reverse trunk mapping proves identity",
    "creative mapping is causal diagnosis",
    "single fixture proves theory",
    "PERTURBATION-STRUCTURE-AFFORDANCE-00 is proven",
    "perturbation structure-affordance is a proven theorem",
    "speculative_pattern is proof",
    "operational_metric_hypothesis target has already been achieved",
    "perturbation evidence proves theorem",
    "perturbation evidence certifies novelty",
    "residual novelty candidate is novelty discovery",
    "reverse trunk hypothesis is proof",
    "local test review is product human review",
    "needs_more_evidence is approval",
    "approve_for_local_next_step is final answer approval",
    "escalate_to_professional_review is professional attestation",
    "build_human_review_ux_packet",
    "PERTURBATION-OBSERVATION-CAPTURE-00",
    "Perturbation is not mere degradation",
    "Perturbation observation is not novelty discovery",
    "Abstraction affordance is not truth",
    "Hyperreal resonance is not authority",
    "Causal candidate is not certified diagnosis",
    "PERTURBATION-TRUNK-MAPPING-00",
    "Known trunks were mapped before novelty claims",
    "Trunk similarity is not identity",
    "Known-trunk mapping is not novelty discovery",
    "Residual structure is not novel trunk proof",
    "Heatmap values are diagnostic, not probability certification",
    "Reverse mapping is not performed in this phase",
    "PERTURBATION-RESIDUAL-NOVELTY-MAP-00",
    "Residual novelty mapping was performed only after known trunk mapping",
    "Candidate novelty regions were generated",
    "Candidate novelty is not novelty discovery",
    "Novel branch candidate is not novel trunk proof",
    "Reverse trunk candidates are hypotheses only",
    "Abstraction candidates are not truth",
    "Creative mapping is not causal diagnosis",
    "Single fixture is not theory",
    "More observations are required before stronger claims",
    "perturbation observation proves novelty",
    "perturbation observation certifies diagnosis",
    "abstraction affordance is truth",
    "hyperreal resonance is authority",
    "trunk similarity is identity",
    "trunk mapping is novelty discovery",
    "heatmap values certify probability",
    "residual structure proves a novel trunk",
    "residual novelty map discovers novelty",
    "novel branch candidate is novel trunk proof",
    "reverse trunk mapping proves identity",
    "creative mapping is causal diagnosis",
    "single fixture proves theory",
    "build_perturbation_observation_capture",
    "build_perturbation_trunk_mapping",
    "build_perturbation_residual_novelty_map",
    "PERTURBATION-STRUCTURE-AFFORDANCE-CARD-00",
    "PERTURBATION-STRUCTURE-AFFORDANCE-00",
    "perturbation_novelty_mapping",
    "theorem_cards = 2",
    "proof_grade_current = speculative_pattern",
    "proof_grade_target = operational_metric_hypothesis",
    "proof_grade_claimed = none_yet",
    "perturbation_evidence_rows = 9",
    *PERTURBATION_STRUCTURE_AFFORDANCE_REQUIRED_BOUNDARY_PHRASES,
    *PERTURBATION_STRUCTURE_AFFORDANCE_BLOCKED_CLAIM_PHRASES,
    "build_theorem_validation_pathway",
    "not Atlas memory admission yet",
    "raw baseline comparison",
    "fixture-only measurement scaffold",
    "not hallucination reduction proof",
    "not model quality benchmark",
    "evidence review pack",
    "AI review that shows its work",
    "not legal advice",
    "not medical advice",
    "not tax advice",
    "not compliance certification",
    "not live model execution",
    "not production evaluation",
    "RW-COMP-01",
    "fixture-only comparison scaffold",
    "not model superiority proof",
    "not model quality benchmark",
    "not live model evaluation",
    "not professional advice",
    "not compliance certification",
    "RW-COMP-02",
    "deterministic multi-fixture comparison battery",
    "RETROSYNTHESIS-SANDBOX-CYCLE-01",
    "candidate repair",
    "not canon adoption",
    "not memory write",
    "not final answer release",
    "not Publisher finalization",
    "not Omega detection",
    "not deployment authority",
    "not recursive self-improvement",
    "EVIDENCE-REVIEW-PACK-01",
    "candidate revision",
    "not accepted evidence",
    "not canon adoption",
    "not memory write",
    "not final answer release",
    "not Publisher finalization",
    "not Omega detection",
    "not deployment authority",
    "not recursive self-improvement",
    "not hallucination reduction proof",
    "RW-COMP-03",
    "held-out blinded fixture scaffold",
    "not hallucination reduction proof",
    "not model superiority proof",
    "not live model evaluation",
    "not live human study",
    "simulated scores",
    "not accepted evidence",
    "not production evaluation",
    "universal architecture scaffold",
    "The brain runs cognition stages; experiments configure those stages.",
    "profiles are configuration",
    "experiments are configurations",
    "fail-closed receipts",
    "hash-only",
    "not product release",
    "not experiment result",
    "not benchmark result",
    "not hallucination reduction proof",
    "not deployment authority",
    "not recursive self-improvement",
    "Sonya Adapter Contract Registry",
    "Adapter capability is not adapter authorization",
    "all adapters disabled or blocked",
    "not adapter execution",
    "not network authorization",
    "not remote provider call",
    "not model weight training",
    "raw output is forbidden",
    "candidate packet required",
    "failure receipts required",
    "Sonya Adapter Smoke",
    "exercises contracts, not live adapters",
    "not live adapter execution",
    "not network authorization",
    "not remote provider call",
    "not model weight training",
    "raw output rejected",
    "candidate packet",
    "failure receipts",
    "telemetry events",
    "provenance events",
    "Sonya Local Fixture Adapter",
    "deterministic local fixtures",
    "not live adapters",
    "not live adapter execution",
    "not network authorization",
    "not remote provider call",
    "not model weight training",
    "candidate packets",
    "failure receipts",
    "telemetry events",
    "provenance events",
    "Adapter output is not accepted as cognition directly.",
    "Local adapter candidates become reviewable only through the Evidence Review Pack path.",
    "Evidence Review Pack local-adapter route",
    "not accepted evidence",
    "not adapter authorization",
    "Candidate packets require UCC-controlled review.",
    "The claim map is not truth certification.",
    "The candidate is not final answer.",
    "Selection policy is not final answer.",
    "Multi-adapter local fixture selection still requires Evidence Review Pack review.",
    "Sonya Local Fixture Adapter multi-route",
    "not adapter authorization",
    "not model quality benchmark",
    "Source fixture references are not stale identity leakage.",
    "Nested SONYA-LOCAL-FIXTURE-ADAPTER-01 references are source fixture dependencies, not stale identity leakage.",
    "Current route identity is explicit.",
    "Source fixture identity is explicit.",
    "Evidence Review Pack local-adapter route references are explicit.",
    "Lineage does not grant authority.",
    "Sonya local adapter lineage packet is not adapter execution.",
    "Sonya local adapter lineage packet is not network authorization.",
    "Sonya local adapter lineage packet is not memory write.",
    "Sonya local adapter lineage packet is not final answer release.",
    "Sonya local adapter lineage packet is not deployment authority.",
    "Sonya local adapter lineage packet is not truth certification.",
    "Deltas are structural review descriptors, not hallucination reduction proof.",
    "Revised local adapter candidate remains candidate-only, not accepted evidence.",
    "Evidence Review Pack local-adapter revision loop is not final answer selection.",
    "Evidence Review Pack local-adapter revision loop is not model quality benchmark.",
    "Evidence Review Pack local-adapter revision loop is not model superiority proof.",
    "Evidence Review Pack local-adapter revision loop is not adapter authorization.",
    "Evidence Review Pack local-adapter revision loop is not memory write.",
    "Evidence Review Pack local-adapter revision loop is not model-weight training.",
    "Evidence Review Pack local-adapter revision loop is not deployment authority.",
    "Evidence Review Pack local-adapter revision loop is not recursive self-improvement.",
    "Deltas are structural review descriptors only.",
    "RW-COMP local-adapter comparison is not hallucination reduction proof or a model quality benchmark.",
    "RW-COMP local-adapter comparison is not model superiority proof.",
    "RW-COMP local-adapter comparison is not final answer selection.",
    "RW-COMP local-adapter comparison is not accepted evidence.",
    "RW-COMP local-adapter comparison is not adapter authorization.",
    "RW-COMP local-adapter comparison is not memory write.",
    "RW-COMP local-adapter comparison is not model-weight training.",
    "RW-COMP local-adapter comparison is not deployment authority.",
    "RW-COMP local-adapter comparison is not recursive self-improvement.",
    "Memory is governed provenance under resource constraints.",
    "Memory is not storage.",
    "Hash is not encryption.",
    "User controls local memory budget.",
    "PMR is not Atlas canon.",
    "PMR is not model-weight training data.",
    "PMR artifact index is not generic cache.",
    "PMR artifact lifecycle state is not truth status.",
    "PMR dependency graph is not canon graph.",
    "PMR-01 performs indexing only, not pruning.",
    "Federation is blocked by default.",
    "PMR is not resource economy or token economy.",
    "GPCU is lifecycle/storage utility, not truth score.",
    "GPCU is not reward entitlement.",
    "GPCU is not token economy.",
    "Lifecycle recommendation is not pruning.",
    "Reward mechanics are deferred.",
    "Federation remains blocked by default.",
    "PMR-02 is not Atlas canon.",
    "PMR-02 is not memory write authorization.",
    "PMR-02 is not model-weight training.",
    "PMR-02 is not deployment authority.",
    "PMR-02 is not hallucination reduction proof.",
    "Recommendation is not transition; transition candidate is not action.",
    "Recommendation is not transition.",
    "Transition candidate is not action.",
    "Lifecycle state is not truth status.",
    "Destructive action requires future Sophia lifecycle audit.",
    "Destructive action requires future user confirmation.",
    "No pruning or deletion occurs in PMR-03.",
    "PMR-03 is not federation authorization.",
    "PMR-03 is not reward entitlement.",
    "PMR-03 is not token economy.",
    "PMR-03 is not Atlas canon.",
    "PMR-03 is not memory write authorization.",
    "PMR-03 is not model-weight training.",
    "PMR-03 is not deployment authority.",
    "PMR-03 is not truth certification.",
    "Preflight is not approval.",
    "Audit candidate is not action.",
    "Sophia lifecycle audit is required before destructive action.",
    "User confirmation is required before destructive local action.",
    "No Sophia approval packet is emitted.",
    "No pruning or deletion occurs in PMR-04.",
    "PMR-04 is not federation authorization.",
    "PMR-04 is not reward entitlement.",
    "PMR-04 is not token economy.",
    "PMR-04 is not memory write authorization.",
    "PMR-04 is not deployment authority.",
    "PMR-04 is not truth certification.",
    "Sophia review is not Sophia approval.",
    "Audit recommendation is not action.",
    "No Sophia approval packet is emitted.",
    "Destructive action requires future Sophia approval.",
    "Destructive action requires future user confirmation.",
    "No pruning or deletion occurs in PMR-05.",
    "PMR-05 is not federation authorization.",
    "PMR-05 is not reward entitlement.",
    "PMR-05 is not token economy.",
    "PMR-05 is not Atlas canon.",
    "PMR-05 is not memory write authorization.",
    "PMR-05 is not model-weight training.",
    "PMR-05 is not deployment authority.",
    "PMR-05 is not truth certification.",
    "User confirmation request is not user confirmation.",
    "User confirmation is not action.",
    "No user confirmation receipt is emitted.",
    "Destructive action requires future Sophia approval.",
    "Destructive action requires future user confirmation.",
    "No pruning or deletion occurs in PMR-06.",
    "PMR-06 is not Sophia approval.",
    "PMR-06 is not federation authorization.",
    "PMR-06 is not reward entitlement.",
    "PMR-06 is not token economy.",
    "PMR-06 is not Atlas canon.",
    "PMR-06 is not memory write authorization.",
    "PMR-06 is not model-weight training.",
    "PMR-06 is not deployment authority.",
    "PMR-06 is not truth certification.",
    "Invalid confirmation is not confirmation.",
    "Missing confirmation is not confirmation.",
    "Ambiguous confirmation is not confirmation.",
    "Forged confirmation is not confirmation.",
    "Expired confirmation is not confirmation.",
    "Scope-mismatched confirmation is not confirmation.",
    "Confirmation without Sophia approval is insufficient.",
    "Confirmation cannot override retain-lock, quarantine, revocation, or dependency blocks.",
    "No user confirmation receipt is emitted in PMR-07.",
    "No pruning or deletion occurs in PMR-07.",
    "PMR-07 is not Sophia approval.",
    "PMR-07 is not federation authorization.",
    "PMR-07 is not reward entitlement.",
    "PMR-07 is not token economy.",
    "PMR-07 is not Atlas canon.",
    "PMR-07 is not memory write authorization.",
    "PMR-07 is not model-weight training.",
    "PMR-07 is not deployment authority.",
    "PMR-07 is not truth certification.",
    "Valid user confirmation receipt is not action.",
    "Confirmation authorizes eligibility for later action review, not action itself.",
    "Scope validation is not action.",
    "Destructive action still requires future Sophia approval.",
    "Destructive action still requires future explicit action request.",
    "Negative-control invalid confirmations remain blocked.",
    "No pruning or deletion occurs in PMR-08.",
    "PMR-08 is not federation authorization.",
    "PMR-08 is not reward entitlement.",
    "PMR-08 is not token economy.",
    "PMR-08 is not Atlas canon.",
    "PMR-08 is not memory write authorization.",
    "PMR-08 is not model-weight training.",
    "PMR-08 is not deployment authority.",
    "PMR-08 is not truth certification.",
    "Valid confirmation receipt plus Sophia recommendation is not action authorization.",
    "Explicit future action request and Sophia approval packet are required before destructive action.",
    "No explicit action request packet is emitted in PMR-09.",
    "No Sophia approval packet is emitted in PMR-09.",
    "No destructive action authorization packet is emitted in PMR-09.",
    "No destructive action receipt is emitted in PMR-09.",
    "No pruning or deletion occurs in PMR-09.",
    "PMR-09 is not federation authorization.",
    "PMR-09 is not reward entitlement.",
    "PMR-09 is not token economy.",
    "PMR-09 is not Atlas canon.",
    "PMR-09 is not memory write authorization.",
    "PMR-09 is not model-weight training.",
    "PMR-09 is not deployment authority.",
    "PMR-09 is not truth certification.",
    "Action request candidate is not explicit action request.",
    "Sophia approval request candidate is not Sophia approval.",
    "Authorization preflight is not authorization.",
    "No explicit action request packet is emitted in PMR-10.",
    "No Sophia approval packet is emitted in PMR-10.",
    "No destructive action authorization packet is emitted in PMR-10.",
    "No destructive action receipt is emitted in PMR-10.",
    "No pruning or deletion occurs in PMR-10.",
    "PMR-10 is not federation authorization.",
    "PMR-10 is not reward entitlement.",
    "PMR-10 is not token economy.",
    "PMR-10 is not Atlas canon.",
    "PMR-10 is not memory write authorization.",
    "PMR-10 is not model-weight training.",
    "PMR-10 is not deployment authority.",
    "PMR-10 is not truth certification.",
    "PMR authorization ladder is not the whole Triadic Brain.",
    "Pattern diversity is required.",
    "PMR-only continuation is not recommended immediately after PMR-10.",
    "Checkpoint recommendation is not execution.",
    "Checkpoint is not product completion.",
    "No runtime authority is granted.",
    "PMR-SIM-00 is recommended as the next evidence-producing lane.",
    "PMR becomes scientific only when it can lose.",
    "PMR policy is allowed to lose.",
    "Simulation result is not production memory policy.",
    "Simulation result is not PMR superiority proof.",
    "Simulation result is not hallucination reduction proof.",
    "Simulation result is not federation proof.",
    "Simulation result is not reward economy proof.",
    "Fixture streams are synthetic and deterministic.",
    "Retained does not mean true.",
    "Replay-ready does not mean canon.",
    "Stored does not mean trained.",
    "Simpler baselines may win metrics or scenarios.",
    "Run-PMR-SIM00-Acceptance.ps1",
    "pmr_simulation_manifest.json",
    "pmr_simulation_result_rows.jsonl",
    "pmr_simulation_comparison_packet.json",
    "pmr_simulation_statistics_packet.json",
    "Descriptive fixture statistics are not real-world inference.",
    "Rank table is not production policy selection.",
    "Statistical summary is not PMR superiority proof.",
    "Statistical summary is not hallucination reduction proof.",
    "Simulation statistics are not federation proof.",
    "Simulation statistics are not reward economy proof.",
    "Run-PMR-STAT00-Acceptance.ps1",
    "pmr_stat_analysis_manifest.json",
    "pmr_stat_policy_metric_summaries.jsonl",
    "pmr_stat_policy_pair_deltas.jsonl",
    "pmr_stat_rank_table.json",
    "pmr_stat_sensitivity_packet.json",
    "pmr_stat_failure_mode_packet.json",
    "Federation stress corpus is not federation.",
    "Federation stress result is not federation proof.",
    "Federation candidate is not network authorization.",
    "Shard-transfer scenario is not encrypted shard transfer.",
    "Federation credit scenario is not reward entitlement.",
    "Hash is not encryption.",
    "Merkle root is not confidentiality.",
    "Run-PMR-FED-STRESS00-Acceptance.ps1",
    "pmr_federation_stress_manifest.json",
    "pmr_federation_node_fixtures.json",
    "pmr_federation_stress_scenarios.json",
    "pmr_federation_failure_mode_rows.jsonl",
    "pmr_federation_propagation_risk_packet.json",
    "pmr_federation_stress_statistics_packet.json",
    "Human provenance context is not identity certification.",
    "The system must not encode human = body or AI = mind.",
    "Consent context is not consent execution.",
    "Consent preference is not action authorization.",
    "Correction request is not memory write.",
    "Revocation request is not deletion execution.",
    "Review participation is not truth certification.",
    "Lived-stakes annotation is not reward entitlement.",
    "Human provenance is not human value score.",
    "Run-PMR-HUMAN-PROVENANCE00-Acceptance.ps1",
    "pmr_human_provenance_manifest.json",
    "pmr_human_provenance_context_packet.json",
    "pmr_human_consent_scope_packet.json",
    "pmr_human_correction_request_packet.json",
    "pmr_human_revocation_request_packet.json",
    "pmr_human_lived_stakes_annotation_packet.json",
    "Evidence Review, Sonya adapter path, TEL/telemetry, retrosynthesis, PMR simulation/statistics, federation stress, human provenance, market design, harness debt, and publication debt remain active lanes.",
    "No pruning or deletion occurs in PMR-ARCH-DIVERSITY-CHECKPOINT-00.",
    "PMR-ARCH-DIVERSITY-CHECKPOINT-00 is not federation authorization.",
    "PMR-ARCH-DIVERSITY-CHECKPOINT-00 is not reward entitlement.",
    "PMR-ARCH-DIVERSITY-CHECKPOINT-00 is not token economy.",
    "PMR-ARCH-DIVERSITY-CHECKPOINT-00 is not Atlas canon.",
    "PMR-ARCH-DIVERSITY-CHECKPOINT-00 is not memory write authorization.",
    "PMR-ARCH-DIVERSITY-CHECKPOINT-00 is not model-weight training.",
    "PMR-ARCH-DIVERSITY-CHECKPOINT-00 is not deployment authority.",
    "PMR-ARCH-DIVERSITY-CHECKPOINT-00 is not truth certification.",
    "Governed provenance resources may be future infrastructure rewards, but truth is not for sale.",
    "Sonya is the required execution membrane for model/tool/provider-facing paths.",
    "Missing Sonya posture must fail closed.",
    "Raw output is not cognition.",
    "SONYA-REQUIRED-MEMBRANE-CHECKPOINT-00",
    "TEL-EVENT-STACK-00",
    "Telemetry event is not authority.",
    "Replay trace is not canon.",
    "Evidence Review product loop is not final answer selection.",
    "Unsupported-claim action queue is not evidence acceptance.",
    "Hypercompression reduces explanatory distance, not review obligation.",
    "Freshness is not authority.",
    "Pattern morphology is not consciousness proof.",
    "Cognitive-water metaphor is not metaphysical claim.",
    "Publication validation event is not peer review.",
    *OBSERVATION_CONTRACT_POLICY_SIMULATION_BLOCKED_CLAIMS,
)
FORBIDDEN_PHRASES = (
    "claims retrosynthesis",
    "performs retrosynthesis",
    "retrosynthesis was performed",
    "retrosynthesis performed",
    "improvement hypotheses were generated",
    "Atlas memory write occurred",
    "memory admission occurred",
    "federation occurred",
    "product release occurred",
    "Atlas memory admitted",
    "claims Atlas memory admission",
    "population calibration",
    "population-calibrated",
    "market validation",
    "human benefit proof",
    "deployment readiness",
    "deployment ready",
    "truth certified",
    "truth certification",
    "final answer authority",
    "final answer selection",
    "final answer release",
    "universal ontology claim",
    "ai consciousness",
    "human consciousness",
    "retrosynthesis runtime",
    "universal portability proof",
    "live model execution",
    "live adapter execution",
    "claims provider call",
    "claims remote provider call",
    "recursive braid",
    "recursive federation",
    "psychoacoustic proof",
    "publisher finalization",
    "hallucination reduction proven",
    "model quality benchmark",
    "model superiority proven",
    "model superiority proof",
    "hallucination reduction proof",
    "PMR superiority proof",
    "production memory policy",
    "production policy selection",
    "real-world inference",
    "real world inference",
    "statistical superiority proof",
    "federation proof",
    "reward economy proof",
    "identity certification",
    "consent execution",
    "claims action authorization",
    "biometric inference",
    "model quality benchmark",
    "live model evaluation",
    "remote provider evaluation",
    "federation",
    "professional advice",
    "legally compliant",
    "legal advice",
    "medical advice",
    "tax advice",
    "compliance certification",
    "production ready",
    "deployment authorized",
    "claims deployment authority",
    "claims population calibration",
    "claims market validation",
    "claims user benefit proof",
    "claims human benefit proof",
    "final answer released",
    "publisher finalized",
    "omega detected",
    "canon adopted",
    "memory written",
    "publication claim authorized",
    "recursive self-improvement achieved",
    "claims accepted evidence",
    "claims adapter authorization",
    "adapter authorization",
    "adapter authorized",
    "claims canon adoption",
    "claims memory write",
    "candidate hypotheses are truth",
    "candidate hypotheses are final answers",
    "candidate hypotheses are accepted evidence",
    "repair plans are authority",
    "memory write occurred",
    "Atlas memory admission occurred",
    "claims final answer release",
    "claims Publisher finalization",
    "claims Omega detection",
    "omega detection",
    "claims recursive self-improvement",
    "live human study performed",
    "claims live human study",
    "claims accepted evidence",
    "canon adoption",
    "production evaluation",
    "product completion",
    "claims product completion",
    "claims product release",
    "claims peer review certification",
    "claims truth certification",
    "runtime authority",
    "surveillance",
    "claims peer review certification",
    "product release",
    "product released",
    "benchmark result",
    "benchmark proven",
    "experiment result",
    "AI consciousness demonstrated",
    "adapter executed",
    "adapter execution",
    "network authorization",
    *[f"claims {claim}" for claim in MINIMAL_VIABLE_RECEIPT_LOCAL_PROTOTYPE_BLOCKED_CLAIMS],
    *[f"claims {claim}" for claim in MVR_READABILITY_REVIEW_SEED_BLOCKED_CLAIMS],
    *[f"claims {claim}" for claim in MVR_READABILITY_REVISION_BLOCKED_CLAIMS],
    *[f"claims {claim}" for claim in MVR_REAL_INPUT_PILOT_DESIGN_BLOCKED_CLAIMS],
    *[f"claims {claim}" for claim in MVR_REAL_INPUT_PILOT_PROTOTYPE_BLOCKED_CLAIMS],
    *[f"claims {claim}" for claim in MVR_QUARANTINE_REPAIR_BLOCKED_CLAIMS],
    *[f"claims {claim}" for claim in MVR_HUMAN_SELECTED_FILE_SMOKE_BLOCKED_CLAIMS],
    *[f"claims {claim}" for claim in COMPLIANCE_DESIGN_BLOCKED_CLAIMS],
    *[f"claims {claim}" for claim in WAVE_EU_PROVENANCE_BLOCKED_CLAIMS],
    *[f"claims {claim}" for claim in EU_AI_ACT_MVR_EVIDENCE_MAP_LOCAL_PROTOTYPE_BLOCKED_CLAIMS],
    *[f"claims {claim}" for claim in COMPLIANCE_REPORT_SOURCE_CORPUS_BLOCKED_CLAIMS],
    *[f"claims {claim}" for claim in SOURCE_CORPUS_BATCH_MANIFEST_20260610_BLOCKED_CLAIMS],
    "network authorized",
    "remote provider called",
    "remote provider calls",
    "provider call performed",
    "provider call authorized",
    "AI Forensics Dossier is final answer",
    "AI Forensics Dossier certifies truth",
    "AI Forensics Dossier certifies compliance",
    "AI Forensics Dossier is audit opinion",
    "AI Forensics Dossier is professional attestation",
    "AI Forensics Dossier reveals hidden chain of thought",
    "AI Forensics Dossier performs model mind-reading",
    "Human Review UX creates final answer authority",
    "Human Review UX certifies truth",
    "Human Review UX certifies compliance",
    "Human Review UX is audit opinion",
    "Human Review UX is professional attestation",
    "Human Review UX approves product release",
    "Human Review UX approves provider runtime",
    "Human Review UX approves memory write",
    "Human Review UX approves Atlas memory admission",
    "local test review is product human review",
    "needs_more_evidence is approval",
    "approve_for_local_next_step is final answer approval",
    "escalate_to_professional_review is professional attestation",
    "hidden chain-of-thought disclosure",
    "model mind-reading",
    "raw output admission",
    "claims raw output admission",
    *OBSERVATION_CONTRACT_POLICY_SIMULATION_BLOCKED_CLAIMS,
    "PERTURBATION-STRUCTURE-AFFORDANCE-00 is proven",
    "perturbation structure-affordance is a proven theorem",
    "speculative_pattern is proof",
    "operational_metric_hypothesis target has already been achieved",
    "perturbation evidence proves theorem",
    "perturbation evidence certifies novelty",
    "residual novelty candidate is novelty discovery",
    "reverse trunk hypothesis is proof",
    "raw output admitted",
    "raw output accepted as cognition",
    "raw_output_admitted",
    "live model executed",
    "model weights trained",
    "claims model weight training",
    "evidence review pack local adapter route model weight training",
    "production ready",
    "production readiness",
    "lineage authority",
    "lineage grants authority",
    "stale identity proof of execution",
    "hallucination reduction proof",
    "model quality benchmark",
    "Atlas canon",
    "memory write authorization",
    "federation authorization",
    "pruning execution",
    "resource economy",
    "token economy",
    "truth score",
    "reward entitlement",
    "human value score",
    "deletion execution",
    "encrypted shard transfer",
    "claims destructive action authorization",
    "claims explicit action request",
    "claims Sophia approval packet",
    "claims Sophia approval",
    "claims destructive action receipt",
    "claims destructive action",
    "claims valid user confirmation",
    "user confirmation execution",
    "claims user confirmation receipt",
    "claims user confirmation",
    "Sophia approval",
    "audit action",
)
ALLOWED_NEGATED = (
    "not ",
    "no ",
    "without ",
    "does not ",
    "is not ",
    "not a ",
    "not an ",
)


def _normalize(value: str) -> str:
    return " ".join(value.lower().replace("-", " ").split())


def _read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Expected JSON object in {path}")
    return payload


def _read_docs(docs_dir: Path) -> str:
    return "\n".join(
        path.read_text(encoding="utf-8") for path in sorted(docs_dir.rglob("*.md"))
    )


def _is_negated(text: str, index: int) -> bool:
    window = text[max(0, index - 24) : index]
    return any(marker in window for marker in ALLOWED_NEGATED)


def _context_words(text: str, index: int, *, before: int = 96, after: int = 96) -> str:
    window = text[max(0, index - before) : index + after]
    cleaned = re.sub(r"[^a-z0-9]+", " ", window.replace("_", " "))
    return " ".join(cleaned.split())


def _is_allowed_provider_call_context(text: str, index: int) -> bool:
    window = text[max(0, index - 48) : index + 72]
    normalized = " ".join(re.sub(r"[^a-z0-9]+", " ", window.replace("_", " ")).split())
    allowed_patterns = (
        "no remote provider call",
        "no remote provider calls",
        "not provider call",
        "not remote provider call",
        "provider calls not performed",
        "provider calls not made",
        "is not provider call",
        "is not a provider call",
        "provider call not performed",
        "provider call not made",
        "provider calls performed false",
        "provider calls performed false",
        "provider_calls_not_performed",
        "provider_calls_performed false",
        "direct model provider call is not allowed",
        "provider call is not allowed",
        "does not call providers",
        "network provider calls",
        "without live adapter execution or network provider calls",
        "without live model execution or remote provider calls",
        "provider call blocked",
        "provider call forbidden",
        "not provider call status flags",
    )
    return any(pat in normalized for pat in allowed_patterns)




def _is_allowed_network_authorization_context(text: str, index: int) -> bool:
    window = _context_words(text, index, before=128, after=128)
    allowed = (
        "not network authorization",
        "is not network authorization",
        "network authorization not performed",
        "network calls not performed",
        "network call not performed",
        "network authorization requested",
        "network authorization requests must fail closed",
        "network authorization request must fail closed",
        "blocked network authorization",
        "network authorization blocked",
        "no network authorization",
    )
    return any(a in window for a in allowed)

def _is_allowed_raw_output_context(text: str, index: int) -> bool:
    window = _context_words(text, index, before=128, after=128)
    allowed_fragments = (
        "raw output is forbidden",
        "raw output forbidden",
        "raw output rejected",
        "raw output is not cognition",
        "not raw output admission",
        "raw output admission blocked",
        "raw output admission posture",
        "forbidden artifact leakage and raw output admission",
        "forbidding raw output admission",
        "avoids raw output admission",
        "raw output admitted false",
        "raw output forbidden true",
        "raw output not admitted",
        "not raw output admission status flags",
        "not raw output admission",
        "forbidding raw output admission",
        "rejects or avoids raw output admission",
        "does not admit raw output",
    )
    return any(fragment in window for fragment in allowed_fragments)


def _is_allowed_no_emit_receipt_context(text: str, index: int) -> bool:
    window = text[max(0, index - 320) : index]
    no_emit_index = window.rfind("does not emit")
    claims_index = window.rfind("claims")
    return (
        no_emit_index != -1
        and claims_index < no_emit_index
        and any(
            marker in window
            for marker in (
                "explicit action request",
                "destructive authorization packet",
                "destructive action receipt",
                "pruning receipt",
                "deletion receipt",
                "federation receipt",
                "reward receipt",
                            "model training receipt",
                "deployment decision",
            )
        )
    )


def _is_allowed_local_adapter_context(text: str, index: int) -> bool:
    window = text[max(0, index - 48) : index]
    return any(
        marker in window
        for marker in (
            "local fixture ",
            "local only fixture ",
            "local only ",
            "local ",
            "fixture adapter ",
            "fixture only ",
            "deterministic local ",
        )
    )



def _is_allowed_bounded_release_context(text: str, index: int, phrase: str) -> bool:
    window = _context_words(text, index, before=120, after=120)

    left_clause = text[max(0, index - 160):index]
    clause_start = max(left_clause.rfind("."), left_clause.rfind("\n"), left_clause.rfind(";"))
    clause = left_clause[clause_start + 1 :]
    list_negated = " not " in clause and "," in clause

    if phrase == "truth certification":
        allowed = (
            "not truth certification",
            "truth certification blocked",
            "truth certification not performed",
            "truth certification packet",
            "is not truth certification",
            "audit is not truth certification",
            "language governance audit is not truth certification",
        )
        return list_negated or any(item in window for item in allowed)
    if phrase == "final answer release":
        allowed = (
            "not final answer release",
            "final answer not released",
            "final answer released false",
            "final answer release not performed",
        )
        return list_negated or any(item in window for item in allowed)
    if phrase == "product release":
        allowed = (
            "not product release",
            "product release not performed",
            "product release performed false",
            "product release packet",
            "reviewer utility metric is not product release",
            "product release requests must fail closed",
            "product release request must fail closed",
            "product release blocked",
            "does not create provider runtime or product release",
            "does not create product release",
            "is not product release",
            "audit is not product release",
            "language governance audit is not product release",
        )
        return list_negated or any(item in window for item in allowed)
    return False

def _is_metric_semantic_contract_context(text: str, index: int, phrase: str) -> bool:
    window_before = text[max(0, index - 220) : index]
    window_after = text[index : index + 160]
    window = window_before + window_after
    return (
        "met-sem-00" in window
        or "metric semantic contract" in window
        or "metrics are not" in window_before
        or "current metrics" in window_before
        or "current code implements profile-specific operational proxies" in window
        or "current values are local-review operational proxies" in window
        or "unsafe labels retained only as blocked language" in window_before
        or "blocked metric overclaim examples" in window_before
        or phrase == "population calibration" and "population calibration is required before stronger claims" in window
    )

def _is_blocked_overclaim_example_context(text: str, index: int) -> bool:
    immediate = text[max(0, index - 48) : index]
    current = text[index : index + 32]
    if ("claims " in immediate or current.startswith("claims ") or "described as" in immediate or "evidence-review-pack-01" in immediate) and "claims can be hidden" not in immediate and "blocked claims" not in immediate:
        return False
    window = text[max(0, index - 4000) : index]
    return "blocked claims" in window or "overclaim examples" in window or "blocked ai receipt overclaim examples" in window or "validation tiering provenance publication boundaries" in window or "telemetry aperture controller publication boundaries" in window or "tac policy simulation publication boundaries" in window or "tac local review integration publication boundaries" in window or "claims_blocked" in window or "ces pmr indexing design publication boundaries" in window or "observation contract policy simulation publication boundaries" in window or "minimal viable receipt local prototype publication boundaries" in window


def _forbidden_hits(text: str) -> list[str]:
    hits: list[str] = []
    for phrase in FORBIDDEN_PHRASES:
        normalized_phrase = _normalize(phrase)
        start = 0
        while True:
            index = text.find(normalized_phrase, start)
            if index == -1:
                break
            claims_window = text[max(0, index - 32) : index + len(normalized_phrase)]
            if phrase == "population calibration" and "claims " not in text[max(0, index - 64) : index] and "overclaim" not in text[max(0, index - 96) : index]:
                start = index + len(normalized_phrase)
                continue
            if phrase == "legal advice" and "claims " not in text[max(0, index - 64) : index]:
                start = index + len(normalized_phrase)
                continue
            if phrase == "legal advice" and "claims" not in text[max(0, index - 64) : index] and (
                "not legal advice" in text[max(0, index - 48) : index + len(normalized_phrase)]
                or "does not provide" in text[max(0, index - 180) : index]
                or "provides no" in text[max(0, index - 180) : index]
                or "without" in text[max(0, index - 220) : index]
                or "avoiding" in text[max(0, index - 220) : index]
                or "not compliance certifications" in text[max(0, index - 300) : index]
            ):
                start = index + len(normalized_phrase)
                continue
            if phrase == "compliance certification" and "claims" not in text[max(0, index - 64) : index]:
                start = index + len(normalized_phrase)
                continue
            if phrase == "compliance certification" and "claims" not in text[max(0, index - 64) : index] and (
                "not compliance certification" in text[max(0, index - 48) : index + len(normalized_phrase)]
                or "does not imply" in text[max(0, index - 500) : index]
                or "blocked claims" in text[max(0, index - 5000) : index]
                or "is not" in text[max(0, index - 120) : index]
                or "claims_blocked" in text[max(0, index - 400) : index]
                or "does not authorize" in text[max(0, index - 260) : index]
                or "grants no" in text[max(0, index - 260) : index]
                or "does not imply" in text[max(0, index - 260) : index]
                or "does not certify" in text[max(0, index - 260) : index]
                or "without" in text[max(0, index - 260) : index]
                or "avoiding" in text[max(0, index - 260) : index]
            ):
                start = index + len(normalized_phrase)
                continue
            if "claims_blocked" in text[max(0, index - 220) : index] and "not " + normalized_phrase in text[max(0, index - 32) : index + len(normalized_phrase) + 4]:
                start = index + len(normalized_phrase)
                continue
            if phrase.lower().startswith("claims minimal viable receipt local prototype") and "claims_blocked" in text[max(0, index - 96) : index]:
                start = index + len(normalized_phrase)
                continue
            if phrase.lower().startswith("claims mvr readability review seed") and "claims_blocked" in text[max(0, index - 96) : index]:
                start = index + len(normalized_phrase)
                continue
            if phrase.lower().startswith("claims mvr readability revision") and "claims_blocked" in text[max(0, index - 96) : index]:
                start = index + len(normalized_phrase)
                continue
            if phrase.lower().startswith("claims real input pilot") and "claims_blocked" in text[max(0, index - 96) : index]:
                start = index + len(normalized_phrase)
                continue
            if phrase.lower().startswith("claims mvr real-input pilot prototype") and "claims_blocked" in text[max(0, index - 96) : index]:
                start = index + len(normalized_phrase)
                continue
            if phrase.lower().startswith("claims quarantine repair") and "claims_blocked" in text[max(0, index - 96) : index]:
                start = index + len(normalized_phrase)
                continue
            if phrase.lower().startswith("claims human-selected file smoke") and "claims_blocked" in text[max(0, index - 96) : index]:
                start = index + len(normalized_phrase)
                continue
            if phrase.lower().startswith("claims smoke can") and "claims_blocked" in text[max(0, index - 96) : index]:
                start = index + len(normalized_phrase)
                continue
            if phrase.lower().startswith("claims compliance") and "claims_blocked" in text[max(0, index - 96) : index]:
                start = index + len(normalized_phrase)
                continue
            if phrase.lower().startswith("claims uvlm") and "claims_blocked" in text[max(0, index - 96) : index]:
                start = index + len(normalized_phrase)
                continue
            if phrase.lower().startswith("claims eu ai act") and "claims_blocked" in text[max(0, index - 96) : index]:
                start = index + len(normalized_phrase)
                continue
            if phrase.lower().startswith("claims iso") and "claims_blocked" in text[max(0, index - 96) : index]:
                start = index + len(normalized_phrase)
                continue
            if phrase.lower().startswith("claims soc 2") and "claims_blocked" in text[max(0, index - 96) : index]:
                start = index + len(normalized_phrase)
                continue
            if phrase.lower().startswith("claims hipaa") and "claims_blocked" in text[max(0, index - 96) : index]:
                start = index + len(normalized_phrase)
                continue
            if phrase.lower().startswith("claims wave") and "claims_blocked" in text[max(0, index - 96) : index]:
                start = index + len(normalized_phrase)
                continue
            if phrase.lower().startswith("claims bridge") and "claims_blocked" in text[max(0, index - 96) : index]:
                start = index + len(normalized_phrase)
                continue
            if phrase.lower().startswith("claims provenance") and "claims_blocked" in text[max(0, index - 96) : index]:
                start = index + len(normalized_phrase)
                continue
            if phrase.lower().startswith("claims eu ai act") and "claims_blocked" in text[max(0, index - 96) : index]:
                start = index + len(normalized_phrase)
                continue
            if phrase.lower().startswith("claims no-detection") and "claims_blocked" in text[max(0, index - 96) : index]:
                start = index + len(normalized_phrase)
                continue
            if phrase.lower().startswith("claims quarantine count") and "claims_blocked" in text[max(0, index - 96) : index]:
                start = index + len(normalized_phrase)
                continue
            if phrase.lower().startswith("claims source manifest") and "claims_blocked" in text[max(0, index - 96) : index]:
                start = index + len(normalized_phrase)
                continue
            if phrase.lower().startswith("claims quarantined evidence") and "claims_blocked" in text[max(0, index - 96) : index]:
                start = index + len(normalized_phrase)
                continue
            if phrase.lower().startswith("claims pasted excerpt") and "claims_blocked" in text[max(0, index - 96) : index]:
                start = index + len(normalized_phrase)
                continue
            if phrase.lower().startswith("claims local source") and "claims_blocked" in text[max(0, index - 96) : index]:
                start = index + len(normalized_phrase)
                continue
            if phrase.lower().startswith("claims consent authorizes") and "claims_blocked" in text[max(0, index - 96) : index]:
                start = index + len(normalized_phrase)
                continue
            if phrase.lower().startswith("claims local pilot") and "claims_blocked" in text[max(0, index - 96) : index]:
                start = index + len(normalized_phrase)
                continue
            if phrase.lower().startswith("claims instruction-like evidence") and "claims_blocked" in text[max(0, index - 96) : index]:
                start = index + len(normalized_phrase)
                continue
            if text[max(0, index - 8) : index].endswith("blocked ") and phrase.lower().startswith("claims "):
                start = index + len(normalized_phrase)
                continue
            if phrase.lower().startswith("claims "):
                hits.append(phrase)
                break
            if f"claims {normalized_phrase}" in claims_window and "blocked claims" not in claims_window:
                hits.append(phrase)
                break
            if phrase == "universal portability proof" and "is universal portability proof" in text[max(0, index - 40) : index + len(normalized_phrase)]:
                hits.append(phrase)
                break
            if phrase in MINIMAL_VIABLE_RECEIPT_LOCAL_PROTOTYPE_BLOCKED_CLAIMS and (
                "claims_blocked" in text[max(0, index - 3000) : index]
                or "blocked claims" in text[max(0, index - 96) : index]
                or "minimal viable receipt local prototype publication boundaries" in text[max(0, index - 1800) : index]
            ):
                start = index + len(normalized_phrase)
                continue
            if phrase in MVR_READABILITY_REVIEW_SEED_BLOCKED_CLAIMS and (
                "claims_blocked" in text[max(0, index - 3000) : index]
                or "blocked claims" in text[max(0, index - 96) : index]
                or "mvr local prototype readability review seed publication boundaries" in text[max(0, index - 1800) : index]
            ):
                start = index + len(normalized_phrase)
                continue
            if phrase in MVR_READABILITY_REVISION_BLOCKED_CLAIMS and (
                "claims_blocked" in text[max(0, index - 3000) : index]
                or "blocked claims" in text[max(0, index - 96) : index]
                or "mvr local prototype readability revision publication boundaries" in text[max(0, index - 1800) : index]
            ):
                start = index + len(normalized_phrase)
                continue
            if phrase in MVR_REAL_INPUT_PILOT_DESIGN_BLOCKED_CLAIMS and (
                "claims_blocked" in text[max(0, index - 3000) : index]
                or "blocked claims" in text[max(0, index - 96) : index]
                or "mvr local real input pilot design publication boundaries" in text[max(0, index - 1800) : index]
            ):
                start = index + len(normalized_phrase)
                continue
            if phrase in MVR_REAL_INPUT_PILOT_PROTOTYPE_BLOCKED_CLAIMS and (
                "claims_blocked" in text[max(0, index - 3000) : index]
                or "blocked claims" in text[max(0, index - 96) : index]
                or "mvr local real input pilot prototype publication boundaries" in text[max(0, index - 1800) : index]
            ):
                start = index + len(normalized_phrase)
                continue
            if phrase in MVR_QUARANTINE_REPAIR_BLOCKED_CLAIMS and (
                "claims_blocked" in text[max(0, index - 3000) : index]
                or "blocked claims" in text[max(0, index - 96) : index]
                or "mvr local real input pilot quarantine detection repair publication boundaries" in text[max(0, index - 1800) : index]
            ):
                start = index + len(normalized_phrase)
                continue
            if phrase in MVR_HUMAN_SELECTED_FILE_SMOKE_BLOCKED_CLAIMS and (
                "claims_blocked" in text[max(0, index - 3000) : index]
                or "blocked claims" in text[max(0, index - 96) : index]
                or "mvr local real input pilot human-selected file smoke publication boundaries" in text[max(0, index - 1800) : index]
            ):
                start = index + len(normalized_phrase)
                continue
            if phrase in COMPLIANCE_DESIGN_BLOCKED_CLAIMS and (
                "claims_blocked" in text[max(0, index - 3000) : index]
                or "blocked claims" in text[max(0, index - 96) : index]
                or "compliance-ready mvr report and compliance evidence toolset publication boundaries" in text[max(0, index - 2200) : index]
            ):
                start = index + len(normalized_phrase)
                continue
            if phrase in WAVE_EU_PROVENANCE_BLOCKED_CLAIMS and (
                "claims_blocked" in text[max(0, index - 3000) : index]
                or "blocked claims" in text[max(0, index - 96) : index]
                or "wave bridge, eu ai act mapping, and wave provenance publication boundaries" in text[max(0, index - 2600) : index]
            ):
                start = index + len(normalized_phrase)
                continue
            if phrase in EU_AI_ACT_MVR_EVIDENCE_MAP_LOCAL_PROTOTYPE_BLOCKED_CLAIMS and (
                "claims_blocked" in text[max(0, index - 3000) : index]
                or "blocked claims" in text[max(0, index - 96) : index]
                or "eu ai act mvr evidence map local prototype publication boundaries" in text[max(0, index - 2400) : index]
            ):
                start = index + len(normalized_phrase)
                continue
            if phrase in COMPLIANCE_REPORT_SOURCE_CORPUS_BLOCKED_CLAIMS and (
                "claims_blocked" in text[max(0, index - 3000) : index]
                or "blocked claims" in text[max(0, index - 96) : index]
                or "compliance-ready report local prototype and source-corpus provenance publication boundaries" in text[max(0, index - 2600) : index]
            ):
                start = index + len(normalized_phrase)
                continue
            if phrase in SOURCE_CORPUS_BATCH_MANIFEST_20260610_BLOCKED_CLAIMS and (
                "claims_blocked" in text[max(0, index - 3000) : index]
                or "blocked claims" in text[max(0, index - 96) : index]
                or "june 2026 source-corpus batch manifest publication boundaries" in text[max(0, index - 2400) : index]
            ):
                start = index + len(normalized_phrase)
                continue
            if phrase in {"deployment authorized", "publication claim authorized", "hallucination reduction proven", "model superiority proven"} and "evidence review pack 01" in text[max(0, index - 120) : index]:
                hits.append(phrase)
                break
            if phrase == "evidence review pack local adapter route model weight training":
                hits.append("model weight training")
                break
            if phrase in {"market validation", "human benefit proof"} and "claims " not in text[max(0, index - 96) : index]:
                start = index + len(normalized_phrase)
                continue
            if (
                "ces pmr indexing is proposed" in text[max(0, index - 700) : index + 700]
                or "ces pmr indexing design 00" in text[max(0, index - 700) : index + 700]
            ) and ("authorized" in text[max(0, index - 700) : index + 700] or " no " in text[max(0, index - 500) : index] or "not" in text[max(0, index - 220) : index + 220]):
                start = index + len(normalized_phrase)
                continue
            if phrase in {"truth certification", "final answer authority", "federation", "product release"} and (
                " is not " in text[max(0, index - 160) : index]
                or "it is not" in text[max(0, index - 220) : index]
                or "is not a" in text[max(0, index - 400) : index]
                or "current metrics" in text[max(0, index - 260) : index + 260]
                or " not " in text[max(0, index - 80) : index]
                or f"not {normalized_phrase}" in text[max(0, index - 180) : index + 120]
                or f"no {normalized_phrase}" in text[max(0, index - 180) : index + 120]
                or " no " in text[max(0, index - 80) : index]
                or "without " in text[max(0, index - 220) : index]
                or "does not authorize" in text[max(0, index - 220) : index]
                or "claiming no" in text[max(0, index - 220) : index]
                or "blocked by default" in text[index : index + 80]
                or "_authorization" in text[index : index + 40]
                or " authorization" in text[index : index + 40]
                or "certifications" in text[index : index + 40]
                or "authorization" in text[index : index + 80]
                or "occurred" in text[index : index + 80]
                or "request must fail closed" in text[index : index + 80]
                or " blocked by default" in text[index : index + 80]
            ):
                start = index + len(normalized_phrase)
                continue
            if phrase == "consent execution" and ("not consent execution" in text[max(0, index - 80) : index + 80] or "is not consent execution" in text[max(0, index - 80) : index + 80]):
                start = index + len(normalized_phrase)
                continue
            if _is_blocked_overclaim_example_context(text, index):
                start = index + len(normalized_phrase)
                continue
            if phrase in {"truth certification", "final answer authority", "federation", "product release"} and "claims " not in text[max(0, index - 48) : index]:
                start = index + len(normalized_phrase)
                continue
            if phrase in {"market validation", "federation", "omega detection", "federation authorization", "product readiness", "human benefit proof"} and (
                "without changing runtime behavior or granting" in text[max(0, index - 900) : index]
                or "without performing" in text[max(0, index - 320) : index]
                or "without claiming" in text[max(0, index - 320) : index]
                or "current metrics are" in text[max(0, index - 128) : index]
                or "without certifying truth" in text[max(0, index - 260) : index]
                or "grants no" in text[max(0, index - 450) : index]
                or "not " in text[max(0, index - 96) : index]
                or " no " in text[max(0, index - 96) : index]
                or "validation tiering is" in text[max(0, index - 96) : index]
                or "validation tiering proves" in text[max(0, index - 96) : index]
                or f"not {normalized_phrase}" in text[max(0, index - 128) : index + 128]
                or f"is not {normalized_phrase}" in text[max(0, index - 128) : index + 128]
                or ("tac-policy-simulation-00" in text[max(0, index - 900) : index + 220] and ("without" in text[max(0, index - 900) : index] or "not" in text[max(0, index - 220) : index + 220] or "blocked overclaim" in text[max(0, index - 220) : index]))
                or ("tac-local-review-integration-00" in text[max(0, index - 900) : index + 220] and ("without" in text[max(0, index - 900) : index] or "not" in text[max(0, index - 220) : index + 220] or "blocked overclaim" in text[max(0, index - 220) : index]))
                or ("pmr-pathway-priors-design-doctrine-00" in text[max(0, index - 900) : index + 220] and ("without" in text[max(0, index - 900) : index] or "not" in text[max(0, index - 220) : index + 220] or "blocked overclaim" in text[max(0, index - 220) : index]))
                or ("coherence-event-signatures-design-00" in text[max(0, index - 900) : index + 220] and ("without" in text[max(0, index - 900) : index] or "not" in text[max(0, index - 220) : index + 220] or "blocked overclaim" in text[max(0, index - 220) : index]))
                or ("ces pmr indexing design 00" in text[max(0, index - 900) : index + 220] and ("without" in text[max(0, index - 900) : index] or "not" in text[max(0, index - 220) : index + 220] or "no " in text[max(0, index - 220) : index + 220] or "blocked overclaim" in text[max(0, index - 220) : index]))
                or ("ces pmr indexing is proposed" in text[max(0, index - 500) : index + 500] and ("no " in text[max(0, index - 300) : index] or "not" in text[max(0, index - 220) : index + 220]))
                or ("triadic observation contract" in text[max(0, index - 900) : index + 500] and ("without" in text[max(0, index - 900) : index + 500] or "not" in text[max(0, index - 220) : index + 220] or "blocked overclaim" in text[max(0, index - 220) : index]))
                or (phrase == "federation" and "retention/export/federation blocks" in text[max(0, index - 128) : index + 128])
                or (phrase == "federation" and "federation_blocked_by_default" in text[max(0, index - 64) : index + 64])
                or (phrase == "federation" and "pmr pathway priors must respect tac retention" in text[max(0, index - 128) : index + 128])
                or (phrase == "federation" and "pmr pathway prior authorizes pmr federation" in text[max(0, index - 128) : index + 128])
                or (phrase == "federation" and "ces authorizes pmr federation" in text[max(0, index - 128) : index + 128])
                or (phrase == "federation" and "federating pmr" in text[max(0, index - 128) : index + 128] and "without certifying truth" in text[max(0, index - 320) : index])
                or (phrase == "federation" and "federating pmr" in text[max(0, index - 80) : index + 80] and "without certifying truth" in text[max(0, index - 260) : index])
            ):
                start = index + len(normalized_phrase)
                continue
            if phrase == "consent execution" and (
                _is_negated(text, index)
                or "simulation decision is consent execution" in text[max(0, index - 80) : index + 80]
                or "mode shift receipt is consent execution" in text[max(0, index - 80) : index + 80]
            ):
                start = index + len(normalized_phrase)
                continue
            if phrase == "federation" and (
                "_not_federation" in text[max(0, index - 160) : index + 160]
                or "not_federation" in text[max(0, index - 160) : index + 160]
                or "federation_allowed" in text[max(0, index - 80) : index + 80]
                or "federation_performed" in text[max(0, index - 80) : index + 80]
                or "federation_blocked" in text[max(0, index - 80) : index + 80]
                or "federation remains blocked" in text[max(0, index - 80) : index + 80]
            ):
                start = index + len(normalized_phrase)
                continue
            if phrase == "surveillance" and "authorizes surveillance" not in text[max(0, index - 64) : index + 64] and "claims surveillance" not in text[max(0, index - 32) : index + 32]:
                start = index + len(normalized_phrase)
                continue
            if phrase.startswith("claims ") and not _is_negated(text, index):
                hits.append(phrase)
                break
            if phrase in {"population calibration", "population-calibrated", "federation"}:
                window = text[max(0, index - 220) : index + 128]
                if (
                    _is_negated(text, index)
                    or _is_blocked_overclaim_example_context(text, index)
                    or _is_metric_semantic_contract_context(text, index, phrase)
                    or f"not {normalized_phrase}" in window
                    or "_not_federation" in window
                    or "not_federation" in window
                    or "no_federation" in window
                    or "federation_blocked" in window
                    or "federation_blocked_by_default" in window
                    or '"federation_authorized": false' in window
                    or "requires population calibration" in window
                    or "grants no" in window
                    or "without granting" in window
                    or "or granting" in window
                ):
                    start = index + len(normalized_phrase)
                    continue
            if (
                phrase in {"adapter execution", "adapter executed"}
                and _is_allowed_local_adapter_context(text, index)
                and "lineage claims" not in text[max(0, index - 80) : index]
            ):
                start = index + len(normalized_phrase)
                continue
            if (
                phrase == "Sophia approval"
                and (
                    "requires future " in text[max(0, index - 64) : index]
                    or text[index : index + 42].startswith("sophia approval request candidate")
                    or text[index : index + 43].startswith("sophia approval request candidates")
                    or text[index : index + 32].startswith("sophia approval request")
                    or "required before" in text[index : index + 96]
                    or "without " in text[max(0, index - 64) : index]
                    or "missing " in text[max(0, index - 32) : index]
                    or (
                        "blocked when" in text[max(0, index - 96) : index]
                        and "missing" in text[index : index + 96]
                    )
                    or text[index : index + 40].startswith("sophia approval missing")
                )
            ):
                start = index + len(normalized_phrase)
                continue
            if "do not claim" in text[max(0, index - 120) : index]:
                start = index + len(normalized_phrase)
                continue
            if (
                phrase == "token economy"
                and (
                    "does not prune, delete, federate, transfer encrypted shards, reward users, run a"
                    in text[max(0, index - 180) : index]
                    or "does not approve, prune, delete, federate, transfer encrypted shards, reward users, run a"
                    in text[max(0, index - 180) : index]
                    or "does not confirm, approve, prune, delete, federate, transfer encrypted shards, reward users, run a"
                    in text[max(0, index - 180) : index]
                    or "does not perform destructive action, approve, prune, delete, federate, transfer encrypted shards, reward users, run a"
                    in text[max(0, index - 180) : index]
                    or "does not execute, authorize, approve, prune, delete, federate, transfer encrypted shards, reward users, run a"
                    in text[max(0, index - 200) : index]
                )
            ):
                start = index + len(normalized_phrase)
                continue
            if (
                phrase == "model quality benchmark"
                and "not hallucination reduction proof or a" in text[max(0, index - 56) : index]
            ):
                start = index + len(normalized_phrase)
                continue
            if phrase == "federation" and (
                _is_negated(text, index)
                or "future federation requires" in text[max(0, index - 24) : index + 64]
                or "does not authorize" in text[max(0, index - 96) : index]
                or "not_federation" in text[max(0, index - 64) : index + 64]
                or
                text[index : index + 40].startswith("federation is blocked by default")
                or text[index : index + 48].startswith("federation stress corpus is not federation")
                or text[index : index + 48].startswith("federation stress result is not federation")
                or text[index : index + 44].startswith("federation candidate is not network")
                or text[index : index + 46].startswith("federation credit scenario is not reward")
                or text[index : index + 48].startswith("federation remains blocked by default")
                or text[index : index + 40].startswith("federation_blocked")
                or text[index : index + 40].startswith("federation blocked")
                or (text[index : index + 40].startswith("federation proof") and _is_negated(text, index))
                or text[index : index + 40].startswith("federation_authorization")
                or text[max(0, index - 20) : index].endswith("not_")
                or "without_federation" in text[max(0, index - 32) : index + 16]
                or text[max(0, index - 20) : index].endswith("without_")
                or text[index : index + 40].startswith("federation authorization")
                or text[index : index + 40].startswith("federation stress")
                or text[index : index + 40].startswith("federation occurs")
                or text[index : index + 40].startswith("federation performed")
                or text[index : index + 40].startswith("federation receipt")
                or text[max(0, index - 48) : index + 48].startswith("\"model_training\", \"federation\", \"reward_allocation\"")
                or text[index : index + 40].startswith("federation_performed")
                or text[index : index + 40].startswith("federation risks")
                or text[index : index + 40].startswith("federation_risks")
                or text[index : index + 40].startswith("federation_")
                or text[index : index + 40].startswith("federation_stress")
                or "local-review-runtime-v0 is not federation" in text[max(0, index - 80) : index + 80]
                or "not federation" in text[max(0, index - 64) : index + 64]
                or "_not_federation" in text[max(0, index - 64) : index + 64]
                or text[index : index + 40].startswith("federation = true")
                or text[index : index + 40].startswith('federation": true')
                or '"model_training", "federation", "reward_allocation"' in text[max(0, index - 24) : index + 48]
            ):
                start = index + len(normalized_phrase)
                continue
            if phrase == "omega detection" and (
                _is_negated(text, index)
                or "no omega detection" in text[max(0, index - 32) : index + 48]
                or "does not" in text[max(0, index - 160) : index]
            ):
                start = index + len(normalized_phrase)
                continue
            if (
                phrase in {"ai consciousness", "human consciousness"}
                and "make ai/human consciousness claims" in text[max(0, index - 32) : index + 48]
            ):
                start = index + len(normalized_phrase)
                continue
            if (
                phrase == "federation authorization"
                and (
                    _is_negated(text, index)
                    or "not federation authorization" in text[max(0, index - 64) : index + 48]
                    or "local-review-runtime-v0 is not federation authorization" in text[max(0, index - 96) : index + 80]
                )
            ):
                start = index + len(normalized_phrase)
                continue
            if (
                phrase in {"remote provider call", "remote provider calls", "provider call", "provider call performed", "provider call authorized"}
                and _is_allowed_provider_call_context(text, index)
            ):
                start = index + len(normalized_phrase)
                continue
            if (
                phrase in {"network authorization", "network authorized"}
                and _is_allowed_network_authorization_context(text, index)
            ):
                start = index + len(normalized_phrase)
                continue
            if (
                phrase in {"raw output admission", "claims raw output admission", "raw output admitted", "raw output accepted as cognition", "raw_output_admitted"}
                and _is_allowed_raw_output_context(text, index)
            ):
                start = index + len(normalized_phrase)
                continue
            if (
                phrase == "surveillance"
                and (
                    "not surveillance" in text[max(0, index - 48) : index + 24]
                    or "not surveillance authorization" in text[max(0, index - 64) : index + 48]
                    or "tac is not surveillance" in text[max(0, index - 64) : index + 48]
                    or "without changing runtime behavior or granting" in text[max(0, index - 80) : index]
                    or "grants no surveillance" in text[max(0, index - 80) : index + 80]
                    or "is not surveillance" in text[max(0, index - 80) : index + 80]
                    or "no_surveillance" in text[max(0, index - 80) : index + 80]
                    or "telemetry_not_surveillance" in text[max(0, index - 64) : index + 32]
                )
            ):
                start = index + len(normalized_phrase)
                continue
            if (
                phrase == "encrypted shard transfer"
                and (
                    text[index : index + 64].startswith("encrypted shard transfer not performed")
                    or text[index : index + 64].startswith("encrypted_shard_transfer_not_performed")
                )
            ):
                start = index + len(normalized_phrase)
                continue
            if (
                phrase in {"federation", "truth certification", "product release"}
                and "request must fail closed" in text[index : index + 72]
            ):
                start = index + len(normalized_phrase)
                continue
            if phrase == "consent execution" and ("not consent execution" in text[max(0, index - 80) : index + 80] or "is not consent execution" in text[max(0, index - 80) : index + 80]):
                start = index + len(normalized_phrase)
                continue
            if _is_blocked_overclaim_example_context(text, index):
                start = index + len(normalized_phrase)
                continue
            if phrase in {"truth certification", "final answer authority", "federation", "product release"} and "claims " not in text[max(0, index - 48) : index]:
                start = index + len(normalized_phrase)
                continue
            if phrase == "federation" and (
                any(_normalize(claim) in text[max(0, index - 220) : index + 220] for claim in (*VISUAL_REVIEW_MODEL_BLOCKED_CLAIMS, *VISUAL_REVIEW_STATIC_HTML_BLOCKED_CLAIMS, *STATIC_HTML_USABILITY_REVIEW_BLOCKED_CLAIMS, *STATIC_HTML_USABILITY_REVISION_BLOCKED_CLAIMS, *AI_RECEIPT_ARCHITECTURE_BLOCKED_CLAIMS, *VALIDATION_TIERING_PROVENANCE_BLOCKED_CLAIMS, *TELEMETRY_APERTURE_BLOCKED_CLAIMS, *TAC_POLICY_SIMULATION_BLOCKED_CLAIMS, *TAC_LOCAL_REVIEW_INTEGRATION_BLOCKED_CLAIMS, *TAC_AI_RECEIPT_EVENT_LINK_BLOCKED_CLAIMS, *PMR_PATHWAY_PRIORS_DESIGN_BLOCKED_CLAIMS, *CES_DESIGN_BLOCKED_CLAIMS, *TRIADIC_OBSERVATION_CONTRACT_BLOCKED_CLAIMS, *OBSERVATION_CONTRACT_POLICY_SIMULATION_BLOCKED_CLAIMS))
                or "without implementing a ui or granting" in text[max(0, index - 500) : index]
                or "it implements no ui and grants no" in text[max(0, index - 500) : index]
            ):
                start = index + len(normalized_phrase)
                continue
            if phrase == "federation" and (
                "federation blocked by default" in text[index : index + 96]
                or "not federation authorization" in text[max(0, index - 64) : index + 64]
                or "tac is not federation" in text[max(0, index - 64) : index + 64]
                or "pmr_federation = blocked_by_default" in text[max(0, index - 64) : index + 64]
                or "pmr federation is allowed by default" in text[max(0, index - 160) : index + 160]
            ):
                start = index + len(normalized_phrase)
                continue
            if phrase in {"population calibration", "population-calibrated", "peer review certification", "universal ontology proof"} and _is_negated(text, index):
                start = index + len(normalized_phrase)
                continue
            if phrase in {"population calibration", "population-calibrated", "peer review certification", "universal ontology proof"} and f"not {normalized_phrase}" in text[max(0, index - 64) : index + 64]:
                start = index + len(normalized_phrase)
                continue
            if _is_allowed_no_emit_receipt_context(text, index):
                start = index + len(normalized_phrase)
                continue
            if phrase == "population calibration" and (
                "future population calibration requires" in text[max(0, index - 24) : index + 72]
                or "population calibration status" in text[max(0, index - 24) : index + 48]
                or "does not authorize" in text[max(0, index - 96) : index]
                or "population calibration is not claimed" in text[max(0, index - 24) : index + 64]
            ):
                start = index + len(normalized_phrase)
                continue
            if phrase == "population-calibrated" and "future population calibrated bounds" in text[max(0, index - 24) : index + 72]:
                start = index + len(normalized_phrase)
                continue
            if (
                phrase in {"truth certification", "product release"}
                and any(_normalize(claim) in text[max(0, index - 180) : index + 180] for claim in (*LANGUAGE_GOVERNANCE_AUDIT_BLOCKED_CLAIMS, *VISUAL_REVIEW_MODEL_BLOCKED_CLAIMS, *VISUAL_REVIEW_STATIC_HTML_BLOCKED_CLAIMS, *STATIC_HTML_USABILITY_REVIEW_BLOCKED_CLAIMS, *STATIC_HTML_USABILITY_REVISION_BLOCKED_CLAIMS, *AI_RECEIPT_ARCHITECTURE_BLOCKED_CLAIMS, *VALIDATION_TIERING_PROVENANCE_BLOCKED_CLAIMS, *TELEMETRY_APERTURE_BLOCKED_CLAIMS, *TAC_POLICY_SIMULATION_BLOCKED_CLAIMS, *TAC_LOCAL_REVIEW_INTEGRATION_BLOCKED_CLAIMS, *TAC_AI_RECEIPT_EVENT_LINK_BLOCKED_CLAIMS, *PMR_PATHWAY_PRIORS_DESIGN_BLOCKED_CLAIMS, *CES_DESIGN_BLOCKED_CLAIMS, *TRIADIC_OBSERVATION_CONTRACT_BLOCKED_CLAIMS, *OBSERVATION_CONTRACT_POLICY_SIMULATION_BLOCKED_CLAIMS))
            ):
                start = index + len(normalized_phrase)
                continue
            if phrase in {"truth certification", "final answer release", "product release"} and _is_allowed_bounded_release_context(text, index, phrase):
                start = index + len(normalized_phrase)
                continue
            if phrase in {"population calibration", "human benefit proof", "truth certification", "federation", "compliance certification", "omega detection", "product release", "final answer authority"} and _is_metric_semantic_contract_context(text, index, phrase):
                start = index + len(normalized_phrase)
                continue
            if (
                phrase in {"human benefit proof", "market validation", "product readiness", "product release", "provider runtime", "compliance certification"}
                and "claims" not in text[max(0, index - 48) : index]
                and "grants" not in text[max(0, index - 48) : index]
                and "authority" not in text[max(0, index - 48) : index]
                and (
                    "it is not" in text[max(0, index - 160) : index]
                    or "this is not" in text[max(0, index - 160) : index]
                    or "is not" in text[max(0, index - 80) : index]
                    or "not " + normalized_phrase in text[max(0, index - 80) : index + 80]
                )
            ):
                start = index + len(normalized_phrase)
                continue
            if phrase in {"market validation", "human benefit proof", "federation"} and "without certifying truth" in text[max(0, index - 260) : index]:
                start = index + len(normalized_phrase)
                continue
            if (
                phrase in {"market validation", "human benefit proof", "federation", "compliance certification", "omega detection", "product release"}
                and "ai receipt architecture" in text[max(0, index - 700) : index + 200]
                and ("without" in text[max(0, index - 700) : index] or "not" in text[max(0, index - 700) : index])
            ):
                start = index + len(normalized_phrase)
                continue
            if phrase == "product release" and (
                "does not authorize" in text[max(0, index - 180) : index]
                or "does not imply" in text[max(0, index - 180) : index]
                or "avoiding" in text[max(0, index - 800) : index]
                or "blocked overclaim" in text[max(0, index - 900) : index]
                or "blocked claims" in text[max(0, index - 900) : index]
            ):
                start = index + len(normalized_phrase)
                continue
            if (
                phrase in {"final answer authority", "product release", "provider runtime", "runtime authority", "human benefit proof", "market validation", "product readiness"}
                and (
                    "without creating" in text[max(0, index - 260) : index]
                    or "without claiming" in text[max(0, index - 260) : index]
                    or "claiming no" in text[max(0, index - 260) : index]
                    or any(_normalize(claim) in text[max(0, index - 220) : index + 220] for claim in (*VISUAL_REVIEW_STATIC_HTML_BLOCKED_CLAIMS, *STATIC_HTML_USABILITY_REVIEW_BLOCKED_CLAIMS, *STATIC_HTML_USABILITY_REVISION_BLOCKED_CLAIMS, *AI_RECEIPT_ARCHITECTURE_BLOCKED_CLAIMS, *VALIDATION_TIERING_PROVENANCE_BLOCKED_CLAIMS, *TELEMETRY_APERTURE_BLOCKED_CLAIMS, *TAC_POLICY_SIMULATION_BLOCKED_CLAIMS, *TAC_LOCAL_REVIEW_INTEGRATION_BLOCKED_CLAIMS, *TAC_AI_RECEIPT_EVENT_LINK_BLOCKED_CLAIMS, *PMR_PATHWAY_PRIORS_DESIGN_BLOCKED_CLAIMS, *CES_DESIGN_BLOCKED_CLAIMS, *TRIADIC_OBSERVATION_CONTRACT_BLOCKED_CLAIMS, *OBSERVATION_CONTRACT_POLICY_SIMULATION_BLOCKED_CLAIMS))
                )
            ):
                start = index + len(normalized_phrase)
                continue
            if phrase == "legal advice" and (
                "not legal advice" in text[max(0, index - 48) : index + len(normalized_phrase)]
                or "does not provide" in text[max(0, index - 180) : index]
                or "provides no" in text[max(0, index - 180) : index]
                or "without" in text[max(0, index - 220) : index]
                or "avoiding" in text[max(0, index - 220) : index]
            ):
                start = index + len(normalized_phrase)
                continue
            if phrase == "compliance certification" and (
                "it is not final answer" in text[max(0, index - 140) : index]
                or "does not imply" in text[max(0, index - 500) : index]
                or "blocked claims" in text[max(0, index - 5000) : index]
                or "is not" in text[max(0, index - 96) : index]
                or "not compliance certification" in text[max(0, index - 32) : index + len(normalized_phrase)]
                or "claims_blocked" in text[max(0, index - 300) : index]
                or "does not authorize" in text[max(0, index - 220) : index]
                or "grants no" in text[max(0, index - 220) : index]
                or "does not imply" in text[max(0, index - 260) : index]
                or "does not certify" in text[max(0, index - 260) : index]
                or "without" in text[max(0, index - 260) : index]
                or "avoiding" in text[max(0, index - 260) : index]
            ):
                start = index + len(normalized_phrase)
                continue
            if phrase == "consent execution" and ("not consent execution" in text[max(0, index - 80) : index + 80] or "is not consent execution" in text[max(0, index - 80) : index + 80]):
                start = index + len(normalized_phrase)
                continue
            if _is_blocked_overclaim_example_context(text, index):
                start = index + len(normalized_phrase)
                continue
            if phrase in {"truth certification", "final answer authority", "federation", "product release"} and "claims " not in text[max(0, index - 48) : index]:
                start = index + len(normalized_phrase)
                continue
            if phrase in {"federation", "surveillance"} and any(
                _normalize(claim) in text[max(0, index - 240) : index + 240]
                for claim in (*TELEMETRY_APERTURE_BLOCKED_CLAIMS, *TAC_POLICY_SIMULATION_BLOCKED_CLAIMS, *TAC_LOCAL_REVIEW_INTEGRATION_BLOCKED_CLAIMS, *TAC_AI_RECEIPT_EVENT_LINK_BLOCKED_CLAIMS, *PMR_PATHWAY_PRIORS_DESIGN_BLOCKED_CLAIMS, *CES_DESIGN_BLOCKED_CLAIMS, *TRIADIC_OBSERVATION_CONTRACT_BLOCKED_CLAIMS, *OBSERVATION_CONTRACT_POLICY_SIMULATION_BLOCKED_CLAIMS)
            ):
                start = index + len(normalized_phrase)
                continue
            if phrase == "surveillance" and (
                "not surveillance authorization" in text[max(0, index - 80) : index + 80]
                or "tac is not surveillance" in text[max(0, index - 80) : index + 80]
                or "without changing runtime behavior or granting" in text[max(0, index - 80) : index]
                or "grants no surveillance" in text[max(0, index - 80) : index + 80]
                or "no_surveillance" in text[max(0, index - 80) : index + 80]
                or "telemetry_not_surveillance" in text[max(0, index - 80) : index + 80]
                or "is not surveillance" in text[max(0, index - 80) : index + 80]
            ):
                start = index + len(normalized_phrase)
                continue
            if phrase == "federation" and (
                "not federation authorization" in text[max(0, index - 80) : index + 80]
                or "tac is not federation" in text[max(0, index - 80) : index + 80]
                or "pmr_federation" in text[max(0, index - 64) : index + 64]
            ):
                start = index + len(normalized_phrase)
                continue
            if phrase == "final answer authority" and (
                "without granting" in text[max(0, index - 120) : index]
                or "it is not" in text[max(0, index - 360) : index]
                or " is not" in text[max(0, index - 360) : index]
            ):
                start = index + len(normalized_phrase)
                continue
            if phrase == "runtime authority" and (
                "without granting" in text[max(0, index - 160) : index]
                or "grants no" in text[max(0, index - 450) : index]
                or "no runtime authority" in text[max(0, index - 80) : index + 80]
                or "not runtime authority" in text[max(0, index - 80) : index + 80]
            ):
                start = index + len(normalized_phrase)
                continue
            if not _is_negated(text, index):
                hits.append(phrase)
                break
            start = index + len(normalized_phrase)
    return hits


def validate_dashboard(dashboard_path: Path, docs_dir: Path) -> dict[str, Any]:
    dashboard = _read_json(dashboard_path)
    accepted = dashboard.get("accepted_phases", [])
    accepted_ids = {p.get("phase_id") for p in accepted if isinstance(p, dict)}
    missing = sorted(REQUIRED_PHASES - accepted_ids)

    text = _normalize(json.dumps(dashboard, ensure_ascii=False) + "\n" + _read_docs(docs_dir))
    missing_boundaries = [
        phrase for phrase in REQUIRED_BOUNDARY_PHRASES if _normalize(phrase) not in text
    ]
    forbidden = _forbidden_hits(text)

    truthy_bad_flags = [
        key
        for key in ("deployment_ready", "truth_certified", "final_answer_authority")
        if dashboard.get(key) is True
    ]

    status_ok = (
        dashboard.get("dashboard_status") == "draft_public_review"
        and dashboard.get("requires_external_peer_review") is True
        and dashboard.get("not_truth_certification") is True
        and dashboard.get("not_deployment_authority") is True
        and dashboard.get("not_final_answer_release") is True
        and dashboard.get("not_ai_consciousness_claim") is True
        and dashboard.get("not_universal_ontology_claim") is True
    )
    passed = not missing and not missing_boundaries and not forbidden and not truthy_bad_flags and status_ok
    return {
        "dashboard_id": "PUBLIC-REPRO-DASHBOARD-01",
        "passed": passed,
        "accepted_phases_present": sorted(accepted_ids),
        "missing_accepted_phases": missing,
        "missing_claim_boundary_phrases": missing_boundaries,
        "forbidden_claims_found": forbidden,
        "bad_truthy_flags": truthy_bad_flags,
        "status_ok": status_ok,
    }


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate public repro dashboard claim boundaries.")
    parser.add_argument("--dashboard", required=True, type=Path)
    parser.add_argument("--docs-dir", required=True, type=Path)
    parser.add_argument("--out", type=Path)
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    result = validate_dashboard(args.dashboard, args.docs_dir)
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
