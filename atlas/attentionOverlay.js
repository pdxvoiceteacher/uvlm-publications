function asArray(value) {
  return Array.isArray(value) ? value : [];
}

function normalizeCanonicalAttention(attentionUpdates, sophiaAttentionState) {
  const canonical = asArray(attentionUpdates?.conceptAttention);
  if (canonical.length > 0) {
    return canonical
      .map((entry, idx) => ({
        id: entry?.id,
        rank: Number(entry?.rank ?? idx + 1),
        weight: Number(entry?.weight ?? 0),
        reason: entry?.reason ?? null
      }))
      .filter((entry) => typeof entry.id === 'string')
      .sort((a, b) => a.rank - b.rank || b.weight - a.weight || a.id.localeCompare(b.id));
  }

  return asArray(sophiaAttentionState?.attention?.concepts)
    .map((entry, idx) => ({
      id: entry?.id,
      rank: idx + 1,
      weight: Number(entry?.weight ?? 0),
      reason: null
    }))
    .filter((entry) => typeof entry.id === 'string');
}

function rankingIndex(entries) {
  const max = Math.max(1, entries.length - 1);
  const byId = new Map();
  entries.forEach((entry, idx) => {
    const normalizedRankWeight = 1 - idx / max;
    byId.set(entry.id, {
      rank: entry.rank,
      attentionWeight: Number.isFinite(entry.weight) ? entry.weight : 0,
      attentionRankWeight: Number.isFinite(normalizedRankWeight) ? normalizedRankWeight : 0,
      attentionReason: entry.reason
    });
  });
  return byId;
}

export async function loadAttentionOverlay() {
  const [
    attentionUpdatesResp,
    coherenceAssessmentResp,
    sophiaRecommendationsResp,
    coherenceWeightsResp,
    sophiaAnnotationsResp,
    sophiaAttentionStateResp,
    sonyaMemoryIndexResp,
    sonyaAttentionCandidatesResp,
    reasoningThreadsResp,
    cognitiveWatchlistResp,
    cognitiveMonitorIndexResp,
    cognitiveStabilityAnnotationsResp,
    recursiveWatchHistoryResp,
    multimodalSignalIndexResp,
    patternDonationAnnotationsResp,
    crossModalAttentionOverlaysResp,
    patternDonationWatchlistResp,
    reviewDocketResp,
    promotionWatchQueueResp,
    governanceReviewDocketResp,
    reviewerIntegrityAnnotationsResp,
    reviewerWatchQueueResp,
    reviewerBehaviorMonitorResp,
    constitutionalStatusResp,
    continuityModeIndexResp,
    constitutionalAnnotationsResp,
    governanceFailureWatchlistResp,
    deliberationDocketResp,
    amendmentQueueResp,
    quorumWatchlistResp,
    constitutionalRevisionAnnotationsResp,
    continuityRosterResp,
    successionDocketResp,
    quorumResilienceWatchlistResp,
    governanceRedundancyAnnotationsResp,
    escrowIndexResp,
    recoveryDocketResp,
    integrityWatchlistResp,
    recoveryAnnotationsResp,
    attestationRegistryResp,
    witnessDocketResp,
    integrityTestimonyWatchlistResp,
    attestationAnnotationsResp,
    precedentRegistryResp,
    caseDocketResp,
    divergenceWatchlistResp,
    precedentAnnotationsResp,
    scenarioRegistryResp,
    stressTestDocketResp,
    resilienceFindingsWatchlistResp,
    scenarioAnnotationsResp,
    institutionalStatusResp,
    systemHealthDashboardResp,
    institutionalConflictWatchlistResp,
    institutionalAnnotationsResp,
    queueHealthDashboardResp,
    reviewBacklogWatchlistResp,
    metricGamingWatchlistResp,
    loadSheddingAnnotationsResp,
    priorityDashboardResp,
    triageDocketResp,
    triageWatchlistResp,
    priorityAnnotationsResp,
    closureRegistryResp,
    repairDocketResp,
    reopenedCaseWatchlistResp,
    closureAnnotationsResp,
    symbolicFieldRegistryResp,
    earlyWarningDashboardResp,
    regimeWatchlistResp,
    symbolicFieldAnnotationsResp,
    verificationDashboardResp,
    entityWatchlistResp,
    claimTypeRegistryResp,
    verificationAnnotationsResp,
    publicRecordDashboardResp,
    entityGraphRegistryResp,
    relationshipWatchlistResp,
    chainOfCustodyAnnotationsResp,
    investigationDashboardResp,
    investigationPlanRegistryResp,
    investigationWatchlistResp,
    investigationAnnotationsResp,
    authorityGateDashboardResp,
    weakEvidenceWatchlistResp,
    propagationAnnotationsResp,
    maturityRestrictionRegistryResp,
    reviewPacketDashboardResp,
    reviewPacketRegistryResp,
    uncertaintyWatchlistResp,
    reviewPacketAnnotationsResp,
    patternDashboardResp,
    patternRegistryResp,
    patternWatchlistResp,
    patternAnnotationsResp,
    patternTimelineDashboardResp,
    patternPersistenceRegistryResp,
    patternTemporalWatchlistResp,
    patternTemporalAnnotationsResp,
    causalDashboardResp,
    mechanismRegistryResp,
    causalWatchlistResp,
    causalAnnotationsResp,
    collaborativeReviewDashboardResp,
    consensusRegistryResp,
    dissentWatchlistResp,
    deliberationAnnotationsResp,
    telemetryDashboardResp,
    latticeProjectionRegistryResp,
    actionFunctionalAnnotationsResp,
    branchDashboardResp,
    branchRegistryResp,
    branchWatchlistResp,
    branchAnnotationsResp,
    predictionDashboardResp,
    forecastRegistryResp,
    predictionWatchlistResp,
    calibrationAnnotationsResp,
    experimentDashboardResp,
    hypothesisRegistryResp,
    falsificationWatchlistResp,
    theoryGateAnnotationsResp,
    theoryDashboardResp,
    theoryRegistryResp,
    negativeResultWatchlistResp,
    theoryAnnotationsResp,
    agencyModeDashboardResp,
    agencyFitRegistryResp,
    agencyDisagreementWatchlistResp,
    agencyGovernanceAnnotationsResp,
    responsibilityDashboardResp,
    supportRegistryResp,
    interventionWatchlistResp,
    responsibilityAnnotationsResp,
    transferDashboardResp,
    theoryTransferRegistryResp,
    transferWatchlistResp,
    transferAnnotationsResp,
    systemForecastDashboardResp,
    regimeTransitionRegistryResp,
    trajectoryWatchlistResp,
    systemForecastAnnotationsResp,
    uncertaintyDashboardResp,
    observationPriorityRegistryResp,
    curiosityWatchlistResp,
    curiosityAnnotationsResp,
    valueDashboardResp,
    knowledgePriorityRegistryResp,
    valueRiskWatchlistResp,
    valueAnnotationsResp,
    metaDashboardResp,
    reasoningPerformanceRegistryResp,
    metaWatchlistResp,
    metaAnnotationsResp,
    architectureDashboardResp,
    modulePerformanceRegistryResp,
    architectureWatchlistResp,
    architectureAnnotationsResp,
    socialEntropyDashboardResp,
    civicCohesionRegistryResp,
    legitimacyWatchlistResp,
    socialRepairAnnotationsResp,
    federationDashboardResp,
    stewardshipRegistryResp,
    captureWatchlistResp,
    federationAnnotationsResp,
    emergentDomainDashboardResp,
    domainBirthRegistryResp,
    domainBoundaryWatchlistResp,
    emergentDomainAnnotationsResp
  ] = await Promise.all([
    fetch('../bridge/attention_updates.json').catch(() => null),
    fetch('../bridge/coherence_assessment.json').catch(() => null),
    fetch('../bridge/sophia_recommendations.json').catch(() => null),
    fetch('../registry/coherence_weights.json').catch(() => null),
    fetch('../registry/sophia_annotations.json').catch(() => null),
    fetch('../registry/sophia_attention_state.json').catch(() => null),
    fetch('../registry/sonya_memory_index.json').catch(() => null),
    fetch('../registry/sonya_attention_candidates.json').catch(() => null),
    fetch('../registry/reasoning_threads.json').catch(() => null),
    fetch('../registry/cognitive_watchlist.json').catch(() => null),
    fetch('../registry/cognitive_monitor_index.json').catch(() => null),
    fetch('../registry/cognitive_stability_annotations.json').catch(() => null),
    fetch('../registry/recursive_watch_history.json').catch(() => null),
    fetch('../registry/multimodal_signal_index.json').catch(() => null),
    fetch('../registry/pattern_donation_annotations.json').catch(() => null),
    fetch('../registry/cross_modal_attention_overlays.json').catch(() => null),
    fetch('../registry/pattern_donation_watchlist.json').catch(() => null),
    fetch('../registry/review_docket.json').catch(() => null),
    fetch('../registry/promotion_watch_queue.json').catch(() => null),
    fetch('../registry/governance_review_docket.json').catch(() => null),
    fetch('../registry/reviewer_integrity_annotations.json').catch(() => null),
    fetch('../registry/reviewer_watch_queue.json').catch(() => null),
    fetch('../registry/reviewer_behavior_monitor.json').catch(() => null),
    fetch('../registry/constitutional_status.json').catch(() => null),
    fetch('../registry/continuity_mode_index.json').catch(() => null),
    fetch('../registry/constitutional_annotations.json').catch(() => null),
    fetch('../registry/governance_failure_watchlist.json').catch(() => null),
    fetch('../registry/deliberation_docket.json').catch(() => null),
    fetch('../registry/amendment_queue.json').catch(() => null),
    fetch('../registry/quorum_watchlist.json').catch(() => null),
    fetch('../registry/constitutional_revision_annotations.json').catch(() => null),
    fetch('../registry/continuity_roster.json').catch(() => null),
    fetch('../registry/succession_docket.json').catch(() => null),
    fetch('../registry/quorum_resilience_watchlist.json').catch(() => null),
    fetch('../registry/governance_redundancy_annotations.json').catch(() => null),
    fetch('../registry/escrow_index.json').catch(() => null),
    fetch('../registry/recovery_docket.json').catch(() => null),
    fetch('../registry/integrity_watchlist.json').catch(() => null),
    fetch('../registry/recovery_annotations.json').catch(() => null),
    fetch('../registry/attestation_registry.json').catch(() => null),
    fetch('../registry/witness_docket.json').catch(() => null),
    fetch('../registry/integrity_testimony_watchlist.json').catch(() => null),
    fetch('../registry/attestation_annotations.json').catch(() => null),
    fetch('../registry/precedent_registry.json').catch(() => null),
    fetch('../registry/case_docket.json').catch(() => null),
    fetch('../registry/divergence_watchlist.json').catch(() => null),
    fetch('../registry/precedent_annotations.json').catch(() => null),
    fetch('../registry/scenario_registry.json').catch(() => null),
    fetch('../registry/stress_test_docket.json').catch(() => null),
    fetch('../registry/resilience_findings_watchlist.json').catch(() => null),
    fetch('../registry/scenario_annotations.json').catch(() => null),
    fetch('../registry/institutional_status.json').catch(() => null),
    fetch('../registry/system_health_dashboard.json').catch(() => null),
    fetch('../registry/institutional_conflict_watchlist.json').catch(() => null),
    fetch('../registry/institutional_annotations.json').catch(() => null),
    fetch('../registry/queue_health_dashboard.json').catch(() => null),
    fetch('../registry/review_backlog_watchlist.json').catch(() => null),
    fetch('../registry/metric_gaming_watchlist.json').catch(() => null),
    fetch('../registry/load_shedding_annotations.json').catch(() => null),
    fetch('../registry/priority_dashboard.json').catch(() => null),
    fetch('../registry/triage_docket.json').catch(() => null),
    fetch('../registry/triage_watchlist.json').catch(() => null),
    fetch('../registry/priority_annotations.json').catch(() => null),
    fetch('../registry/closure_registry.json').catch(() => null),
    fetch('../registry/repair_docket.json').catch(() => null),
    fetch('../registry/reopened_case_watchlist.json').catch(() => null),
    fetch('../registry/closure_annotations.json').catch(() => null),
    fetch('../registry/symbolic_field_registry.json').catch(() => null),
    fetch('../registry/early_warning_dashboard.json').catch(() => null),
    fetch('../registry/regime_watchlist.json').catch(() => null),
    fetch('../registry/symbolic_field_annotations.json').catch(() => null),
    fetch('../registry/verification_dashboard.json').catch(() => null),
    fetch('../registry/entity_watchlist.json').catch(() => null),
    fetch('../registry/claim_type_registry.json').catch(() => null),
    fetch('../registry/verification_annotations.json').catch(() => null),
    fetch('../registry/public_record_dashboard.json').catch(() => null),
    fetch('../registry/entity_graph_registry.json').catch(() => null),
    fetch('../registry/relationship_watchlist.json').catch(() => null),
    fetch('../registry/chain_of_custody_annotations.json').catch(() => null),
    fetch('../registry/investigation_dashboard.json').catch(() => null),
    fetch('../registry/investigation_plan_registry.json').catch(() => null),
    fetch('../registry/investigation_watchlist.json').catch(() => null),
    fetch('../registry/investigation_annotations.json').catch(() => null),
    fetch('../registry/authority_gate_dashboard.json').catch(() => null),
    fetch('../registry/weak_evidence_watchlist.json').catch(() => null),
    fetch('../registry/propagation_annotations.json').catch(() => null),
    fetch('../registry/maturity_restriction_registry.json').catch(() => null),
    fetch('../registry/review_packet_dashboard.json').catch(() => null),
    fetch('../registry/review_packet_registry.json').catch(() => null),
    fetch('../registry/uncertainty_watchlist.json').catch(() => null),
    fetch('../registry/review_packet_annotations.json').catch(() => null),
    fetch('../registry/pattern_dashboard.json').catch(() => null),
    fetch('../registry/pattern_registry.json').catch(() => null),
    fetch('../registry/pattern_watchlist.json').catch(() => null),
    fetch('../registry/pattern_annotations.json').catch(() => null),
    fetch('../registry/pattern_timeline_dashboard.json').catch(() => null),
    fetch('../registry/pattern_persistence_registry.json').catch(() => null),
    fetch('../registry/pattern_temporal_watchlist.json').catch(() => null),
    fetch('../registry/pattern_temporal_annotations.json').catch(() => null),
    fetch('../registry/causal_dashboard.json').catch(() => null),
    fetch('../registry/mechanism_registry.json').catch(() => null),
    fetch('../registry/causal_watchlist.json').catch(() => null),
    fetch('../registry/causal_annotations.json').catch(() => null),
    fetch('../registry/collaborative_review_dashboard.json').catch(() => null),
    fetch('../registry/consensus_registry.json').catch(() => null),
    fetch('../registry/dissent_watchlist.json').catch(() => null),
    fetch('../registry/deliberation_annotations.json').catch(() => null),
    fetch('../registry/telemetry_dashboard.json').catch(() => null),
    fetch('../registry/lattice_projection_registry.json').catch(() => null),
    fetch('../registry/action_functional_annotations.json').catch(() => null),
    fetch('../registry/branch_dashboard.json').catch(() => null),
    fetch('../registry/branch_registry.json').catch(() => null),
    fetch('../registry/branch_watchlist.json').catch(() => null),
    fetch('../registry/branch_annotations.json').catch(() => null),
    fetch('../registry/prediction_dashboard.json').catch(() => null),
    fetch('../registry/forecast_registry.json').catch(() => null),
    fetch('../registry/prediction_watchlist.json').catch(() => null),
    fetch('../registry/calibration_annotations.json').catch(() => null),
    fetch('../registry/experiment_dashboard.json').catch(() => null),
    fetch('../registry/hypothesis_registry.json').catch(() => null),
    fetch('../registry/falsification_watchlist.json').catch(() => null),
    fetch('../registry/theory_gate_annotations.json').catch(() => null),
    fetch('../registry/theory_dashboard.json').catch(() => null),
    fetch('../registry/theory_registry.json').catch(() => null),
    fetch('../registry/negative_result_watchlist.json').catch(() => null),
    fetch('../registry/theory_annotations.json').catch(() => null),
    fetch('../registry/agency_mode_dashboard.json').catch(() => null),
    fetch('../registry/agency_fit_registry.json').catch(() => null),
    fetch('../registry/agency_disagreement_watchlist.json').catch(() => null),
    fetch('../registry/agency_governance_annotations.json').catch(() => null),
    fetch('../registry/responsibility_dashboard.json').catch(() => null),
    fetch('../registry/support_registry.json').catch(() => null),
    fetch('../registry/intervention_watchlist.json').catch(() => null),
    fetch('../registry/responsibility_annotations.json').catch(() => null),
    fetch('../registry/transfer_dashboard.json').catch(() => null),
    fetch('../registry/theory_transfer_registry.json').catch(() => null),
    fetch('../registry/transfer_watchlist.json').catch(() => null),
    fetch('../registry/transfer_annotations.json').catch(() => null),
    fetch('../registry/system_forecast_dashboard.json').catch(() => null),
    fetch('../registry/regime_transition_registry.json').catch(() => null),
    fetch('../registry/trajectory_watchlist.json').catch(() => null),
    fetch('../registry/system_forecast_annotations.json').catch(() => null),
    fetch('../registry/uncertainty_dashboard.json').catch(() => null),
    fetch('../registry/observation_priority_registry.json').catch(() => null),
    fetch('../registry/curiosity_watchlist.json').catch(() => null),
    fetch('../registry/curiosity_annotations.json').catch(() => null),
    fetch('../registry/value_dashboard.json').catch(() => null),
    fetch('../registry/knowledge_priority_registry.json').catch(() => null),
    fetch('../registry/value_risk_watchlist.json').catch(() => null),
    fetch('../registry/value_annotations.json').catch(() => null),
    fetch('../registry/meta_dashboard.json').catch(() => null),
    fetch('../registry/reasoning_performance_registry.json').catch(() => null),
    fetch('../registry/meta_watchlist.json').catch(() => null),
    fetch('../registry/meta_annotations.json').catch(() => null),
    fetch('../registry/architecture_dashboard.json').catch(() => null),
    fetch('../registry/module_performance_registry.json').catch(() => null),
    fetch('../registry/architecture_watchlist.json').catch(() => null),
    fetch('../registry/architecture_annotations.json').catch(() => null),
    fetch('../registry/social_entropy_dashboard.json').catch(() => null),
    fetch('../registry/civic_cohesion_registry.json').catch(() => null),
    fetch('../registry/legitimacy_watchlist.json').catch(() => null),
    fetch('../registry/social_repair_annotations.json').catch(() => null),
    fetch('../registry/federation_dashboard.json').catch(() => null),
    fetch('../registry/stewardship_registry.json').catch(() => null),
    fetch('../registry/capture_watchlist.json').catch(() => null),
    fetch('../registry/federation_annotations.json').catch(() => null),
    fetch('../registry/emergent_domain_dashboard.json').catch(() => null),
    fetch('../registry/domain_birth_registry.json').catch(() => null),
    fetch('../registry/domain_boundary_watchlist.json').catch(() => null),
    fetch('../registry/emergent_domain_annotations.json').catch(() => null)
  ]);

  return {
    attentionUpdates: attentionUpdatesResp ? await attentionUpdatesResp.json() : {},
    coherenceAssessment: coherenceAssessmentResp ? await coherenceAssessmentResp.json() : {},
    sophiaRecommendations: sophiaRecommendationsResp ? await sophiaRecommendationsResp.json() : {},
    coherenceWeights: coherenceWeightsResp ? await coherenceWeightsResp.json() : {},
    sophiaAnnotations: sophiaAnnotationsResp ? await sophiaAnnotationsResp.json() : {},
    sophiaAttentionState: sophiaAttentionStateResp ? await sophiaAttentionStateResp.json() : {},
    sonyaMemoryIndex: sonyaMemoryIndexResp ? await sonyaMemoryIndexResp.json() : {},
    sonyaAttentionCandidates: sonyaAttentionCandidatesResp ? await sonyaAttentionCandidatesResp.json() : {},
    reasoningThreads: reasoningThreadsResp ? await reasoningThreadsResp.json() : {},
    cognitiveWatchlist: cognitiveWatchlistResp ? await cognitiveWatchlistResp.json() : {},
    cognitiveMonitorIndex: cognitiveMonitorIndexResp ? await cognitiveMonitorIndexResp.json() : {},
    cognitiveStabilityAnnotations: cognitiveStabilityAnnotationsResp ? await cognitiveStabilityAnnotationsResp.json() : {},
    recursiveWatchHistory: recursiveWatchHistoryResp ? await recursiveWatchHistoryResp.json() : {},
    multimodalSignalIndex: multimodalSignalIndexResp ? await multimodalSignalIndexResp.json() : {},
    patternDonationAnnotations: patternDonationAnnotationsResp ? await patternDonationAnnotationsResp.json() : {},
    crossModalAttentionOverlays: crossModalAttentionOverlaysResp ? await crossModalAttentionOverlaysResp.json() : {},
    patternDonationWatchlist: patternDonationWatchlistResp ? await patternDonationWatchlistResp.json() : {},
    reviewDocket: reviewDocketResp ? await reviewDocketResp.json() : {},
    promotionWatchQueue: promotionWatchQueueResp ? await promotionWatchQueueResp.json() : {},
    governanceReviewDocket: governanceReviewDocketResp ? await governanceReviewDocketResp.json() : {},
    reviewerIntegrityAnnotations: reviewerIntegrityAnnotationsResp ? await reviewerIntegrityAnnotationsResp.json() : {},
    reviewerWatchQueue: reviewerWatchQueueResp ? await reviewerWatchQueueResp.json() : {},
    reviewerBehaviorMonitor: reviewerBehaviorMonitorResp ? await reviewerBehaviorMonitorResp.json() : {},
    constitutionalStatus: constitutionalStatusResp ? await constitutionalStatusResp.json() : {},
    continuityModeIndex: continuityModeIndexResp ? await continuityModeIndexResp.json() : {},
    constitutionalAnnotations: constitutionalAnnotationsResp ? await constitutionalAnnotationsResp.json() : {},
    governanceFailureWatchlist: governanceFailureWatchlistResp ? await governanceFailureWatchlistResp.json() : {},
    deliberationDocket: deliberationDocketResp ? await deliberationDocketResp.json() : {},
    amendmentQueue: amendmentQueueResp ? await amendmentQueueResp.json() : {},
    quorumWatchlist: quorumWatchlistResp ? await quorumWatchlistResp.json() : {},
    constitutionalRevisionAnnotations: constitutionalRevisionAnnotationsResp ? await constitutionalRevisionAnnotationsResp.json() : {},
    continuityRoster: continuityRosterResp ? await continuityRosterResp.json() : {},
    successionDocket: successionDocketResp ? await successionDocketResp.json() : {},
    quorumResilienceWatchlist: quorumResilienceWatchlistResp ? await quorumResilienceWatchlistResp.json() : {},
    governanceRedundancyAnnotations: governanceRedundancyAnnotationsResp ? await governanceRedundancyAnnotationsResp.json() : {},
    escrowIndex: escrowIndexResp ? await escrowIndexResp.json() : {},
    recoveryDocket: recoveryDocketResp ? await recoveryDocketResp.json() : {},
    integrityWatchlist: integrityWatchlistResp ? await integrityWatchlistResp.json() : {},
    recoveryAnnotations: recoveryAnnotationsResp ? await recoveryAnnotationsResp.json() : {},
    attestationRegistry: attestationRegistryResp ? await attestationRegistryResp.json() : {},
    witnessDocket: witnessDocketResp ? await witnessDocketResp.json() : {},
    integrityTestimonyWatchlist: integrityTestimonyWatchlistResp ? await integrityTestimonyWatchlistResp.json() : {},
    attestationAnnotations: attestationAnnotationsResp ? await attestationAnnotationsResp.json() : {},
    precedentRegistry: precedentRegistryResp ? await precedentRegistryResp.json() : {},
    caseDocket: caseDocketResp ? await caseDocketResp.json() : {},
    divergenceWatchlist: divergenceWatchlistResp ? await divergenceWatchlistResp.json() : {},
    precedentAnnotations: precedentAnnotationsResp ? await precedentAnnotationsResp.json() : {},
    scenarioRegistry: scenarioRegistryResp ? await scenarioRegistryResp.json() : {},
    stressTestDocket: stressTestDocketResp ? await stressTestDocketResp.json() : {},
    resilienceFindingsWatchlist: resilienceFindingsWatchlistResp ? await resilienceFindingsWatchlistResp.json() : {},
    scenarioAnnotations: scenarioAnnotationsResp ? await scenarioAnnotationsResp.json() : {},
    institutionalStatus: institutionalStatusResp ? await institutionalStatusResp.json() : {},
    systemHealthDashboard: systemHealthDashboardResp ? await systemHealthDashboardResp.json() : {},
    institutionalConflictWatchlist: institutionalConflictWatchlistResp ? await institutionalConflictWatchlistResp.json() : {},
    institutionalAnnotations: institutionalAnnotationsResp ? await institutionalAnnotationsResp.json() : {},
    queueHealthDashboard: queueHealthDashboardResp ? await queueHealthDashboardResp.json() : {},
    reviewBacklogWatchlist: reviewBacklogWatchlistResp ? await reviewBacklogWatchlistResp.json() : {},
    metricGamingWatchlist: metricGamingWatchlistResp ? await metricGamingWatchlistResp.json() : {},
    loadSheddingAnnotations: loadSheddingAnnotationsResp ? await loadSheddingAnnotationsResp.json() : {},
    priorityDashboard: priorityDashboardResp ? await priorityDashboardResp.json() : {},
    triageDocket: triageDocketResp ? await triageDocketResp.json() : {},
    triageWatchlist: triageWatchlistResp ? await triageWatchlistResp.json() : {},
    priorityAnnotations: priorityAnnotationsResp ? await priorityAnnotationsResp.json() : {},
    closureRegistry: closureRegistryResp ? await closureRegistryResp.json() : {},
    repairDocket: repairDocketResp ? await repairDocketResp.json() : {},
    reopenedCaseWatchlist: reopenedCaseWatchlistResp ? await reopenedCaseWatchlistResp.json() : {},
    closureAnnotations: closureAnnotationsResp ? await closureAnnotationsResp.json() : {},
    symbolicFieldRegistry: symbolicFieldRegistryResp ? await symbolicFieldRegistryResp.json() : {},
    earlyWarningDashboard: earlyWarningDashboardResp ? await earlyWarningDashboardResp.json() : {},
    regimeWatchlist: regimeWatchlistResp ? await regimeWatchlistResp.json() : {},
    symbolicFieldAnnotations: symbolicFieldAnnotationsResp ? await symbolicFieldAnnotationsResp.json() : {},
    verificationDashboard: verificationDashboardResp ? await verificationDashboardResp.json() : {},
    entityWatchlist: entityWatchlistResp ? await entityWatchlistResp.json() : {},
    claimTypeRegistry: claimTypeRegistryResp ? await claimTypeRegistryResp.json() : {},
    verificationAnnotations: verificationAnnotationsResp ? await verificationAnnotationsResp.json() : {},
    publicRecordDashboard: publicRecordDashboardResp ? await publicRecordDashboardResp.json() : {},
    entityGraphRegistry: entityGraphRegistryResp ? await entityGraphRegistryResp.json() : {},
    relationshipWatchlist: relationshipWatchlistResp ? await relationshipWatchlistResp.json() : {},
    chainOfCustodyAnnotations: chainOfCustodyAnnotationsResp ? await chainOfCustodyAnnotationsResp.json() : {},
    investigationDashboard: investigationDashboardResp ? await investigationDashboardResp.json() : {},
    investigationPlanRegistry: investigationPlanRegistryResp ? await investigationPlanRegistryResp.json() : {},
    investigationWatchlist: investigationWatchlistResp ? await investigationWatchlistResp.json() : {},
    investigationAnnotations: investigationAnnotationsResp ? await investigationAnnotationsResp.json() : {},
    authorityGateDashboard: authorityGateDashboardResp ? await authorityGateDashboardResp.json() : {},
    weakEvidenceWatchlist: weakEvidenceWatchlistResp ? await weakEvidenceWatchlistResp.json() : {},
    propagationAnnotations: propagationAnnotationsResp ? await propagationAnnotationsResp.json() : {},
    maturityRestrictionRegistry: maturityRestrictionRegistryResp ? await maturityRestrictionRegistryResp.json() : {},
    reviewPacketDashboard: reviewPacketDashboardResp ? await reviewPacketDashboardResp.json() : {},
    reviewPacketRegistry: reviewPacketRegistryResp ? await reviewPacketRegistryResp.json() : {},
    uncertaintyWatchlist: uncertaintyWatchlistResp ? await uncertaintyWatchlistResp.json() : {},
    reviewPacketAnnotations: reviewPacketAnnotationsResp ? await reviewPacketAnnotationsResp.json() : {},
    patternDashboard: patternDashboardResp ? await patternDashboardResp.json() : {},
    patternRegistry: patternRegistryResp ? await patternRegistryResp.json() : {},
    patternWatchlist: patternWatchlistResp ? await patternWatchlistResp.json() : {},
    patternAnnotations: patternAnnotationsResp ? await patternAnnotationsResp.json() : {},
    patternTimelineDashboard: patternTimelineDashboardResp ? await patternTimelineDashboardResp.json() : {},
    patternPersistenceRegistry: patternPersistenceRegistryResp ? await patternPersistenceRegistryResp.json() : {},
    patternTemporalWatchlist: patternTemporalWatchlistResp ? await patternTemporalWatchlistResp.json() : {},
    patternTemporalAnnotations: patternTemporalAnnotationsResp ? await patternTemporalAnnotationsResp.json() : {},
    causalDashboard: causalDashboardResp ? await causalDashboardResp.json() : {},
    mechanismRegistry: mechanismRegistryResp ? await mechanismRegistryResp.json() : {},
    causalWatchlist: causalWatchlistResp ? await causalWatchlistResp.json() : {},
    causalAnnotations: causalAnnotationsResp ? await causalAnnotationsResp.json() : {},
    collaborativeReviewDashboard: collaborativeReviewDashboardResp ? await collaborativeReviewDashboardResp.json() : {},
    consensusRegistry: consensusRegistryResp ? await consensusRegistryResp.json() : {},
    dissentWatchlist: dissentWatchlistResp ? await dissentWatchlistResp.json() : {},
    deliberationAnnotations: deliberationAnnotationsResp ? await deliberationAnnotationsResp.json() : {},
    telemetryDashboard: telemetryDashboardResp ? await telemetryDashboardResp.json() : {},
    latticeProjectionRegistry: latticeProjectionRegistryResp ? await latticeProjectionRegistryResp.json() : {},
    actionFunctionalAnnotations: actionFunctionalAnnotationsResp ? await actionFunctionalAnnotationsResp.json() : {},
    branchDashboard: branchDashboardResp ? await branchDashboardResp.json() : {},
    branchRegistry: branchRegistryResp ? await branchRegistryResp.json() : {},
    branchWatchlist: branchWatchlistResp ? await branchWatchlistResp.json() : {},
    branchAnnotations: branchAnnotationsResp ? await branchAnnotationsResp.json() : {},
    predictionDashboard: predictionDashboardResp ? await predictionDashboardResp.json() : {},
    forecastRegistry: forecastRegistryResp ? await forecastRegistryResp.json() : {},
    predictionWatchlist: predictionWatchlistResp ? await predictionWatchlistResp.json() : {},
    calibrationAnnotations: calibrationAnnotationsResp ? await calibrationAnnotationsResp.json() : {},
    experimentDashboard: experimentDashboardResp ? await experimentDashboardResp.json() : {},
    hypothesisRegistry: hypothesisRegistryResp ? await hypothesisRegistryResp.json() : {},
    falsificationWatchlist: falsificationWatchlistResp ? await falsificationWatchlistResp.json() : {},
    theoryGateAnnotations: theoryGateAnnotationsResp ? await theoryGateAnnotationsResp.json() : {},
    theoryDashboard: theoryDashboardResp ? await theoryDashboardResp.json() : {},
    theoryRegistry: theoryRegistryResp ? await theoryRegistryResp.json() : {},
    negativeResultWatchlist: negativeResultWatchlistResp ? await negativeResultWatchlistResp.json() : {},
    theoryAnnotations: theoryAnnotationsResp ? await theoryAnnotationsResp.json() : {},
    agencyModeDashboard: agencyModeDashboardResp ? await agencyModeDashboardResp.json() : {},
    agencyFitRegistry: agencyFitRegistryResp ? await agencyFitRegistryResp.json() : {},
    agencyDisagreementWatchlist: agencyDisagreementWatchlistResp ? await agencyDisagreementWatchlistResp.json() : {},
    agencyGovernanceAnnotations: agencyGovernanceAnnotationsResp ? await agencyGovernanceAnnotationsResp.json() : {},
    responsibilityDashboard: responsibilityDashboardResp ? await responsibilityDashboardResp.json() : {},
    supportRegistry: supportRegistryResp ? await supportRegistryResp.json() : {},
    interventionWatchlist: interventionWatchlistResp ? await interventionWatchlistResp.json() : {},
    responsibilityAnnotations: responsibilityAnnotationsResp ? await responsibilityAnnotationsResp.json() : {},
    transferDashboard: transferDashboardResp ? await transferDashboardResp.json() : {},
    theoryTransferRegistry: theoryTransferRegistryResp ? await theoryTransferRegistryResp.json() : {},
    transferWatchlist: transferWatchlistResp ? await transferWatchlistResp.json() : {},
    transferAnnotations: transferAnnotationsResp ? await transferAnnotationsResp.json() : {},
    systemForecastDashboard: systemForecastDashboardResp ? await systemForecastDashboardResp.json() : {},
    regimeTransitionRegistry: regimeTransitionRegistryResp ? await regimeTransitionRegistryResp.json() : {},
    trajectoryWatchlist: trajectoryWatchlistResp ? await trajectoryWatchlistResp.json() : {},
    systemForecastAnnotations: systemForecastAnnotationsResp ? await systemForecastAnnotationsResp.json() : {},
    uncertaintyDashboard: uncertaintyDashboardResp ? await uncertaintyDashboardResp.json() : {},
    observationPriorityRegistry: observationPriorityRegistryResp ? await observationPriorityRegistryResp.json() : {},
    curiosityWatchlist: curiosityWatchlistResp ? await curiosityWatchlistResp.json() : {},
    curiosityAnnotations: curiosityAnnotationsResp ? await curiosityAnnotationsResp.json() : {},
    valueDashboard: valueDashboardResp ? await valueDashboardResp.json() : {},
    knowledgePriorityRegistry: knowledgePriorityRegistryResp ? await knowledgePriorityRegistryResp.json() : {},
    valueRiskWatchlist: valueRiskWatchlistResp ? await valueRiskWatchlistResp.json() : {},
    valueAnnotations: valueAnnotationsResp ? await valueAnnotationsResp.json() : {},
    metaDashboard: metaDashboardResp ? await metaDashboardResp.json() : {},
    reasoningPerformanceRegistry: reasoningPerformanceRegistryResp ? await reasoningPerformanceRegistryResp.json() : {},
    metaWatchlist: metaWatchlistResp ? await metaWatchlistResp.json() : {},
    metaAnnotations: metaAnnotationsResp ? await metaAnnotationsResp.json() : {},
    architectureDashboard: architectureDashboardResp ? await architectureDashboardResp.json() : {},
    modulePerformanceRegistry: modulePerformanceRegistryResp ? await modulePerformanceRegistryResp.json() : {},
    architectureWatchlist: architectureWatchlistResp ? await architectureWatchlistResp.json() : {},
    architectureAnnotations: architectureAnnotationsResp ? await architectureAnnotationsResp.json() : {},
    socialEntropyDashboard: socialEntropyDashboardResp ? await socialEntropyDashboardResp.json() : {},
    civicCohesionRegistry: civicCohesionRegistryResp ? await civicCohesionRegistryResp.json() : {},
    legitimacyWatchlist: legitimacyWatchlistResp ? await legitimacyWatchlistResp.json() : {},
    socialRepairAnnotations: socialRepairAnnotationsResp ? await socialRepairAnnotationsResp.json() : {},
    federationDashboard: federationDashboardResp ? await federationDashboardResp.json() : {},
    stewardshipRegistry: stewardshipRegistryResp ? await stewardshipRegistryResp.json() : {},
    captureWatchlist: captureWatchlistResp ? await captureWatchlistResp.json() : {},
    federationAnnotations: federationAnnotationsResp ? await federationAnnotationsResp.json() : {},
    emergentDomainDashboard: emergentDomainDashboardResp ? await emergentDomainDashboardResp.json() : {},
    domainBirthRegistry: domainBirthRegistryResp ? await domainBirthRegistryResp.json() : {},
    domainBoundaryWatchlist: domainBoundaryWatchlistResp ? await domainBoundaryWatchlistResp.json() : {},
    emergentDomainAnnotations: emergentDomainAnnotationsResp ? await emergentDomainAnnotationsResp.json() : {}
  };
}



