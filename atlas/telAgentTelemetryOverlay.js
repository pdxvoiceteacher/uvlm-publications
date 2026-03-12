export const AGENT_TELEMETRY_RESETTABLE_CLASSES = [
  'agent-novelty-hotspot',
  'agent-contradiction-hotspot'
];

function safeGet(obj, path, fallback = null) {
  try {
    return path.reduce((acc, k) => (acc && acc[k] !== undefined ? acc[k] : undefined), obj) ?? fallback;
  } catch (_err) {
    return fallback;
  }
}

export function clearAgentTelemetryOverlay(cy) {
  if (!cy) return;
  cy.nodes().removeClass(AGENT_TELEMETRY_RESETTABLE_CLASSES.join(' '));
}

export function applyAgentTelemetryOverlay(cy, agentTelemetryMap, enabled = true, opts = {}) {
  if (!cy) return;
  clearAgentTelemetryOverlay(cy);
  if (!enabled) return;

  const noveltyThresh = opts.noveltyThreshold ?? 0.65;
  const contradictionThresh = opts.contradictionThreshold ?? 0.65;

  const events = safeGet(agentTelemetryMap, ['events'], []);
  if (!Array.isArray(events) || events.length === 0) return;

  const noveltyByTarget = new Map();
  const contradictionByTarget = new Map();

  for (const e of events) {
    const targets = Array.isArray(e.targetIds) ? e.targetIds : ['global'];
    const novelty = typeof e.noveltyScore === 'number' ? e.noveltyScore : 0;
    const contradiction = typeof e.contradictionDensity === 'number' ? e.contradictionDensity : 0;

    for (const t of targets) {
      noveltyByTarget.set(t, Math.max(noveltyByTarget.get(t) ?? 0, novelty));
      contradictionByTarget.set(t, Math.max(contradictionByTarget.get(t) ?? 0, contradiction));
    }
  }

  cy.nodes().forEach((n) => {
    const nid = n.data('id') || n.id();
    const novelty = noveltyByTarget.get(nid) ?? noveltyByTarget.get('global') ?? 0;
    const contradiction = contradictionByTarget.get(nid) ?? contradictionByTarget.get('global') ?? 0;

    if (novelty >= noveltyThresh) n.addClass('agent-novelty-hotspot');
    if (contradiction >= contradictionThresh) n.addClass('agent-contradiction-hotspot');
  });
}

export function bindAgentTelemetryOverlayToggle(toggleEl, cy, getAgentTelemetryMap) {
  if (!toggleEl) return;
  toggleEl.addEventListener('change', () => {
    const enabled = Boolean(toggleEl.checked);
    const data = typeof getAgentTelemetryMap === 'function' ? getAgentTelemetryMap() : null;
    if (!enabled) clearAgentTelemetryOverlay(cy);
    else applyAgentTelemetryOverlay(cy, data, true);
  });
}
