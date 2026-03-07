function normalizeCounts(values) {
  if (!values.length) {
    return [];
  }
  const lo = Math.min(...values);
  const hi = Math.max(...values);
  if (hi === lo) {
    return values.map(() => 1);
  }
  return values.map((v) => (v - lo) / (hi - lo));
}

export async function loadDriftOverlay() {
  const response = await fetch('../bridge/coherence_drift_map.json').catch(() => null);
  return response ? response.json() : {};
}

export function applyDriftVisualization(cy, driftOverlay, options = {}) {
  const formalThreshold = Number(options.formalThreshold ?? 0.35);
  const conceptDrift = driftOverlay?.conceptDrift ?? {};

  const conceptNodes = cy.nodes('[class = "concept"]');
  const publicationCounts = conceptNodes.map((node) => Number(node.data('visiblePublicationCount') ?? 0));
  const normalizedCounts = normalizeCounts(publicationCounts);

  conceptNodes.forEach((node, idx) => {
    const id = node.id();
    const formal = conceptDrift[id] ?? {};
    const formalDriftScore = Number(formal?.driftScore ?? 0);
    const formalDirection = formal?.driftDirection ?? 'stable';

    const expectedWeight = normalizedCounts[idx] ?? 0;
    const coherenceWeight = Number(node.data('coherenceWeight') ?? 0);
    const activityMismatchScore = Math.abs(expectedWeight - coherenceWeight);

    node.data('driftScore', Number.isFinite(formalDriftScore) ? Number(formalDriftScore.toFixed(4)) : 0);
    node.data('driftDirection', formalDirection);
    node.data('activityMismatchScore', Number(activityMismatchScore.toFixed(4)));

    node.removeClass('drift-high drift-low');
    if (formalDriftScore >= formalThreshold) {
      node.addClass('drift-high');
    } else {
      node.addClass('drift-low');
    }
  });
}
