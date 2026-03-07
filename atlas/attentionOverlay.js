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
    reviewerBehaviorMonitorResp
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
    fetch('../registry/reviewer_behavior_monitor.json').catch(() => null)
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
    reviewerBehaviorMonitor: reviewerBehaviorMonitorResp ? await reviewerBehaviorMonitorResp.json() : {}
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

    node.removeClass('attention-priority attention-secondary sonya-candidate reasoning-thread reasoning-watch stability-positive stability-watch multimodal-donation multimodal-watch review-candidate watch-queue governance-review governance-watch');
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
  });
}
