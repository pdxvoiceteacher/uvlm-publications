function row(key, value) {
  return `<div class="meta-key">${key}</div><div class="meta-val">${value ?? '—'}</div>`;
}

function asList(values) {
  if (!Array.isArray(values) || values.length === 0) {
    return '—';
  }
  return values.join(', ');
}

function renderConceptRelations(relatedConcepts) {
  if (!Array.isArray(relatedConcepts) || relatedConcepts.length === 0) {
    return row('Theory Relations', '—');
  }

  const items = relatedConcepts
    .map((item) => {
      const rel = item.label ?? item.type ?? 'related';
      const targetLabel = item.targetLabel ?? item.target ?? 'unknown';
      return `<button class="concept-relation-link" data-concept-target="${item.target}">${rel}: ${targetLabel}</button>`;
    })
    .join('');

  return `<div class="meta-key">Theory Relations</div><div class="meta-val relation-list">${items}</div>`;
}

function renderPublication(data) {
  const doiLink = data.doi && data.doi !== 'pending'
    ? `<a href="https://doi.org/${data.doi}" target="_blank" rel="noopener noreferrer">${data.doi}</a>`
    : (data.doi ?? 'pending');

  const pageLink = data.url
    ? `<a href="${data.url}" target="_blank" rel="noopener noreferrer">Open publication</a>`
    : '—';

  return [
    row('Node Class', 'publication'),
    row('Title', data.title),
    row('Authors', asList(data.authors)),
    row('Date', data.date),
    row('DOI', doiLink),
    row('Abstract', data.abstract),
    row('Concepts', asList(data.concepts)),
    row('Keywords', asList(data.keywords)),
    row('Series', data.series),
    row('Type', data.type ?? data.publication_type),
    row('Publication Page', pageLink)
  ].join('');
}