function buildSonyaConceptSignals(sonyaMemoryIndex, sonyaAttentionCandidates) {
  const admittedInputIds = new Set(
    asArray(sonyaMemoryIndex?.entries)
      .filter((e) => typeof e?.inputId === 'string')
      .map((e) => e.inputId)
  );

  const byConcept = new Map();
  asArray(sonyaAttentionCandidates?.candidates).forEach((candidate) => {
    const inputId = candidate?.inputId;
    if (typeof inputId !== 'string' || !admittedInputIds.has(inputId)) {
      return;
    }
    asArray(candidate?.conceptTargets).forEach((conceptId) => {
      if (typeof conceptId !== 'string') {
        return;
      }
      const existing = byConcept.get(conceptId) ?? { admittedSignals: 0, attentionCandidates: [] };
      existing.admittedSignals += 1;
      existing.attentionCandidates.push({
        inputId,
        status: candidate?.status ?? 'stored',
        attentionWeight: Number(candidate?.attentionWeight ?? 0)
      });
      byConcept.set(conceptId, existing);
    });
  });

  return byConcept;
}



function buildReasoningConceptSignals(reasoningThreads, cognitiveWatchlist) {
  const result = new Map();

  asArray(reasoningThreads?.threads).forEach((thread) => {
    asArray(thread?.linkedConceptIds).forEach((conceptId) => {
      if (typeof conceptId !== 'string') {
        return;
      }
      const existing = result.get(conceptId) ?? { threadCount: 0, watchCount: 0, watchStatus: 'none' };
      existing.threadCount += 1;
      result.set(conceptId, existing);
    });
  });

  asArray(cognitiveWatchlist?.entries).forEach((entry) => {
    asArray(entry?.linkedConceptIds).forEach((conceptId) => {
      if (typeof conceptId !== 'string') {
        return;
      }
      const existing = result.get(conceptId) ?? { threadCount: 0, watchCount: 0, watchStatus: 'none' };
      existing.watchCount += 1;
      existing.watchStatus = existing.watchCount > 0 ? 'watch' : 'none';
      result.set(conceptId, existing);
    });
  });

  return result;
}



function buildCognitiveMonitorConceptSignals(reasoningThreads, cognitiveMonitorIndex, recursiveWatchHistory) {
  const threadConcepts = new Map();
  asArray(reasoningThreads?.threads).forEach((thread) => {
    if (typeof thread?.threadId !== 'string') {
      return;
    }
    threadConcepts.set(thread.threadId, asArray(thread?.linkedConceptIds).filter((id) => typeof id === 'string'));
  });

  const byConcept = new Map();

  function bump(conceptId, update) {
    const existing = byConcept.get(conceptId) ?? {
      stabilityStatus: 'unknown',
      persistenceTrend: 'unknown',
      monitorCount: 0,
      watchHistoryCount: 0,
      watchStatus: 'none'
    };
    update(existing);
    byConcept.set(conceptId, existing);
  }

  asArray(cognitiveMonitorIndex?.entries).forEach((entry) => {
    const concepts = threadConcepts.get(entry?.threadId) ?? [];
    concepts.forEach((conceptId) => {
      bump(conceptId, (c) => {
        c.monitorCount += 1;
        c.stabilityStatus = entry?.stabilityStatus ?? c.stabilityStatus;
        c.persistenceTrend = entry?.persistenceTrend ?? c.persistenceTrend;
        c.watchStatus = entry?.watchStatus ?? c.watchStatus;
      });
    });
  });

  asArray(recursiveWatchHistory?.entries).forEach((entry) => {
    const concepts = threadConcepts.get(entry?.threadId) ?? [];
    concepts.forEach((conceptId) => {
      bump(conceptId, (c) => {
        c.watchHistoryCount += 1;
        c.watchStatus = entry?.watchStatus ?? c.watchStatus;
        c.persistenceTrend = entry?.persistenceTrend ?? c.persistenceTrend;
        if (c.stabilityStatus === 'unknown') {
          c.stabilityStatus = entry?.stabilityStatus ?? c.stabilityStatus;
        }
      });
    });
  });

  return byConcept;
}



function buildMultimodalConceptSignals(multimodalSignalIndex, crossModalAttentionOverlays, patternDonationWatchlist) {
  const overlayByDonation = new Map();
  asArray(crossModalAttentionOverlays?.overlays).forEach((overlay) => {
    if (typeof overlay?.donationId === 'string') {
      overlayByDonation.set(overlay.donationId, overlay);
    }
  });

  const byConcept = new Map();

  function bump(conceptId, update) {
    const existing = byConcept.get(conceptId) ?? {
      donationCount: 0,
      donationWatchStatus: 'none',
      reinforcementStatus: 'none'
    };
    update(existing);
    byConcept.set(conceptId, existing);
  }

  asArray(multimodalSignalIndex?.signals).forEach((signal) => {
    if (signal?.targetType !== 'concept' || typeof signal?.targetId !== 'string') {
      return;
    }
    const overlay = overlayByDonation.get(signal?.donationId);
    bump(signal.targetId, (s) => {
      s.donationCount += 1;
      s.reinforcementStatus = overlay?.reinforcementStatus ?? s.reinforcementStatus;
      s.donationWatchStatus = 'admit-overlay';
    });
  });

  asArray(patternDonationWatchlist?.entries).forEach((entry) => {
    if (entry?.targetType !== 'concept' || typeof entry?.targetId !== 'string') {
      return;
    }
    bump(entry.targetId, (s) => {
      s.donationWatchStatus = entry?.watchStatus ?? s.donationWatchStatus;
      s.reinforcementStatus = entry?.reinforcementStatus ?? s.reinforcementStatus;
    });
  });

  return byConcept;
}



function buildPromotionConceptSignals(reviewDocket, promotionWatchQueue) {
  const byConcept = new Map();

  function bump(targetId, update) {
    if (typeof targetId !== 'string') {
      return;
    }
    const existing = byConcept.get(targetId) ?? { reviewCandidateCount: 0, reviewWatchCount: 0, reviewQueueStatus: 'none' };
    update(existing);
    byConcept.set(targetId, existing);
  }

  asArray(reviewDocket?.entries).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (e) => {
        e.reviewCandidateCount += 1;
        e.reviewQueueStatus = 'docket';
      });
    });
  });

  asArray(promotionWatchQueue?.entries).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (e) => {
        e.reviewWatchCount += 1;
        if (e.reviewQueueStatus !== 'docket') {
          e.reviewQueueStatus = 'watch';
        }
      });
    });
  });

  return byConcept;
}



function buildGovernanceConceptSignals(governanceReviewDocket, reviewerWatchQueue, reviewerBehaviorMonitor) {
  const behaviorByReviewer = new Map();
  asArray(reviewerBehaviorMonitor?.entries).forEach((entry) => {
    if (typeof entry?.reviewerId === 'string') {
      behaviorByReviewer.set(entry.reviewerId, entry);
    }
  });

  const byConcept = new Map();

  function bump(targetId, update) {
    if (typeof targetId !== 'string') {
      return;
    }
    const existing = byConcept.get(targetId) ?? {
      governanceStatus: 'none',
      integrityWatchStatus: 'none',
      behaviorTrend: 'unknown',
      humanReviewFlag: false
    };
    update(existing);
    byConcept.set(targetId, existing);
  }

  asArray(governanceReviewDocket?.entries).forEach((entry) => {
    const behavior = behaviorByReviewer.get(entry?.reviewerId);
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.governanceStatus = entry?.governanceStatus ?? 'recommend-human-review';
        s.integrityWatchStatus = 'docket';
        s.humanReviewFlag = Boolean(entry?.humanReviewFlag);
        s.behaviorTrend = behavior?.behaviorTrend ?? s.behaviorTrend;
      });
    });
  });

  asArray(reviewerWatchQueue?.entries).forEach((entry) => {
    const behavior = behaviorByReviewer.get(entry?.reviewerId);
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        if (s.governanceStatus === 'none') {
          s.governanceStatus = entry?.governanceStatus ?? 'watch';
        }
        if (s.integrityWatchStatus !== 'docket') {
          s.integrityWatchStatus = 'watch';
        }
        s.humanReviewFlag = s.humanReviewFlag || Boolean(entry?.humanReviewFlag);
        if (s.behaviorTrend === 'unknown') {
          s.behaviorTrend = behavior?.behaviorTrend ?? s.behaviorTrend;
        }
      });
    });
  });

  return byConcept;
}


function buildDeliberationConceptSignals(deliberationDocket, amendmentQueue, quorumWatchlist, constitutionalRevisionAnnotations) {
  const byConcept = new Map();

  function bump(targetId, update) {
    if (typeof targetId !== 'string') {
      return;
    }
    const existing = byConcept.get(targetId) ?? {
      quorumStatus: 'none',
      amendmentStatus: 'none',
      deliberationUrgency: 'routine',
      antiCaptureSignals: [],
      deliberationQueueStatus: 'none'
    };
    update(existing);
    existing.antiCaptureSignals = Array.from(new Set(existing.antiCaptureSignals)).sort();
    byConcept.set(targetId, existing);
  }

  asArray(deliberationDocket?.entries).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.quorumStatus = entry?.quorumStatus ?? s.quorumStatus;
        s.amendmentStatus = entry?.amendmentStatus ?? s.amendmentStatus;
        s.deliberationUrgency = entry?.deliberationUrgency ?? s.deliberationUrgency;
        s.antiCaptureSignals.push(...asArray(entry?.antiCaptureSignals).filter((sig) => typeof sig === 'string'));
        s.deliberationQueueStatus = 'docket';
      });
    });
  });

  asArray(amendmentQueue?.entries).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.amendmentStatus = entry?.amendmentStatus ?? s.amendmentStatus;
        if (s.deliberationQueueStatus === 'none') {
          s.deliberationQueueStatus = 'amendment-queue';
        }
      });
    });
  });

  asArray(quorumWatchlist?.entries).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.quorumStatus = entry?.quorumStatus ?? s.quorumStatus;
        s.amendmentStatus = entry?.amendmentStatus ?? s.amendmentStatus;
        s.deliberationUrgency = entry?.deliberationUrgency ?? s.deliberationUrgency;
        s.antiCaptureSignals.push(...asArray(entry?.antiCaptureSignals).filter((sig) => typeof sig === 'string'));
        if (s.deliberationQueueStatus !== 'docket') {
          s.deliberationQueueStatus = 'watch';
        }
      });
    });
  });

  asArray(constitutionalRevisionAnnotations?.annotations).forEach((entry) => {
    const targets = asArray(entry?.linkedTargetIds);
    targets.forEach((targetId) => {
      bump(targetId, (s) => {
        s.quorumStatus = entry?.quorumStatus ?? s.quorumStatus;
        s.amendmentStatus = entry?.amendmentStatus ?? s.amendmentStatus;
        s.deliberationUrgency = entry?.deliberationUrgency ?? s.deliberationUrgency;
        s.antiCaptureSignals.push(...asArray(entry?.antiCaptureSignals).filter((sig) => typeof sig === 'string'));
      });
    });
  });

  return byConcept;
}



function buildContinuityConceptSignals(continuityRoster, successionDocket, quorumResilienceWatchlist, governanceRedundancyAnnotations) {
  const byConcept = new Map();

  function bump(targetId, update) {
    if (typeof targetId !== 'string') {
      return;
    }
    const existing = byConcept.get(targetId) ?? {
      resilienceStatus: 'none',
      successionReadiness: 'unknown',
      fragilityStatus: 'unknown',
      continuityWatchState: 'none',
      governanceFragilityScore: 0,
      successionReadinessScore: 0,
      antiCaptureSignals: [],
      continuityQueueStatus: 'none'
    };
    update(existing);
    existing.antiCaptureSignals = Array.from(new Set(existing.antiCaptureSignals)).sort();
    byConcept.set(targetId, existing);
  }

  asArray(successionDocket?.entries).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.resilienceStatus = entry?.resilienceStatus ?? s.resilienceStatus;
        s.successionReadiness = entry?.successionReadiness ?? s.successionReadiness;
        s.fragilityStatus = entry?.fragilityStatus ?? s.fragilityStatus;
        s.continuityWatchState = entry?.continuityWatchState ?? s.continuityWatchState;
        s.governanceFragilityScore = Number(entry?.governanceFragilityScore ?? s.governanceFragilityScore ?? 0);
        s.successionReadinessScore = Number(entry?.successionReadinessScore ?? s.successionReadinessScore ?? 0);
        s.antiCaptureSignals.push(...asArray(entry?.antiCaptureSignals).filter((sig) => typeof sig === 'string'));
        s.continuityQueueStatus = 'docket';
      });
    });
  });

  asArray(continuityRoster?.entries).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.resilienceStatus = entry?.resilienceStatus ?? s.resilienceStatus;
        s.successionReadiness = entry?.successionReadiness ?? s.successionReadiness;
        s.fragilityStatus = entry?.fragilityStatus ?? s.fragilityStatus;
        s.continuityWatchState = entry?.continuityWatchState ?? s.continuityWatchState;
        s.governanceFragilityScore = Number(entry?.governanceFragilityScore ?? s.governanceFragilityScore ?? 0);
        s.successionReadinessScore = Number(entry?.successionReadinessScore ?? s.successionReadinessScore ?? 0);
        if (s.continuityQueueStatus === 'none') {
          s.continuityQueueStatus = 'roster';
        }
      });
    });
  });

  asArray(quorumResilienceWatchlist?.entries).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.resilienceStatus = entry?.resilienceStatus ?? s.resilienceStatus;
        s.successionReadiness = entry?.successionReadiness ?? s.successionReadiness;
        s.fragilityStatus = entry?.fragilityStatus ?? s.fragilityStatus;
        s.continuityWatchState = entry?.continuityWatchState ?? s.continuityWatchState;
        s.governanceFragilityScore = Number(entry?.governanceFragilityScore ?? s.governanceFragilityScore ?? 0);
        s.successionReadinessScore = Number(entry?.successionReadinessScore ?? s.successionReadinessScore ?? 0);
        s.antiCaptureSignals.push(...asArray(entry?.antiCaptureSignals).filter((sig) => typeof sig === 'string'));
        if (s.continuityQueueStatus !== 'docket') {
          s.continuityQueueStatus = 'watch';
        }
      });
    });
  });

  asArray(governanceRedundancyAnnotations?.annotations).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.resilienceStatus = entry?.resilienceStatus ?? s.resilienceStatus;
        s.successionReadiness = entry?.successionReadiness ?? s.successionReadiness;
        s.fragilityStatus = entry?.fragilityStatus ?? s.fragilityStatus;
        s.continuityWatchState = entry?.continuityWatchState ?? s.continuityWatchState;
        s.governanceFragilityScore = Number(entry?.governanceFragilityScore ?? s.governanceFragilityScore ?? 0);
        s.successionReadinessScore = Number(entry?.successionReadinessScore ?? s.successionReadinessScore ?? 0);
        s.antiCaptureSignals.push(...asArray(entry?.antiCaptureSignals).filter((sig) => typeof sig === 'string'));
      });
    });
  });

  return byConcept;
}



function buildRecoveryConceptSignals(escrowIndex, recoveryDocket, integrityWatchlist, recoveryAnnotations) {
  const byConcept = new Map();

  function bump(targetId, update) {
    if (typeof targetId !== 'string') {
      return;
    }
    const existing = byConcept.get(targetId) ?? {
      preservationCriticality: 'moderate',
      escrowStatus: 'review-pending',
      recoveryReadiness: 'unknown',
      integrityWatchState: 'none',
      recoverabilityScore: 0,
      recoveryQueueStatus: 'none'
    };
    update(existing);
    byConcept.set(targetId, existing);
  }

  asArray(recoveryDocket?.entries).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.preservationCriticality = entry?.preservationCriticality ?? s.preservationCriticality;
        s.escrowStatus = entry?.escrowStatus ?? s.escrowStatus;
        s.recoveryReadiness = entry?.recoveryReadiness ?? s.recoveryReadiness;
        s.integrityWatchState = entry?.integrityWatchState ?? s.integrityWatchState;
        s.recoverabilityScore = Number(entry?.recoverabilityScore ?? s.recoverabilityScore ?? 0);
        s.recoveryQueueStatus = 'docket';
      });
    });
  });

  asArray(integrityWatchlist?.entries).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.preservationCriticality = entry?.preservationCriticality ?? s.preservationCriticality;
        s.escrowStatus = entry?.escrowStatus ?? s.escrowStatus;
        s.recoveryReadiness = entry?.recoveryReadiness ?? s.recoveryReadiness;
        s.integrityWatchState = entry?.integrityWatchState ?? s.integrityWatchState;
        s.recoverabilityScore = Number(entry?.recoverabilityScore ?? s.recoverabilityScore ?? 0);
        if (s.recoveryQueueStatus !== 'docket') {
          s.recoveryQueueStatus = 'watch';
        }
      });
    });
  });

  asArray(recoveryAnnotations?.annotations).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.preservationCriticality = entry?.preservationCriticality ?? s.preservationCriticality;
        s.escrowStatus = entry?.escrowStatus ?? s.escrowStatus;
        s.recoveryReadiness = entry?.recoveryReadiness ?? s.recoveryReadiness;
        s.integrityWatchState = entry?.integrityWatchState ?? s.integrityWatchState;
        s.recoverabilityScore = Number(entry?.recoverabilityScore ?? s.recoverabilityScore ?? 0);
      });
    });
  });

  const escrowByArtifact = new Map();
  asArray(escrowIndex?.entries).forEach((entry) => {
    if (typeof entry?.artifactId === 'string') {
      escrowByArtifact.set(entry.artifactId, entry);
    }
  });

  asArray(recoveryAnnotations?.annotations).forEach((entry) => {
    const escrow = escrowByArtifact.get(entry?.artifactId);
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.escrowStatus = escrow?.escrowStatus ?? s.escrowStatus;
      });
    });
  });

  return byConcept;
}



function buildAttestationConceptSignals(attestationRegistry, witnessDocket, integrityTestimonyWatchlist, attestationAnnotations) {
  const byConcept = new Map();

  function bump(targetId, update) {
    if (typeof targetId !== 'string') {
      return;
    }
    const existing = byConcept.get(targetId) ?? {
      attestationStatus: 'review-pending',
      witnessSufficiency: 'unknown',
      integrityTestimonyWatchState: 'none',
      attestationNeed: 'moderate',
      tamperSensitivity: 'unknown',
      attestationQueueStatus: 'none'
    };
    update(existing);
    byConcept.set(targetId, existing);
  }

  asArray(witnessDocket?.entries).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.attestationStatus = entry?.attestationStatus ?? s.attestationStatus;
        s.witnessSufficiency = entry?.witnessSufficiency ?? s.witnessSufficiency;
        s.integrityTestimonyWatchState = entry?.integrityTestimonyWatchState ?? s.integrityTestimonyWatchState;
        s.attestationNeed = entry?.attestationNeed ?? s.attestationNeed;
        s.tamperSensitivity = entry?.tamperSensitivity ?? s.tamperSensitivity;
        s.attestationQueueStatus = 'docket';
      });
    });
  });

  asArray(integrityTestimonyWatchlist?.entries).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.attestationStatus = entry?.attestationStatus ?? s.attestationStatus;
        s.witnessSufficiency = entry?.witnessSufficiency ?? s.witnessSufficiency;
        s.integrityTestimonyWatchState = entry?.integrityTestimonyWatchState ?? s.integrityTestimonyWatchState;
        s.attestationNeed = entry?.attestationNeed ?? s.attestationNeed;
        s.tamperSensitivity = entry?.tamperSensitivity ?? s.tamperSensitivity;
        if (s.attestationQueueStatus !== 'docket') {
          s.attestationQueueStatus = 'watch';
        }
      });
    });
  });

  asArray(attestationAnnotations?.annotations).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.attestationStatus = entry?.attestationStatus ?? s.attestationStatus;
        s.witnessSufficiency = entry?.witnessSufficiency ?? s.witnessSufficiency;
        s.integrityTestimonyWatchState = entry?.integrityTestimonyWatchState ?? s.integrityTestimonyWatchState;
        s.attestationNeed = entry?.attestationNeed ?? s.attestationNeed;
        s.tamperSensitivity = entry?.tamperSensitivity ?? s.tamperSensitivity;
      });
    });
  });

  const registryByArtifact = new Map();
  asArray(attestationRegistry?.entries).forEach((entry) => {
    if (typeof entry?.artifactId === 'string') {
      registryByArtifact.set(entry.artifactId, entry);
    }
  });

  asArray(attestationAnnotations?.annotations).forEach((entry) => {
    const registryEntry = registryByArtifact.get(entry?.artifactId);
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.attestationStatus = registryEntry?.attestationStatus ?? s.attestationStatus;
        s.witnessSufficiency = registryEntry?.witnessSufficiency ?? s.witnessSufficiency;
      });
    });
  });

  return byConcept;
}



function buildPrecedentConceptSignals(precedentRegistry, caseDocket, divergenceWatchlist, precedentAnnotations) {
  const byConcept = new Map();

  function bump(targetId, update) {
    if (typeof targetId !== 'string') {
      return;
    }
    const existing = byConcept.get(targetId) ?? {
      precedentStatus: 'review-pending',
      analogyConfidence: 0,
      divergenceLevel: 'none',
      precedentWatchState: 'none',
      precedentQueueStatus: 'none'
    };
    update(existing);
    byConcept.set(targetId, existing);
  }

  asArray(caseDocket?.entries).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.precedentStatus = entry?.precedentStatus ?? s.precedentStatus;
        s.analogyConfidence = Number(entry?.analogyConfidence ?? s.analogyConfidence ?? 0);
        s.divergenceLevel = entry?.divergenceLevel ?? s.divergenceLevel;
        s.precedentWatchState = entry?.watchState ?? s.precedentWatchState;
        s.precedentQueueStatus = 'docket';
      });
    });
  });

  asArray(divergenceWatchlist?.entries).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.precedentStatus = entry?.precedentStatus ?? s.precedentStatus;
        s.analogyConfidence = Number(entry?.analogyConfidence ?? s.analogyConfidence ?? 0);
        s.divergenceLevel = entry?.divergenceLevel ?? s.divergenceLevel;
        s.precedentWatchState = entry?.watchState ?? s.precedentWatchState;
        if (s.precedentQueueStatus !== 'docket') {
          s.precedentQueueStatus = 'watch';
        }
      });
    });
  });

  asArray(precedentAnnotations?.annotations).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.precedentStatus = entry?.precedentStatus ?? s.precedentStatus;
        s.analogyConfidence = Number(entry?.analogyConfidence ?? s.analogyConfidence ?? 0);
        s.divergenceLevel = entry?.divergenceLevel ?? s.divergenceLevel;
        s.precedentWatchState = entry?.watchState ?? s.precedentWatchState;
      });
    });
  });

  const registryByCandidate = new Map();
  asArray(precedentRegistry?.entries).forEach((entry) => {
    if (typeof entry?.candidateId === 'string') {
      registryByCandidate.set(entry.candidateId, entry);
    }
  });

  asArray(precedentAnnotations?.annotations).forEach((entry) => {
    const reg = registryByCandidate.get(entry?.candidateId);
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.precedentStatus = reg?.precedentStatus ?? s.precedentStatus;
        s.analogyConfidence = Number(reg?.analogyConfidence ?? s.analogyConfidence ?? 0);
      });
    });
  });

  return byConcept;
}

