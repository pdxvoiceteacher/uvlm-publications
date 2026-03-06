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

export function applyDriftVisualization(cy, options = {}) {
  const threshold = Number(options.threshold ?? 0.35);
  const conceptNodes = cy.nodes('[class = "concept"]');
  const publicationCounts = conceptNodes.map((node) => Number(node.data('visiblePublicationCount') ?? 0));
  const normalizedCounts = normalizeCounts(publicationCounts);

  conceptNodes.forEach((node, idx) => {
    const expectedWeight = normalizedCounts[idx] ?? 0;
    const coherenceWeight = Number(node.data('coherenceWeight') ?? 0);
    const driftScore = Math.abs(expectedWeight - coherenceWeight);

    node.data('driftScore', Number(driftScore.toFixed(4)));
    node.data('driftDirection', expectedWeight > coherenceWeight ? 'under-modeled' : 'over-modeled');

    node.removeClass('drift-high drift-low');
    if (driftScore >= threshold) {
      node.addClass('drift-high');
    } else {
      node.addClass('drift-low');
    }
  });
}