function renderConcept(data) {
  return [
    row('Node Class', 'concept'),
    row('Concept', data.value),
    row('First Appearance', data.appearanceDate),
    row('Related Papers (visible)', data.visiblePublicationCount ?? 0),
    row('Concept Importance', (data.importanceScore ?? 0).toFixed(2)),
    row('Coherence Weight', (data.coherenceWeight ?? 0).toFixed(2)),
    row('Attention Rank', data.attentionRank ?? '—'),
    row('Attention Weight', (data.attentionWeight ?? 0).toFixed(2)),
    row('Drift Score (formal)', (data.driftScore ?? 0).toFixed(2)),
    row('Activity Mismatch Score (publisher-local)', data.activityMismatchScore == null ? '—' : Number(data.activityMismatchScore).toFixed(2)),
    row('Drift Direction (formal)', data.driftDirection ?? '—'),
    row('Sophia Note', data.sophiaNote ?? '—'),
    row('Sonya Admitted Signals', data.sonyaAdmittedSignalCount ?? 0),
    row('Reasoning Threads', data.reasoningThreadCount ?? 0),
    row('Reasoning Watch Status', data.reasoningWatchStatus ?? 'none'),
    row('Stability Status', data.stabilityStatus ?? 'unknown'),
    row('Persistence Trend', data.persistenceTrend ?? 'unknown'),
    row('Monitor Watch Status', data.monitorWatchStatus ?? 'none'),
    row('Multimodal Donation Count', data.multimodalDonationCount ?? 0),
    row('Donation Watch Status', data.donationWatchStatus ?? 'none'),
    row('Reinforcement Status', data.reinforcementStatus ?? 'none'),
    row('Review Candidate Count', data.reviewCandidateCount ?? 0),
    row('Review Watch Count', data.reviewWatchCount ?? 0),
    row('Review Queue Status', data.reviewQueueStatus ?? 'none'),
    row('Governance Status', data.governanceStatus ?? 'none'),
    row('Integrity Watch Status', data.integrityWatchStatus ?? 'none'),
    row('Behavior Trend', data.behaviorTrend ?? 'unknown'),
    row('Human Review Flag', data.humanReviewFlag ? 'yes' : 'no'),
    row('Constitutional Status', data.constitutionalStatus ?? 'stable'),
    row('Continuity Mode', data.continuityMode ?? 'normal'),
    row('Freeze Recommendation', data.freezeRecommendation ? 'yes' : 'no'),
    row('Constitutional Watch Status', data.constitutionalWatchStatus ?? 'none'),
    row('Quorum Status', data.quorumStatus ?? 'none'),
    row('Amendment Status', data.amendmentStatus ?? 'none'),
    row('Deliberation Urgency', data.deliberationUrgency ?? 'routine'),
    row('Anti-Capture Watch Signals', asList(data.antiCaptureSignals)),
    row('Resilience Status', data.resilienceStatus ?? 'none'),
    row('Succession Readiness', data.successionReadiness ?? 'unknown'),
    row('Succession Readiness Score', Number(data.successionReadinessScore ?? 0).toFixed(2)),
    row('Fragility / Thinning Status', data.fragilityStatus ?? 'unknown'),
    row('Governance Fragility Score', Number(data.governanceFragilityScore ?? 0).toFixed(2)),
    row('Continuity Watch State', data.continuityWatchState ?? 'none'),
    row('Preservation Criticality', data.preservationCriticality ?? 'moderate'),
    row('Escrow Status', data.escrowStatus ?? 'review-pending'),
    row('Recovery Readiness', data.recoveryReadiness ?? 'unknown'),
    row('Recoverability Score', Number(data.recoverabilityScore ?? 0).toFixed(2)),
    row('Integrity Watch State', data.integrityWatchState ?? 'none'),
    row('Attestation Status', data.attestationStatus ?? 'review-pending'),
    row('Witness Sufficiency', data.witnessSufficiency ?? 'unknown'),
    row('Integrity Testimony Watch State', data.integrityTestimonyWatchState ?? 'none'),
    row('Attestation Need', data.attestationNeed ?? 'moderate'),
    row('Tamper Sensitivity', data.tamperSensitivity ?? 'unknown'),
    row('Precedent Status', data.precedentStatus ?? 'review-pending'),
    row('Analogy Confidence', Number(data.analogyConfidence ?? 0).toFixed(2)),
    row('Divergence Level', data.divergenceLevel ?? 'none'),
    row('Precedent Watch State', data.precedentWatchState ?? 'none'),
    row('Scenario Status', data.scenarioStatus ?? 'review-pending'),
    row('Projected Capture Risk', data.projectedCaptureRisk ?? 'unknown'),
    row('Projected Continuity Risk', data.projectedContinuityRisk ?? 'unknown'),
    row('Preparedness Recommendation', data.preparednessRecommendation ?? 'rehearse-recovery'),
    row('Institutional Status', data.institutionalStatus ?? 'review-pending'),
    row('Chamber Conflict Level', data.chamberConflictLevel ?? 'none'),
    row('System Health Score', Number(data.systemHealthScore ?? 0).toFixed(2)),
    row('System Health Overview', data.systemHealthOverview ?? 'bounded-rehearsal'),
    row('Institutional Schema Version', data.institutionalSchemaVersion ?? 'unknown'),
    row('Institutional Producer Commit(s)', data.institutionalProducerCommits ?? 'unknown'),
    row('Institutional Source Mode', data.institutionalSourceMode ?? 'unknown'),
    row('Queue Status', data.queueStatus ?? 'normal'),
    row('Backlog Pressure', data.backlogPressure ?? 'low'),
    row('Fatigue / Load Class', data.fatigueLoadClass ?? 'normal'),
    row('Metric-Gaming Watch Status', data.metricGamingWatchStatus ?? 'none'),
    row('Load-Shedding Recommendation', data.loadSheddingRecommendationSummary ?? 'none'),
    row('Queue-Health Schema Version', data.queueHealthSchemaVersion ?? 'unknown'),
    row('Queue-Health Producer Commit(s)', data.queueHealthProducerCommits ?? 'unknown'),
    row('Queue-Health Source Mode', data.queueHealthSourceMode ?? 'unknown'),
    row('Triage Status', data.triageStatus ?? 'pending'),
    row('Urgency Level', data.urgencyLevel ?? 'routine'),
    row('Priority Class', data.priorityClass ?? 'standard'),
    row('Triage Conflict Status', data.triageConflictStatus ?? 'none'),
    row('Triage Recommendation Summary', data.triageRecommendationSummary ?? 'none'),
    row('Priority Schema Version', data.prioritySchemaVersion ?? 'unknown'),
    row('Priority Producer Commit(s)', data.priorityProducerCommits ?? 'unknown'),
    row('Priority Source Mode', data.prioritySourceMode ?? 'unknown'),
    row('Closure Status', data.closureStatus ?? 'pending'),
    row('Closure Confidence', data.closureConfidence ?? 'low'),
    row('Repair Urgency', data.repairUrgency ?? 'routine'),
    row('Reopened-Case Watch Status', data.reopenedCaseWatchStatus ?? 'none'),
    row('Closure Schema Version', data.closureSchemaVersion ?? 'unknown'),
    row('Closure Producer Commit(s)', data.closureProducerCommits ?? 'unknown'),
    row('Closure Source Mode', data.closureSourceMode ?? 'unknown'),
    row('Symbolic Field Status', data.symbolicFieldStatus ?? 'stable'),
    row('Regime Class', data.regimeClass ?? 'bounded-order'),
    row('Lambda-Zone Warning Level', data.lambdaZoneWarningLevel ?? 'low'),
    row('Architecture Hint', data.architectureHint ?? 'monitor'),
    row('Symbolic-Field Schema Version', data.symbolicFieldSchemaVersion ?? 'unknown'),
    row('Symbolic-Field Producer Commit(s)', data.symbolicFieldProducerCommits ?? 'unknown'),
    row('Symbolic-Field Source Mode', data.symbolicFieldSourceMode ?? 'unknown'),
    row('Claim Type', data.claimType ?? 'untyped'),
    row('Entity-Resolution Status', data.entityResolutionStatus ?? 'unresolved'),
    row('Ambiguity Level', data.ambiguityLevel ?? 'medium'),
    row('Verification Urgency', data.verificationUrgency ?? 'routine'),
    row('Verification Schema Version', data.verificationSchemaVersion ?? 'unknown'),
    row('Verification Producer Commit(s)', data.verificationProducerCommits ?? 'unknown'),
    row('Verification Source Mode', data.verificationSourceMode ?? 'unknown'),
    row('Record Type', data.recordType ?? 'unknown'),
    row('Machine-Readability Score', Number(data.machineReadabilityScore ?? 0).toFixed(2)),
    row('Entity Graph Status', data.entityGraphStatus ?? 'pending'),
    row('Relationship Ambiguity', data.relationshipAmbiguity ?? 'medium'),
    row('Custody Integrity Score', Number(data.custodyIntegrityScore ?? 0).toFixed(2)),
    row('Public-Record Schema Version', data.publicRecordSchemaVersion ?? 'unknown'),
    row('Public-Record Producer Commit(s)', data.publicRecordProducerCommits ?? 'unknown'),
    row('Public-Record Source Mode', data.publicRecordSourceMode ?? 'unknown'),
    row('Investigation Stage', data.investigationStage ?? 'intake'),
    row('Investigation Stage Rank', Number(data.investigationStageRank ?? 1).toFixed(0)),
    row('Investigation Plan Status', data.investigationPlanStatus ?? 'none'),
    row('Investigation Plan Progress', Number(data.investigationPlanProgress ?? 0).toFixed(2)),
    row('Investigation Dependency Count', data.investigationDependencyCount ?? 0),
    row('Investigation Plan Steps', `${data.investigationPlanCompletedSteps ?? 0}/${data.investigationPlanTotalSteps ?? 0}`),
    row('Investigation Blocked Dependencies', asList(data.investigationBlockedDependencies)),
    row('Investigation Schema Version', data.investigationSchemaVersion ?? 'unknown'),
    row('Investigation Producer Commit(s)', data.investigationProducerCommits ?? 'unknown'),
    row('Investigation Source Mode', data.investigationSourceMode ?? 'unknown'),
    row('Evidence Maturity', data.evidenceMaturity ?? 'unknown'),
    row('Authority Claim Type', data.evidenceAuthorityClaimType ?? data.claimType ?? 'untyped'),
    row('Allowed Authority Class', data.allowedAuthorityClass ?? 'restricted'),
    row('Authority Mismatch Flag', data.authorityMismatchFlag ? 'yes' : 'no'),
    row('Propagation Restrictions', asList(data.propagationRestrictions)),
    row('Allowed Propagation Rights', asList(data.allowedPropagationRights)),
    row('Maturity Gate Status', data.maturityGateStatus ?? 'hold'),
    row('Maturity Gate Reason', data.maturityGateReason ?? 'insufficient-evidence-maturity'),
    row('Authority-Gate Schema Version', data.authorityGateSchemaVersion ?? 'unknown'),
    row('Authority-Gate Producer Commit(s)', data.authorityGateProducerCommits ?? 'unknown'),
    row('Authority-Gate Source Mode', data.authorityGateSourceMode ?? 'unknown'),
    row('Review Packet Status', data.reviewPacketStatus ?? 'pending-review'),
    row('Maturity Ceiling', data.maturityCeiling ?? 'bounded-review'),
    row('Packet Ambiguity Level', data.reviewPacketAmbiguityLevel ?? 'medium'),
    row('Uncertainty Disclosures', asList(data.uncertaintyDisclosures)),
    row('Excluded Conclusions', asList(data.excludedConclusions)),
    row('Synthesis Status', data.synthesisStatus ?? 'bounded'),
    row('Review-Packet Schema Version', data.reviewPacketSchemaVersion ?? 'unknown'),
    row('Review-Packet Producer Commit(s)', data.reviewPacketProducerCommits ?? 'unknown'),
    row('Review-Packet Source Mode', data.reviewPacketSourceMode ?? 'unknown'),
    row('Pattern Cluster', data.patternCluster ?? 'unclustered'),
    row('Pattern Maturity', data.patternMaturity ?? 'speculative'),
    row('Cross-Case Relationship Hints', asList(data.crossCaseRelationshipHints)),
    row('Pattern Conflict Markers', asList(data.patternConflictMarkers)),
    row('Pattern Schema Version', data.patternSchemaVersion ?? 'unknown'),
    row('Pattern Producer Commit(s)', data.patternProducerCommits ?? 'unknown'),
    row('Pattern Source Mode', data.patternSourceMode ?? 'unknown'),
    row('Pattern Timeline Status', data.patternTimelineStatus ?? 'tracked'),
    row('Pattern Persistence', data.patternPersistence ?? 'fragile'),
    row('Pattern Timeline Events', asList((Array.isArray(data.patternTimelineEvents) ? data.patternTimelineEvents.map((e) => `${e.date}:${e.event}`) : []))),
    row('Temporal Conflict Markers', asList(data.temporalConflictMarkers)),
    row('Pattern-Temporal Schema Version', data.patternTemporalSchemaVersion ?? 'unknown'),
    row('Pattern-Temporal Producer Commit(s)', data.patternTemporalProducerCommits ?? 'unknown'),
    row('Pattern-Temporal Source Mode', data.patternTemporalSourceMode ?? 'unknown'),
    row('Collaborative Status', data.collaborativeStatus ?? 'none'),
    row('Consensus Class', data.consensusClass ?? 'none'),
    row('Dissent Presence', data.dissentPresence ? 'yes' : 'no'),
    row('Dissent Trace Count', data.dissentTraceCount ?? 0),
    row('Collaborative Maturity Constraints', asList(data.collaborativeMaturityConstraints)),
    row('Collaborative Schema Version', data.collaborativeSchemaVersion ?? 'unknown'),
    row('Collaborative Producer Commit(s)', data.collaborativeProducerCommits ?? 'unknown'),
    row('Collaborative Source Mode', data.collaborativeSourceMode ?? 'unknown'),
    row('Telemetry Field Status', data.telemetryFieldStatus ?? 'monitor'),
    row('Lattice Coordinates', data.latticeCoordinates ?? '0,0,0'),
    row('Lattice Regime', data.latticeRegime ?? 'bounded-order'),
    row('Donor Pattern Pedigree', asList(data.donorPatternPedigree)),
    row('TAF Score Summary', data.tafScoreSummary ?? 'bounded'),
    row('TAF Score', Number(data.tafScore ?? 0).toFixed(2)),
    row('Branch Novelty', data.branchNovelty ?? 'low'),
    row('Branch Maturity Ceiling', data.branchMaturityCeiling ?? 'bounded-review'),
    row('Telemetry Schema Version', data.telemetrySchemaVersion ?? 'unknown'),
    row('Telemetry Producer Commit(s)', data.telemetryProducerCommits ?? 'unknown'),
    row('Telemetry Source Mode', data.telemetrySourceMode ?? 'unknown'),
    row('Related Concepts', data.relatedConceptCount ?? 0),
    renderConceptRelations(data.relatedConcepts)
  ].join('');
}

