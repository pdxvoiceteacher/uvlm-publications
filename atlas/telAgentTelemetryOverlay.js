export const AGENT_TELEMETRY_RESETTABLE_CLASSES = [
  'agent-novelty-hotspot',
  'agent-contradiction-hotspot'
];

function getBridgeTelemetryMap() {
  return window.__bridgeArtifacts?.agent_telemetry_event_map
    ?? window.__bridgeArtifacts?.agentTelemetryMap
    ?? {};
}

export function clearAgentTelemetryOverlay(cy) {
  if (!cy) return;
  cy.elements('.agent-novelty-hotspot').removeClass('agent-novelty-hotspot');
  cy.elements('.agent-contradiction-hotspot').removeClass('agent-contradiction-hotspot');
}

export function applyAgentTelemetryOverlay(cy, agentTelemetryMap = null, enabled = true, opts = {}) {
  if (!cy) return;
  clearAgentTelemetryOverlay(cy);
  if (!enabled) return;

  const noveltyThreshold = opts.noveltyThreshold ?? 0.8;
  const contradictionThreshold = opts.contradictionThreshold ?? 0.8;

  const data = agentTelemetryMap ?? getBridgeTelemetryMap();
  const events = Array.isArray(data?.events) ? data.events : [];

  events.forEach((ev) => {
    const novelty = typeof ev?.noveltyScore === 'number' ? ev.noveltyScore : 0;
    const contradiction = typeof ev?.contradictionDensity === 'number' ? ev.contradictionDensity : 0;

    if (novelty > noveltyThreshold && ev?.agentId) {
      cy.getElementById(ev.agentId).addClass('agent-novelty-hotspot');
    }
    if (contradiction > contradictionThreshold && ev?.agentId) {
      cy.getElementById(ev.agentId).addClass('agent-contradiction-hotspot');
    }
  });
}

export const agentTelemetryOverlay = {
  apply: (cy) => {
    applyAgentTelemetryOverlay(cy, getBridgeTelemetryMap(), true);
  },
  clear: (cy) => {
    clearAgentTelemetryOverlay(cy);
  }
};

export function bindAgentTelemetryOverlayToggle(toggleEl, cy, getAgentTelemetryMap) {
  if (!toggleEl) return;
  toggleEl.addEventListener('change', () => {
    const enabled = Boolean(toggleEl.checked);
    const data = typeof getAgentTelemetryMap === 'function' ? getAgentTelemetryMap() : getBridgeTelemetryMap();
    if (!enabled) clearAgentTelemetryOverlay(cy);
    else applyAgentTelemetryOverlay(cy, data, true);
  });
}