function buildScenarioConceptSignals(scenarioRegistry, stressTestDocket, resilienceFindingsWatchlist, scenarioAnnotations) {
  const byConcept = new Map();

  function bump(targetId, update) {
    if (typeof targetId !== 'string') {
      return;
    }
    const existing = byConcept.get(targetId) ?? {
      scenarioStatus: 'review-pending',
      projectedCaptureRisk: 'unknown',
      projectedContinuityRisk: 'unknown',
      preparednessRecommendation: 'rehearse-recovery',
      scenarioWatchState: 'none',
      scenarioQueueStatus: 'none'
    };
    update(existing);
    byConcept.set(targetId, existing);
  }

  asArray(stressTestDocket?.entries).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.scenarioStatus = entry?.scenarioStatus ?? s.scenarioStatus;
        s.projectedCaptureRisk = entry?.projectedCaptureRisk ?? s.projectedCaptureRisk;
        s.projectedContinuityRisk = entry?.projectedContinuityRisk ?? s.projectedContinuityRisk;
        s.preparednessRecommendation = entry?.preparednessRecommendation ?? s.preparednessRecommendation;
        s.scenarioWatchState = entry?.watchState ?? s.scenarioWatchState;
        s.scenarioQueueStatus = 'docket';
      });
    });
  });

  asArray(resilienceFindingsWatchlist?.entries).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.scenarioStatus = entry?.scenarioStatus ?? s.scenarioStatus;
        s.projectedCaptureRisk = entry?.projectedCaptureRisk ?? s.projectedCaptureRisk;
        s.projectedContinuityRisk = entry?.projectedContinuityRisk ?? s.projectedContinuityRisk;
        s.preparednessRecommendation = entry?.preparednessRecommendation ?? s.preparednessRecommendation;
        s.scenarioWatchState = entry?.watchState ?? s.scenarioWatchState;
        if (s.scenarioQueueStatus !== 'docket') {
          s.scenarioQueueStatus = 'watch';
        }
      });
    });
  });

  asArray(scenarioAnnotations?.annotations).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.scenarioStatus = entry?.scenarioStatus ?? s.scenarioStatus;
        s.projectedCaptureRisk = entry?.projectedCaptureRisk ?? s.projectedCaptureRisk;
        s.projectedContinuityRisk = entry?.projectedContinuityRisk ?? s.projectedContinuityRisk;
        s.preparednessRecommendation = entry?.preparednessRecommendation ?? s.preparednessRecommendation;
        s.scenarioWatchState = entry?.watchState ?? s.scenarioWatchState;
      });
    });
  });

  const registryByScenario = new Map();
  asArray(scenarioRegistry?.entries).forEach((entry) => {
    if (typeof entry?.scenarioId === 'string') {
      registryByScenario.set(entry.scenarioId, entry);
    }
  });

  asArray(scenarioAnnotations?.annotations).forEach((entry) => {
    const reg = registryByScenario.get(entry?.scenarioId);
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.scenarioStatus = reg?.scenarioStatus ?? s.scenarioStatus;
        s.projectedCaptureRisk = reg?.projectedCaptureRisk ?? s.projectedCaptureRisk;
        s.projectedContinuityRisk = reg?.projectedContinuityRisk ?? s.projectedContinuityRisk;
        s.preparednessRecommendation = reg?.preparednessRecommendation ?? s.preparednessRecommendation;
      });
    });
  });

  return byConcept;
}


function buildInstitutionalConceptSignals(institutionalStatus, systemHealthDashboard, institutionalConflictWatchlist, institutionalAnnotations) {
  const byConcept = new Map();

  function bump(targetId, update) {
    if (typeof targetId !== 'string') {
      return;
    }
    const existing = byConcept.get(targetId) ?? {
      institutionalStatus: 'review-pending',
      chamberConflictLevel: 'none',
      systemHealthScore: 0,
      systemHealthOverview: 'bounded-rehearsal',
      institutionalQueueStatus: 'none'
    };
    update(existing);
    byConcept.set(targetId, existing);
  }

  asArray(systemHealthDashboard?.entries).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.institutionalStatus = entry?.institutionalStatus ?? s.institutionalStatus;
        s.chamberConflictLevel = entry?.chamberConflictLevel ?? s.chamberConflictLevel;
        s.systemHealthScore = Number(entry?.systemHealthScore ?? s.systemHealthScore ?? 0);
        s.systemHealthOverview = entry?.systemHealthOverview ?? s.systemHealthOverview;
        s.institutionalQueueStatus = 'docket';
      });
    });
  });

  asArray(institutionalConflictWatchlist?.entries).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.institutionalStatus = entry?.institutionalStatus ?? s.institutionalStatus;
        s.chamberConflictLevel = entry?.chamberConflictLevel ?? s.chamberConflictLevel;
        s.systemHealthScore = Number(entry?.systemHealthScore ?? s.systemHealthScore ?? 0);
        s.systemHealthOverview = entry?.systemHealthOverview ?? s.systemHealthOverview;
        if (s.institutionalQueueStatus !== 'docket') {
          s.institutionalQueueStatus = 'watch';
        }
      });
    });
  });

  asArray(institutionalAnnotations?.annotations).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.institutionalStatus = entry?.institutionalStatus ?? s.institutionalStatus;
        s.chamberConflictLevel = entry?.chamberConflictLevel ?? s.chamberConflictLevel;
        s.systemHealthScore = Number(entry?.systemHealthScore ?? s.systemHealthScore ?? 0);
        s.systemHealthOverview = entry?.systemHealthOverview ?? s.systemHealthOverview;
      });
    });
  });

  const statusByInstitution = new Map();
  asArray(institutionalStatus?.entries).forEach((entry) => {
    if (typeof entry?.institutionId === 'string') {
      statusByInstitution.set(entry.institutionId, entry);
    }
  });

  asArray(institutionalAnnotations?.annotations).forEach((entry) => {
    const reg = statusByInstitution.get(entry?.institutionId);
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.institutionalStatus = reg?.institutionalStatus ?? s.institutionalStatus;
        s.chamberConflictLevel = reg?.chamberConflictLevel ?? s.chamberConflictLevel;
        s.systemHealthScore = Number(reg?.systemHealthScore ?? s.systemHealthScore ?? 0);
        s.systemHealthOverview = reg?.systemHealthOverview ?? s.systemHealthOverview;
      });
    });
  });

  return byConcept;
}


function buildQueueHealthConceptSignals(queueHealthDashboard, reviewBacklogWatchlist, metricGamingWatchlist, loadSheddingAnnotations) {
  const byConcept = new Map();

  function bump(targetId, update) {
    if (typeof targetId !== 'string') {
      return;
    }
    const existing = byConcept.get(targetId) ?? {
      queueStatus: 'normal',
      backlogPressure: 'low',
      fatigueLoadClass: 'normal',
      metricGamingWatchStatus: 'none',
      loadSheddingRecommendationSummary: 'none',
      queueHealthQueueStatus: 'none'
    };
    update(existing);
    byConcept.set(targetId, existing);
  }

  asArray(queueHealthDashboard?.entries).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.queueStatus = entry?.queueStatus ?? s.queueStatus;
        s.backlogPressure = entry?.backlogPressure ?? s.backlogPressure;
        s.fatigueLoadClass = entry?.fatigueLoadClass ?? s.fatigueLoadClass;
        s.metricGamingWatchStatus = entry?.metricGamingWatchStatus ?? s.metricGamingWatchStatus;
        s.loadSheddingRecommendationSummary = entry?.loadSheddingRecommendationSummary ?? s.loadSheddingRecommendationSummary;
        s.queueHealthQueueStatus = 'dashboard';
      });
    });
  });

  asArray(reviewBacklogWatchlist?.entries).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.queueStatus = entry?.queueStatus ?? s.queueStatus;
        s.backlogPressure = entry?.backlogPressure ?? s.backlogPressure;
        s.fatigueLoadClass = entry?.fatigueLoadClass ?? s.fatigueLoadClass;
        s.metricGamingWatchStatus = entry?.metricGamingWatchStatus ?? s.metricGamingWatchStatus;
        s.loadSheddingRecommendationSummary = entry?.loadSheddingRecommendationSummary ?? s.loadSheddingRecommendationSummary;
        if (s.queueHealthQueueStatus !== 'dashboard') {
          s.queueHealthQueueStatus = 'backlog-watch';
        }
      });
    });
  });

  asArray(metricGamingWatchlist?.entries).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.queueStatus = entry?.queueStatus ?? s.queueStatus;
        s.backlogPressure = entry?.backlogPressure ?? s.backlogPressure;
        s.fatigueLoadClass = entry?.fatigueLoadClass ?? s.fatigueLoadClass;
        s.metricGamingWatchStatus = entry?.metricGamingWatchStatus ?? s.metricGamingWatchStatus;
        s.loadSheddingRecommendationSummary = entry?.loadSheddingRecommendationSummary ?? s.loadSheddingRecommendationSummary;
        if (s.queueHealthQueueStatus !== 'dashboard') {
          s.queueHealthQueueStatus = 'goodhart-watch';
        }
      });
    });
  });

  asArray(loadSheddingAnnotations?.annotations).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.queueStatus = entry?.queueStatus ?? s.queueStatus;
        s.backlogPressure = entry?.backlogPressure ?? s.backlogPressure;
        s.fatigueLoadClass = entry?.fatigueLoadClass ?? s.fatigueLoadClass;
        s.metricGamingWatchStatus = entry?.metricGamingWatchStatus ?? s.metricGamingWatchStatus;
        s.loadSheddingRecommendationSummary = entry?.loadSheddingRecommendationSummary ?? s.loadSheddingRecommendationSummary;
      });
    });
  });

  return byConcept;
}


function buildPriorityConceptSignals(priorityDashboard, triageDocket, triageWatchlist, priorityAnnotations) {
  const byConcept = new Map();

  function bump(targetId, update) {
    if (typeof targetId !== 'string') {
      return;
    }
    const existing = byConcept.get(targetId) ?? {
      triageStatus: 'pending',
      urgencyLevel: 'routine',
      priorityClass: 'standard',
      triageConflictStatus: 'none',
      recommendationSummary: 'none',
      triageQueueStatus: 'none'
    };
    update(existing);
    byConcept.set(targetId, existing);
  }

  asArray(priorityDashboard?.entries).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.triageStatus = entry?.triageStatus ?? s.triageStatus;
        s.urgencyLevel = entry?.urgencyLevel ?? s.urgencyLevel;
        s.priorityClass = entry?.priorityClass ?? s.priorityClass;
        s.triageConflictStatus = entry?.triageConflictStatus ?? s.triageConflictStatus;
        s.recommendationSummary = entry?.recommendationSummary ?? s.recommendationSummary;
        s.triageQueueStatus = 'dashboard';
      });
    });
  });

  asArray(triageDocket?.entries).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.triageStatus = entry?.triageStatus ?? s.triageStatus;
        s.urgencyLevel = entry?.urgencyLevel ?? s.urgencyLevel;
        s.priorityClass = entry?.priorityClass ?? s.priorityClass;
        s.triageConflictStatus = entry?.triageConflictStatus ?? s.triageConflictStatus;
        s.recommendationSummary = entry?.recommendationSummary ?? s.recommendationSummary;
        s.triageQueueStatus = 'docket';
      });
    });
  });

  asArray(triageWatchlist?.entries).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.triageStatus = entry?.triageStatus ?? s.triageStatus;
        s.urgencyLevel = entry?.urgencyLevel ?? s.urgencyLevel;
        s.priorityClass = entry?.priorityClass ?? s.priorityClass;
        s.triageConflictStatus = entry?.triageConflictStatus ?? s.triageConflictStatus;
        s.recommendationSummary = entry?.recommendationSummary ?? s.recommendationSummary;
        if (!['dashboard', 'docket'].includes(s.triageQueueStatus)) {
          s.triageQueueStatus = 'watch';
        }
      });
    });
  });

  asArray(priorityAnnotations?.annotations).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.triageStatus = entry?.triageStatus ?? s.triageStatus;
        s.urgencyLevel = entry?.urgencyLevel ?? s.urgencyLevel;
        s.priorityClass = entry?.priorityClass ?? s.priorityClass;
        s.triageConflictStatus = entry?.triageConflictStatus ?? s.triageConflictStatus;
        s.recommendationSummary = entry?.recommendationSummary ?? s.recommendationSummary;
      });
    });
  });

  return byConcept;
}


function buildClosureConceptSignals(closureRegistry, repairDocket, reopenedCaseWatchlist, closureAnnotations) {
  const byConcept = new Map();

  function bump(targetId, update) {
    if (typeof targetId !== 'string') {
      return;
    }
    const existing = byConcept.get(targetId) ?? {
      closureStatus: 'pending',
      closureConfidence: 'low',
      repairUrgency: 'routine',
      reopenedCaseWatchStatus: 'none',
      closureQueueStatus: 'none'
    };
    update(existing);
    byConcept.set(targetId, existing);
  }

  asArray(closureRegistry?.entries).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.closureStatus = entry?.closureStatus ?? s.closureStatus;
        s.closureConfidence = entry?.closureConfidence ?? s.closureConfidence;
        s.repairUrgency = entry?.repairUrgency ?? s.repairUrgency;
        s.reopenedCaseWatchStatus = entry?.reopenedCaseWatchStatus ?? s.reopenedCaseWatchStatus;
        s.closureQueueStatus = 'registry';
      });
    });
  });

  asArray(repairDocket?.entries).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.closureStatus = entry?.closureStatus ?? s.closureStatus;
        s.closureConfidence = entry?.closureConfidence ?? s.closureConfidence;
        s.repairUrgency = entry?.repairUrgency ?? s.repairUrgency;
        s.reopenedCaseWatchStatus = entry?.reopenedCaseWatchStatus ?? s.reopenedCaseWatchStatus;
        s.closureQueueStatus = 'docket';
      });
    });
  });

  asArray(reopenedCaseWatchlist?.entries).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.closureStatus = entry?.closureStatus ?? s.closureStatus;
        s.closureConfidence = entry?.closureConfidence ?? s.closureConfidence;
        s.repairUrgency = entry?.repairUrgency ?? s.repairUrgency;
        s.reopenedCaseWatchStatus = entry?.reopenedCaseWatchStatus ?? s.reopenedCaseWatchStatus;
        if (!['registry', 'docket'].includes(s.closureQueueStatus)) {
          s.closureQueueStatus = 'watch';
        }
      });
    });
  });

  asArray(closureAnnotations?.annotations).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.closureStatus = entry?.closureStatus ?? s.closureStatus;
        s.closureConfidence = entry?.closureConfidence ?? s.closureConfidence;
        s.repairUrgency = entry?.repairUrgency ?? s.repairUrgency;
        s.reopenedCaseWatchStatus = entry?.reopenedCaseWatchStatus ?? s.reopenedCaseWatchStatus;
      });
    });
  });

  return byConcept;
}


function buildSymbolicFieldConceptSignals(symbolicFieldRegistry, earlyWarningDashboard, regimeWatchlist, symbolicFieldAnnotations) {
  const byConcept = new Map();

  function bump(targetId, update) {
    if (typeof targetId !== 'string') {
      return;
    }
    const existing = byConcept.get(targetId) ?? {
      symbolicFieldStatus: 'stable',
      regimeClass: 'bounded-order',
      lambdaZoneWarningLevel: 'low',
      architectureHint: 'monitor',
      regimeWatchStatus: 'none',
      symbolicFieldQueueStatus: 'none'
    };
    update(existing);
    byConcept.set(targetId, existing);
  }

  asArray(symbolicFieldRegistry?.entries).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.symbolicFieldStatus = entry?.symbolicFieldStatus ?? s.symbolicFieldStatus;
        s.regimeClass = entry?.regimeClass ?? s.regimeClass;
        s.lambdaZoneWarningLevel = entry?.lambdaZoneWarningLevel ?? s.lambdaZoneWarningLevel;
        s.architectureHint = entry?.architectureHint ?? s.architectureHint;
        s.regimeWatchStatus = entry?.regimeWatchStatus ?? s.regimeWatchStatus;
        s.symbolicFieldQueueStatus = 'registry';
      });
    });
  });

  asArray(earlyWarningDashboard?.entries).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.symbolicFieldStatus = entry?.symbolicFieldStatus ?? s.symbolicFieldStatus;
        s.regimeClass = entry?.regimeClass ?? s.regimeClass;
        s.lambdaZoneWarningLevel = entry?.lambdaZoneWarningLevel ?? s.lambdaZoneWarningLevel;
        s.architectureHint = entry?.architectureHint ?? s.architectureHint;
        s.regimeWatchStatus = entry?.regimeWatchStatus ?? s.regimeWatchStatus;
        s.symbolicFieldQueueStatus = 'dashboard';
      });
    });
  });

  asArray(regimeWatchlist?.entries).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.symbolicFieldStatus = entry?.symbolicFieldStatus ?? s.symbolicFieldStatus;
        s.regimeClass = entry?.regimeClass ?? s.regimeClass;
        s.lambdaZoneWarningLevel = entry?.lambdaZoneWarningLevel ?? s.lambdaZoneWarningLevel;
        s.architectureHint = entry?.architectureHint ?? s.architectureHint;
        s.regimeWatchStatus = entry?.regimeWatchStatus ?? s.regimeWatchStatus;
        if (!['registry', 'dashboard'].includes(s.symbolicFieldQueueStatus)) {
          s.symbolicFieldQueueStatus = 'watch';
        }
      });
    });
  });

  asArray(symbolicFieldAnnotations?.annotations).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.symbolicFieldStatus = entry?.symbolicFieldStatus ?? s.symbolicFieldStatus;
        s.regimeClass = entry?.regimeClass ?? s.regimeClass;
        s.lambdaZoneWarningLevel = entry?.lambdaZoneWarningLevel ?? s.lambdaZoneWarningLevel;
        s.architectureHint = entry?.architectureHint ?? s.architectureHint;
        s.regimeWatchStatus = entry?.regimeWatchStatus ?? s.regimeWatchStatus;
      });
    });
  });

  return byConcept;
}


function buildVerificationConceptSignals(verificationDashboard, entityWatchlist, claimTypeRegistry, verificationAnnotations) {
  const byConcept = new Map();

  function bump(targetId, update) {
    if (typeof targetId !== 'string') {
      return;
    }
    const existing = byConcept.get(targetId) ?? {
      claimType: 'untyped',
      entityResolutionStatus: 'unresolved',
      ambiguityLevel: 'medium',
      verificationUrgency: 'routine',
      verificationQueueStatus: 'none'
    };
    update(existing);
    byConcept.set(targetId, existing);
  }

  asArray(claimTypeRegistry?.entries).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.claimType = entry?.claimType ?? s.claimType;
        s.entityResolutionStatus = entry?.entityResolutionStatus ?? s.entityResolutionStatus;
        s.ambiguityLevel = entry?.ambiguityLevel ?? s.ambiguityLevel;
        s.verificationUrgency = entry?.verificationUrgency ?? s.verificationUrgency;
        s.verificationQueueStatus = 'registry';
      });
    });
  });

  asArray(verificationDashboard?.entries).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.claimType = entry?.claimType ?? s.claimType;
        s.entityResolutionStatus = entry?.entityResolutionStatus ?? s.entityResolutionStatus;
        s.ambiguityLevel = entry?.ambiguityLevel ?? s.ambiguityLevel;
        s.verificationUrgency = entry?.verificationUrgency ?? s.verificationUrgency;
        s.verificationQueueStatus = 'dashboard';
      });
    });
  });

  asArray(entityWatchlist?.entries).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.claimType = entry?.claimType ?? s.claimType;
        s.entityResolutionStatus = entry?.entityResolutionStatus ?? s.entityResolutionStatus;
        s.ambiguityLevel = entry?.ambiguityLevel ?? s.ambiguityLevel;
        s.verificationUrgency = entry?.verificationUrgency ?? s.verificationUrgency;
        if (!['registry', 'dashboard'].includes(s.verificationQueueStatus)) {
          s.verificationQueueStatus = 'watch';
        }
      });
    });
  });

  asArray(verificationAnnotations?.annotations).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.claimType = entry?.claimType ?? s.claimType;
        s.entityResolutionStatus = entry?.entityResolutionStatus ?? s.entityResolutionStatus;
        s.ambiguityLevel = entry?.ambiguityLevel ?? s.ambiguityLevel;
        s.verificationUrgency = entry?.verificationUrgency ?? s.verificationUrgency;
      });
    });
  });

  return byConcept;
}


function buildPublicRecordConceptSignals(publicRecordDashboard, entityGraphRegistry, relationshipWatchlist, chainOfCustodyAnnotations) {
  const byConcept = new Map();

  function bump(targetId, update) {
    if (typeof targetId !== 'string') {
      return;
    }
    const existing = byConcept.get(targetId) ?? {
      recordType: 'unknown',
      machineReadabilityScore: 0,
      entityGraphStatus: 'pending',
      relationshipAmbiguity: 'medium',
      custodyIntegrityScore: 0,
      publicRecordQueueStatus: 'none'
    };
    update(existing);
    byConcept.set(targetId, existing);
  }

  asArray(entityGraphRegistry?.entries).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.recordType = entry?.recordType ?? s.recordType;
        s.machineReadabilityScore = Number(entry?.machineReadabilityScore ?? s.machineReadabilityScore);
        s.entityGraphStatus = entry?.entityGraphStatus ?? s.entityGraphStatus;
        s.relationshipAmbiguity = entry?.relationshipAmbiguity ?? s.relationshipAmbiguity;
        s.custodyIntegrityScore = Number(entry?.custodyIntegrityScore ?? s.custodyIntegrityScore);
        s.publicRecordQueueStatus = 'registry';
      });
    });
  });

  asArray(publicRecordDashboard?.entries).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.recordType = entry?.recordType ?? s.recordType;
        s.machineReadabilityScore = Number(entry?.machineReadabilityScore ?? s.machineReadabilityScore);
        s.entityGraphStatus = entry?.entityGraphStatus ?? s.entityGraphStatus;
        s.relationshipAmbiguity = entry?.relationshipAmbiguity ?? s.relationshipAmbiguity;
        s.custodyIntegrityScore = Number(entry?.custodyIntegrityScore ?? s.custodyIntegrityScore);
        s.publicRecordQueueStatus = 'dashboard';
      });
    });
  });

  asArray(relationshipWatchlist?.entries).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.recordType = entry?.recordType ?? s.recordType;
        s.machineReadabilityScore = Number(entry?.machineReadabilityScore ?? s.machineReadabilityScore);
        s.entityGraphStatus = entry?.entityGraphStatus ?? s.entityGraphStatus;
        s.relationshipAmbiguity = entry?.relationshipAmbiguity ?? s.relationshipAmbiguity;
        s.custodyIntegrityScore = Number(entry?.custodyIntegrityScore ?? s.custodyIntegrityScore);
        if (!['registry', 'dashboard'].includes(s.publicRecordQueueStatus)) {
          s.publicRecordQueueStatus = 'watch';
        }
      });
    });
  });

  asArray(chainOfCustodyAnnotations?.annotations).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.recordType = entry?.recordType ?? s.recordType;
        s.machineReadabilityScore = Number(entry?.machineReadabilityScore ?? s.machineReadabilityScore);
        s.entityGraphStatus = entry?.entityGraphStatus ?? s.entityGraphStatus;
        s.relationshipAmbiguity = entry?.relationshipAmbiguity ?? s.relationshipAmbiguity;
        s.custodyIntegrityScore = Number(entry?.custodyIntegrityScore ?? s.custodyIntegrityScore);
      });
    });
  });

  return byConcept;
}

function buildInvestigationConceptSignals(investigationDashboard, investigationPlanRegistry, investigationWatchlist, investigationAnnotations) {
  const byConcept = new Map();

  function bump(targetId, update) {
    if (typeof targetId !== 'string') {
      return;
    }
    const existing = byConcept.get(targetId) ?? {
      investigationStage: 'intake',
      stageRank: 1,
      planStatus: 'none',
      planProgress: 0,
      investigationQueueStatus: 'none',
      dependencyCount: 0,
      dependencyGraph: { nodes: [], edges: [] },
      blockedDependencies: [],
      planTotalSteps: 0,
      planCompletedSteps: 0,
    };
    update(existing);
    byConcept.set(targetId, existing);
  }

  const plansByReview = new Map();
  asArray(investigationPlanRegistry?.entries).forEach((entry) => {
    if (typeof entry?.reviewId === 'string') {
      plansByReview.set(entry.reviewId, entry);
    }
  });

  asArray(investigationDashboard?.entries).forEach((entry) => {
    const plan = plansByReview.get(entry?.reviewId);
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.investigationStage = entry?.investigationStage ?? s.investigationStage;
        s.stageRank = Number(entry?.stageRank ?? s.stageRank);
        s.planStatus = entry?.planStatus ?? plan?.planStatus ?? s.planStatus;
        s.planProgress = Number(entry?.planProgress ?? plan?.planProgress ?? s.planProgress);
        s.dependencyCount = Number(entry?.dependencyCount ?? plan?.dependencyCount ?? s.dependencyCount);
        s.dependencyGraph = entry?.dependencyGraph ?? s.dependencyGraph;
        s.blockedDependencies = asArray(plan?.blockedBy);
        s.planTotalSteps = Number(plan?.totalSteps ?? s.planTotalSteps);
        s.planCompletedSteps = Number(plan?.completedSteps ?? s.planCompletedSteps);
        s.investigationQueueStatus = 'dashboard';
      });
    });
  });

  asArray(investigationWatchlist?.entries).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.investigationStage = entry?.investigationStage ?? s.investigationStage;
        s.planProgress = Number(entry?.planProgress ?? s.planProgress);
        s.dependencyCount = Number(entry?.dependencyCount ?? s.dependencyCount);
        if (s.investigationQueueStatus !== 'dashboard') {
          s.investigationQueueStatus = 'watch';
        }
      });
    });
  });

  asArray(investigationAnnotations?.annotations).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.investigationStage = entry?.investigationStage ?? s.investigationStage;
        s.planProgress = Number(entry?.planProgress ?? s.planProgress);
        s.dependencyCount = Number(entry?.dependencyCount ?? s.dependencyCount);
      });
    });
  });

  return byConcept;
}

function buildEvidenceAuthorityConceptSignals(authorityGateDashboard, weakEvidenceWatchlist, propagationAnnotations, maturityRestrictionRegistry) {
  const byConcept = new Map();

  function bump(targetId, update) {
    if (typeof targetId !== 'string') {
      return;
    }
    const existing = byConcept.get(targetId) ?? {
      evidenceMaturity: 'unknown',
      evidenceAuthorityClaimType: 'untyped',
      allowedAuthorityClass: 'restricted',
      authorityMismatchFlag: false,
      propagationRestrictions: [],
      allowedPropagationRights: [],
      maturityGateStatus: 'hold',
      maturityGateReason: 'insufficient-evidence-maturity',
      authorityQueueStatus: 'none',
    };
    update(existing);
    byConcept.set(targetId, existing);
  }

  const maturityByReview = new Map();
  asArray(maturityRestrictionRegistry?.entries).forEach((entry) => {
    if (typeof entry?.reviewId === 'string') {
      maturityByReview.set(entry.reviewId, entry);
    }
  });

  asArray(authorityGateDashboard?.entries).forEach((entry) => {
    const maturity = maturityByReview.get(entry?.reviewId);
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.evidenceMaturity = entry?.evidenceMaturity ?? s.evidenceMaturity;
        s.evidenceAuthorityClaimType = entry?.claimType ?? s.evidenceAuthorityClaimType;
        s.allowedAuthorityClass = entry?.allowedAuthorityClass ?? s.allowedAuthorityClass;
        s.authorityMismatchFlag = Boolean(entry?.authorityMismatchFlag ?? s.authorityMismatchFlag);
        s.propagationRestrictions = asArray(entry?.propagationRestrictions ?? maturity?.propagationRestrictions);
        s.allowedPropagationRights = asArray(entry?.allowedPropagationRights ?? maturity?.allowedPropagationRights);
        s.maturityGateStatus = entry?.maturityGateStatus ?? maturity?.maturityGateStatus ?? s.maturityGateStatus;
        s.maturityGateReason = entry?.maturityGateReason ?? maturity?.maturityGateReason ?? s.maturityGateReason;
        s.authorityQueueStatus = 'dashboard';
      });
    });
  });

  asArray(weakEvidenceWatchlist?.entries).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.evidenceMaturity = entry?.evidenceMaturity ?? s.evidenceMaturity;
        s.evidenceAuthorityClaimType = entry?.claimType ?? s.evidenceAuthorityClaimType;
        s.allowedAuthorityClass = entry?.allowedAuthorityClass ?? s.allowedAuthorityClass;
        s.authorityMismatchFlag = Boolean(entry?.authorityMismatchFlag ?? s.authorityMismatchFlag);
        s.propagationRestrictions = asArray(entry?.propagationRestrictions ?? s.propagationRestrictions);
        s.allowedPropagationRights = asArray(entry?.allowedPropagationRights ?? s.allowedPropagationRights);
        s.maturityGateStatus = entry?.maturityGateStatus ?? s.maturityGateStatus;
        s.maturityGateReason = entry?.maturityGateReason ?? s.maturityGateReason;
        if (s.authorityQueueStatus !== 'dashboard') {
          s.authorityQueueStatus = 'watch';
        }
      });
    });
  });

  asArray(propagationAnnotations?.annotations).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.evidenceMaturity = entry?.evidenceMaturity ?? s.evidenceMaturity;
        s.evidenceAuthorityClaimType = entry?.claimType ?? s.evidenceAuthorityClaimType;
        s.allowedAuthorityClass = entry?.allowedAuthorityClass ?? s.allowedAuthorityClass;
        s.authorityMismatchFlag = Boolean(entry?.authorityMismatchFlag ?? s.authorityMismatchFlag);
        s.propagationRestrictions = asArray(entry?.propagationRestrictions ?? s.propagationRestrictions);
        s.allowedPropagationRights = asArray(entry?.allowedPropagationRights ?? s.allowedPropagationRights);
        s.maturityGateStatus = entry?.maturityGateStatus ?? s.maturityGateStatus;
        s.maturityGateReason = entry?.maturityGateReason ?? s.maturityGateReason;
      });
    });
  });

  return byConcept;
}

