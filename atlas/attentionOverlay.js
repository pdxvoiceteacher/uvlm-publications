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
    verificationAnnotationsResp
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
    fetch('../registry/verification_annotations.json').catch(() => null)
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
    verificationAnnotations: verificationAnnotationsResp ? await verificationAnnotationsResp.json() : {}
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

    node.removeClass('attention-priority attention-secondary sonya-candidate reasoning-thread reasoning-watch stability-positive stability-watch multimodal-donation multimodal-watch review-candidate watch-queue governance-review governance-watch constitutional-watch constitutional-freeze deliberation-docket deliberation-watch deliberation-urgent anti-capture-watch continuity-docket continuity-watch continuity-fragile continuity-freeze recovery-docket recovery-watch escrow-ready recovery-fragile attestation-docket attestation-watch witness-sufficient attestation-sensitive precedent-docket precedent-watch precedent-divergent precedent-strong scenario-docket scenario-watch scenario-freeze scenario-rehearse-recovery institutional-status-indicator chamber-conflict-indicator system-health-overview queue-health-actionable backlog-pressure-watch review-fatigue-watch metric-gaming-watch load-shedding-recommended priority-actionable triage-watch urgency-high priority-critical triage-conflict closure-active closure-provisional repair-urgent reopened-watch symbolic-field-active regime-shift-watch lambda-warning architecture-hint verification-active entity-ambiguity verification-urgent claim-typed');
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
  });
}
