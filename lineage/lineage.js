import { normalizeLineageEntries, buildTraceIndex } from '../atlas/components/legibilityRoutes.js';

const table = document.getElementById('lineage-table');
async function fetchJsonWithFallback(primary, fallback) {
  const primaryRes = await fetch(primary);
  if (primaryRes.ok) {
    return primaryRes.json();
  }
  const fallbackRes = await fetch(fallback);
  if (!fallbackRes.ok) {
    throw new Error(`Unable to load ${primary} or ${fallback}`);
  }
  return fallbackRes.json();
}

const traceEl = document.getElementById('trace-overlay');

function renderTrace(phaseId, trace) {
  traceEl.innerHTML = `
    <div class="meta-key">phaseId</div><div class="meta-val">${phaseId}</div>
    <div class="meta-key">donorPatternsApplied</div><div class="meta-val">${(trace?.donorPatternsApplied ?? []).join(', ') || '—'}</div>
    <div class="meta-key">unresolvedTensions</div><div class="meta-val">${(trace?.unresolvedTensions ?? []).join(', ') || '—'}</div>
    <div class="meta-key">orthodoxyScore</div><div class="meta-val">${trace?.orthodoxyScore ?? 0}</div>
    <div class="meta-key">corridorPotential</div><div class="meta-val">${trace?.corridorPotential ?? 0}</div>
    <div class="meta-key">signalArtifactHash</div><div class="meta-val">${trace?.signalArtifactHash ?? 'unknown-artifact-hash'}</div>
    <div class="meta-key">schismPotential</div><div class="meta-val">${trace?.schismPotential ?? 0} (Advisory indicator: dual coherence emerging)</div>
    <div class="meta-key">schismAlert</div><div class="meta-val">${trace?.schismAlert ?? 'bounded'}</div>
    <div class="meta-key">rebraidPotential</div><div class="meta-val">${trace?.rebraidPotential ?? 0} (Advisory indicator: emergent information exchange)</div>
    <div class="meta-key">rebraidAlert</div><div class="meta-val">${trace?.rebraidAlert ?? 'false'}</div>
    <div class="meta-key">riverFlow</div><div class="meta-val">${trace?.riverFlow ? 'true' : 'false'} (Advisory indicator: knowledge river in formation)</div>
    <div class="meta-key">deltaPotential</div><div class="meta-val">${trace?.deltaPotential ?? 0} (Advisory indicator: civilizational delta emerging)</div>
    <div class="meta-key">ruptureAlert</div><div class="meta-val">${trace?.ruptureAlert ?? 'false'} (Advisory watch-only)</div>
    <div class="meta-key">boundary</div><div class="meta-val">Advisory indicators only; supportive overlays, not final conclusions or governance claims.</div>
  `;
}

async function main() {
  const [lineagePayload, tracePayload] = await Promise.all([
    fetchJsonWithFallback('../registry/phase_lineage_dashboard.json', '../tests/fixtures/legibility_routes/lineage_route_sample.json'),
    fetchJsonWithFallback('../bridge/coherence_memory_trace.json', '../tests/fixtures/legibility_routes/coherence_memory_trace_sample.json'),
  ]);
  const lineage = normalizeLineageEntries(lineagePayload);
  const traceIndex = buildTraceIndex(tracePayload);

  const head = `
    <thead><tr>
      <th>phaseId</th><th>lineageVisibility</th><th>glossary</th><th>canonicalBoundaryNote</th><th>upstreamArtifacts</th><th>downstreamArtifacts</th>
    </tr></thead>`;
  const body = lineage
    .map((row) => `
      <tr data-phase-id="${row.phaseId}">
        <td>${row.phaseId}</td>
        <td>${row.phaseLineageVisibility}</td>
        <td>${row.glossaryAvailability}</td>
        <td>${row.canonicalBoundaryNote}</td>
        <td>${row.upstreamArtifacts.join(', ') || '—'}</td>
        <td>${row.downstreamArtifacts.join(', ') || '—'}</td>
      </tr>
    `)
    .join('');

  table.innerHTML = `${head}<tbody>${body}</tbody>`;

  for (const tr of table.querySelectorAll('tbody tr')) {
    const phaseId = tr.getAttribute('data-phase-id');
    tr.addEventListener('mouseenter', () => renderTrace(phaseId, traceIndex.get(phaseId)));
    tr.addEventListener('click', () => renderTrace(phaseId, traceIndex.get(phaseId)));
  }
}

main().catch((err) => {
  traceEl.innerHTML = `<p>Failed to load lineage route: ${err.message}</p>`;
});
