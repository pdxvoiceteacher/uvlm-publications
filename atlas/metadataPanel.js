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