function buildReviewPacketConceptSignals(reviewPacketDashboard, reviewPacketRegistry, uncertaintyWatchlist, reviewPacketAnnotations) {
  const byConcept = new Map();

  function bump(targetId, update) {
    if (typeof targetId !== 'string') {
      return;
    }
    const existing = byConcept.get(targetId) ?? {
      reviewPacketStatus: 'pending-review',
      maturityCeiling: 'bounded-review',
      reviewPacketAmbiguityLevel: 'medium',
      uncertaintyDisclosures: [],
      excludedConclusions: [],
      synthesisStatus: 'bounded',
      reviewPacketQueueStatus: 'none',
    };
    update(existing);
    byConcept.set(targetId, existing);
  }

  const registryByReview = new Map();
  asArray(reviewPacketRegistry?.entries).forEach((entry) => {
    if (typeof entry?.reviewId === 'string') {
      registryByReview.set(entry.reviewId, entry);
    }
  });

  asArray(reviewPacketDashboard?.entries).forEach((entry) => {
    const reg = registryByReview.get(entry?.reviewId);
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.reviewPacketStatus = entry?.packetStatus ?? reg?.packetStatus ?? s.reviewPacketStatus;
        s.maturityCeiling = entry?.maturityCeiling ?? reg?.maturityCeiling ?? s.maturityCeiling;
        s.reviewPacketAmbiguityLevel = entry?.ambiguityLevel ?? reg?.ambiguityLevel ?? s.reviewPacketAmbiguityLevel;
        s.uncertaintyDisclosures = asArray(entry?.uncertaintyDisclosures ?? reg?.uncertaintyDisclosures);
        s.excludedConclusions = asArray(entry?.excludedConclusions ?? reg?.excludedConclusions);
        s.synthesisStatus = entry?.synthesisStatus ?? reg?.synthesisStatus ?? s.synthesisStatus;
        s.reviewPacketQueueStatus = 'dashboard';
      });
    });
  });

  asArray(uncertaintyWatchlist?.entries).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.reviewPacketStatus = entry?.packetStatus ?? s.reviewPacketStatus;
        s.maturityCeiling = entry?.maturityCeiling ?? s.maturityCeiling;
        s.reviewPacketAmbiguityLevel = entry?.ambiguityLevel ?? s.reviewPacketAmbiguityLevel;
        s.uncertaintyDisclosures = asArray(entry?.uncertaintyDisclosures ?? s.uncertaintyDisclosures);
        s.excludedConclusions = asArray(entry?.excludedConclusions ?? s.excludedConclusions);
        s.synthesisStatus = entry?.synthesisStatus ?? s.synthesisStatus;
        if (s.reviewPacketQueueStatus !== 'dashboard') {
          s.reviewPacketQueueStatus = 'watch';
        }
      });
    });
  });

  asArray(reviewPacketAnnotations?.annotations).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.reviewPacketStatus = entry?.packetStatus ?? s.reviewPacketStatus;
        s.maturityCeiling = entry?.maturityCeiling ?? s.maturityCeiling;
        s.reviewPacketAmbiguityLevel = entry?.ambiguityLevel ?? s.reviewPacketAmbiguityLevel;
        s.uncertaintyDisclosures = asArray(entry?.uncertaintyDisclosures ?? s.uncertaintyDisclosures);
        s.excludedConclusions = asArray(entry?.excludedConclusions ?? s.excludedConclusions);
        s.synthesisStatus = entry?.synthesisStatus ?? s.synthesisStatus;
      });
    });
  });

  return byConcept;
}

function buildPatternConceptSignals(patternDashboard, patternRegistry, patternWatchlist, patternAnnotations) {
  const byConcept = new Map();

  function bump(targetId, update) {
    if (typeof targetId !== 'string') {
      return;
    }
    const existing = byConcept.get(targetId) ?? {
      patternCluster: 'unclustered',
      patternMaturity: 'speculative',
      crossCaseRelationshipHints: [],
      patternConflictMarkers: [],
      patternQueueStatus: 'none',
    };
    update(existing);
    byConcept.set(targetId, existing);
  }

  const registryByReview = new Map();
  asArray(patternRegistry?.entries).forEach((entry) => {
    if (typeof entry?.reviewId === 'string') {
      registryByReview.set(entry.reviewId, entry);
    }
  });

  asArray(patternDashboard?.entries).forEach((entry) => {
    const reg = registryByReview.get(entry?.reviewId);
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.patternCluster = entry?.patternCluster ?? reg?.patternCluster ?? s.patternCluster;
        s.patternMaturity = entry?.patternMaturity ?? reg?.patternMaturity ?? s.patternMaturity;
        s.crossCaseRelationshipHints = asArray(entry?.crossCaseRelationshipHints ?? reg?.crossCaseRelationshipHints);
        s.patternConflictMarkers = asArray(entry?.conflictMarkers ?? reg?.conflictMarkers);
        s.patternQueueStatus = 'dashboard';
      });
    });
  });

  asArray(patternWatchlist?.entries).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.patternCluster = entry?.patternCluster ?? s.patternCluster;
        s.patternMaturity = entry?.patternMaturity ?? s.patternMaturity;
        s.crossCaseRelationshipHints = asArray(entry?.crossCaseRelationshipHints ?? s.crossCaseRelationshipHints);
        s.patternConflictMarkers = asArray(entry?.conflictMarkers ?? s.patternConflictMarkers);
        if (s.patternQueueStatus !== 'dashboard') {
          s.patternQueueStatus = 'watch';
        }
      });
    });
  });

  asArray(patternAnnotations?.annotations).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.patternCluster = entry?.patternCluster ?? s.patternCluster;
        s.patternMaturity = entry?.patternMaturity ?? s.patternMaturity;
        s.crossCaseRelationshipHints = asArray(entry?.crossCaseRelationshipHints ?? s.crossCaseRelationshipHints);
        s.patternConflictMarkers = asArray(entry?.conflictMarkers ?? s.patternConflictMarkers);
      });
    });
  });

  return byConcept;
}

function buildPatternTemporalConceptSignals(patternTimelineDashboard, patternPersistenceRegistry, patternTemporalWatchlist, patternTemporalAnnotations) {
  const byConcept = new Map();

  function bump(targetId, update) {
    if (typeof targetId !== 'string') {
      return;
    }
    const existing = byConcept.get(targetId) ?? {
      patternTimelineStatus: 'tracked',
      patternPersistence: 'fragile',
      temporalConflictMarkers: [],
      patternTimelineEvents: [],
      patternTemporalQueueStatus: 'none',
    };
    update(existing);
    byConcept.set(targetId, existing);
  }

  const persistenceByReview = new Map();
  asArray(patternPersistenceRegistry?.entries).forEach((entry) => {
    if (typeof entry?.reviewId === 'string') {
      persistenceByReview.set(entry.reviewId, entry);
    }
  });

  asArray(patternTimelineDashboard?.entries).forEach((entry) => {
    const persist = persistenceByReview.get(entry?.reviewId);
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.patternTimelineStatus = entry?.patternTimelineStatus ?? persist?.patternTimelineStatus ?? s.patternTimelineStatus;
        s.patternPersistence = entry?.patternPersistence ?? persist?.patternPersistence ?? s.patternPersistence;
        s.temporalConflictMarkers = asArray(entry?.temporalConflictMarkers ?? persist?.temporalConflictMarkers);
        s.patternTimelineEvents = asArray(entry?.timelineEvents ?? persist?.timelineEvents);
        s.patternTemporalQueueStatus = 'dashboard';
      });
    });
  });

  asArray(patternTemporalWatchlist?.entries).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.patternTimelineStatus = entry?.patternTimelineStatus ?? s.patternTimelineStatus;
        s.patternPersistence = entry?.patternPersistence ?? s.patternPersistence;
        s.temporalConflictMarkers = asArray(entry?.temporalConflictMarkers ?? s.temporalConflictMarkers);
        s.patternTimelineEvents = asArray(entry?.timelineEvents ?? s.patternTimelineEvents);
        if (s.patternTemporalQueueStatus !== 'dashboard') {
          s.patternTemporalQueueStatus = 'watch';
        }
      });
    });
  });

  asArray(patternTemporalAnnotations?.annotations).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.patternTimelineStatus = entry?.patternTimelineStatus ?? s.patternTimelineStatus;
        s.patternPersistence = entry?.patternPersistence ?? s.patternPersistence;
        s.temporalConflictMarkers = asArray(entry?.temporalConflictMarkers ?? s.temporalConflictMarkers);
        s.patternTimelineEvents = asArray(entry?.timelineEvents ?? s.patternTimelineEvents);
      });
    });
  });

  return byConcept;
}

function buildCausalConceptSignals(causalDashboard, mechanismRegistry, causalWatchlist, causalAnnotations) {
  const byConcept = new Map();

  function bump(targetId, update) {
    if (typeof targetId !== 'string') {
      return;
    }
    const existing = byConcept.get(targetId) ?? {
      causalBundleType: 'unknown-bundle',
      mechanismCandidates: [],
      explanatoryGap: 'high',
      prohibitedConclusions: [],
      causalConflictState: 'none',
      causalQueueStatus: 'none',
    };
    update(existing);
    byConcept.set(targetId, existing);
  }

  const mechanismByReview = new Map();
  asArray(mechanismRegistry?.entries).forEach((entry) => {
    if (typeof entry?.reviewId === 'string') {
      mechanismByReview.set(entry.reviewId, entry);
    }
  });

  asArray(causalDashboard?.entries).forEach((entry) => {
    const mech = mechanismByReview.get(entry?.reviewId);
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.causalBundleType = entry?.causalBundleType ?? mech?.causalBundleType ?? s.causalBundleType;
        s.mechanismCandidates = asArray(entry?.mechanismCandidates ?? mech?.mechanismCandidates);
        s.explanatoryGap = entry?.explanatoryGap ?? mech?.explanatoryGap ?? s.explanatoryGap;
        s.prohibitedConclusions = asArray(entry?.prohibitedConclusions ?? mech?.prohibitedConclusions);
        s.causalConflictState = entry?.causalConflictState ?? mech?.causalConflictState ?? s.causalConflictState;
        s.causalQueueStatus = 'dashboard';
      });
    });
  });

  asArray(causalWatchlist?.entries).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.causalBundleType = entry?.causalBundleType ?? s.causalBundleType;
        s.mechanismCandidates = asArray(entry?.mechanismCandidates ?? s.mechanismCandidates);
        s.explanatoryGap = entry?.explanatoryGap ?? s.explanatoryGap;
        s.prohibitedConclusions = asArray(entry?.prohibitedConclusions ?? s.prohibitedConclusions);
        s.causalConflictState = entry?.causalConflictState ?? s.causalConflictState;
        if (s.causalQueueStatus !== 'dashboard') {
          s.causalQueueStatus = 'watch';
        }
      });
    });
  });

  asArray(causalAnnotations?.annotations).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.causalBundleType = entry?.causalBundleType ?? s.causalBundleType;
        s.mechanismCandidates = asArray(entry?.mechanismCandidates ?? s.mechanismCandidates);
        s.explanatoryGap = entry?.explanatoryGap ?? s.explanatoryGap;
        s.prohibitedConclusions = asArray(entry?.prohibitedConclusions ?? s.prohibitedConclusions);
        s.causalConflictState = entry?.causalConflictState ?? s.causalConflictState;
      });
    });
  });

  return byConcept;
}



function buildCollaborativeConceptSignals(collaborativeReviewDashboard, consensusRegistry, dissentWatchlist, deliberationAnnotations) {
  const byConcept = new Map();

  function bump(targetId, update) {
    if (typeof targetId !== 'string') {
      return;
    }
    const existing = byConcept.get(targetId) ?? {
      collaborativeStatus: 'none',
      consensusClass: 'none',
      dissentPresent: false,
      dissentTraceCount: 0,
      maturityConstraints: [],
      collaborativeQueueStatus: 'none',
    };
    update(existing);
    byConcept.set(targetId, existing);
  }

  const consensusByReview = new Map();
  asArray(consensusRegistry?.entries).forEach((entry) => {
    if (typeof entry?.reviewId === 'string') {
      consensusByReview.set(entry.reviewId, entry);
    }
  });

  asArray(collaborativeReviewDashboard?.entries).forEach((entry) => {
    const consensus = consensusByReview.get(entry?.reviewId);
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.collaborativeStatus = entry?.collaborativeStatus ?? s.collaborativeStatus;
        s.consensusClass = entry?.consensusClass ?? consensus?.consensusClass ?? s.consensusClass;
        s.dissentPresent = Boolean(entry?.dissentPresent ?? consensus?.dissentPresent ?? s.dissentPresent);
        s.dissentTraceCount = Number(entry?.dissentTraceCount ?? consensus?.dissentTraceCount ?? s.dissentTraceCount);
        s.maturityConstraints = asArray(entry?.maturityConstraints ?? consensus?.maturityConstraints);
        s.collaborativeQueueStatus = 'dashboard';
      });
    });
  });

  asArray(dissentWatchlist?.entries).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.collaborativeStatus = entry?.collaborativeStatus ?? s.collaborativeStatus;
        s.consensusClass = entry?.consensusClass ?? s.consensusClass;
        s.dissentPresent = Boolean(entry?.dissentPresent ?? s.dissentPresent);
        s.dissentTraceCount = Number(entry?.dissentTraceCount ?? s.dissentTraceCount);
        s.maturityConstraints = asArray(entry?.maturityConstraints ?? s.maturityConstraints);
        if (s.collaborativeQueueStatus !== 'dashboard') {
          s.collaborativeQueueStatus = 'watch';
        }
      });
    });
  });

  asArray(deliberationAnnotations?.annotations).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.collaborativeStatus = entry?.collaborativeStatus ?? s.collaborativeStatus;
        s.consensusClass = entry?.consensusClass ?? s.consensusClass;
        s.dissentPresent = Boolean(entry?.dissentPresent ?? s.dissentPresent);
        s.dissentTraceCount = Number(entry?.dissentTraceCount ?? s.dissentTraceCount);
        s.maturityConstraints = asArray(entry?.maturityConstraints ?? s.maturityConstraints);
      });
    });
  });

  return byConcept;
}



function buildTelemetryConceptSignals(telemetryDashboard, latticeProjectionRegistry, patternDonationWatchlist, actionFunctionalAnnotations) {
  const byConcept = new Map();

  function bump(targetId, update) {
    if (typeof targetId !== 'string') {
      return;
    }
    const existing = byConcept.get(targetId) ?? {
      telemetryFieldStatus: 'monitor',
      latticeCoordinates: '0,0,0',
      latticeRegime: 'bounded-order',
      donorPatternPedigree: [],
      tafScoreSummary: 'bounded',
      tafScore: 0,
      branchNovelty: 'low',
      branchMaturityCeiling: 'bounded-review',
      telemetryQueueStatus: 'none',
    };
    update(existing);
    byConcept.set(targetId, existing);
  }

  const latticeByReview = new Map();
  asArray(latticeProjectionRegistry?.entries).forEach((entry) => {
    if (typeof entry?.reviewId === 'string') {
      latticeByReview.set(entry.reviewId, entry);
    }
  });

  asArray(telemetryDashboard?.entries).forEach((entry) => {
    const lattice = latticeByReview.get(entry?.reviewId);
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.telemetryFieldStatus = entry?.telemetryFieldStatus ?? s.telemetryFieldStatus;
        s.latticeCoordinates = entry?.latticeCoordinates ?? lattice?.latticeCoordinates ?? s.latticeCoordinates;
        s.latticeRegime = entry?.latticeRegime ?? lattice?.latticeRegime ?? s.latticeRegime;
        s.donorPatternPedigree = asArray(entry?.donorPatternPedigree ?? lattice?.donorPatternPedigree);
        s.tafScoreSummary = entry?.tafScoreSummary ?? lattice?.tafScoreSummary ?? s.tafScoreSummary;
        s.tafScore = Number(entry?.tafScore ?? lattice?.tafScore ?? s.tafScore);
        s.branchNovelty = entry?.branchNovelty ?? lattice?.branchNovelty ?? s.branchNovelty;
        s.branchMaturityCeiling = entry?.maturityCeiling ?? lattice?.maturityCeiling ?? s.branchMaturityCeiling;
        s.telemetryQueueStatus = 'dashboard';
      });
    });
  });

  asArray(patternDonationWatchlist?.entries).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.telemetryFieldStatus = entry?.telemetryFieldStatus ?? s.telemetryFieldStatus;
        s.latticeCoordinates = entry?.latticeCoordinates ?? s.latticeCoordinates;
        s.latticeRegime = entry?.latticeRegime ?? s.latticeRegime;
        s.donorPatternPedigree = asArray(entry?.donorPatternPedigree ?? s.donorPatternPedigree);
        s.tafScoreSummary = entry?.tafScoreSummary ?? s.tafScoreSummary;
        s.tafScore = Number(entry?.tafScore ?? s.tafScore);
        s.branchNovelty = entry?.branchNovelty ?? s.branchNovelty;
        s.branchMaturityCeiling = entry?.maturityCeiling ?? s.branchMaturityCeiling;
        if (s.telemetryQueueStatus !== 'dashboard') {
          s.telemetryQueueStatus = 'watch';
        }
      });
    });
  });

  asArray(actionFunctionalAnnotations?.annotations).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.telemetryFieldStatus = entry?.telemetryFieldStatus ?? s.telemetryFieldStatus;
        s.latticeCoordinates = entry?.latticeCoordinates ?? s.latticeCoordinates;
        s.latticeRegime = entry?.latticeRegime ?? s.latticeRegime;
        s.donorPatternPedigree = asArray(entry?.donorPatternPedigree ?? s.donorPatternPedigree);
        s.tafScoreSummary = entry?.tafScoreSummary ?? s.tafScoreSummary;
        s.tafScore = Number(entry?.tafScore ?? s.tafScore);
        s.branchNovelty = entry?.branchNovelty ?? s.branchNovelty;
        s.branchMaturityCeiling = entry?.maturityCeiling ?? s.branchMaturityCeiling;
      });
    });
  });

  return byConcept;
}



function buildBranchLifecycleConceptSignals(branchDashboard, branchRegistry, branchWatchlist, branchAnnotations) {
  const byConcept = new Map();

  function bump(targetId, update) {
    if (typeof targetId !== 'string') {
      return;
    }
    const existing = byConcept.get(targetId) ?? {
      branchLifecycleStatus: 'monitor',
      branchStage: 'emergent',
      branchConflictNodes: [],
      branchConflictEdges: [],
      branchDecayRisk: 'low',
      branchDecaySignals: [],
      reinforcementTrend: 'balanced',
      contradictionTrend: 'low',
      branchQueueStatus: 'none',
    };
    update(existing);
    byConcept.set(targetId, existing);
  }

  const registryByReview = new Map();
  asArray(branchRegistry?.entries).forEach((entry) => {
    if (typeof entry?.reviewId === 'string') {
      registryByReview.set(entry.reviewId, entry);
    }
  });

  asArray(branchDashboard?.entries).forEach((entry) => {
    const reg = registryByReview.get(entry?.reviewId);
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.branchLifecycleStatus = entry?.branchLifecycleStatus ?? reg?.branchLifecycleStatus ?? s.branchLifecycleStatus;
        s.branchStage = entry?.branchStage ?? reg?.branchStage ?? s.branchStage;
        s.branchConflictNodes = asArray(entry?.conflictNodes ?? reg?.conflictNodes);
        s.branchConflictEdges = asArray(entry?.conflictEdges ?? reg?.conflictEdges);
        s.branchDecayRisk = entry?.decayRisk ?? reg?.decayRisk ?? s.branchDecayRisk;
        s.branchDecaySignals = asArray(entry?.decaySignals ?? reg?.decaySignals);
        s.reinforcementTrend = entry?.reinforcementTrend ?? reg?.reinforcementTrend ?? s.reinforcementTrend;
        s.contradictionTrend = entry?.contradictionTrend ?? reg?.contradictionTrend ?? s.contradictionTrend;
        s.branchQueueStatus = 'dashboard';
      });
    });
  });

  asArray(branchWatchlist?.entries).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.branchLifecycleStatus = entry?.branchLifecycleStatus ?? s.branchLifecycleStatus;
        s.branchStage = entry?.branchStage ?? s.branchStage;
        s.branchConflictNodes = asArray(entry?.conflictNodes ?? s.branchConflictNodes);
        s.branchConflictEdges = asArray(entry?.conflictEdges ?? s.branchConflictEdges);
        s.branchDecayRisk = entry?.decayRisk ?? s.branchDecayRisk;
        s.branchDecaySignals = asArray(entry?.decaySignals ?? s.branchDecaySignals);
        s.reinforcementTrend = entry?.reinforcementTrend ?? s.reinforcementTrend;
        s.contradictionTrend = entry?.contradictionTrend ?? s.contradictionTrend;
        if (s.branchQueueStatus !== 'dashboard') {
          s.branchQueueStatus = 'watch';
        }
      });
    });
  });

  asArray(branchAnnotations?.annotations).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.branchLifecycleStatus = entry?.branchLifecycleStatus ?? s.branchLifecycleStatus;
        s.branchStage = entry?.branchStage ?? s.branchStage;
        s.branchConflictNodes = asArray(entry?.conflictNodes ?? s.branchConflictNodes);
        s.branchConflictEdges = asArray(entry?.conflictEdges ?? s.branchConflictEdges);
        s.branchDecayRisk = entry?.decayRisk ?? s.branchDecayRisk;
        s.branchDecaySignals = asArray(entry?.decaySignals ?? s.branchDecaySignals);
        s.reinforcementTrend = entry?.reinforcementTrend ?? s.reinforcementTrend;
        s.contradictionTrend = entry?.contradictionTrend ?? s.contradictionTrend;
      });
    });
  });

  return byConcept;
}



function buildPredictionConceptSignals(predictionDashboard, forecastRegistry, predictionWatchlist, calibrationAnnotations) {
  const byConcept = new Map();

  function bump(targetId, update) {
    if (typeof targetId !== 'string') {
      return;
    }
    const existing = byConcept.get(targetId) ?? {
      forecastAccuracy: 'unknown',
      forecastConfidence: 'bounded',
      calibrationTrend: 'stable',
      calibrationError: 0,
      branchReliability: 'unknown',
      reliabilityScore: 0,
      outcomeTimeline: [],
      predictionQueueStatus: 'none',
    };
    update(existing);
    byConcept.set(targetId, existing);
  }

  const registryByReview = new Map();
  asArray(forecastRegistry?.entries).forEach((entry) => {
    if (typeof entry?.reviewId === 'string') {
      registryByReview.set(entry.reviewId, entry);
    }
  });

  asArray(predictionDashboard?.entries).forEach((entry) => {
    const reg = registryByReview.get(entry?.reviewId);
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.forecastAccuracy = entry?.forecastAccuracy ?? reg?.forecastAccuracy ?? s.forecastAccuracy;
        s.forecastConfidence = entry?.forecastConfidence ?? reg?.forecastConfidence ?? s.forecastConfidence;
        s.calibrationTrend = entry?.calibrationTrend ?? reg?.calibrationTrend ?? s.calibrationTrend;
        s.calibrationError = Number(entry?.calibrationError ?? reg?.calibrationError ?? s.calibrationError);
        s.branchReliability = entry?.branchReliability ?? reg?.branchReliability ?? s.branchReliability;
        s.reliabilityScore = Number(entry?.reliabilityScore ?? reg?.reliabilityScore ?? s.reliabilityScore);
        s.outcomeTimeline = asArray(entry?.outcomeTimeline ?? reg?.outcomeTimeline);
        s.predictionQueueStatus = 'dashboard';
      });
    });
  });

  asArray(predictionWatchlist?.entries).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.forecastAccuracy = entry?.forecastAccuracy ?? s.forecastAccuracy;
        s.forecastConfidence = entry?.forecastConfidence ?? s.forecastConfidence;
        s.calibrationTrend = entry?.calibrationTrend ?? s.calibrationTrend;
        s.calibrationError = Number(entry?.calibrationError ?? s.calibrationError);
        s.branchReliability = entry?.branchReliability ?? s.branchReliability;
        s.reliabilityScore = Number(entry?.reliabilityScore ?? s.reliabilityScore);
        s.outcomeTimeline = asArray(entry?.outcomeTimeline ?? s.outcomeTimeline);
        if (s.predictionQueueStatus !== 'dashboard') {
          s.predictionQueueStatus = 'watch';
        }
      });
    });
  });

  asArray(calibrationAnnotations?.annotations).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.forecastAccuracy = entry?.forecastAccuracy ?? s.forecastAccuracy;
        s.forecastConfidence = entry?.forecastConfidence ?? s.forecastConfidence;
        s.calibrationTrend = entry?.calibrationTrend ?? s.calibrationTrend;
        s.calibrationError = Number(entry?.calibrationError ?? s.calibrationError);
        s.branchReliability = entry?.branchReliability ?? s.branchReliability;
        s.reliabilityScore = Number(entry?.reliabilityScore ?? s.reliabilityScore);
        s.outcomeTimeline = asArray(entry?.outcomeTimeline ?? s.outcomeTimeline);
      });
    });
  });

  return byConcept;
}



function buildExperimentalConceptSignals(experimentDashboard, hypothesisRegistry, falsificationWatchlist, theoryGateAnnotations) {
  const byConcept = new Map();

  function bump(targetId, update) {
    if (typeof targetId !== 'string') {
      return;
    }
    const existing = byConcept.get(targetId) ?? {
      experimentalStatus: 'design',
      falsificationReadiness: 'pending',
      replicationPathwayStatus: 'pending',
      theoryGateClass: 'hold',
      hypothesisClass: 'exploratory',
      experimentalQueueStatus: 'none',
    };
    update(existing);
    byConcept.set(targetId, existing);
  }

  const registryByReview = new Map();
  asArray(hypothesisRegistry?.entries).forEach((entry) => {
    if (typeof entry?.reviewId === 'string') {
      registryByReview.set(entry.reviewId, entry);
    }
  });

  asArray(experimentDashboard?.entries).forEach((entry) => {
    const reg = registryByReview.get(entry?.reviewId);
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.experimentalStatus = entry?.experimentalStatus ?? reg?.experimentalStatus ?? s.experimentalStatus;
        s.falsificationReadiness = entry?.falsificationReadiness ?? reg?.falsificationReadiness ?? s.falsificationReadiness;
        s.replicationPathwayStatus = entry?.replicationPathwayStatus ?? reg?.replicationPathwayStatus ?? s.replicationPathwayStatus;
        s.theoryGateClass = entry?.theoryGateClass ?? reg?.theoryGateClass ?? s.theoryGateClass;
        s.hypothesisClass = entry?.hypothesisClass ?? reg?.hypothesisClass ?? s.hypothesisClass;
        s.experimentalQueueStatus = 'dashboard';
      });
    });
  });

  asArray(falsificationWatchlist?.entries).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.experimentalStatus = entry?.experimentalStatus ?? s.experimentalStatus;
        s.falsificationReadiness = entry?.falsificationReadiness ?? s.falsificationReadiness;
        s.replicationPathwayStatus = entry?.replicationPathwayStatus ?? s.replicationPathwayStatus;
        s.theoryGateClass = entry?.theoryGateClass ?? s.theoryGateClass;
        s.hypothesisClass = entry?.hypothesisClass ?? s.hypothesisClass;
        if (s.experimentalQueueStatus !== 'dashboard') {
          s.experimentalQueueStatus = 'watch';
        }
      });
    });
  });

  asArray(theoryGateAnnotations?.annotations).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.experimentalStatus = entry?.experimentalStatus ?? s.experimentalStatus;
        s.falsificationReadiness = entry?.falsificationReadiness ?? s.falsificationReadiness;
        s.replicationPathwayStatus = entry?.replicationPathwayStatus ?? s.replicationPathwayStatus;
        s.theoryGateClass = entry?.theoryGateClass ?? s.theoryGateClass;
        s.hypothesisClass = entry?.hypothesisClass ?? s.hypothesisClass;
      });
    });
  });

  return byConcept;
}



function buildTheoryCorpusConceptSignals(theoryDashboard, theoryRegistry, negativeResultWatchlist, theoryAnnotations) {
  const byConcept = new Map();

  function bump(targetId, update) {
    if (typeof targetId !== 'string') {
      return;
    }
    const existing = byConcept.get(targetId) ?? {
      theoryStatus: 'under-review',
      falsificationStatus: 'pending',
      replicationStatus: 'pending',
      revisionLineage: [],
      negativeResultIndicators: [],
      competitionState: 'unresolved',
      competitionPeers: [],
      theoryQueueStatus: 'none',
    };
    update(existing);
    byConcept.set(targetId, existing);
  }

  const registryByReview = new Map();
  asArray(theoryRegistry?.entries).forEach((entry) => {
    if (typeof entry?.reviewId === 'string') {
      registryByReview.set(entry.reviewId, entry);
    }
  });

  asArray(theoryDashboard?.entries).forEach((entry) => {
    const reg = registryByReview.get(entry?.reviewId);
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.theoryStatus = entry?.theoryStatus ?? reg?.theoryStatus ?? s.theoryStatus;
        s.falsificationStatus = entry?.falsificationStatus ?? reg?.falsificationStatus ?? s.falsificationStatus;
        s.replicationStatus = entry?.replicationStatus ?? reg?.replicationStatus ?? s.replicationStatus;
        s.revisionLineage = asArray(entry?.revisionLineage ?? reg?.revisionLineage ?? s.revisionLineage);
        s.negativeResultIndicators = asArray(entry?.negativeResultIndicators ?? reg?.negativeResultIndicators ?? s.negativeResultIndicators);
        s.competitionState = entry?.competitionState ?? reg?.competitionState ?? s.competitionState;
        s.competitionPeers = asArray(entry?.competitionPeers ?? reg?.competitionPeers ?? s.competitionPeers);
        s.theoryQueueStatus = 'dashboard';
      });
    });
  });

  asArray(negativeResultWatchlist?.entries).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.theoryStatus = entry?.theoryStatus ?? s.theoryStatus;
        s.falsificationStatus = entry?.falsificationStatus ?? s.falsificationStatus;
        s.replicationStatus = entry?.replicationStatus ?? s.replicationStatus;
        s.revisionLineage = asArray(entry?.revisionLineage ?? s.revisionLineage);
        s.negativeResultIndicators = asArray(entry?.negativeResultIndicators ?? s.negativeResultIndicators);
        s.competitionState = entry?.competitionState ?? s.competitionState;
        s.competitionPeers = asArray(entry?.competitionPeers ?? s.competitionPeers);
        if (s.theoryQueueStatus !== 'dashboard') {
          s.theoryQueueStatus = 'watch';
        }
      });
    });
  });

  asArray(theoryAnnotations?.annotations).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.theoryStatus = entry?.theoryStatus ?? s.theoryStatus;
        s.falsificationStatus = entry?.falsificationStatus ?? s.falsificationStatus;
        s.replicationStatus = entry?.replicationStatus ?? s.replicationStatus;
        s.revisionLineage = asArray(entry?.revisionLineage ?? s.revisionLineage);
        s.negativeResultIndicators = asArray(entry?.negativeResultIndicators ?? s.negativeResultIndicators);
        s.competitionState = entry?.competitionState ?? s.competitionState;
        s.competitionPeers = asArray(entry?.competitionPeers ?? s.competitionPeers);
      });
    });
  });

  return byConcept;
}



