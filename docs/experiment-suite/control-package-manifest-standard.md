# Control Package Manifest Standard

CONTROL-PACKAGE-MANIFEST-STANDARD-00 synchronizes the design-only control package manifest standard into publication dashboards. This is publication/dashboard synchronization only and grants no runtime authority.

## Bounded allowed claim

CONTROL-PACKAGE-MANIFEST-STANDARD-00 defines a design-only manifest standard for installable Triadic Brain control packages, framework evidence packs, ingress packages, report/export packages, and review workflow packages, including package identity, authorship, licensing, entitlement model, free/paid/public-good status, dependencies, compatible core versions, emitted artifacts, schemas, control objectives, framework mappings, data-access requirements, retention behavior, human review requirements, source provenance references, installation/activation states, and non-authority boundaries, without implementing payment, subscriptions, remote marketplace installs, runtime package execution, compliance certification, legal advice, audit pass, attestation success, product readiness, product release, truth certification, final-answer authority, accepted-evidence authority, memory write, Atlas admission, trace export, PMR federation, provider runtime, or network calls.

## Dashboard summary

- policy_status = active_design_only
- package_standard_status = active_design_only
- runtime_package_install_enabled = false
- remote_marketplace_enabled = false
- subscription_billing_enabled = false
- package_execution_enabled = false
- runtime_behavior_changed = false
- product_release_performed = false
- product_readiness_claimed = false
- compliance_certification_emitted = false
- legal_advice_emitted = false
- audit_pass_claimed = false
- attestation_success_claimed = false
- final_answer_authority_granted = false
- accepted_evidence_authority_granted = false
- truth_certification_emitted = false
- memory_write_performed = false
- atlas_memory_admission_performed = false
- trace_export_performed = false
- pmr_federation_performed = false
- provider_runtime_performed = false
- network_call_performed = false
- package_types = 9
- package_families = 33
- manifest_fields = 30
- example_packages = 8

## Package types

- core_platform_package
- control_package
- framework_evidence_pack
- ingress_package
- report_export_package
- review_workflow_package
- public_good_package
- enterprise_package
- author_contributed_package

## Package families

- ai_receipt_gateway_core
- minimal_viable_receipt_core
- source_manifest_hash_core
- non_authority_boundary_core
- artifact_inventory_export_core
- local_file_ingress
- pasted_excerpt_ingress
- api_proxy_ingress
- sdk_wrapper_ingress
- browser_extension_ingress
- saas_connector_ingress
- model_gateway_ingress
- observation_contract_control
- telemetry_aperture_control
- prompt_injection_quarantine_control
- unsupported_claims_register
- retention_boundary_control
- contestability_recovery_control
- human_review_signoff_control
- incident_forensic_dossier_control
- pmr_recall_control
- eu_ai_act_evidence_support_pack
- nist_ai_rmf_evidence_pack
- iso_iec_42001_aims_evidence_pack
- soc2_ai_governance_evidence_pack
- hipaa_ai_governance_evidence_pack
- coso_ai_control_evidence_pack
- owasp_genai_security_evidence_pack
- compliance_ready_mvr_report_pack
- executive_summary_pack
- evidence_index_csv_pack
- machine_readable_json_evidence_pack
- forensic_dossier_export_pack

## Manifest fields

- package_id
- package_name
- package_type
- package_family
- package_version
- author_owner
- license_id
- license_url
- entitlement_model
- free_or_paid_status
- public_good_status
- commercial_entitlement_required
- subscription_eligible
- local_install_supported
- remote_install_supported_future_only
- dependencies
- compatible_core_versions
- emitted_artifacts
- schemas_added
- control_objectives
- framework_mappings
- data_access_required
- retention_behavior
- connector_scope_required
- human_review_required
- authorized_professional_signoff_required_for_compliance_use
- source_provenance_refs
- non_authority_boundaries
- installation_status
- activation_status

## Entitlement models

- free_core
- public_good_free
- paid_single_package
- paid_framework_pack
- enterprise_subscription
- author_contributed_free
- author_contributed_commercial
- restricted_internal
- future_marketplace

## Installation states

- not_installed
- installed_disabled
- installed_enabled
- dependency_missing
- incompatible_core_version
- license_required
- entitlement_required
- retired
- revoked

## Activation states

- inactive
- active_design_only
- active_local_runtime
- active_subscription_required
- blocked_by_policy
- blocked_by_missing_dependency
- blocked_by_license
- future_only

## Data-access categories

- no_data_access
- explicit_local_file_only
- pasted_excerpt_only
- configured_api_proxy
- configured_connector_scope
- directory_scope_requires_policy
- hidden_file_access_forbidden
- provider_network_access_forbidden_by_default

## Retention categories

- no_raw_retention
- hash_only
- summary_only
- explicit_retention_scope_required
- customer_managed_retention
- export_only
- future_policy_managed_retention

## Example packages

