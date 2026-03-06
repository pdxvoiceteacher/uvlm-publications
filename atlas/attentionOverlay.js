function normalizeAttentionRank(rankings = []) {
  const max = Math.max(1, rankings.length - 1);
  const byId = new Map();
  rankings.forEach((entry, idx) => {
    const score = Number(entry?.weight ?? 0);
    const normalizedRank = 1 - idx / max;
    byId.set(entry.id, {
      rank: idx + 1,
      rankWeight: Number.isFinite(normalizedRank) ? normalizedRank : 0,
      attentionWeight: Number.isFinite(score) ? score : 0
    });
  });
  return byId;
}

export async function loadAttentionOverlay() {
  const [coherenceResp, annotationResp, attentionStateResp] = await Promise.all([
    fetch('../registry/coherence_weights.json').catch(() => null),
    fetch('../registry/sophia_annotations.json').catch(() => null),
    fetch('../registry/sophia_attention_state.json').catch(() => null)
  ]);

  const coherence = coherenceResp ? await coherenceResp.json() : {};
  const annotations = annotationResp ? await annotationResp.json() : {};
  const attention = attentionStateResp ? await attentionStateResp.json() : {};

  return { coherence, annotations, attention };
}

export function applyAttentionOverlay(cy, overlay) {
  const conceptWeights = overlay?.coherence?.conceptWeights ?? {};
  const conceptAnnotations = overlay?.annotations?.conceptAnnotations ?? {};
  const conceptRanking = normalizeAttentionRank(overlay?.attention?.attention?.concepts ?? []);

  cy.nodes('[class = "concept"]').forEach((node) => {
    const id = node.id();
    const coherenceWeight = Number(conceptWeights[id] ?? conceptAnnotations[id]?.weight ?? 1);
    const rank = conceptRanking.get(id);

    node.data('coherenceWeight', Number.isFinite(coherenceWeight) ? coherenceWeight : 1);
    node.data('attentionWeight', rank?.attentionWeight ?? 0);
    node.data('attentionRank', rank?.rank ?? null);
    node.data('attentionRankWeight', rank?.rankWeight ?? 0);
    node.data('sophiaNote', conceptAnnotations[id]?.note ?? null);

    node.removeClass('attention-priority attention-secondary');
    if ((rank?.rank ?? Infinity) <= 2) {
      node.addClass('attention-priority');
    } else if ((rank?.rank ?? Infinity) <= 5) {
      node.addClass('attention-secondary');
    }
  });
}