function buildAgencyModeConceptSignals(agencyModeDashboard, agencyFitRegistry, agencyDisagreementWatchlist, agencyGovernanceAnnotations) {
  const byConcept = new Map();

  function bump(targetId, update) {
    if (typeof targetId !== 'string') {
      return;
    }
    const existing = byConcept.get(targetId) ?? {
      agencyStatus: 'under-review',
      deterministicFit: 0,
      volitionalFit: 0,
      provisionalVHat: 0,
      telBranchSignature: 'untyped',
      governanceModeClass: 'bounded-watch',
      consentSignal: 'required',
      blameSuppressionSignal: 'enabled',
      agencyQueueStatus: 'none',
    };
    update(existing);
    byConcept.set(targetId, existing);
  }

  const registryByReview = new Map();
  asArray(agencyFitRegistry?.entries).forEach((entry) => {
    if (typeof entry?.reviewId === 'string') {
      registryByReview.set(entry.reviewId, entry);
    }
  });

  asArray(agencyModeDashboard?.entries).forEach((entry) => {
    const reg = registryByReview.get(entry?.reviewId);
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.agencyStatus = entry?.agencyStatus ?? reg?.agencyStatus ?? s.agencyStatus;
        s.deterministicFit = Number(entry?.deterministicFit ?? reg?.deterministicFit ?? s.deterministicFit);
        s.volitionalFit = Number(entry?.volitionalFit ?? reg?.volitionalFit ?? s.volitionalFit);
        s.provisionalVHat = Number(entry?.provisionalVHat ?? reg?.provisionalVHat ?? s.provisionalVHat);
        s.telBranchSignature = entry?.telBranchSignature ?? reg?.telBranchSignature ?? s.telBranchSignature;
        s.governanceModeClass = entry?.governanceModeClass ?? reg?.governanceModeClass ?? s.governanceModeClass;
        s.consentSignal = entry?.consentSignal ?? reg?.consentSignal ?? s.consentSignal;
        s.blameSuppressionSignal = entry?.blameSuppressionSignal ?? reg?.blameSuppressionSignal ?? s.blameSuppressionSignal;
        s.agencyQueueStatus = 'dashboard';
      });
    });
  });

  asArray(agencyDisagreementWatchlist?.entries).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.agencyStatus = entry?.agencyStatus ?? s.agencyStatus;
        s.deterministicFit = Number(entry?.deterministicFit ?? s.deterministicFit);
        s.volitionalFit = Number(entry?.volitionalFit ?? s.volitionalFit);
        s.provisionalVHat = Number(entry?.provisionalVHat ?? s.provisionalVHat);
        s.telBranchSignature = entry?.telBranchSignature ?? s.telBranchSignature;
        s.governanceModeClass = entry?.governanceModeClass ?? s.governanceModeClass;
        s.consentSignal = entry?.consentSignal ?? s.consentSignal;
        s.blameSuppressionSignal = entry?.blameSuppressionSignal ?? s.blameSuppressionSignal;
        if (s.agencyQueueStatus !== 'dashboard') {
          s.agencyQueueStatus = 'watch';
        }
      });
    });
  });

  asArray(agencyGovernanceAnnotations?.annotations).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.agencyStatus = entry?.agencyStatus ?? s.agencyStatus;
        s.deterministicFit = Number(entry?.deterministicFit ?? s.deterministicFit);
        s.volitionalFit = Number(entry?.volitionalFit ?? s.volitionalFit);
        s.provisionalVHat = Number(entry?.provisionalVHat ?? s.provisionalVHat);
        s.telBranchSignature = entry?.telBranchSignature ?? s.telBranchSignature;
        s.governanceModeClass = entry?.governanceModeClass ?? s.governanceModeClass;
        s.consentSignal = entry?.consentSignal ?? s.consentSignal;
        s.blameSuppressionSignal = entry?.blameSuppressionSignal ?? s.blameSuppressionSignal;
      });
    });
  });

  return byConcept;
}



function buildResponsibilityConceptSignals(responsibilityDashboard, supportRegistry, interventionWatchlist, responsibilityAnnotations) {
  const byConcept = new Map();

  function bump(targetId, update) {
    if (typeof targetId !== 'string') {
      return;
    }
    const existing = byConcept.get(targetId) ?? {
      responsibilityStatus: 'under-review',
      supportPathway: 'monitor',
      consentRequirement: 'required',
      coercionCeiling: 'strict',
      sanctionSuppressionState: 'enabled',
      interventionBoundaryState: 'bounded',
      responsibilityQueueStatus: 'none',
    };
    update(existing);
    byConcept.set(targetId, existing);
  }

  const registryByReview = new Map();
  asArray(supportRegistry?.entries).forEach((entry) => {
    if (typeof entry?.reviewId === 'string') {
      registryByReview.set(entry.reviewId, entry);
    }
  });

  asArray(responsibilityDashboard?.entries).forEach((entry) => {
    const reg = registryByReview.get(entry?.reviewId);
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.responsibilityStatus = entry?.responsibilityStatus ?? reg?.responsibilityStatus ?? s.responsibilityStatus;
        s.supportPathway = entry?.supportPathway ?? reg?.supportPathway ?? s.supportPathway;
        s.consentRequirement = entry?.consentRequirement ?? reg?.consentRequirement ?? s.consentRequirement;
        s.coercionCeiling = entry?.coercionCeiling ?? reg?.coercionCeiling ?? s.coercionCeiling;
        s.sanctionSuppressionState = entry?.sanctionSuppressionState ?? reg?.sanctionSuppressionState ?? s.sanctionSuppressionState;
        s.interventionBoundaryState = entry?.interventionBoundaryState ?? reg?.interventionBoundaryState ?? s.interventionBoundaryState;
        s.responsibilityQueueStatus = 'dashboard';
      });
    });
  });

  asArray(interventionWatchlist?.entries).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.responsibilityStatus = entry?.responsibilityStatus ?? s.responsibilityStatus;
        s.supportPathway = entry?.supportPathway ?? s.supportPathway;
        s.consentRequirement = entry?.consentRequirement ?? s.consentRequirement;
        s.coercionCeiling = entry?.coercionCeiling ?? s.coercionCeiling;
        s.sanctionSuppressionState = entry?.sanctionSuppressionState ?? s.sanctionSuppressionState;
        s.interventionBoundaryState = entry?.interventionBoundaryState ?? s.interventionBoundaryState;
        if (s.responsibilityQueueStatus !== 'dashboard') {
          s.responsibilityQueueStatus = 'watch';
        }
      });
    });
  });

  asArray(responsibilityAnnotations?.annotations).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.responsibilityStatus = entry?.responsibilityStatus ?? s.responsibilityStatus;
        s.supportPathway = entry?.supportPathway ?? s.supportPathway;
        s.consentRequirement = entry?.consentRequirement ?? s.consentRequirement;
        s.coercionCeiling = entry?.coercionCeiling ?? s.coercionCeiling;
        s.sanctionSuppressionState = entry?.sanctionSuppressionState ?? s.sanctionSuppressionState;
        s.interventionBoundaryState = entry?.interventionBoundaryState ?? s.interventionBoundaryState;
      });
    });
  });

  return byConcept;
}



function buildTheoryTransferConceptSignals(transferDashboard, theoryTransferRegistry, transferWatchlist, transferAnnotations) {
  const byConcept = new Map();

  function bump(targetId, update) {
    if (typeof targetId !== 'string') {
      return;
    }
    const existing = byConcept.get(targetId) ?? {
      transferStatus: 'under-review',
      donorTargetAsymmetry: 'unknown',
      replicationGateState: 'hold',
      prohibitedClaims: [],
      riskRegisterSummary: 'bounded',
      transferQueueStatus: 'none',
    };
    update(existing);
    byConcept.set(targetId, existing);
  }

  const registryByReview = new Map();
  asArray(theoryTransferRegistry?.entries).forEach((entry) => {
    if (typeof entry?.reviewId === 'string') {
      registryByReview.set(entry.reviewId, entry);
    }
  });

  asArray(transferDashboard?.entries).forEach((entry) => {
    const reg = registryByReview.get(entry?.reviewId);
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.transferStatus = entry?.transferStatus ?? reg?.transferStatus ?? s.transferStatus;
        s.donorTargetAsymmetry = entry?.donorTargetAsymmetry ?? reg?.donorTargetAsymmetry ?? s.donorTargetAsymmetry;
        s.replicationGateState = entry?.replicationGateState ?? reg?.replicationGateState ?? s.replicationGateState;
        s.prohibitedClaims = asArray(entry?.prohibitedClaims ?? reg?.prohibitedClaims ?? s.prohibitedClaims);
        s.riskRegisterSummary = entry?.riskRegisterSummary ?? reg?.riskRegisterSummary ?? s.riskRegisterSummary;
        s.transferQueueStatus = 'dashboard';
      });
    });
  });

  asArray(transferWatchlist?.entries).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.transferStatus = entry?.transferStatus ?? s.transferStatus;
        s.donorTargetAsymmetry = entry?.donorTargetAsymmetry ?? s.donorTargetAsymmetry;
        s.replicationGateState = entry?.replicationGateState ?? s.replicationGateState;
        s.prohibitedClaims = asArray(entry?.prohibitedClaims ?? s.prohibitedClaims);
        s.riskRegisterSummary = entry?.riskRegisterSummary ?? s.riskRegisterSummary;
        if (s.transferQueueStatus !== 'dashboard') {
          s.transferQueueStatus = 'watch';
        }
      });
    });
  });

  asArray(transferAnnotations?.annotations).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.transferStatus = entry?.transferStatus ?? s.transferStatus;
        s.donorTargetAsymmetry = entry?.donorTargetAsymmetry ?? s.donorTargetAsymmetry;
        s.replicationGateState = entry?.replicationGateState ?? s.replicationGateState;
        s.prohibitedClaims = asArray(entry?.prohibitedClaims ?? s.prohibitedClaims);
        s.riskRegisterSummary = entry?.riskRegisterSummary ?? s.riskRegisterSummary;
      });
    });
  });

  return byConcept;
}



function buildSystemForecastConceptSignals(systemForecastDashboard, regimeTransitionRegistry, trajectoryWatchlist, systemForecastAnnotations) {
  const byConcept = new Map();

  function bump(targetId, update) {
    if (typeof targetId !== 'string') {
      return;
    }
    const existing = byConcept.get(targetId) ?? {
      regimeTransitionProbability: 0,
      entropyAccumulationGraph: [],
      branchEcosystemStability: 'unknown',
      trajectoryDivergenceMarkers: [],
      donorTargetAsymmetry: 'unknown',
      replicationGateState: 'hold',
      prohibitedClaims: [],
      riskRegisterSummary: 'bounded',
      forecastQueueStatus: 'none',
    };
    update(existing);
    byConcept.set(targetId, existing);
  }

  const registryByReview = new Map();
  asArray(regimeTransitionRegistry?.entries).forEach((entry) => {
    if (typeof entry?.reviewId === 'string') {
      registryByReview.set(entry.reviewId, entry);
    }
  });

  asArray(systemForecastDashboard?.entries).forEach((entry) => {
    const reg = registryByReview.get(entry?.reviewId);
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.regimeTransitionProbability = Number(entry?.regimeTransitionProbability ?? reg?.regimeTransitionProbability ?? s.regimeTransitionProbability);
        s.entropyAccumulationGraph = asArray(entry?.entropyAccumulationGraph ?? reg?.entropyAccumulationGraph ?? s.entropyAccumulationGraph);
        s.branchEcosystemStability = entry?.branchEcosystemStability ?? reg?.branchEcosystemStability ?? s.branchEcosystemStability;
        s.trajectoryDivergenceMarkers = asArray(entry?.trajectoryDivergenceMarkers ?? reg?.trajectoryDivergenceMarkers ?? s.trajectoryDivergenceMarkers);
        s.donorTargetAsymmetry = entry?.donorTargetAsymmetry ?? reg?.donorTargetAsymmetry ?? s.donorTargetAsymmetry;
        s.replicationGateState = entry?.replicationGateState ?? reg?.replicationGateState ?? s.replicationGateState;
        s.prohibitedClaims = asArray(entry?.prohibitedClaims ?? reg?.prohibitedClaims ?? s.prohibitedClaims);
        s.riskRegisterSummary = entry?.riskRegisterSummary ?? reg?.riskRegisterSummary ?? s.riskRegisterSummary;
        s.forecastQueueStatus = 'dashboard';
      });
    });
  });

  asArray(trajectoryWatchlist?.entries).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.regimeTransitionProbability = Number(entry?.regimeTransitionProbability ?? s.regimeTransitionProbability);
        s.entropyAccumulationGraph = asArray(entry?.entropyAccumulationGraph ?? s.entropyAccumulationGraph);
        s.branchEcosystemStability = entry?.branchEcosystemStability ?? s.branchEcosystemStability;
        s.trajectoryDivergenceMarkers = asArray(entry?.trajectoryDivergenceMarkers ?? s.trajectoryDivergenceMarkers);
        s.donorTargetAsymmetry = entry?.donorTargetAsymmetry ?? s.donorTargetAsymmetry;
        s.replicationGateState = entry?.replicationGateState ?? s.replicationGateState;
        s.prohibitedClaims = asArray(entry?.prohibitedClaims ?? s.prohibitedClaims);
        s.riskRegisterSummary = entry?.riskRegisterSummary ?? s.riskRegisterSummary;
        if (s.forecastQueueStatus !== 'dashboard') {
          s.forecastQueueStatus = 'watch';
        }
      });
    });
  });

  asArray(systemForecastAnnotations?.annotations).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.regimeTransitionProbability = Number(entry?.regimeTransitionProbability ?? s.regimeTransitionProbability);
        s.entropyAccumulationGraph = asArray(entry?.entropyAccumulationGraph ?? s.entropyAccumulationGraph);
        s.branchEcosystemStability = entry?.branchEcosystemStability ?? s.branchEcosystemStability;
        s.trajectoryDivergenceMarkers = asArray(entry?.trajectoryDivergenceMarkers ?? s.trajectoryDivergenceMarkers);
        s.donorTargetAsymmetry = entry?.donorTargetAsymmetry ?? s.donorTargetAsymmetry;
        s.replicationGateState = entry?.replicationGateState ?? s.replicationGateState;
        s.prohibitedClaims = asArray(entry?.prohibitedClaims ?? s.prohibitedClaims);
        s.riskRegisterSummary = entry?.riskRegisterSummary ?? s.riskRegisterSummary;
      });
    });
  });

  return byConcept;
}



function buildInformationValueConceptSignals(uncertaintyDashboard, observationPriorityRegistry, curiosityWatchlist, curiosityAnnotations) {
  const byConcept = new Map();

  function bump(targetId, update) {
    if (typeof targetId !== 'string') {
      return;
    }
    const existing = byConcept.get(targetId) ?? {
      uncertaintyGradient: 'moderate',
      informationGain: 0,
      experimentPriority: 'monitor',
      entropyReductionForecast: 0,
      curiosityQueueStatus: 'none',
    };
    update(existing);
    byConcept.set(targetId, existing);
  }

  const registryByReview = new Map();
  asArray(observationPriorityRegistry?.entries).forEach((entry) => {
    if (typeof entry?.reviewId === 'string') {
      registryByReview.set(entry.reviewId, entry);
    }
  });

  asArray(uncertaintyDashboard?.entries).forEach((entry) => {
    const reg = registryByReview.get(entry?.reviewId);
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.uncertaintyGradient = entry?.uncertaintyGradient ?? reg?.uncertaintyGradient ?? s.uncertaintyGradient;
        s.informationGain = Number(entry?.informationGain ?? reg?.informationGain ?? s.informationGain);
        s.experimentPriority = entry?.experimentPriority ?? reg?.experimentPriority ?? s.experimentPriority;
        s.entropyReductionForecast = Number(entry?.entropyReductionForecast ?? reg?.entropyReductionForecast ?? s.entropyReductionForecast);
        s.curiosityQueueStatus = 'dashboard';
      });
    });
  });

  asArray(curiosityWatchlist?.entries).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.uncertaintyGradient = entry?.uncertaintyGradient ?? s.uncertaintyGradient;
        s.informationGain = Number(entry?.informationGain ?? s.informationGain);
        s.experimentPriority = entry?.experimentPriority ?? s.experimentPriority;
        s.entropyReductionForecast = Number(entry?.entropyReductionForecast ?? s.entropyReductionForecast);
        if (s.curiosityQueueStatus !== 'dashboard') {
          s.curiosityQueueStatus = 'watch';
        }
      });
    });
  });

  asArray(curiosityAnnotations?.annotations).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.uncertaintyGradient = entry?.uncertaintyGradient ?? s.uncertaintyGradient;
        s.informationGain = Number(entry?.informationGain ?? s.informationGain);
        s.experimentPriority = entry?.experimentPriority ?? s.experimentPriority;
        s.entropyReductionForecast = Number(entry?.entropyReductionForecast ?? s.entropyReductionForecast);
      });
    });
  });

  return byConcept;
}


function buildValueAlignmentConceptSignals(valueDashboard, knowledgePriorityRegistry, valueRiskWatchlist, valueAnnotations) {
  const byConcept = new Map();

  function bump(targetId, update) {
    if (typeof targetId !== 'string') {
      return;
    }
    const existing = byConcept.get(targetId) ?? {
      knowledgePriorityRank: 99,
      welfareImpactScore: 0,
      welfareImpactIndicator: 'monitor',
      fairnessImpactMarker: 'monitor',
      valueRiskFlag: 'bounded',
      valueRiskScore: 0,
      valueQueueStatus: 'none',
    };
    update(existing);
    byConcept.set(targetId, existing);
  }

  const registryByReview = new Map();
  asArray(knowledgePriorityRegistry?.entries).forEach((entry) => {
    if (typeof entry?.reviewId === 'string') {
      registryByReview.set(entry.reviewId, entry);
    }
  });

  asArray(valueDashboard?.entries).forEach((entry) => {
    const reg = registryByReview.get(entry?.reviewId);
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.knowledgePriorityRank = Number(entry?.knowledgePriorityRank ?? reg?.knowledgePriorityRank ?? s.knowledgePriorityRank);
        s.welfareImpactScore = Number(entry?.welfareImpactScore ?? reg?.welfareImpactScore ?? s.welfareImpactScore);
        s.welfareImpactIndicator = entry?.welfareImpactIndicator ?? reg?.welfareImpactIndicator ?? s.welfareImpactIndicator;
        s.fairnessImpactMarker = entry?.fairnessImpactMarker ?? reg?.fairnessImpactMarker ?? s.fairnessImpactMarker;
        s.valueRiskFlag = entry?.valueRiskFlag ?? reg?.valueRiskFlag ?? s.valueRiskFlag;
        s.valueRiskScore = Number(entry?.valueRiskScore ?? reg?.valueRiskScore ?? s.valueRiskScore);
        s.valueQueueStatus = 'dashboard';
      });
    });
  });

  asArray(valueRiskWatchlist?.entries).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.knowledgePriorityRank = Number(entry?.knowledgePriorityRank ?? s.knowledgePriorityRank);
        s.welfareImpactScore = Number(entry?.welfareImpactScore ?? s.welfareImpactScore);
        s.welfareImpactIndicator = entry?.welfareImpactIndicator ?? s.welfareImpactIndicator;
        s.fairnessImpactMarker = entry?.fairnessImpactMarker ?? s.fairnessImpactMarker;
        s.valueRiskFlag = entry?.valueRiskFlag ?? s.valueRiskFlag;
        s.valueRiskScore = Number(entry?.valueRiskScore ?? s.valueRiskScore);
        if (s.valueQueueStatus !== 'dashboard') {
          s.valueQueueStatus = 'watch';
        }
      });
    });
  });

  asArray(valueAnnotations?.annotations).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.knowledgePriorityRank = Number(entry?.knowledgePriorityRank ?? s.knowledgePriorityRank);
        s.welfareImpactScore = Number(entry?.welfareImpactScore ?? s.welfareImpactScore);
        s.welfareImpactIndicator = entry?.welfareImpactIndicator ?? s.welfareImpactIndicator;
        s.fairnessImpactMarker = entry?.fairnessImpactMarker ?? s.fairnessImpactMarker;
        s.valueRiskFlag = entry?.valueRiskFlag ?? s.valueRiskFlag;
        s.valueRiskScore = Number(entry?.valueRiskScore ?? s.valueRiskScore);
      });
    });
  });

  return byConcept;
}


function buildMetaCognitionConceptSignals(metaDashboard, reasoningPerformanceRegistry, metaWatchlist, metaAnnotations) {
  const byConcept = new Map();

  function bump(targetId, update) {
    if (typeof targetId !== 'string') {
      return;
    }
    const existing = byConcept.get(targetId) ?? {
      reasoningEfficiency: 0,
      patternDonorReliability: 'unknown',
      governanceConstraintPerformance: 'bounded',
      discoveryProductivity: 0,
      metaQueueStatus: 'none',
    };
    update(existing);
    byConcept.set(targetId, existing);
  }

  const registryByReview = new Map();
  asArray(reasoningPerformanceRegistry?.entries).forEach((entry) => {
    if (typeof entry?.reviewId === 'string') {
      registryByReview.set(entry.reviewId, entry);
    }
  });

  asArray(metaDashboard?.entries).forEach((entry) => {
    const reg = registryByReview.get(entry?.reviewId);
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.reasoningEfficiency = Number(entry?.reasoningEfficiency ?? reg?.reasoningEfficiency ?? s.reasoningEfficiency);
        s.patternDonorReliability = entry?.patternDonorReliability ?? reg?.patternDonorReliability ?? s.patternDonorReliability;
        s.governanceConstraintPerformance = entry?.governanceConstraintPerformance ?? reg?.governanceConstraintPerformance ?? s.governanceConstraintPerformance;
        s.discoveryProductivity = Number(entry?.discoveryProductivity ?? reg?.discoveryProductivity ?? s.discoveryProductivity);
        s.metaQueueStatus = 'dashboard';
      });
    });
  });

  asArray(metaWatchlist?.entries).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.reasoningEfficiency = Number(entry?.reasoningEfficiency ?? s.reasoningEfficiency);
        s.patternDonorReliability = entry?.patternDonorReliability ?? s.patternDonorReliability;
        s.governanceConstraintPerformance = entry?.governanceConstraintPerformance ?? s.governanceConstraintPerformance;
        s.discoveryProductivity = Number(entry?.discoveryProductivity ?? s.discoveryProductivity);
        if (s.metaQueueStatus !== 'dashboard') {
          s.metaQueueStatus = 'watch';
        }
      });
    });
  });

  asArray(metaAnnotations?.annotations).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.reasoningEfficiency = Number(entry?.reasoningEfficiency ?? s.reasoningEfficiency);
        s.patternDonorReliability = entry?.patternDonorReliability ?? s.patternDonorReliability;
        s.governanceConstraintPerformance = entry?.governanceConstraintPerformance ?? s.governanceConstraintPerformance;
        s.discoveryProductivity = Number(entry?.discoveryProductivity ?? s.discoveryProductivity);
      });
    });
  });

  return byConcept;
}


function buildArchitectureConceptSignals(architectureDashboard, modulePerformanceRegistry, architectureWatchlist, architectureAnnotations) {
  const byConcept = new Map();

  function bump(targetId, update) {
    if (typeof targetId !== 'string') {
      return;
    }
    const existing = byConcept.get(targetId) ?? {
      modulePerformance: 'monitor',
      modulePerformanceScore: 0,
      architectureDiscoveryProductivity: 0,
      safeguardPerformance: 'bounded',
      architectureImprovementProposal: 'none',
      architectureQueueStatus: 'none',
    };
    update(existing);
    byConcept.set(targetId, existing);
  }

  const registryByReview = new Map();
  asArray(modulePerformanceRegistry?.entries).forEach((entry) => {
    if (typeof entry?.reviewId === 'string') {
      registryByReview.set(entry.reviewId, entry);
    }
  });

  asArray(architectureDashboard?.entries).forEach((entry) => {
    const reg = registryByReview.get(entry?.reviewId);
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.modulePerformance = entry?.modulePerformance ?? reg?.modulePerformance ?? s.modulePerformance;
        s.modulePerformanceScore = Number(entry?.modulePerformanceScore ?? reg?.modulePerformanceScore ?? s.modulePerformanceScore);
        s.architectureDiscoveryProductivity = Number(entry?.discoveryProductivity ?? reg?.discoveryProductivity ?? s.architectureDiscoveryProductivity);
        s.safeguardPerformance = entry?.safeguardPerformance ?? reg?.safeguardPerformance ?? s.safeguardPerformance;
        s.architectureImprovementProposal = entry?.architectureImprovementProposal ?? reg?.architectureImprovementProposal ?? s.architectureImprovementProposal;
        s.architectureQueueStatus = 'dashboard';
      });
    });
  });

  asArray(architectureWatchlist?.entries).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.modulePerformance = entry?.modulePerformance ?? s.modulePerformance;
        s.modulePerformanceScore = Number(entry?.modulePerformanceScore ?? s.modulePerformanceScore);
        s.architectureDiscoveryProductivity = Number(entry?.discoveryProductivity ?? s.architectureDiscoveryProductivity);
        s.safeguardPerformance = entry?.safeguardPerformance ?? s.safeguardPerformance;
        s.architectureImprovementProposal = entry?.architectureImprovementProposal ?? s.architectureImprovementProposal;
        if (s.architectureQueueStatus !== 'dashboard') {
          s.architectureQueueStatus = 'watch';
        }
      });
    });
  });

  asArray(architectureAnnotations?.annotations).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.modulePerformance = entry?.modulePerformance ?? s.modulePerformance;
        s.modulePerformanceScore = Number(entry?.modulePerformanceScore ?? s.modulePerformanceScore);
        s.architectureDiscoveryProductivity = Number(entry?.discoveryProductivity ?? s.architectureDiscoveryProductivity);
        s.safeguardPerformance = entry?.safeguardPerformance ?? s.safeguardPerformance;
        s.architectureImprovementProposal = entry?.architectureImprovementProposal ?? s.architectureImprovementProposal;
      });
    });
  });

  return byConcept;
}


function buildSocialEntropyConceptSignals(socialEntropyDashboard, civicCohesionRegistry, legitimacyWatchlist, socialRepairAnnotations) {
  const byConcept = new Map();

  function bump(targetId, update) {
    if (typeof targetId !== 'string') {
      return;
    }
    const existing = byConcept.get(targetId) ?? {
      socialStatus: 'monitor',
      cohesionClass: 'mixed',
      legitimacyDrift: 'bounded',
      reviewerConcentration: 0,
      reviewerFatigue: 'bounded',
      repairPriority: 'routine',
      socialQueueStatus: 'none',
    };
    update(existing);
    byConcept.set(targetId, existing);
  }

  const registryByReview = new Map();
  asArray(civicCohesionRegistry?.entries).forEach((entry) => {
    if (typeof entry?.reviewId === 'string') {
      registryByReview.set(entry.reviewId, entry);
    }
  });

  asArray(socialEntropyDashboard?.entries).forEach((entry) => {
    const reg = registryByReview.get(entry?.reviewId);
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.socialStatus = entry?.socialStatus ?? reg?.socialStatus ?? s.socialStatus;
        s.cohesionClass = entry?.cohesionClass ?? reg?.cohesionClass ?? s.cohesionClass;
        s.legitimacyDrift = entry?.legitimacyDrift ?? reg?.legitimacyDrift ?? s.legitimacyDrift;
        s.reviewerConcentration = Number(entry?.reviewerConcentration ?? reg?.reviewerConcentration ?? s.reviewerConcentration);
        s.reviewerFatigue = entry?.reviewerFatigue ?? reg?.reviewerFatigue ?? s.reviewerFatigue;
        s.repairPriority = entry?.repairPriority ?? reg?.repairPriority ?? s.repairPriority;
        s.socialQueueStatus = 'dashboard';
      });
    });
  });

  asArray(legitimacyWatchlist?.entries).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.socialStatus = entry?.socialStatus ?? s.socialStatus;
        s.cohesionClass = entry?.cohesionClass ?? s.cohesionClass;
        s.legitimacyDrift = entry?.legitimacyDrift ?? s.legitimacyDrift;
        s.reviewerConcentration = Number(entry?.reviewerConcentration ?? s.reviewerConcentration);
        s.reviewerFatigue = entry?.reviewerFatigue ?? s.reviewerFatigue;
        s.repairPriority = entry?.repairPriority ?? s.repairPriority;
        if (s.socialQueueStatus !== 'dashboard') {
          s.socialQueueStatus = 'watch';
        }
      });
    });
  });

  asArray(socialRepairAnnotations?.annotations).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.socialStatus = entry?.socialStatus ?? s.socialStatus;
        s.cohesionClass = entry?.cohesionClass ?? s.cohesionClass;
        s.legitimacyDrift = entry?.legitimacyDrift ?? s.legitimacyDrift;
        s.reviewerConcentration = Number(entry?.reviewerConcentration ?? s.reviewerConcentration);
        s.reviewerFatigue = entry?.reviewerFatigue ?? s.reviewerFatigue;
        s.repairPriority = entry?.repairPriority ?? s.repairPriority;
      });
    });
  });

  return byConcept;
}