- ai_receipt_gateway_core_free
- minimal_viable_receipt_core_free
- eu_ai_act_evidence_support_pack_paid
- prompt_injection_quarantine_control_paid
- source_manifest_hash_core_public_good
- compliance_ready_mvr_report_pack_paid
- local_file_ingress_free_or_core
- human_review_signoff_control_enterprise

## Doctrine language

- Control Package Manifest Standard
- Triadic Brain Core is the governed substrate.
- Controls ship as installable packages.
- Customers should pay for the controls and framework packs they need.
- Some packages may be free or public-good when licensed or donated by authoring owners.
- Package installation is not control effectiveness.
- Package availability is not compliance.
- Package activation is not audit pass.
- Framework evidence packs are evidence support, not certification.
- Human review remains required.
- Authorized professional signoff remains required for compliance use.
- Package authorship and license terms must be explicit.
- Data-access requirements must be visible before activation.
- Retention behavior must be visible before activation.
- Non-authority boundaries must travel with the package.
- CONTROL-PACKAGE-MANIFEST-STANDARD-00 does not implement payment.
- CONTROL-PACKAGE-MANIFEST-STANDARD-00 does not implement remote marketplace installs.
- CONTROL-PACKAGE-MANIFEST-STANDARD-00 does not activate packages at runtime.

## Non-authority guardrails

- package_installation_is_not_control_effectiveness
- package_installation_is_not_compliance
- package_activation_is_not_audit_pass
- framework_pack_is_not_certification
- evidence_pack_is_not_legal_advice
- package_manifest_is_not_product_release
- package_manifest_is_not_product_readiness
- package_manifest_is_not_truth_certification
- package_manifest_is_not_final_answer_authority
- package_manifest_is_not_accepted_evidence_authority
- package_manifest_does_not_write_memory
- package_manifest_does_not_admit_atlas_memory
- package_manifest_does_not_export_traces
- package_manifest_does_not_federate_pmr
- human_review_required

## Env-isolation repair language

- CONTROL-PACKAGE-MANIFEST-STANDARD-ENV-ISOLATION-REPAIR-00 narrows forbidden-artifact validation to avoid failing on local generated developer workspace artifacts.
- Runtime artifact emission is tested in runtime/prototype phases via explicit bridge output checks.
- CONTROL-PACKAGE-MANIFEST-STANDARD-00 remains design-only after the repair.
- The repair does not enable payment, marketplace, package execution, provider/network calls, memory, Atlas, export, federation, compliance/legal/audit/product/authority behavior.

## Relation to prior phases

- AI-RECEIPT-GATEWAY-LOCAL-INGRESS-PROTOTYPE-00 provides the local explicit-ingress prototype.
- COMPLIANCE-REPORT-PRESENTATION-STANDARD-00 defines report presentation constraints.
- COMPLIANCE-EVIDENCE-TOOLSET-LIBRARY-DESIGN-00 defines compliance evidence toolsets.
- SOURCE-CORPUS-PROVENANCE-ARCHIVE-00 defines provenance archive practices.
- CONTROL-PACKAGE-MANIFEST-STANDARD-00 defines package metadata and boundaries.
- CONTROL-PACKAGE-MANIFEST-STANDARD-ENV-ISOLATION-REPAIR-00 repairs validation isolation only.


## Artifact references

- docs/CONTROL_PACKAGE_MANIFEST_STANDARD.md
- config/packages/control_package_manifest_standard.v1.json
- schema/bridge/control_package_manifest.schema.json
- schema/bridge/control_package_entitlement_profile.schema.json
- schema/bridge/control_package_dependency_profile.schema.json
- schema/bridge/control_package_non_authority_boundary.schema.json
- python/tests/product/test_control_package_manifest_standard.py

## Blocked claims

- package installation means control effectiveness
- package installation means compliance
- package activation passes audit
- framework evidence pack certifies compliance
- evidence pack provides legal advice
- package manifest proves product readiness
- package manifest releases product
- package manifest certifies truth
- package manifest grants accepted-evidence authority
- package manifest authorizes final answers
- package manifest writes memory
- package manifest admits Atlas memory
- package manifest exports traces
- package manifest federates PMR
- free package means public domain
- author contributed means unrestricted commercial use
- subscription eligible means billing is implemented
- marketplace ready means marketplace exists
- package available means customer is entitled
- control package manifest standard implements payment
- control package manifest standard activates packages at runtime
- control package manifest standard enables marketplace installs

## Reproducibility

- test_control_package_manifest_standard.py
- control_package_manifest_standard.v1.json
- `python -m pytest -q python/tests/product/test_control_package_manifest_standard.py tests/test_experiment_registry.py`

## Runtime authority boundary

Publication sync grants no runtime authority. It does not imply payment implementation, subscription billing, remote marketplace availability, runtime package install, package execution, package activation, provider runtime, network calls, memory writes, Atlas memory admission, trace export, PMR federation, compliance certification, legal advice, audit pass, attestation success, product readiness, product release, truth certification, final-answer authority, accepted-evidence authority, model training, review skipping, or customer entitlement.

## Control package registry design publication sync

