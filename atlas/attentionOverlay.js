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
    sophiaAttentionStateResp
  ] = await Promise.all([
    fetch('../bridge/attention_updates.json').catch(() => null),
    fetch('../bridge/coherence_assessment.json').catch(() => null),
    fetch('../bridge/sophia_recommendations.json').catch(() => null),
    fetch('../registry/coherence_weights.json').catch(() => null),
    fetch('../registry/sophia_annotations.json').catch(() => null),
    fetch('../registry/sophia_attention_state.json').catch(() => null)
  ]);

  return {
    attentionUpdates: attentionUpdatesResp ? await attentionUpdatesResp.json() : {},
    coherenceAssessment: coherenceAssessmentResp ? await coherenceAssessmentResp.json() : {},
    sophiaRecommendations: sophiaRecommendationsResp ? await sophiaRecommendationsResp.json() : {},
    coherenceWeights: coherenceWeightsResp ? await coherenceWeightsResp.json() : {},
    sophiaAnnotations: sophiaAnnotationsResp ? await sophiaAnnotationsResp.json() : {},
    sophiaAttentionState: sophiaAttentionStateResp ? await sophiaAttentionStateResp.json() : {}
  };
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

    node.removeClass('attention-priority attention-secondary');
    if ((rankData?.rank ?? Infinity) <= 2) {
      node.addClass('attention-priority');
    } else if ((rankData?.rank ?? Infinity) <= 5) {
      node.addClass('attention-secondary');
    }
  });
}