function buildFederatedGovernanceConceptSignals(federationDashboard, stewardshipRegistry, captureWatchlist, federationAnnotations) {
  const byConcept = new Map();

  function bump(targetId, update) {
    if (typeof targetId !== 'string') {
      return;
    }
    const existing = byConcept.get(targetId) ?? {
      federationStatus: 'monitor',
      stewardshipNodeClass: 'bounded',
      dissentPortability: 'bounded',
      captureRisk: 'bounded',
      legitimacySignal: 'stable',
      mitigationRequirement: 'monitor',
      captureRiskScore: 0,
      federationQueueStatus: 'none',
    };
    update(existing);
    byConcept.set(targetId, existing);
  }

  const registryByReview = new Map();
  asArray(stewardshipRegistry?.entries).forEach((entry) => {
    if (typeof entry?.reviewId === 'string') {
      registryByReview.set(entry.reviewId, entry);
    }
  });

  asArray(federationDashboard?.entries).forEach((entry) => {
    const reg = registryByReview.get(entry?.reviewId);
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.federationStatus = entry?.federationStatus ?? reg?.federationStatus ?? s.federationStatus;
        s.stewardshipNodeClass = entry?.nodeClass ?? reg?.nodeClass ?? s.stewardshipNodeClass;
        s.dissentPortability = entry?.dissentPortability ?? reg?.dissentPortability ?? s.dissentPortability;
        s.captureRisk = entry?.captureRisk ?? reg?.captureRisk ?? s.captureRisk;
        s.legitimacySignal = entry?.legitimacySignal ?? reg?.legitimacySignal ?? s.legitimacySignal;
        s.mitigationRequirement = entry?.mitigationRequirement ?? reg?.mitigationRequirement ?? s.mitigationRequirement;
        s.captureRiskScore = Number(entry?.captureRiskScore ?? reg?.captureRiskScore ?? s.captureRiskScore);
        s.federationQueueStatus = 'dashboard';
      });
    });
  });

  asArray(captureWatchlist?.entries).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.federationStatus = entry?.federationStatus ?? s.federationStatus;
        s.stewardshipNodeClass = entry?.nodeClass ?? s.stewardshipNodeClass;
        s.dissentPortability = entry?.dissentPortability ?? s.dissentPortability;
        s.captureRisk = entry?.captureRisk ?? s.captureRisk;
        s.legitimacySignal = entry?.legitimacySignal ?? s.legitimacySignal;
        s.mitigationRequirement = entry?.mitigationRequirement ?? s.mitigationRequirement;
        s.captureRiskScore = Number(entry?.captureRiskScore ?? s.captureRiskScore);
        if (s.federationQueueStatus !== 'dashboard') {
          s.federationQueueStatus = 'watch';
        }
      });
    });
  });

  asArray(federationAnnotations?.annotations).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.federationStatus = entry?.federationStatus ?? s.federationStatus;
        s.stewardshipNodeClass = entry?.nodeClass ?? s.stewardshipNodeClass;
        s.dissentPortability = entry?.dissentPortability ?? s.dissentPortability;
        s.captureRisk = entry?.captureRisk ?? s.captureRisk;
        s.legitimacySignal = entry?.legitimacySignal ?? s.legitimacySignal;
        s.mitigationRequirement = entry?.mitigationRequirement ?? s.mitigationRequirement;
        s.captureRiskScore = Number(entry?.captureRiskScore ?? s.captureRiskScore);
      });
    });
  });

  return byConcept;
}


function buildEmergentDomainConceptSignals(emergentDomainDashboard, domainBirthRegistry, domainBoundaryWatchlist, emergentDomainAnnotations) {
  const byConcept = new Map();

  function bump(targetId, update) {
    if (typeof targetId !== 'string') {
      return;
    }
    const existing = byConcept.get(targetId) ?? {
      domainStatus: 'monitor',
      sourceDomains: [],
      invariantPatternClass: 'unclassified',
      fieldBirthPressure: 'bounded',
      fieldBirthPressureScore: 0,
      domainBoundaryFailure: 'bounded',
      commonsLegibilityRequirement: 'required',
      emergentDomainQueueStatus: 'none',
    };
    update(existing);
    existing.sourceDomains = Array.from(new Set(asArray(existing.sourceDomains).filter((v) => typeof v === 'string'))).sort();
    byConcept.set(targetId, existing);
  }

  const registryByReview = new Map();
  asArray(domainBirthRegistry?.entries).forEach((entry) => {
    if (typeof entry?.reviewId === 'string') {
      registryByReview.set(entry.reviewId, entry);
    }
  });

  asArray(emergentDomainDashboard?.entries).forEach((entry) => {
    const reg = registryByReview.get(entry?.reviewId);
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.domainStatus = entry?.domainStatus ?? reg?.domainStatus ?? s.domainStatus;
        s.sourceDomains = asArray(entry?.sourceDomains ?? reg?.sourceDomains ?? s.sourceDomains);
        s.invariantPatternClass = entry?.invariantPatternClass ?? reg?.invariantPatternClass ?? s.invariantPatternClass;
        s.fieldBirthPressure = entry?.fieldBirthPressure ?? reg?.fieldBirthPressure ?? s.fieldBirthPressure;
        s.fieldBirthPressureScore = Number(entry?.fieldBirthPressureScore ?? reg?.fieldBirthPressureScore ?? s.fieldBirthPressureScore);
        s.domainBoundaryFailure = entry?.domainBoundaryFailure ?? reg?.domainBoundaryFailure ?? s.domainBoundaryFailure;
        s.commonsLegibilityRequirement = entry?.commonsLegibilityRequirement ?? reg?.commonsLegibilityRequirement ?? s.commonsLegibilityRequirement;
        s.emergentDomainQueueStatus = 'dashboard';
      });
    });
  });

  asArray(domainBoundaryWatchlist?.entries).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.domainStatus = entry?.domainStatus ?? s.domainStatus;
        s.sourceDomains = asArray(entry?.sourceDomains ?? s.sourceDomains);
        s.invariantPatternClass = entry?.invariantPatternClass ?? s.invariantPatternClass;
        s.fieldBirthPressure = entry?.fieldBirthPressure ?? s.fieldBirthPressure;
        s.fieldBirthPressureScore = Number(entry?.fieldBirthPressureScore ?? s.fieldBirthPressureScore);
        s.domainBoundaryFailure = entry?.domainBoundaryFailure ?? s.domainBoundaryFailure;
        s.commonsLegibilityRequirement = entry?.commonsLegibilityRequirement ?? s.commonsLegibilityRequirement;
        if (s.emergentDomainQueueStatus !== 'dashboard') {
          s.emergentDomainQueueStatus = 'watch';
        }
      });
    });
  });

  asArray(emergentDomainAnnotations?.annotations).forEach((entry) => {
    asArray(entry?.linkedTargetIds).forEach((targetId) => {
      bump(targetId, (s) => {
        s.domainStatus = entry?.domainStatus ?? s.domainStatus;
        s.sourceDomains = asArray(entry?.sourceDomains ?? s.sourceDomains);
        s.invariantPatternClass = entry?.invariantPatternClass ?? s.invariantPatternClass;
        s.fieldBirthPressure = entry?.fieldBirthPressure ?? s.fieldBirthPressure;
        s.fieldBirthPressureScore = Number(entry?.fieldBirthPressureScore ?? s.fieldBirthPressureScore);
        s.domainBoundaryFailure = entry?.domainBoundaryFailure ?? s.domainBoundaryFailure;
        s.commonsLegibilityRequirement = entry?.commonsLegibilityRequirement ?? s.commonsLegibilityRequirement;
      });
    });
  });

  return byConcept;
}

function buildConstitutionalConceptSignals(constitutionalAnnotations, governanceFailureWatchlist) {
  const byConcept = new Map();

  const watchByArtifact = new Map();
  asArray(governanceFailureWatchlist?.entries).forEach((entry) => {
    if (typeof entry?.artifactId === 'string') {
      watchByArtifact.set(entry.artifactId, entry);
    }
  });

  asArray(constitutionalAnnotations?.annotations).forEach((entry) => {
    const artifactId = entry?.artifactId;
    if (typeof artifactId !== 'string') {
      return;
    }
    const watch = watchByArtifact.get(artifactId);
    asArray(watch?.linkedTargetIds).forEach((targetId) => {
      if (typeof targetId !== 'string') {
        return;
      }
      byConcept.set(targetId, {
        constitutionalStatus: entry?.constitutionalStatus ?? 'watch',
        freezeRecommendation: watch?.watchStatus === 'freeze-recommended',
        constitutionalWatchStatus: watch?.watchStatus ?? 'none'
      });
    });
  });

  return byConcept;
}