CONTROL-PACKAGE-REGISTRY-DESIGN-00 records package availability and state only. It does not install, activate, or execute packages; does not implement payment, subscriptions, or marketplace downloads; and grants no customer entitlement, compliance, legal, audit, product, truth, final-answer, accepted-evidence, memory, Atlas, export, federation, provider, or network authority.

- CONTROL-PACKAGE-MANIFEST-STANDARD-00 defines package metadata and boundaries.
- CONTROL-PACKAGE-MANIFEST-STANDARD-ENV-ISOLATION-REPAIR-00 repairs validation isolation only.
- CONTROL-PACKAGE-REGISTRY-DESIGN-00 records package availability and state.
- AI-RECEIPT-GATEWAY-LOCAL-INGRESS-PROTOTYPE-00 provides the local explicit-ingress prototype.
- COMPLIANCE-EVIDENCE-TOOLSET-LIBRARY-DESIGN-00 defines compliance evidence toolsets.

## Control package install simulation publication sync

CONTROL-PACKAGE-INSTALL-SIMULATION-00 rehearses package state transitions only. It does not install, activate, execute, download, bill, entitle, prove control effectiveness, certify compliance, pass audit, release product, certify truth, write memory, admit Atlas memory, export traces, federate PMR, authorize final answers, or grant accepted-evidence authority.

- CONTROL-PACKAGE-MANIFEST-STANDARD-00 defines package metadata and boundaries.
- CONTROL-PACKAGE-REGISTRY-DESIGN-00 records package availability and state.
- CONTROL-PACKAGE-INSTALL-SIMULATION-00 simulates package state transitions.
- AI-RECEIPT-GATEWAY-LOCAL-INGRESS-PROTOTYPE-00 provides the local explicit-ingress prototype.
- COMPLIANCE-EVIDENCE-TOOLSET-LIBRARY-DESIGN-00 defines compliance evidence toolsets.

## Catalog bundle and pricing/release provenance publication sync

CONTROL-PACKAGE-CATALOG-BUNDLE-DESIGN-00 groups packages into customer-facing bundles without implementing payment, subscriptions, marketplace downloads, customer entitlement, install, activation, execution, compliance, audit, product release, product readiness, or authority. SOURCE-CORPUS-PRICING-RELEASE-REPORTS-BATCH-2026-06-12-00 preserves pricing/release strategy reports as hash-only provenance, and SOURCE-CORPUS-PRICING-RELEASE-REPORTS-BATCH-SCHEMA-REPAIR-00 repairs schema validation only.

- CONTROL-PACKAGE-MANIFEST-STANDARD-00 defines package metadata and boundaries.
- CONTROL-PACKAGE-REGISTRY-DESIGN-00 records package availability and state.
- CONTROL-PACKAGE-INSTALL-SIMULATION-00 simulates package state transitions.
- CONTROL-PACKAGE-CATALOG-BUNDLE-DESIGN-00 groups packages into customer-facing bundles.
- SOURCE-CORPUS-PRICING-RELEASE-REPORTS-BATCH-2026-06-12-00 preserves pricing/release strategy provenance.
- SOURCE-CORPUS-PRICING-RELEASE-REPORTS-BATCH-SCHEMA-REPAIR-00 repairs schema validation for the source batch.
- AI-RECEIPT-GATEWAY-LOCAL-INGRESS-PROTOTYPE-00 provides the local explicit-ingress prototype.

## Product Readiness Roadmap Matrix sync

PRODUCT-READINESS-ROADMAP-MATRIX-00 applies PRODUCT-MATURITY-LABEL-TAXONOMY-00 maturity labels to product roadmap rows. Roadmap matrix is planning evidence, not product readiness. Roadmap matrix is not product release. Roadmap matrix is not customer entitlement. Roadmap matrix is not compliance certification. Roadmap matrix is not audit pass. Live-bounded-local rows are locally validated for bounded scope only, not generally available. Design-only rows do not enable runtime behavior. Simulation-only rows rehearse behavior but do not perform real behavior. Future rows are not implemented. Out-of-scope rows are intentionally excluded. Human review remains required. Authorized professional signoff remains required for compliance use. Publication sync grants no runtime authority.

## Product Maturity Label Taxonomy sync

PRODUCT-MATURITY-LABEL-TAXONOMY-00 defines maturity labels for product surfaces. Maturity labels prevent design drift. A maturity label is not product readiness. A maturity label is not product release. A maturity label is not compliance certification. A maturity label is not audit pass. A maturity label is not customer entitlement. Live means locally implemented and validated for its bounded scope, not generally released. Near-ready means implementation is substantially complete but still requires review, polish, integration, or pilot evidence. Design-only means policy/config/docs/schemas/tests exist, but runtime behavior is not enabled. Simulation-only means behavior is rehearsed with fixtures or state-transition simulation, not performed for real. Future means intentionally planned but not implemented. Out-of-scope means intentionally excluded. Human review remains required. Authorized professional signoff remains required for compliance use. Publication sync grants no runtime authority.
