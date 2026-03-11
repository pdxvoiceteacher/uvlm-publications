export function asArray(value) {
  return Array.isArray(value) ? value : [];
}

export function sortByKey(entries, key) {
  return [...entries].sort((a, b) => String(a?.[key] ?? '').localeCompare(String(b?.[key] ?? '')));
}

export function normalizeLineageEntries(payload) {
  return sortByKey(asArray(payload?.entries), 'phaseId').map((entry) => ({
    phaseId: String(entry.phaseId ?? entry.reviewId ?? 'unknown-phase'),
    phaseLineageVisibility: Boolean(entry.phaseLineageVisibility),
    glossaryAvailability: Boolean(entry.glossaryAvailability),
    governanceBreadcrumbVisibility: Boolean(entry.governanceBreadcrumbVisibility),
    canonicalBoundaryNote: String(entry.canonicalBoundaryNote ?? 'Canonical legibility aid only; no governance claim.'),
    upstreamArtifacts: asArray(entry.upstreamArtifacts).map((v) => String(v)),
    downstreamArtifacts: asArray(entry.downstreamArtifacts).map((v) => String(v)),
    canonicalIntegrityMarkers: asArray(entry.canonicalIntegrityMarkers).map((v) => String(v)),
    provenanceMarkers: asArray(entry.provenanceMarkers).map((v) => String(v)),
  }));
}

export function normalizeMemoryEntries(payload) {
  return sortByKey(asArray(payload?.entries), 'memoryId').map((entry) => ({
    memoryId: String(entry.memoryId ?? entry.reviewId ?? 'unknown-memory'),
    memoryTier: String(entry.memoryTier ?? 'unknown').toLowerCase(),
    preservationCriticality: String(entry.preservationCriticality ?? 'bounded'),
    invariantHash: String(entry.invariantHash ?? 'missing'),
    phaseId: String(entry.phaseId ?? ''),
  }));
}

export function buildTraceIndex(tracePayload) {
  const idx = new Map();
  for (const row of asArray(tracePayload?.entries)) {
    const phaseId = String(row?.phaseId ?? row?.reviewId ?? '').trim();
    if (!phaseId) continue;
    idx.set(phaseId, {
      donorPatternsApplied: asArray(row.donorPatternsApplied).map((v) => String(v)),
      unresolvedTensions: asArray(row.unresolvedTensions).map((v) => String(v)),
    });
  }
  return idx;
}