export function applyAttentionOverlay(cy, overlay) {
  const conceptWeights = overlay?.coherenceWeights?.conceptWeights ?? {};
  const conceptAnnotations = overlay?.sophiaAnnotations?.conceptAnnotations ?? {};
  const fallbackAssessmentNotes = overlay?.coherenceAssessment?.conceptNotes ?? {};
  const canonicalAttention = normalizeCanonicalAttention(
    overlay?.attentionUpdates,
    overlay?.sophiaAttentionState
  );
  const byConcept = rankingIndex(canonicalAttention);
  const sonyaSignals = buildSonyaConceptSignals(overlay?.sonyaMemoryIndex, overlay?.sonyaAttentionCandidates);
  const reasoningSignals = buildReasoningConceptSignals(overlay?.reasoningThreads, overlay?.cognitiveWatchlist);
  const monitorSignals = buildCognitiveMonitorConceptSignals(
    overlay?.reasoningThreads,
    overlay?.cognitiveMonitorIndex,
    overlay?.recursiveWatchHistory
  );
  const multimodalSignals = buildMultimodalConceptSignals(
    overlay?.multimodalSignalIndex,
    overlay?.crossModalAttentionOverlays,
    overlay?.patternDonationWatchlist
  );
  const promotionSignals = buildPromotionConceptSignals(overlay?.reviewDocket, overlay?.promotionWatchQueue);
  const governanceSignals = buildGovernanceConceptSignals(
    overlay?.governanceReviewDocket,
    overlay?.reviewerWatchQueue,
    overlay?.reviewerBehaviorMonitor
  );
  const constitutionalSignals = buildConstitutionalConceptSignals(
    overlay?.constitutionalAnnotations,
    overlay?.governanceFailureWatchlist
  );
  const deliberationSignals = buildDeliberationConceptSignals(
    overlay?.deliberationDocket,
    overlay?.amendmentQueue,
    overlay?.quorumWatchlist,
    overlay?.constitutionalRevisionAnnotations
  );
  const continuitySignals = buildContinuityConceptSignals(
    overlay?.continuityRoster,
    overlay?.successionDocket,
    overlay?.quorumResilienceWatchlist,
    overlay?.governanceRedundancyAnnotations
  );
  const recoverySignals = buildRecoveryConceptSignals(
    overlay?.escrowIndex,
    overlay?.recoveryDocket,
    overlay?.integrityWatchlist,
    overlay?.recoveryAnnotations
  );
  const attestationSignals = buildAttestationConceptSignals(
    overlay?.attestationRegistry,
    overlay?.witnessDocket,
    overlay?.integrityTestimonyWatchlist,
    overlay?.attestationAnnotations
  );
  const precedentSignals = buildPrecedentConceptSignals(
    overlay?.precedentRegistry,
    overlay?.caseDocket,
    overlay?.divergenceWatchlist,
    overlay?.precedentAnnotations
  );
  const scenarioSignals = buildScenarioConceptSignals(
    overlay?.scenarioRegistry,
    overlay?.stressTestDocket,
    overlay?.resilienceFindingsWatchlist,
    overlay?.scenarioAnnotations
  );
  const institutionalSignals = buildInstitutionalConceptSignals(
    overlay?.institutionalStatus,
    overlay?.systemHealthDashboard,
    overlay?.institutionalConflictWatchlist,
    overlay?.institutionalAnnotations
  );
  const queueHealthSignals = buildQueueHealthConceptSignals(
    overlay?.queueHealthDashboard,
    overlay?.reviewBacklogWatchlist,
    overlay?.metricGamingWatchlist,
    overlay?.loadSheddingAnnotations
  );
  const prioritySignals = buildPriorityConceptSignals(
    overlay?.priorityDashboard,
    overlay?.triageDocket,
    overlay?.triageWatchlist,
    overlay?.priorityAnnotations
  );
  const closureSignals = buildClosureConceptSignals(
    overlay?.closureRegistry,
    overlay?.repairDocket,
    overlay?.reopenedCaseWatchlist,
    overlay?.closureAnnotations
  );
  const symbolicFieldSignals = buildSymbolicFieldConceptSignals(
    overlay?.symbolicFieldRegistry,
    overlay?.earlyWarningDashboard,
    overlay?.regimeWatchlist,
    overlay?.symbolicFieldAnnotations
  );
  const verificationSignals = buildVerificationConceptSignals(
    overlay?.verificationDashboard,
    overlay?.entityWatchlist,
    overlay?.claimTypeRegistry,
    overlay?.verificationAnnotations
  );
  const publicRecordSignals = buildPublicRecordConceptSignals(
    overlay?.publicRecordDashboard,
    overlay?.entityGraphRegistry,
    overlay?.relationshipWatchlist,
    overlay?.chainOfCustodyAnnotations
  );
  const investigationSignals = buildInvestigationConceptSignals(
    overlay?.investigationDashboard,
    overlay?.investigationPlanRegistry,
    overlay?.investigationWatchlist,
    overlay?.investigationAnnotations
  );
  const authoritySignals = buildEvidenceAuthorityConceptSignals(
    overlay?.authorityGateDashboard,
    overlay?.weakEvidenceWatchlist,
    overlay?.propagationAnnotations,
    overlay?.maturityRestrictionRegistry
  );
  const reviewPacketSignals = buildReviewPacketConceptSignals(
    overlay?.reviewPacketDashboard,
    overlay?.reviewPacketRegistry,
    overlay?.uncertaintyWatchlist,
    overlay?.reviewPacketAnnotations
  );
  const patternSignals = buildPatternConceptSignals(
    overlay?.patternDashboard,
    overlay?.patternRegistry,
    overlay?.patternWatchlist,
    overlay?.patternAnnotations
  );
  const patternTemporalSignals = buildPatternTemporalConceptSignals(
    overlay?.patternTimelineDashboard,
    overlay?.patternPersistenceRegistry,
    overlay?.patternTemporalWatchlist,
    overlay?.patternTemporalAnnotations
  );
  const causalSignals = buildCausalConceptSignals(
    overlay?.causalDashboard,
    overlay?.mechanismRegistry,
    overlay?.causalWatchlist,
    overlay?.causalAnnotations
  );
  const collaborativeSignals = buildCollaborativeConceptSignals(
    overlay?.collaborativeReviewDashboard,
    overlay?.consensusRegistry,
    overlay?.dissentWatchlist,
    overlay?.deliberationAnnotations
  );
  const telemetrySignals = buildTelemetryConceptSignals(
    overlay?.telemetryDashboard,
    overlay?.latticeProjectionRegistry,
    overlay?.patternDonationWatchlist,
    overlay?.actionFunctionalAnnotations
  );
  const branchSignals = buildBranchLifecycleConceptSignals(
    overlay?.branchDashboard,
    overlay?.branchRegistry,
    overlay?.branchWatchlist,
    overlay?.branchAnnotations
  );
  const predictionSignals = buildPredictionConceptSignals(
    overlay?.predictionDashboard,
    overlay?.forecastRegistry,
    overlay?.predictionWatchlist,
    overlay?.calibrationAnnotations
  );
  const experimentalSignals = buildExperimentalConceptSignals(
    overlay?.experimentDashboard,
    overlay?.hypothesisRegistry,
    overlay?.falsificationWatchlist,
    overlay?.theoryGateAnnotations
  );
  const theorySignals = buildTheoryCorpusConceptSignals(
    overlay?.theoryDashboard,
    overlay?.theoryRegistry,
    overlay?.negativeResultWatchlist,
    overlay?.theoryAnnotations
  );
  const agencySignals = buildAgencyModeConceptSignals(
    overlay?.agencyModeDashboard,
    overlay?.agencyFitRegistry,
    overlay?.agencyDisagreementWatchlist,
    overlay?.agencyGovernanceAnnotations
  );
  const responsibilitySignals = buildResponsibilityConceptSignals(
    overlay?.responsibilityDashboard,
    overlay?.supportRegistry,
    overlay?.interventionWatchlist,
    overlay?.responsibilityAnnotations
  );
  const transferSignals = buildTheoryTransferConceptSignals(
    overlay?.transferDashboard,
    overlay?.theoryTransferRegistry,
    overlay?.transferWatchlist,
    overlay?.transferAnnotations
  );
  const systemForecastSignals = buildSystemForecastConceptSignals(
    overlay?.systemForecastDashboard,
    overlay?.regimeTransitionRegistry,
    overlay?.trajectoryWatchlist,
    overlay?.systemForecastAnnotations
  );
  const informationValueSignals = buildInformationValueConceptSignals(
    overlay?.uncertaintyDashboard,
    overlay?.observationPriorityRegistry,
    overlay?.curiosityWatchlist,
    overlay?.curiosityAnnotations
  );
  const valueAlignmentSignals = buildValueAlignmentConceptSignals(
    overlay?.valueDashboard,
    overlay?.knowledgePriorityRegistry,
    overlay?.valueRiskWatchlist,
    overlay?.valueAnnotations
  );
  const metaCognitionSignals = buildMetaCognitionConceptSignals(
    overlay?.metaDashboard,
    overlay?.reasoningPerformanceRegistry,
    overlay?.metaWatchlist,
    overlay?.metaAnnotations
  );
  const architectureSignals = buildArchitectureConceptSignals(
    overlay?.architectureDashboard,
    overlay?.modulePerformanceRegistry,
    overlay?.architectureWatchlist,
    overlay?.architectureAnnotations
  );
  const socialEntropySignals = buildSocialEntropyConceptSignals(
    overlay?.socialEntropyDashboard,
    overlay?.civicCohesionRegistry,
    overlay?.legitimacyWatchlist,
    overlay?.socialRepairAnnotations
  );
  const federatedGovernanceSignals = buildFederatedGovernanceConceptSignals(
    overlay?.federationDashboard,
    overlay?.stewardshipRegistry,
    overlay?.captureWatchlist,
    overlay?.federationAnnotations
  );
  const emergentDomainSignals = buildEmergentDomainConceptSignals(
    overlay?.emergentDomainDashboard,
    overlay?.domainBirthRegistry,
    overlay?.domainBoundaryWatchlist,
    overlay?.emergentDomainAnnotations
  );

  const institutionalProvenance = overlay?.institutionalStatus?.provenance ?? {};
  const institutionalSchemaVersion = institutionalProvenance?.schemaVersions?.institutional_state_summary
    ?? institutionalProvenance?.schemaVersions?.institutional_state_map
    ?? 'unknown';
  const institutionalProducerCommits = asArray(institutionalProvenance?.producerCommits).join(', ') || 'unknown';
  const institutionalSourceMode = institutionalProvenance?.derivedFromFixtures ? 'fixture' : 'live';
  const queueProvenance = overlay?.queueHealthDashboard?.provenance ?? {};
  const queueHealthSchemaVersion = queueProvenance?.schemaVersions?.queue_pressure_summary
    ?? queueProvenance?.schemaVersions?.queue_pressure_map
    ?? 'unknown';
  const queueHealthProducerCommits = asArray(queueProvenance?.producerCommits).join(', ') || 'unknown';
  const queueHealthSourceMode = queueProvenance?.derivedFromFixtures ? 'fixture' : 'live';
  const priorityProvenance = overlay?.priorityDashboard?.provenance ?? {};
  const prioritySchemaVersion = priorityProvenance?.schemaVersions?.priority_state_summary
    ?? priorityProvenance?.schemaVersions?.priority_state_map
    ?? 'unknown';
  const priorityProducerCommits = asArray(priorityProvenance?.producerCommits).join(', ') || 'unknown';
  const prioritySourceMode = priorityProvenance?.derivedFromFixtures ? 'fixture' : 'live';
  const closureProvenance = overlay?.closureRegistry?.provenance ?? {};
  const closureSchemaVersion = closureProvenance?.schemaVersions?.closure_state_summary
    ?? closureProvenance?.schemaVersions?.closure_state_map
    ?? 'unknown';
  const closureProducerCommits = asArray(closureProvenance?.producerCommits).join(', ') || 'unknown';
  const closureSourceMode = closureProvenance?.derivedFromFixtures ? 'fixture' : 'live';
  const symbolicFieldProvenance = overlay?.symbolicFieldRegistry?.provenance ?? {};
  const symbolicFieldSchemaVersion = symbolicFieldProvenance?.schemaVersions?.symbolic_field_summary
    ?? symbolicFieldProvenance?.schemaVersions?.symbolic_field_state
    ?? 'unknown';
  const symbolicFieldProducerCommits = asArray(symbolicFieldProvenance?.producerCommits).join(', ') || 'unknown';
  const symbolicFieldSourceMode = symbolicFieldProvenance?.derivedFromFixtures ? 'fixture' : 'live';
  const verificationProvenance = overlay?.verificationDashboard?.provenance ?? {};
  const verificationSchemaVersion = verificationProvenance?.schemaVersions?.entity_resolution_summary
    ?? verificationProvenance?.schemaVersions?.entity_resolution_map
    ?? 'unknown';
  const verificationProducerCommits = asArray(verificationProvenance?.producerCommits).join(', ') || 'unknown';
  const verificationSourceMode = verificationProvenance?.derivedFromFixtures ? 'fixture' : 'live';
  const publicRecordProvenance = overlay?.publicRecordDashboard?.provenance ?? {};
  const publicRecordSchemaVersion = publicRecordProvenance?.schemaVersions?.public_record_intake_map
    ?? publicRecordProvenance?.schemaVersions?.entity_graph_map
    ?? 'unknown';
  const publicRecordProducerCommits = asArray(publicRecordProvenance?.producerCommits).join(', ') || 'unknown';
  const publicRecordSourceMode = publicRecordProvenance?.derivedFromFixtures ? 'fixture' : 'live';
  const investigationProvenance = overlay?.investigationDashboard?.provenance ?? {};
  const investigationSchemaVersion = investigationProvenance?.schemaVersions?.triage_recommendations
    ?? investigationProvenance?.schemaVersions?.verification_recommendations
    ?? 'unknown';
  const investigationProducerCommits = asArray(investigationProvenance?.producerCommits).join(', ') || 'unknown';
  const investigationSourceMode = investigationProvenance?.derivedFromFixtures ? 'fixture' : 'live';
  const authorityProvenance = overlay?.authorityGateDashboard?.provenance ?? {};
  const authoritySchemaVersion = authorityProvenance?.schemaVersions?.evidence_authority_summary
    ?? authorityProvenance?.schemaVersions?.evidence_authority_map
    ?? 'unknown';
  const authorityProducerCommits = asArray(authorityProvenance?.producerCommits).join(', ') || 'unknown';
  const authoritySourceMode = authorityProvenance?.derivedFromFixtures ? 'fixture' : 'live';
  const reviewPacketProvenance = overlay?.reviewPacketDashboard?.provenance ?? {};
  const reviewPacketSchemaVersion = reviewPacketProvenance?.schemaVersions?.review_packet_summary
    ?? reviewPacketProvenance?.schemaVersions?.review_packet_map
    ?? 'unknown';
  const reviewPacketProducerCommits = asArray(reviewPacketProvenance?.producerCommits).join(', ') || 'unknown';
  const reviewPacketSourceMode = reviewPacketProvenance?.derivedFromFixtures ? 'fixture' : 'live';
  const patternProvenance = overlay?.patternDashboard?.provenance ?? {};
  const patternSchemaVersion = patternProvenance?.schemaVersions?.pattern_maturity_map
    ?? patternProvenance?.schemaVersions?.pattern_cluster_map
    ?? 'unknown';
  const patternProducerCommits = asArray(patternProvenance?.producerCommits).join(', ') || 'unknown';
  const patternSourceMode = patternProvenance?.derivedFromFixtures ? 'fixture' : 'live';
  const patternTemporalProvenance = overlay?.patternTimelineDashboard?.provenance ?? {};
  const patternTemporalSchemaVersion = patternTemporalProvenance?.schemaVersions?.pattern_persistence_map
    ?? patternTemporalProvenance?.schemaVersions?.pattern_timeline_map
    ?? 'unknown';
  const patternTemporalProducerCommits = asArray(patternTemporalProvenance?.producerCommits).join(', ') || 'unknown';
  const patternTemporalSourceMode = patternTemporalProvenance?.derivedFromFixtures ? 'fixture' : 'live';
  const causalProvenance = overlay?.causalDashboard?.provenance ?? {};
  const causalSchemaVersion = causalProvenance?.schemaVersions?.mechanism_separation_report
    ?? causalProvenance?.schemaVersions?.causal_bundle_map
    ?? 'unknown';
  const causalProducerCommits = asArray(causalProvenance?.producerCommits).join(', ') || 'unknown';
  const causalSourceMode = causalProvenance?.derivedFromFixtures ? 'fixture' : 'live';
  const collaborativeProvenance = overlay?.collaborativeReviewDashboard?.provenance ?? {};
  const collaborativeSchemaVersion = collaborativeProvenance?.schemaVersions?.consensus_state_report
    ?? collaborativeProvenance?.schemaVersions?.reviewer_position_map
    ?? 'unknown';
  const collaborativeProducerCommits = asArray(collaborativeProvenance?.producerCommits).join(', ') || 'unknown';
  const collaborativeSourceMode = collaborativeProvenance?.derivedFromFixtures ? 'fixture' : 'live';
  const telemetryProvenance = overlay?.telemetryDashboard?.provenance ?? {};
  const telemetrySchemaVersion = telemetryProvenance?.schemaVersions?.action_functional_scorecard
    ?? telemetryProvenance?.schemaVersions?.telemetry_field_map
    ?? 'unknown';
  const telemetryProducerCommits = asArray(telemetryProvenance?.producerCommits).join(', ') || 'unknown';
  const telemetrySourceMode = telemetryProvenance?.derivedFromFixtures ? 'fixture' : 'live';
  const branchProvenance = overlay?.branchDashboard?.provenance ?? {};
  const branchSchemaVersion = branchProvenance?.schemaVersions?.branch_state_map
    ?? branchProvenance?.schemaVersions?.branch_conflict_graph
    ?? 'unknown';
  const branchProducerCommits = asArray(branchProvenance?.producerCommits).join(', ') || 'unknown';
  const branchSourceMode = branchProvenance?.derivedFromFixtures ? 'fixture' : 'live';
  const predictionProvenance = overlay?.predictionDashboard?.provenance ?? {};
  const predictionSchemaVersion = predictionProvenance?.schemaVersions?.forecast_map
    ?? predictionProvenance?.schemaVersions?.calibration_report
    ?? 'unknown';
  const predictionProducerCommits = asArray(predictionProvenance?.producerCommits).join(', ') || 'unknown';
  const predictionSourceMode = predictionProvenance?.derivedFromFixtures ? 'fixture' : 'live';
  const experimentalProvenance = overlay?.experimentDashboard?.provenance ?? {};
  const experimentalSchemaVersion = experimentalProvenance?.schemaVersions?.experimental_hypothesis_map
    ?? experimentalProvenance?.schemaVersions?.falsification_design_report
    ?? 'unknown';
  const experimentalProducerCommits = asArray(experimentalProvenance?.producerCommits).join(', ') || 'unknown';
  const experimentalSourceMode = experimentalProvenance?.derivedFromFixtures ? 'fixture' : 'live';
  const theoryProvenance = overlay?.theoryDashboard?.provenance ?? {};
  const theorySchemaVersion = theoryProvenance?.schemaVersions?.theory_corpus_map
    ?? theoryProvenance?.schemaVersions?.theory_revision_lineage
    ?? 'unknown';
  const theoryProducerCommits = asArray(theoryProvenance?.producerCommits).join(', ') || 'unknown';
  const theorySourceMode = theoryProvenance?.derivedFromFixtures ? 'fixture' : 'live';
  const agencyProvenance = overlay?.agencyModeDashboard?.provenance ?? {};
  const agencySchemaVersion = agencyProvenance?.schemaVersions?.agency_mode_hypothesis_map
    ?? agencyProvenance?.schemaVersions?.agency_fit_comparison_report
    ?? 'unknown';
  const agencyProducerCommits = asArray(agencyProvenance?.producerCommits).join(', ') || 'unknown';
  const agencySourceMode = agencyProvenance?.derivedFromFixtures ? 'fixture' : 'live';
  const responsibilityProvenance = overlay?.responsibilityDashboard?.provenance ?? {};
  const responsibilitySchemaVersion = responsibilityProvenance?.schemaVersions?.responsibility_mode_map
    ?? responsibilityProvenance?.schemaVersions?.support_pathway_map
    ?? 'unknown';
  const responsibilityProducerCommits = asArray(responsibilityProvenance?.producerCommits).join(', ') || 'unknown';
  const responsibilitySourceMode = responsibilityProvenance?.derivedFromFixtures ? 'fixture' : 'live';
  const transferProvenance = overlay?.transferDashboard?.provenance ?? {};
  const transferSchemaVersion = transferProvenance?.schemaVersions?.theory_transfer_map
    ?? transferProvenance?.schemaVersions?.donor_target_asymmetry_report
    ?? 'unknown';
  const transferProducerCommits = asArray(transferProvenance?.producerCommits).join(', ') || 'unknown';
  const transferSourceMode = transferProvenance?.derivedFromFixtures ? 'fixture' : 'live';
  const systemForecastProvenance = overlay?.systemForecastDashboard?.provenance ?? {};
  const systemForecastSchemaVersion = systemForecastProvenance?.schemaVersions?.theory_transfer_map
    ?? systemForecastProvenance?.schemaVersions?.transfer_replication_gate
    ?? 'unknown';
  const systemForecastProducerCommits = asArray(systemForecastProvenance?.producerCommits).join(', ') || 'unknown';
  const systemForecastSourceMode = systemForecastProvenance?.derivedFromFixtures ? 'fixture' : 'live';
  const informationValueProvenance = overlay?.uncertaintyDashboard?.provenance ?? {};
  const informationValueSchemaVersion = informationValueProvenance?.schemaVersions?.uncertainty_map
    ?? informationValueProvenance?.schemaVersions?.information_gain_report
    ?? 'unknown';
  const informationValueProducerCommits = asArray(informationValueProvenance?.producerCommits).join(', ') || 'unknown';
  const informationValueSourceMode = informationValueProvenance?.derivedFromFixtures ? 'fixture' : 'live';
  const valueAlignmentProvenance = overlay?.valueDashboard?.provenance ?? {};
  const valueAlignmentSchemaVersion = valueAlignmentProvenance?.schemaVersions?.knowledge_priority_map
    ?? valueAlignmentProvenance?.schemaVersions?.welfare_impact_report
    ?? 'unknown';
  const valueAlignmentProducerCommits = asArray(valueAlignmentProvenance?.producerCommits).join(', ') || 'unknown';
  const valueAlignmentSourceMode = valueAlignmentProvenance?.derivedFromFixtures ? 'fixture' : 'live';
  const metaCognitionProvenance = overlay?.metaDashboard?.provenance ?? {};
  const metaCognitionSchemaVersion = metaCognitionProvenance?.schemaVersions?.reasoning_efficiency_report
    ?? metaCognitionProvenance?.schemaVersions?.meta_cognition_recommendations
    ?? 'unknown';
  const metaCognitionProducerCommits = asArray(metaCognitionProvenance?.producerCommits).join(', ') || 'unknown';
  const metaCognitionSourceMode = metaCognitionProvenance?.derivedFromFixtures ? 'fixture' : 'live';
  const architectureProvenance = overlay?.architectureDashboard?.provenance ?? {};
  const architectureSchemaVersion = architectureProvenance?.schemaVersions?.module_performance_report
    ?? architectureProvenance?.schemaVersions?.safeguard_performance_report
    ?? 'unknown';
  const architectureProducerCommits = asArray(architectureProvenance?.producerCommits).join(', ') || 'unknown';
  const architectureSourceMode = architectureProvenance?.derivedFromFixtures ? 'fixture' : 'live';
  const socialEntropyProvenance = overlay?.socialEntropyDashboard?.provenance ?? {};
  const socialEntropySchemaVersion = socialEntropyProvenance?.schemaVersions?.social_entropy_map
    ?? socialEntropyProvenance?.schemaVersions?.civic_cohesion_report
    ?? 'unknown';
  const socialEntropyProducerCommits = asArray(socialEntropyProvenance?.producerCommits).join(', ') || 'unknown';
  const socialEntropySourceMode = socialEntropyProvenance?.derivedFromFixtures ? 'fixture' : 'live';
  const federatedGovernanceProvenance = overlay?.federationDashboard?.provenance ?? {};
  const federatedGovernanceSchemaVersion = federatedGovernanceProvenance?.schemaVersions?.stewardship_node_map
    ?? federatedGovernanceProvenance?.schemaVersions?.federation_coherence_report
    ?? 'unknown';
  const federatedGovernanceProducerCommits = asArray(federatedGovernanceProvenance?.producerCommits).join(', ') || 'unknown';
  const federatedGovernanceSourceMode = federatedGovernanceProvenance?.derivedFromFixtures ? 'fixture' : 'live';
  const emergentDomainProvenance = overlay?.emergentDomainDashboard?.provenance ?? {};
  const emergentDomainSchemaVersion = emergentDomainProvenance?.schemaVersions?.emergent_domain_audit
    ?? emergentDomainProvenance?.schemaVersions?.emergent_domain_map
    ?? 'unknown';
  const emergentDomainProducerCommits = asArray(emergentDomainProvenance?.producerCommits).join(', ') || 'unknown';
  const emergentDomainSourceMode = emergentDomainProvenance?.derivedFromFixtures ? 'fixture' : 'live';

  cy.nodes('[class = "concept"]').forEach((node) => {
    const id = node.id();
    const rankData = byConcept.get(id);
    const coherenceWeight = Number(conceptWeights[id] ?? conceptAnnotations[id]?.weight ?? 1);

    node.data('coherenceWeight', Number.isFinite(coherenceWeight) ? coherenceWeight : 1);
    node.data('attentionRank', rankData?.rank ?? null);
    node.data('attentionWeight', rankData?.attentionWeight ?? 0);
    node.data('attentionRankWeight', rankData?.attentionRankWeight ?? 0);
    node.data('attentionReason', rankData?.attentionReason ?? null);
    node.data('sophiaNote', conceptAnnotations[id]?.note ?? fallbackAssessmentNotes[id] ?? null);

    const sonya = sonyaSignals.get(id);
    node.data('sonyaAdmittedSignalCount', sonya?.admittedSignals ?? 0);
    node.data('sonyaAttentionCandidates', sonya?.attentionCandidates ?? []);

    const reasoning = reasoningSignals.get(id);
    node.data('reasoningThreadCount', reasoning?.threadCount ?? 0);
    node.data('reasoningWatchCount', reasoning?.watchCount ?? 0);
    node.data('reasoningWatchStatus', reasoning?.watchStatus ?? 'none');

    const monitor = monitorSignals.get(id);
    node.data('stabilityStatus', monitor?.stabilityStatus ?? 'unknown');
    node.data('persistenceTrend', monitor?.persistenceTrend ?? 'unknown');
    node.data('monitorWatchStatus', monitor?.watchStatus ?? 'none');

    const multimodal = multimodalSignals.get(id);
    node.data('multimodalDonationCount', multimodal?.donationCount ?? 0);
    node.data('donationWatchStatus', multimodal?.donationWatchStatus ?? 'none');
    node.data('reinforcementStatus', multimodal?.reinforcementStatus ?? 'none');

    const promotion = promotionSignals.get(id);
    node.data('reviewCandidateCount', promotion?.reviewCandidateCount ?? 0);
    node.data('reviewWatchCount', promotion?.reviewWatchCount ?? 0);
    node.data('reviewQueueStatus', promotion?.reviewQueueStatus ?? 'none');

    const governance = governanceSignals.get(id);
    node.data('governanceStatus', governance?.governanceStatus ?? 'none');
    node.data('integrityWatchStatus', governance?.integrityWatchStatus ?? 'none');
    node.data('behaviorTrend', governance?.behaviorTrend ?? 'unknown');
    node.data('humanReviewFlag', governance?.humanReviewFlag ?? false);
    const constitutional = constitutionalSignals.get(id);
    node.data('constitutionalStatus', constitutional?.constitutionalStatus ?? (overlay?.constitutionalStatus?.constitutionalStatus ?? 'stable'));
    node.data('continuityMode', overlay?.continuityModeIndex?.continuityMode ?? 'normal');
    node.data('freezeRecommendation', constitutional?.freezeRecommendation ?? Boolean(overlay?.continuityModeIndex?.freezeRecommended));
    node.data('constitutionalWatchStatus', constitutional?.constitutionalWatchStatus ?? 'none');
    const deliberation = deliberationSignals.get(id);
    node.data('quorumStatus', deliberation?.quorumStatus ?? 'none');
    node.data('amendmentStatus', deliberation?.amendmentStatus ?? 'none');
    node.data('deliberationUrgency', deliberation?.deliberationUrgency ?? 'routine');
    node.data('antiCaptureSignals', deliberation?.antiCaptureSignals ?? []);
    const continuity = continuitySignals.get(id);
    node.data('resilienceStatus', continuity?.resilienceStatus ?? 'none');
    node.data('successionReadiness', continuity?.successionReadiness ?? 'unknown');
    node.data('fragilityStatus', continuity?.fragilityStatus ?? 'unknown');
    node.data('continuityWatchState', continuity?.continuityWatchState ?? 'none');
    node.data('governanceFragilityScore', Number(continuity?.governanceFragilityScore ?? 0));
    node.data('successionReadinessScore', Number(continuity?.successionReadinessScore ?? 0));
    const recovery = recoverySignals.get(id);
    node.data('preservationCriticality', recovery?.preservationCriticality ?? 'moderate');
    node.data('escrowStatus', recovery?.escrowStatus ?? 'review-pending');
    node.data('recoveryReadiness', recovery?.recoveryReadiness ?? 'unknown');
    node.data('integrityWatchState', recovery?.integrityWatchState ?? 'none');
    node.data('recoverabilityScore', Number(recovery?.recoverabilityScore ?? 0));
    const attestation = attestationSignals.get(id);
    node.data('attestationStatus', attestation?.attestationStatus ?? 'review-pending');
    node.data('witnessSufficiency', attestation?.witnessSufficiency ?? 'unknown');
    node.data('integrityTestimonyWatchState', attestation?.integrityTestimonyWatchState ?? 'none');
    node.data('attestationNeed', attestation?.attestationNeed ?? 'moderate');
    node.data('tamperSensitivity', attestation?.tamperSensitivity ?? 'unknown');
    const precedent = precedentSignals.get(id);
    node.data('precedentStatus', precedent?.precedentStatus ?? 'review-pending');
    node.data('analogyConfidence', Number(precedent?.analogyConfidence ?? 0));
    node.data('divergenceLevel', precedent?.divergenceLevel ?? 'none');
    node.data('precedentWatchState', precedent?.precedentWatchState ?? 'none');
    const scenario = scenarioSignals.get(id);
    node.data('scenarioStatus', scenario?.scenarioStatus ?? 'review-pending');
    node.data('projectedCaptureRisk', scenario?.projectedCaptureRisk ?? 'unknown');
    node.data('projectedContinuityRisk', scenario?.projectedContinuityRisk ?? 'unknown');
    node.data('preparednessRecommendation', scenario?.preparednessRecommendation ?? 'rehearse-recovery');
    const institutional = institutionalSignals.get(id);
    node.data('institutionalStatus', institutional?.institutionalStatus ?? 'review-pending');
    node.data('chamberConflictLevel', institutional?.chamberConflictLevel ?? 'none');
    node.data('systemHealthScore', Number(institutional?.systemHealthScore ?? 0));
    node.data('systemHealthOverview', institutional?.systemHealthOverview ?? 'bounded-rehearsal');
    node.data('institutionalSchemaVersion', institutionalSchemaVersion);
    node.data('institutionalProducerCommits', institutionalProducerCommits);
    node.data('institutionalSourceMode', institutionalSourceMode);
    const queueHealth = queueHealthSignals.get(id);
    node.data('queueStatus', queueHealth?.queueStatus ?? 'normal');
    node.data('backlogPressure', queueHealth?.backlogPressure ?? 'low');
    node.data('fatigueLoadClass', queueHealth?.fatigueLoadClass ?? 'normal');
    node.data('metricGamingWatchStatus', queueHealth?.metricGamingWatchStatus ?? 'none');
    node.data('loadSheddingRecommendationSummary', queueHealth?.loadSheddingRecommendationSummary ?? 'none');
    node.data('queueHealthSchemaVersion', queueHealthSchemaVersion);
    node.data('queueHealthProducerCommits', queueHealthProducerCommits);
    node.data('queueHealthSourceMode', queueHealthSourceMode);
    const priority = prioritySignals.get(id);
    node.data('triageStatus', priority?.triageStatus ?? 'pending');
    node.data('urgencyLevel', priority?.urgencyLevel ?? 'routine');
    node.data('priorityClass', priority?.priorityClass ?? 'standard');
    node.data('triageConflictStatus', priority?.triageConflictStatus ?? 'none');
    node.data('triageRecommendationSummary', priority?.recommendationSummary ?? 'none');
    node.data('prioritySchemaVersion', prioritySchemaVersion);
    node.data('priorityProducerCommits', priorityProducerCommits);
    node.data('prioritySourceMode', prioritySourceMode);
    const closure = closureSignals.get(id);
    node.data('closureStatus', closure?.closureStatus ?? 'pending');
    node.data('closureConfidence', closure?.closureConfidence ?? 'low');
    node.data('repairUrgency', closure?.repairUrgency ?? 'routine');
    node.data('reopenedCaseWatchStatus', closure?.reopenedCaseWatchStatus ?? 'none');
    node.data('closureSchemaVersion', closureSchemaVersion);
    node.data('closureProducerCommits', closureProducerCommits);
    node.data('closureSourceMode', closureSourceMode);
    const symbolicField = symbolicFieldSignals.get(id);
    node.data('symbolicFieldStatus', symbolicField?.symbolicFieldStatus ?? 'stable');
    node.data('regimeClass', symbolicField?.regimeClass ?? 'bounded-order');
    node.data('lambdaZoneWarningLevel', symbolicField?.lambdaZoneWarningLevel ?? 'low');
    node.data('architectureHint', symbolicField?.architectureHint ?? 'monitor');
    node.data('symbolicFieldSchemaVersion', symbolicFieldSchemaVersion);
    node.data('symbolicFieldProducerCommits', symbolicFieldProducerCommits);
    node.data('symbolicFieldSourceMode', symbolicFieldSourceMode);
    const verification = verificationSignals.get(id);
    node.data('claimType', verification?.claimType ?? 'untyped');
    node.data('entityResolutionStatus', verification?.entityResolutionStatus ?? 'unresolved');
    node.data('ambiguityLevel', verification?.ambiguityLevel ?? 'medium');
    node.data('verificationUrgency', verification?.verificationUrgency ?? 'routine');
    node.data('verificationSchemaVersion', verificationSchemaVersion);
    node.data('verificationProducerCommits', verificationProducerCommits);
    node.data('verificationSourceMode', verificationSourceMode);
    const publicRecord = publicRecordSignals.get(id);
    node.data('recordType', publicRecord?.recordType ?? 'unknown');
    node.data('machineReadabilityScore', Number(publicRecord?.machineReadabilityScore ?? 0));
    node.data('entityGraphStatus', publicRecord?.entityGraphStatus ?? 'pending');
    node.data('relationshipAmbiguity', publicRecord?.relationshipAmbiguity ?? 'medium');
    node.data('custodyIntegrityScore', Number(publicRecord?.custodyIntegrityScore ?? 0));
    node.data('publicRecordSchemaVersion', publicRecordSchemaVersion);
    node.data('publicRecordProducerCommits', publicRecordProducerCommits);
    node.data('publicRecordSourceMode', publicRecordSourceMode);
    const investigation = investigationSignals.get(id);
    node.data('investigationStage', investigation?.investigationStage ?? 'intake');
    node.data('investigationStageRank', Number(investigation?.stageRank ?? 1));
    node.data('investigationPlanStatus', investigation?.planStatus ?? 'none');
    node.data('investigationPlanProgress', Number(investigation?.planProgress ?? 0));
    node.data('investigationDependencyCount', Number(investigation?.dependencyCount ?? 0));
    node.data('investigationPlanTotalSteps', Number(investigation?.planTotalSteps ?? 0));
    node.data('investigationPlanCompletedSteps', Number(investigation?.planCompletedSteps ?? 0));
    node.data('investigationBlockedDependencies', asArray(investigation?.blockedDependencies));
    node.data('investigationDependencyGraph', investigation?.dependencyGraph ?? { nodes: [], edges: [] });
    node.data('investigationSchemaVersion', investigationSchemaVersion);
    node.data('investigationProducerCommits', investigationProducerCommits);
    node.data('investigationSourceMode', investigationSourceMode);
    const authority = authoritySignals.get(id);
    node.data('evidenceMaturity', authority?.evidenceMaturity ?? 'unknown');
    node.data('evidenceAuthorityClaimType', authority?.evidenceAuthorityClaimType ?? (verification?.claimType ?? 'untyped'));
    node.data('allowedAuthorityClass', authority?.allowedAuthorityClass ?? 'restricted');
    node.data('authorityMismatchFlag', Boolean(authority?.authorityMismatchFlag ?? false));
    node.data('propagationRestrictions', asArray(authority?.propagationRestrictions));
    node.data('allowedPropagationRights', asArray(authority?.allowedPropagationRights));
    node.data('maturityGateStatus', authority?.maturityGateStatus ?? 'hold');
    node.data('maturityGateReason', authority?.maturityGateReason ?? 'insufficient-evidence-maturity');
    node.data('authorityGateSchemaVersion', authoritySchemaVersion);
    node.data('authorityGateProducerCommits', authorityProducerCommits);
    node.data('authorityGateSourceMode', authoritySourceMode);
    const reviewPacket = reviewPacketSignals.get(id);
    node.data('reviewPacketStatus', reviewPacket?.reviewPacketStatus ?? 'pending-review');
    node.data('maturityCeiling', reviewPacket?.maturityCeiling ?? 'bounded-review');
    node.data('reviewPacketAmbiguityLevel', reviewPacket?.reviewPacketAmbiguityLevel ?? 'medium');
    node.data('uncertaintyDisclosures', asArray(reviewPacket?.uncertaintyDisclosures));
    node.data('excludedConclusions', asArray(reviewPacket?.excludedConclusions));
    node.data('synthesisStatus', reviewPacket?.synthesisStatus ?? 'bounded');
    node.data('reviewPacketSchemaVersion', reviewPacketSchemaVersion);
    node.data('reviewPacketProducerCommits', reviewPacketProducerCommits);
    node.data('reviewPacketSourceMode', reviewPacketSourceMode);
    const pattern = patternSignals.get(id);
    node.data('patternCluster', pattern?.patternCluster ?? 'unclustered');
    node.data('patternMaturity', pattern?.patternMaturity ?? 'speculative');
    node.data('crossCaseRelationshipHints', asArray(pattern?.crossCaseRelationshipHints));
    node.data('patternConflictMarkers', asArray(pattern?.patternConflictMarkers));
    node.data('patternSchemaVersion', patternSchemaVersion);
    node.data('patternProducerCommits', patternProducerCommits);
    node.data('patternSourceMode', patternSourceMode);
    const patternTemporal = patternTemporalSignals.get(id);
    node.data('patternTimelineStatus', patternTemporal?.patternTimelineStatus ?? 'tracked');
    node.data('patternPersistence', patternTemporal?.patternPersistence ?? 'fragile');
    node.data('temporalConflictMarkers', asArray(patternTemporal?.temporalConflictMarkers));
    node.data('patternTimelineEvents', asArray(patternTemporal?.patternTimelineEvents));
    node.data('patternTemporalSchemaVersion', patternTemporalSchemaVersion);
    node.data('patternTemporalProducerCommits', patternTemporalProducerCommits);
    node.data('patternTemporalSourceMode', patternTemporalSourceMode);
    const causal = causalSignals.get(id);
    node.data('causalBundleType', causal?.causalBundleType ?? 'unknown-bundle');
    node.data('mechanismCandidates', asArray(causal?.mechanismCandidates));
    node.data('explanatoryGap', causal?.explanatoryGap ?? 'high');
    node.data('prohibitedConclusions', asArray(causal?.prohibitedConclusions));
    node.data('causalConflictState', causal?.causalConflictState ?? 'none');
    node.data('causalSchemaVersion', causalSchemaVersion);
    node.data('causalProducerCommits', causalProducerCommits);
    node.data('causalSourceMode', causalSourceMode);
    const collaborative = collaborativeSignals.get(id);
    node.data('collaborativeStatus', collaborative?.collaborativeStatus ?? 'none');
    node.data('consensusClass', collaborative?.consensusClass ?? 'none');
    node.data('dissentPresence', collaborative?.dissentPresent ?? false);
    node.data('dissentTraceCount', collaborative?.dissentTraceCount ?? 0);
    node.data('collaborativeMaturityConstraints', asArray(collaborative?.maturityConstraints));
    node.data('collaborativeSchemaVersion', collaborativeSchemaVersion);
    node.data('collaborativeProducerCommits', collaborativeProducerCommits);
    node.data('collaborativeSourceMode', collaborativeSourceMode);
    const telemetry = telemetrySignals.get(id);
    node.data('telemetryFieldStatus', telemetry?.telemetryFieldStatus ?? 'monitor');
    node.data('latticeCoordinates', telemetry?.latticeCoordinates ?? '0,0,0');
    node.data('latticeRegime', telemetry?.latticeRegime ?? 'bounded-order');
    node.data('donorPatternPedigree', asArray(telemetry?.donorPatternPedigree));
    node.data('tafScoreSummary', telemetry?.tafScoreSummary ?? 'bounded');
    node.data('tafScore', Number(telemetry?.tafScore ?? 0));
    node.data('branchNovelty', telemetry?.branchNovelty ?? 'low');
    node.data('branchMaturityCeiling', telemetry?.branchMaturityCeiling ?? 'bounded-review');
    node.data('telemetrySchemaVersion', telemetrySchemaVersion);
    node.data('telemetryProducerCommits', telemetryProducerCommits);
    node.data('telemetrySourceMode', telemetrySourceMode);
    const branch = branchSignals.get(id);
    node.data('branchLifecycleStatus', branch?.branchLifecycleStatus ?? 'monitor');
    node.data('branchStage', branch?.branchStage ?? 'emergent');
    node.data('branchConflictNodes', asArray(branch?.branchConflictNodes));
    node.data('branchConflictEdges', asArray(branch?.branchConflictEdges));
    node.data('branchDecayRisk', branch?.branchDecayRisk ?? 'low');
    node.data('branchDecaySignals', asArray(branch?.branchDecaySignals));
    node.data('reinforcementTrend', branch?.reinforcementTrend ?? 'balanced');
    node.data('contradictionTrend', branch?.contradictionTrend ?? 'low');
    node.data('branchSchemaVersion', branchSchemaVersion);
    node.data('branchProducerCommits', branchProducerCommits);
    node.data('branchSourceMode', branchSourceMode);
    const prediction = predictionSignals.get(id);
    node.data('forecastAccuracy', prediction?.forecastAccuracy ?? 'unknown');
    node.data('forecastConfidence', prediction?.forecastConfidence ?? 'bounded');
    node.data('calibrationTrend', prediction?.calibrationTrend ?? 'stable');
    node.data('calibrationError', Number(prediction?.calibrationError ?? 0));
    node.data('branchReliability', prediction?.branchReliability ?? 'unknown');
    node.data('reliabilityScore', Number(prediction?.reliabilityScore ?? 0));
    node.data('predictionOutcomeTimeline', asArray(prediction?.outcomeTimeline));
    node.data('predictionSchemaVersion', predictionSchemaVersion);
    node.data('predictionProducerCommits', predictionProducerCommits);
    node.data('predictionSourceMode', predictionSourceMode);
    const experimental = experimentalSignals.get(id);
    node.data('experimentalStatus', experimental?.experimentalStatus ?? 'design');
    node.data('falsificationReadiness', experimental?.falsificationReadiness ?? 'pending');
    node.data('replicationPathwayStatus', experimental?.replicationPathwayStatus ?? 'pending');
    node.data('theoryGateClass', experimental?.theoryGateClass ?? 'hold');
    node.data('hypothesisClass', experimental?.hypothesisClass ?? 'exploratory');
    node.data('experimentalSchemaVersion', experimentalSchemaVersion);
    node.data('experimentalProducerCommits', experimentalProducerCommits);
    node.data('experimentalSourceMode', experimentalSourceMode);
    const theory = theorySignals.get(id);
    node.data('theoryStatus', theory?.theoryStatus ?? 'under-review');
    node.data('theoryFalsificationStatus', theory?.falsificationStatus ?? 'pending');
    node.data('theoryReplicationStatus', theory?.replicationStatus ?? 'pending');
    node.data('revisionLineage', asArray(theory?.revisionLineage));
    node.data('negativeResultIndicators', asArray(theory?.negativeResultIndicators));
    node.data('competitionState', theory?.competitionState ?? 'unresolved');
    node.data('competitionPeers', asArray(theory?.competitionPeers));
    node.data('theorySchemaVersion', theorySchemaVersion);
    node.data('theoryProducerCommits', theoryProducerCommits);
    node.data('theorySourceMode', theorySourceMode);
    const agency = agencySignals.get(id);
    node.data('agencyStatus', agency?.agencyStatus ?? 'under-review');
    node.data('deterministicFit', Number(agency?.deterministicFit ?? 0));
    node.data('volitionalFit', Number(agency?.volitionalFit ?? 0));
    node.data('provisionalVHat', Number(agency?.provisionalVHat ?? 0));
    node.data('telBranchSignature', agency?.telBranchSignature ?? 'untyped');
    node.data('governanceModeClass', agency?.governanceModeClass ?? 'bounded-watch');
    node.data('consentSignal', agency?.consentSignal ?? 'required');
    node.data('blameSuppressionSignal', agency?.blameSuppressionSignal ?? 'enabled');
    node.data('agencySchemaVersion', agencySchemaVersion);
    node.data('agencyProducerCommits', agencyProducerCommits);
    node.data('agencySourceMode', agencySourceMode);
    const responsibility = responsibilitySignals.get(id);
    node.data('responsibilityStatus', responsibility?.responsibilityStatus ?? 'under-review');
    node.data('supportPathway', responsibility?.supportPathway ?? 'monitor');
    node.data('consentRequirement', responsibility?.consentRequirement ?? 'required');
    node.data('coercionCeiling', responsibility?.coercionCeiling ?? 'strict');
    node.data('sanctionSuppressionState', responsibility?.sanctionSuppressionState ?? 'enabled');
    node.data('interventionBoundaryState', responsibility?.interventionBoundaryState ?? 'bounded');
    node.data('responsibilitySchemaVersion', responsibilitySchemaVersion);
    node.data('responsibilityProducerCommits', responsibilityProducerCommits);
    node.data('responsibilitySourceMode', responsibilitySourceMode);
    const transfer = transferSignals.get(id);
    node.data('transferStatus', transfer?.transferStatus ?? 'under-review');
    node.data('donorTargetAsymmetry', transfer?.donorTargetAsymmetry ?? 'unknown');
    node.data('replicationGateState', transfer?.replicationGateState ?? 'hold');
    node.data('prohibitedClaims', asArray(transfer?.prohibitedClaims));
    node.data('riskRegisterSummary', transfer?.riskRegisterSummary ?? 'bounded');
    node.data('transferSchemaVersion', transferSchemaVersion);
    node.data('transferProducerCommits', transferProducerCommits);
    node.data('transferSourceMode', transferSourceMode);
    const systemForecast = systemForecastSignals.get(id);
    node.data('regimeTransitionProbability', Number(systemForecast?.regimeTransitionProbability ?? 0));
    node.data('entropyAccumulationGraph', asArray(systemForecast?.entropyAccumulationGraph));
    node.data('branchEcosystemStability', systemForecast?.branchEcosystemStability ?? 'unknown');
    node.data('trajectoryDivergenceMarkers', asArray(systemForecast?.trajectoryDivergenceMarkers));
    node.data('forecastDonorTargetAsymmetry', systemForecast?.donorTargetAsymmetry ?? 'unknown');
    node.data('forecastReplicationGateState', systemForecast?.replicationGateState ?? 'hold');
    node.data('forecastProhibitedClaims', asArray(systemForecast?.prohibitedClaims));
    node.data('forecastRiskRegisterSummary', systemForecast?.riskRegisterSummary ?? 'bounded');
    node.data('systemForecastSchemaVersion', systemForecastSchemaVersion);
    node.data('systemForecastProducerCommits', systemForecastProducerCommits);
    node.data('systemForecastSourceMode', systemForecastSourceMode);
    const informationValue = informationValueSignals.get(id);
    node.data('uncertaintyGradient', informationValue?.uncertaintyGradient ?? 'moderate');
    node.data('informationGain', Number(informationValue?.informationGain ?? 0));
    node.data('experimentPriority', informationValue?.experimentPriority ?? 'monitor');
    node.data('entropyReductionForecast', Number(informationValue?.entropyReductionForecast ?? 0));
    node.data('informationValueSchemaVersion', informationValueSchemaVersion);
    node.data('informationValueProducerCommits', informationValueProducerCommits);
    node.data('informationValueSourceMode', informationValueSourceMode);
    const valueAlignment = valueAlignmentSignals.get(id);
    node.data('knowledgePriorityRank', Number(valueAlignment?.knowledgePriorityRank ?? 99));
    node.data('welfareImpactScore', Number(valueAlignment?.welfareImpactScore ?? 0));
    node.data('welfareImpactIndicator', valueAlignment?.welfareImpactIndicator ?? 'monitor');
    node.data('fairnessImpactMarker', valueAlignment?.fairnessImpactMarker ?? 'monitor');
    node.data('valueRiskFlag', valueAlignment?.valueRiskFlag ?? 'bounded');
    node.data('valueRiskScore', Number(valueAlignment?.valueRiskScore ?? 0));
    node.data('valueAlignmentSchemaVersion', valueAlignmentSchemaVersion);
    node.data('valueAlignmentProducerCommits', valueAlignmentProducerCommits);
    node.data('valueAlignmentSourceMode', valueAlignmentSourceMode);
    const metaCognition = metaCognitionSignals.get(id);
    node.data('reasoningEfficiency', Number(metaCognition?.reasoningEfficiency ?? 0));
    node.data('patternDonorReliability', metaCognition?.patternDonorReliability ?? 'unknown');
    node.data('governanceConstraintPerformance', metaCognition?.governanceConstraintPerformance ?? 'bounded');
    node.data('discoveryProductivity', Number(metaCognition?.discoveryProductivity ?? 0));
    node.data('metaCognitionSchemaVersion', metaCognitionSchemaVersion);
    node.data('metaCognitionProducerCommits', metaCognitionProducerCommits);
    node.data('metaCognitionSourceMode', metaCognitionSourceMode);
    const architecture = architectureSignals.get(id);
    node.data('modulePerformance', architecture?.modulePerformance ?? 'monitor');
    node.data('modulePerformanceScore', Number(architecture?.modulePerformanceScore ?? 0));
    node.data('architectureDiscoveryProductivity', Number(architecture?.architectureDiscoveryProductivity ?? 0));
    node.data('safeguardPerformance', architecture?.safeguardPerformance ?? 'bounded');
    node.data('architectureImprovementProposal', architecture?.architectureImprovementProposal ?? 'none');
    node.data('architectureSchemaVersion', architectureSchemaVersion);
    node.data('architectureProducerCommits', architectureProducerCommits);
    node.data('architectureSourceMode', architectureSourceMode);
    const socialEntropy = socialEntropySignals.get(id);
    node.data('socialStatus', socialEntropy?.socialStatus ?? 'monitor');
    node.data('cohesionClass', socialEntropy?.cohesionClass ?? 'mixed');
    node.data('legitimacyDrift', socialEntropy?.legitimacyDrift ?? 'bounded');
    node.data('reviewerConcentration', Number(socialEntropy?.reviewerConcentration ?? 0));
    node.data('reviewerFatigue', socialEntropy?.reviewerFatigue ?? 'bounded');
    node.data('repairPriority', socialEntropy?.repairPriority ?? 'routine');
    node.data('socialEntropySchemaVersion', socialEntropySchemaVersion);
    node.data('socialEntropyProducerCommits', socialEntropyProducerCommits);
    node.data('socialEntropySourceMode', socialEntropySourceMode);
    const federated = federatedGovernanceSignals.get(id);
    node.data('federationStatus', federated?.federationStatus ?? 'monitor');
    node.data('stewardshipNodeClass', federated?.stewardshipNodeClass ?? 'bounded');
    node.data('dissentPortability', federated?.dissentPortability ?? 'bounded');
    node.data('captureRisk', federated?.captureRisk ?? 'bounded');
    node.data('federationLegitimacySignal', federated?.legitimacySignal ?? 'stable');
    node.data('mitigationRequirement', federated?.mitigationRequirement ?? 'monitor');
    node.data('captureRiskScore', Number(federated?.captureRiskScore ?? 0));
    node.data('federatedGovernanceSchemaVersion', federatedGovernanceSchemaVersion);
    node.data('federatedGovernanceProducerCommits', federatedGovernanceProducerCommits);
    node.data('federatedGovernanceSourceMode', federatedGovernanceSourceMode);
    const emergentDomain = emergentDomainSignals.get(id);
    node.data('domainStatus', emergentDomain?.domainStatus ?? 'monitor');
    node.data('sourceDomains', emergentDomain?.sourceDomains ?? []);
    node.data('invariantPatternClass', emergentDomain?.invariantPatternClass ?? 'unclassified');
    node.data('fieldBirthPressure', emergentDomain?.fieldBirthPressure ?? 'bounded');
    node.data('fieldBirthPressureScore', Number(emergentDomain?.fieldBirthPressureScore ?? 0));
    node.data('domainBoundaryFailure', emergentDomain?.domainBoundaryFailure ?? 'bounded');
    node.data('commonsLegibilityRequirement', emergentDomain?.commonsLegibilityRequirement ?? 'required');
    node.data('emergentDomainSchemaVersion', emergentDomainSchemaVersion);
    node.data('emergentDomainProducerCommits', emergentDomainProducerCommits);
    node.data('emergentDomainSourceMode', emergentDomainSourceMode);

    node.removeClass('attention-priority attention-secondary sonya-candidate reasoning-thread reasoning-watch stability-positive stability-watch multimodal-donation multimodal-watch review-candidate watch-queue governance-review governance-watch constitutional-watch constitutional-freeze deliberation-docket deliberation-watch deliberation-urgent anti-capture-watch continuity-docket continuity-watch continuity-fragile continuity-freeze recovery-docket recovery-watch escrow-ready recovery-fragile attestation-docket attestation-watch witness-sufficient attestation-sensitive precedent-docket precedent-watch precedent-divergent precedent-strong scenario-docket scenario-watch scenario-freeze scenario-rehearse-recovery institutional-status-indicator chamber-conflict-indicator system-health-overview queue-health-actionable backlog-pressure-watch review-fatigue-watch metric-gaming-watch load-shedding-recommended priority-actionable triage-watch urgency-high priority-critical triage-conflict closure-active closure-provisional repair-urgent reopened-watch symbolic-field-active regime-shift-watch lambda-warning architecture-hint verification-active entity-ambiguity verification-urgent claim-typed public-record-active entity-graph-linked relationship-ambiguous custody-fragile machine-readable-record investigation-active investigation-stage-mid investigation-stage-late investigation-plan-progressing investigation-blocked dependency-graph-linked authority-gated weak-evidence-signal authority-mismatch propagation-restricted maturity-gated review-packet-ready review-packet-watch packet-ambiguity-high uncertainty-disclosed synthesis-bounded pattern-cluster-active cross-case-hints pattern-maturity-stable pattern-conflict pattern-timeline-active persistence-stable temporal-conflict-marker causal-bundle-active mechanism-candidate explanatory-gap-high prohibited-conclusion causal-conflict-marker collaborative-review-active consensus-provisional dissent-present collaborative-maturity-bound telemetry-field-active lattice-transition donor-pattern-active taf-elevated branch-novel branch-maturity-bound branch-lifecycle-active branch-conflict-graph branch-decay-indicator branch-reinforcement-trend branch-contradiction-trend forecast-accuracy-high calibration-improving branch-reliability-stable prediction-timeline-active experimental-active falsification-ready replication-defined theory-gate-hold theory-corpus-active theory-negative-results theory-revision-lineage theory-competition-open agency-mode-active agency-volitional-edge agency-deterministic-edge agency-vhat-provisional agency-governance-bounded agency-consent-required agency-blame-suppressed responsibility-active support-pathway-defined consent-required coercion-ceiling-strict sanction-suppressed intervention-bounded transfer-active transfer-asymmetry-high transfer-replication-gated transfer-prohibited-claims transfer-risk-elevated system-forecast-active regime-transition-probable entropy-accumulating branch-ecosystem-fragile trajectory-divergent uncertainty-gradient-high information-gain-high experiment-priority-high entropy-reduction-positive curiosity-active value-alignment-active knowledge-priority-top welfare-impact-positive fairness-impact-watch value-risk-flagged meta-active reasoning-efficiency-high donor-reliability-high governance-constraint-strong discovery-productive architecture-active module-performance-strong architecture-discovery-productive safeguard-performance-strong architecture-proposal-queued social-entropy-active social-status-fraying cohesion-fragile legitimacy-drift-elevated reviewer-concentration-high reviewer-fatigue-high repair-priority-high federation-active federation-status-coherent stewardship-node-distributed dissent-portable capture-risk-elevated mitigation-required emergent-domain-active domain-status-emergent invariant-pattern-convergent field-birth-pressure-high domain-boundary-failure-active commons-legibility-required');
    if ((rankData?.rank ?? Infinity) <= 2) {
      node.addClass('attention-priority');
    } else if ((rankData?.rank ?? Infinity) <= 5) {
      node.addClass('attention-secondary');
    }

    if ((sonya?.admittedSignals ?? 0) > 0) {
      node.addClass('sonya-candidate');
    }

    if ((reasoning?.threadCount ?? 0) > 0) {
      node.addClass('reasoning-thread');
    }
    if ((reasoning?.watchCount ?? 0) > 0) {
      node.addClass('reasoning-watch');
    }

    if ((monitor?.stabilityStatus ?? 'unknown') === 'stable') {
      node.addClass('stability-positive');
    }
    if (['watch', 'escalate-human-review'].includes(monitor?.watchStatus ?? 'none')) {
      node.addClass('stability-watch');
    }

    if ((multimodal?.donationCount ?? 0) > 0) {
      node.addClass('multimodal-donation');
    }
    if (['watch', 'defer', 'escalate-human-review'].includes(multimodal?.donationWatchStatus ?? 'none')) {
      node.addClass('multimodal-watch');
    }

    if ((promotion?.reviewCandidateCount ?? 0) > 0) {
      node.addClass('review-candidate');
    }
    if ((promotion?.reviewWatchCount ?? 0) > 0) {
      node.addClass('watch-queue');
    }

    if ((governance?.integrityWatchStatus ?? 'none') === 'docket') {
      node.addClass('governance-review');
    }
    if ((governance?.integrityWatchStatus ?? 'none') === 'watch') {
      node.addClass('governance-watch');
    }
    if ((constitutional?.constitutionalWatchStatus ?? 'none') !== 'none') {
      node.addClass('constitutional-watch');
    }
    if ((constitutional?.freezeRecommendation ?? false) === true) {
      node.addClass('constitutional-freeze');
    }

    if ((deliberation?.deliberationQueueStatus ?? 'none') === 'docket') {
      node.addClass('deliberation-docket');
    }
    if ((deliberation?.deliberationQueueStatus ?? 'none') === 'watch') {
      node.addClass('deliberation-watch');
    }
    if ((deliberation?.deliberationUrgency ?? 'routine') === 'urgent') {
      node.addClass('deliberation-urgent');
    }
    if (asArray(deliberation?.antiCaptureSignals).length > 0) {
      node.addClass('anti-capture-watch');
    }

    if ((continuity?.continuityQueueStatus ?? 'none') === 'docket') {
      node.addClass('continuity-docket');
    }
    if ((continuity?.continuityQueueStatus ?? 'none') === 'watch') {
      node.addClass('continuity-watch');
    }
    if ((continuity?.fragilityStatus ?? 'unknown') === 'thinning') {
      node.addClass('continuity-fragile');
    }
    if ((continuity?.continuityWatchState ?? 'none') === 'freeze') {
      node.addClass('continuity-freeze');
    }

    if ((recovery?.recoveryQueueStatus ?? 'none') === 'docket') {
      node.addClass('recovery-docket');
    }
    if ((recovery?.recoveryQueueStatus ?? 'none') === 'watch') {
      node.addClass('recovery-watch');
    }
    if ((recovery?.escrowStatus ?? 'review-pending') === 'ready-for-review') {
      node.addClass('escrow-ready');
    }
    if (['watch', 'freeze'].includes(recovery?.integrityWatchState ?? 'none')) {
      node.addClass('recovery-fragile');
    }

    if ((attestation?.attestationQueueStatus ?? 'none') === 'docket') {
      node.addClass('attestation-docket');
    }
    if ((attestation?.attestationQueueStatus ?? 'none') === 'watch') {
      node.addClass('attestation-watch');
    }
    if ((attestation?.witnessSufficiency ?? 'unknown') === 'sufficient') {
      node.addClass('witness-sufficient');
    }
    if (['high', 'critical'].includes(attestation?.attestationNeed ?? 'moderate') || (attestation?.tamperSensitivity ?? 'unknown') === 'high') {
      node.addClass('attestation-sensitive');
    }

    if ((precedent?.precedentQueueStatus ?? 'none') === 'docket') {
      node.addClass('precedent-docket');
    }
    if ((precedent?.precedentQueueStatus ?? 'none') === 'watch') {
      node.addClass('precedent-watch');
    }
    if (['medium', 'high'].includes(precedent?.divergenceLevel ?? 'none')) {
      node.addClass('precedent-divergent');
    }
    if ((precedent?.analogyConfidence ?? 0) >= 0.8) {
      node.addClass('precedent-strong');
    }

    if ((scenario?.scenarioQueueStatus ?? 'none') === 'docket') {
      node.addClass('scenario-docket');
    }
    if ((scenario?.scenarioQueueStatus ?? 'none') === 'watch') {
      node.addClass('scenario-watch');
    }
    if ((scenario?.preparednessRecommendation ?? 'rehearse-recovery') === 'freeze-recommended') {
      node.addClass('scenario-freeze');
    }
    if ((scenario?.preparednessRecommendation ?? 'rehearse-recovery') === 'rehearse-recovery') {
      node.addClass('scenario-rehearse-recovery');
    }

    if ((institutional?.institutionalQueueStatus ?? 'none') !== 'none') {
      node.addClass('institutional-status-indicator');
    }
    if (['medium', 'high'].includes(institutional?.chamberConflictLevel ?? 'none')) {
      node.addClass('chamber-conflict-indicator');
    }
    if ((institutional?.systemHealthScore ?? 0) >= 0.75) {
      node.addClass('system-health-overview');
    }

    if ((queueHealth?.queueHealthQueueStatus ?? 'none') === 'dashboard') {
      node.addClass('queue-health-actionable');
    }
    if (['medium', 'high'].includes(queueHealth?.backlogPressure ?? 'low')) {
      node.addClass('backlog-pressure-watch');
    }
    if (['elevated', 'fatigued'].includes(queueHealth?.fatigueLoadClass ?? 'normal')) {
      node.addClass('review-fatigue-watch');
    }
    if ((queueHealth?.metricGamingWatchStatus ?? 'none') !== 'none') {
      node.addClass('metric-gaming-watch');
    }
    if ((queueHealth?.loadSheddingRecommendationSummary ?? 'none') !== 'none') {
      node.addClass('load-shedding-recommended');
    }

    if (['dashboard', 'docket'].includes(priority?.triageQueueStatus ?? 'none')) {
      node.addClass('priority-actionable');
    }
    if ((priority?.triageQueueStatus ?? 'none') === 'watch') {
      node.addClass('triage-watch');
    }
    if ((priority?.urgencyLevel ?? 'routine') === 'high') {
      node.addClass('urgency-high');
    }
    if ((priority?.priorityClass ?? 'standard') === 'critical-integrity') {
      node.addClass('priority-critical');
    }
    if ((priority?.triageConflictStatus ?? 'none') !== 'none') {
      node.addClass('triage-conflict');
    }

    if (['registry', 'docket'].includes(closure?.closureQueueStatus ?? 'none')) {
      node.addClass('closure-active');
    }
    if ((closure?.closureStatus ?? 'pending') === 'provisional-closed') {
      node.addClass('closure-provisional');
    }
    if ((closure?.repairUrgency ?? 'routine') === 'high') {
      node.addClass('repair-urgent');
    }
    if ((closure?.reopenedCaseWatchStatus ?? 'none') !== 'none') {
      node.addClass('reopened-watch');
    }

    if (['registry', 'dashboard'].includes(symbolicField?.symbolicFieldQueueStatus ?? 'none')) {
      node.addClass('symbolic-field-active');
    }
    if (['transition-risk', 'drift-watch', 'uncertain'].includes(symbolicField?.regimeClass ?? 'bounded-order')) {
      node.addClass('regime-shift-watch');
    }
    if (['medium', 'high'].includes(symbolicField?.lambdaZoneWarningLevel ?? 'low')) {
      node.addClass('lambda-warning');
    }
    if ((symbolicField?.architectureHint ?? 'monitor') !== 'monitor') {
      node.addClass('architecture-hint');
    }

    if (['registry', 'dashboard'].includes(verification?.verificationQueueStatus ?? 'none')) {
      node.addClass('verification-active');
    }
    if ((verification?.claimType ?? 'untyped') !== 'untyped') {
      node.addClass('claim-typed');
    }
    if (['medium', 'high'].includes(verification?.ambiguityLevel ?? 'medium')) {
      node.addClass('entity-ambiguity');
    }
    if ((verification?.verificationUrgency ?? 'routine') === 'high') {
      node.addClass('verification-urgent');
    }

    if (['registry', 'dashboard'].includes(publicRecord?.publicRecordQueueStatus ?? 'none')) {
      node.addClass('public-record-active');
    }
    if ((publicRecord?.entityGraphStatus ?? 'pending') === 'linked') {
      node.addClass('entity-graph-linked');
    }
    if (['medium', 'high'].includes(publicRecord?.relationshipAmbiguity ?? 'medium')) {
      node.addClass('relationship-ambiguous');
    }
    if ((publicRecord?.custodyIntegrityScore ?? 0) < 0.7) {
      node.addClass('custody-fragile');
    }
    if ((publicRecord?.machineReadabilityScore ?? 0) >= 0.75) {
      node.addClass('machine-readable-record');
    }

    if (['dashboard', 'watch'].includes(investigation?.investigationQueueStatus ?? 'none')) {
      node.addClass('investigation-active');
    }
    if ((investigation?.stageRank ?? 1) >= 3) {
      node.addClass('investigation-stage-mid');
    }
    if ((investigation?.stageRank ?? 1) >= 4) {
      node.addClass('investigation-stage-late');
    }
    if ((investigation?.planProgress ?? 0) > 0 && (investigation?.planProgress ?? 0) < 1) {
      node.addClass('investigation-plan-progressing');
    }
    if (asArray(investigation?.blockedDependencies).length > 0) {
      node.addClass('investigation-blocked');
    }
    if (Number(investigation?.dependencyCount ?? 0) > 0) {
      node.addClass('dependency-graph-linked');
    }

    if (['dashboard', 'watch'].includes(authority?.authorityQueueStatus ?? 'none')) {
      node.addClass('authority-gated');
    }
    if (['weak', 'speculative'].includes(authority?.evidenceMaturity ?? 'unknown')) {
      node.addClass('weak-evidence-signal');
    }
    if ((authority?.authorityMismatchFlag ?? false) === true) {
      node.addClass('authority-mismatch');
    }
    if (asArray(authority?.propagationRestrictions).length > 0) {
      node.addClass('propagation-restricted');
    }
    if ((authority?.maturityGateStatus ?? 'hold') !== 'open') {
      node.addClass('maturity-gated');
    }

    if (['dashboard', 'registry'].includes(reviewPacket?.reviewPacketQueueStatus ?? 'none')) {
      node.addClass('review-packet-ready');
    }
    if ((reviewPacket?.reviewPacketQueueStatus ?? 'none') === 'watch') {
      node.addClass('review-packet-watch');
    }
    if ((reviewPacket?.reviewPacketAmbiguityLevel ?? 'medium') === 'high') {
      node.addClass('packet-ambiguity-high');
    }
    if (asArray(reviewPacket?.uncertaintyDisclosures).length > 0) {
      node.addClass('uncertainty-disclosed');
    }
    if ((reviewPacket?.synthesisStatus ?? 'bounded') === 'bounded') {
      node.addClass('synthesis-bounded');
    }

    if (['dashboard', 'watch'].includes(pattern?.patternQueueStatus ?? 'none')) {
      node.addClass('pattern-cluster-active');
    }
    if (asArray(pattern?.crossCaseRelationshipHints).length > 0) {
      node.addClass('cross-case-hints');
    }
    if (['emergent-stable', 'stable', 'confirmed'].includes(pattern?.patternMaturity ?? 'speculative')) {
      node.addClass('pattern-maturity-stable');
    }
    if (asArray(pattern?.patternConflictMarkers).length > 0) {
      node.addClass('pattern-conflict');
    }

    if (['dashboard', 'watch'].includes(patternTemporal?.patternTemporalQueueStatus ?? 'none')) {
      node.addClass('pattern-timeline-active');
    }
    if ((patternTemporal?.patternPersistence ?? 'fragile') === 'stable') {
      node.addClass('persistence-stable');
    }
    if (asArray(patternTemporal?.temporalConflictMarkers).length > 0) {
      node.addClass('temporal-conflict-marker');
    }

    if (['dashboard', 'watch'].includes(causal?.causalQueueStatus ?? 'none')) {
      node.addClass('causal-bundle-active');
    }
    if (asArray(causal?.mechanismCandidates).length > 0) {
      node.addClass('mechanism-candidate');
    }
    if ((causal?.explanatoryGap ?? 'high') === 'high') {
      node.addClass('explanatory-gap-high');
    }
    if (asArray(causal?.prohibitedConclusions).length > 0) {
      node.addClass('prohibited-conclusion');
    }
    if ((causal?.causalConflictState ?? 'none') !== 'none') {
      node.addClass('causal-conflict-marker');
    }

    if (['dashboard', 'watch'].includes(collaborative?.collaborativeQueueStatus ?? 'none')) {
      node.addClass('collaborative-review-active');
    }
    if ((collaborative?.consensusClass ?? 'none') === 'provisional-consensus') {
      node.addClass('consensus-provisional');
    }
    if ((collaborative?.dissentPresent ?? false) === true) {
      node.addClass('dissent-present');
    }
    if (asArray(collaborative?.maturityConstraints).length > 0) {
      node.addClass('collaborative-maturity-bound');
    }

    if (['dashboard', 'watch'].includes(telemetry?.telemetryQueueStatus ?? 'none')) {
      node.addClass('telemetry-field-active');
    }
    if (['transition-risk', 'uncertain'].includes(telemetry?.latticeRegime ?? 'bounded-order')) {
      node.addClass('lattice-transition');
    }
    if (asArray(telemetry?.donorPatternPedigree).length > 0) {
      node.addClass('donor-pattern-active');
    }
    if ((telemetry?.tafScore ?? 0) >= 0.6) {
      node.addClass('taf-elevated');
    }
    if (['moderate', 'high'].includes(telemetry?.branchNovelty ?? 'low')) {
      node.addClass('branch-novel');
    }
    if ((telemetry?.branchMaturityCeiling ?? 'bounded-review') !== 'open') {
      node.addClass('branch-maturity-bound');
    }

    if (['dashboard', 'watch'].includes(branch?.branchQueueStatus ?? 'none')) {
      node.addClass('branch-lifecycle-active');
    }
    if (asArray(branch?.branchConflictNodes).length > 0 || asArray(branch?.branchConflictEdges).length > 0) {
      node.addClass('branch-conflict-graph');
    }
    if ((branch?.branchDecayRisk ?? 'low') === 'high' || asArray(branch?.branchDecaySignals).length > 0) {
      node.addClass('branch-decay-indicator');
    }
    if ((branch?.reinforcementTrend ?? 'balanced') === 'up') {
      node.addClass('branch-reinforcement-trend');
    }
    if ((branch?.contradictionTrend ?? 'low') === 'high') {
      node.addClass('branch-contradiction-trend');
    }

    if ((prediction?.forecastAccuracy ?? 'unknown') === 'high') {
      node.addClass('forecast-accuracy-high');
    }
    if ((prediction?.calibrationTrend ?? 'stable') === 'improving') {
      node.addClass('calibration-improving');
    }
    if ((prediction?.branchReliability ?? 'unknown') === 'stable') {
      node.addClass('branch-reliability-stable');
    }
    if (asArray(prediction?.outcomeTimeline).length > 0) {
      node.addClass('prediction-timeline-active');
    }

    if (['dashboard', 'watch'].includes(experimental?.experimentalQueueStatus ?? 'none')) {
      node.addClass('experimental-active');
    }
    if ((experimental?.falsificationReadiness ?? 'pending') === 'ready') {
      node.addClass('falsification-ready');
    }
    if ((experimental?.replicationPathwayStatus ?? 'pending') === 'defined') {
      node.addClass('replication-defined');
    }
    if ((experimental?.theoryGateClass ?? 'hold') === 'hold') {
      node.addClass('theory-gate-hold');
    }

    if (['dashboard', 'watch'].includes(theory?.theoryQueueStatus ?? 'none')) {
      node.addClass('theory-corpus-active');
    }
    if (asArray(theory?.negativeResultIndicators).length > 0) {
      node.addClass('theory-negative-results');
    }
    if (asArray(theory?.revisionLineage).length > 0) {
      node.addClass('theory-revision-lineage');
    }
    if (['active-competition', 'contested-leading', 'unresolved'].includes(theory?.competitionState ?? 'unresolved')) {
      node.addClass('theory-competition-open');
    }

    if (['dashboard', 'watch'].includes(agency?.agencyQueueStatus ?? 'none')) {
      node.addClass('agency-mode-active');
    }
    if ((agency?.volitionalFit ?? 0) > (agency?.deterministicFit ?? 0)) {
      node.addClass('agency-volitional-edge');
    }
    if ((agency?.deterministicFit ?? 0) > (agency?.volitionalFit ?? 0)) {
      node.addClass('agency-deterministic-edge');
    }
    if ((agency?.provisionalVHat ?? 0) > 0) {
      node.addClass('agency-vhat-provisional');
    }
    if (['bounded-consensual', 'bounded-watch', 'disagreement-hold'].includes(agency?.governanceModeClass ?? 'bounded-watch')) {
      node.addClass('agency-governance-bounded');
    }
    if ((agency?.consentSignal ?? 'required') === 'required') {
      node.addClass('agency-consent-required');
    }
    if (['enabled', 'elevated'].includes(agency?.blameSuppressionSignal ?? 'enabled')) {
      node.addClass('agency-blame-suppressed');
    }

    if (['dashboard', 'watch'].includes(responsibility?.responsibilityQueueStatus ?? 'none')) {
      node.addClass('responsibility-active');
    }
    if ((responsibility?.supportPathway ?? 'monitor') !== 'monitor') {
      node.addClass('support-pathway-defined');
    }
    if ((responsibility?.consentRequirement ?? 'required') === 'required') {
      node.addClass('consent-required');
    }
    if ((responsibility?.coercionCeiling ?? 'strict') === 'strict') {
      node.addClass('coercion-ceiling-strict');
    }
    if (['enabled', 'elevated'].includes(responsibility?.sanctionSuppressionState ?? 'enabled')) {
      node.addClass('sanction-suppressed');
    }
    if (['bounded', 'uncertain'].includes(responsibility?.interventionBoundaryState ?? 'bounded')) {
      node.addClass('intervention-bounded');
    }

    if (['dashboard', 'watch'].includes(transfer?.transferQueueStatus ?? 'none')) {
      node.addClass('transfer-active');
    }
    if ((transfer?.donorTargetAsymmetry ?? 'unknown') === 'high') {
      node.addClass('transfer-asymmetry-high');
    }
    if ((transfer?.replicationGateState ?? 'hold') !== 'gated-open') {
      node.addClass('transfer-replication-gated');
    }
    if (asArray(transfer?.prohibitedClaims).length > 0) {
      node.addClass('transfer-prohibited-claims');
    }
    if ((transfer?.riskRegisterSummary ?? 'bounded') === 'elevated') {
      node.addClass('transfer-risk-elevated');
    }

    if (['dashboard', 'watch'].includes(systemForecast?.forecastQueueStatus ?? 'none')) {
      node.addClass('system-forecast-active');
    }
    if ((systemForecast?.regimeTransitionProbability ?? 0) >= 0.6) {
      node.addClass('regime-transition-probable');
    }
    if (asArray(systemForecast?.entropyAccumulationGraph).length > 0) {
      node.addClass('entropy-accumulating');
    }
    if ((systemForecast?.branchEcosystemStability ?? 'unknown') === 'fragile') {
      node.addClass('branch-ecosystem-fragile');
    }
    if (asArray(systemForecast?.trajectoryDivergenceMarkers).length > 0) {
      node.addClass('trajectory-divergent');
    }

    if (['dashboard', 'watch'].includes(informationValue?.curiosityQueueStatus ?? 'none')) {
      node.addClass('curiosity-active');
    }
    if ((informationValue?.uncertaintyGradient ?? 'moderate') === 'high') {
      node.addClass('uncertainty-gradient-high');
    }
    if ((informationValue?.informationGain ?? 0) >= 0.65) {
      node.addClass('information-gain-high');
    }
    if ((informationValue?.experimentPriority ?? 'monitor') === 'high') {
      node.addClass('experiment-priority-high');
    }
    if ((informationValue?.entropyReductionForecast ?? 0) > 0) {
      node.addClass('entropy-reduction-positive');
    }

    if (['dashboard', 'watch'].includes(valueAlignment?.valueQueueStatus ?? 'none')) {
      node.addClass('value-alignment-active');
    }
    if ((valueAlignment?.knowledgePriorityRank ?? 99) <= 3) {
      node.addClass('knowledge-priority-top');
    }
    if ((valueAlignment?.welfareImpactIndicator ?? 'monitor') === 'positive' || (valueAlignment?.welfareImpactScore ?? 0) >= 0.65) {
      node.addClass('welfare-impact-positive');
    }
    if (['equity-watch', 'disparity-risk'].includes(valueAlignment?.fairnessImpactMarker ?? 'monitor')) {
      node.addClass('fairness-impact-watch');
    }
    if (['elevated', 'restricted'].includes(valueAlignment?.valueRiskFlag ?? 'bounded') || (valueAlignment?.valueRiskScore ?? 0) >= 0.6) {
      node.addClass('value-risk-flagged');
    }

    if (['dashboard', 'watch'].includes(metaCognition?.metaQueueStatus ?? 'none')) {
      node.addClass('meta-active');
    }
    if ((metaCognition?.reasoningEfficiency ?? 0) >= 0.7) {
      node.addClass('reasoning-efficiency-high');
    }
    if ((metaCognition?.patternDonorReliability ?? 'unknown') === 'reliable') {
      node.addClass('donor-reliability-high');
    }
    if ((metaCognition?.governanceConstraintPerformance ?? 'bounded') === 'strong') {
      node.addClass('governance-constraint-strong');
    }
    if ((metaCognition?.discoveryProductivity ?? 0) >= 0.6) {
      node.addClass('discovery-productive');
    }

    if (['dashboard', 'watch'].includes(architecture?.architectureQueueStatus ?? 'none')) {
      node.addClass('architecture-active');
    }
    if ((architecture?.modulePerformance ?? 'monitor') === 'strong' || (architecture?.modulePerformanceScore ?? 0) >= 0.75) {
      node.addClass('module-performance-strong');
    }
    if ((architecture?.architectureDiscoveryProductivity ?? 0) >= 0.6) {
      node.addClass('architecture-discovery-productive');
    }
    if ((architecture?.safeguardPerformance ?? 'bounded') === 'strong') {
      node.addClass('safeguard-performance-strong');
    }
    if ((architecture?.architectureImprovementProposal ?? 'none') !== 'none' && (architecture?.architectureImprovementProposal ?? 'none') !== 'proposal-hold') {
      node.addClass('architecture-proposal-queued');
    }

    if (['dashboard', 'watch'].includes(socialEntropy?.socialQueueStatus ?? 'none')) {
      node.addClass('social-entropy-active');
    }
    if ((socialEntropy?.socialStatus ?? 'monitor') === 'fraying') {
      node.addClass('social-status-fraying');
    }
    if ((socialEntropy?.cohesionClass ?? 'mixed') === 'fragile') {
      node.addClass('cohesion-fragile');
    }
    if ((socialEntropy?.legitimacyDrift ?? 'bounded') === 'elevated') {
      node.addClass('legitimacy-drift-elevated');
    }
    if ((socialEntropy?.reviewerConcentration ?? 0) >= 0.6) {
      node.addClass('reviewer-concentration-high');
    }
    if ((socialEntropy?.reviewerFatigue ?? 'bounded') === 'high') {
      node.addClass('reviewer-fatigue-high');
    }
    if ((socialEntropy?.repairPriority ?? 'routine') === 'high') {
      node.addClass('repair-priority-high');
    }

    if (['dashboard', 'watch'].includes(federated?.federationQueueStatus ?? 'none')) {
      node.addClass('federation-active');
    }
    if ((federated?.federationStatus ?? 'monitor') === 'coherent') {
      node.addClass('federation-status-coherent');
    }
    if ((federated?.stewardshipNodeClass ?? 'bounded') === 'distributed') {
      node.addClass('stewardship-node-distributed');
    }
    if ((federated?.dissentPortability ?? 'bounded') === 'portable') {
      node.addClass('dissent-portable');
    }
    if ((federated?.captureRisk ?? 'bounded') === 'elevated' || (federated?.captureRiskScore ?? 0) >= 0.6) {
      node.addClass('capture-risk-elevated');
    }
    if ((federated?.mitigationRequirement ?? 'monitor') === 'high') {
      node.addClass('mitigation-required');
    }

    if (['dashboard', 'watch'].includes(emergentDomain?.emergentDomainQueueStatus ?? 'none')) {
      node.addClass('emergent-domain-active');
    }
    if ((emergentDomain?.domainStatus ?? 'monitor') === 'emergent' || (emergentDomain?.domainStatus ?? 'monitor') === 'forming') {
      node.addClass('domain-status-emergent');
    }
    if ((emergentDomain?.invariantPatternClass ?? 'unclassified') === 'convergent' || (emergentDomain?.invariantPatternClass ?? 'unclassified') === 'stable-convergence') {
      node.addClass('invariant-pattern-convergent');
    }
    if ((emergentDomain?.fieldBirthPressure ?? 'bounded') === 'high' || (emergentDomain?.fieldBirthPressureScore ?? 0) >= 0.7) {
      node.addClass('field-birth-pressure-high');
    }
    if ((emergentDomain?.domainBoundaryFailure ?? 'bounded') !== 'bounded') {
      node.addClass('domain-boundary-failure-active');
    }
    if ((emergentDomain?.commonsLegibilityRequirement ?? 'required') === 'required') {
      node.addClass('commons-legibility-required');
    }
  });
}
