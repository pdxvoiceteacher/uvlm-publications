import { normalizeMemoryEntries, buildTraceIndex } from '../atlas/components/legibilityRoutes.js';

const table = document.getElementById('memory-table');
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

const traceEl = document.getElementById('memory-trace');

function renderTrace(phaseId, trace) {
  if (!phaseId) {
    traceEl.innerHTML = '<p>No phaseId associated with this memory entry.</p>';
    return;
  }
  traceEl.innerHTML = `
    <div class="meta-key">phaseId</div><div class="meta-val">${phaseId}</div>
    <div class="meta-key">donorPatternsApplied</div><div class="meta-val">${(trace?.donorPatternsApplied ?? []).join(', ') || '—'}</div>
    <div class="meta-key">unresolvedTensions</div><div class="meta-val">${(trace?.unresolvedTensions ?? []).join(', ') || '—'}</div>
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
  const [memoryPayload, tracePayload] = await Promise.all([
    fetchJsonWithFallback('../registry/civilizational_memory_dashboard.json', '../tests/fixtures/legibility_routes/memory_route_sample.json'),
    fetchJsonWithFallback('../bridge/coherence_memory_trace.json', '../tests/fixtures/legibility_routes/coherence_memory_trace_sample.json'),
  ]);
  const memories = normalizeMemoryEntries(memoryPayload);
  const traceIndex = buildTraceIndex(tracePayload);

  const head = `
    <thead><tr>
      <th>memoryId</th><th>memoryTier</th><th>preservationCriticality</th><th>invariantHash</th><th>phaseId</th>
    </tr></thead>`;
  const body = memories
    .map((row) => `
      <tr data-phase-id="${row.phaseId}">
        <td>${row.memoryId}</td>
        <td>${row.memoryTier}</td>
        <td>${row.preservationCriticality}</td>
        <td>${row.invariantHash}</td>
        <td>${row.phaseId || '—'}</td>
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
  traceEl.innerHTML = `<p>Failed to load memory route: ${err.message}</p>`;
});