function renderEdge(data, edgeLabelMap = {}) {
  return [
    row('Edge Type', edgeLabelMap[data.type] ?? data.type ?? '—'),
    row('Source', data.source),
    row('Target', data.target),
    row('Date', data.appearanceDate)
  ].join('');
}

function renderConstellation(data) {
  return [
    row('Node Class', 'constellation'),
    row('Title', data.title),
    row('Constellation ID', data.id),
    row('Primary Signals', asList(data.explanation?.primarySignals)),
    row('Publications', data.stats?.publicationCount ?? 0),
    row('Concepts', data.stats?.conceptCount ?? 0),
    row('Authors', data.stats?.authorCount ?? 0),
    row('Series', data.stats?.seriesCount ?? 0),
    row('Visible Members', data.visibleMemberCount ?? 0),
    row('Total Members', data.memberNodeIds?.length ?? 0)
  ].join('');
}

export function renderMetadataPanel(container, data, options = {}) {
  const edgeLabelMap = options.edgeLabelMap ?? {};

  if (data.class === 'constellation') {
    container.innerHTML = renderConstellation(data);
    return;
  }

  if (data.source && data.target) {
    container.innerHTML = renderEdge(data, edgeLabelMap);
    return;
  }

  if (data.class === 'publication') {
    container.innerHTML = renderPublication(data);
    return;
  }

  if (data.class === 'concept') {
    container.innerHTML = renderConcept(data);
    return;
  }

  const preferred = ['class', 'type', 'title', 'name', 'value', 'doi', 'url', 'date'];
  const keys = [...new Set([...preferred, ...Object.keys(data)])];
  container.innerHTML = keys
    .filter((k) => !['id', 'source', 'target'].includes(k) && data[k] !== undefined)
    .map((k) => row(k, Array.isArray(data[k]) ? data[k].join(', ') : data[k]))
    .join('');
}

export function setDefaultPanel(container) {
  container.innerHTML = '<p>Select a node, edge, or constellation to inspect metadata.</p>';
}
