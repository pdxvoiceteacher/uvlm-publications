export const AGENT_TELEMETRY_CLASSES = {
  novelty: 'agent-novelty-hotspot',
  contradiction: 'agent-contradiction-hotspot'
};

export const AGENT_TELEMETRY_RESETTABLE_CLASSES = [
  AGENT_TELEMETRY_CLASSES.novelty,
  AGENT_TELEMETRY_CLASSES.contradiction
];

function getBridgeTelemetryMap() {
  return window.__bridgeArtifacts?.agent_telemetry_event_map
    ?? window.__bridgeArtifacts?.agentTelemetryMap
    ?? {};
}

export function clearAgentTelemetryOverlay(cy) {
  if (!cy) return;
  cy.elements(`.${AGENT_TELEMETRY_CLASSES.novelty}`).removeClass(AGENT_TELEMETRY_CLASSES.novelty);
  cy.elements(`.${AGENT_TELEMETRY_CLASSES.contradiction}`).removeClass(AGENT_TELEMETRY_CLASSES.contradiction);
}

function applyTelemetryEventsForAgent(cy, agentId, events = [], opts = {}) {
  if (!agentId) return;
  const noveltyThreshold = opts.noveltyThreshold ?? 0.8;
  const contradictionThreshold = opts.contradictionThreshold ?? 0.8;

  const node = cy.nodes().filter((n) => n.data('agentId') === agentId);
  if (!node.length) return;

  events.forEach((ev) => {
    const novelty = typeof ev?.noveltyScore === 'number' ? ev.noveltyScore : 0;
    const contradiction = typeof ev?.contradictionDensity === 'number' ? ev.contradictionDensity : 0;

    if (novelty > noveltyThreshold) {
      node.addClass(AGENT_TELEMETRY_CLASSES.novelty);
    }
    if (contradiction > contradictionThreshold) {
      node.addClass(AGENT_TELEMETRY_CLASSES.contradiction);
    }
  });
}

export function applyAgentTelemetryOverlay(cy, agentTelemetryMap = null, enabled = true, opts = {}) {
  if (!cy) return;
  clearAgentTelemetryOverlay(cy);
  if (!enabled) return;

  const data = agentTelemetryMap ?? getBridgeTelemetryMap();
  const events = Array.isArray(data?.events) ? data.events : [];

  events.forEach((ev) => {
    applyTelemetryEventsForAgent(cy, ev?.agentId, [ev], opts);
  });
}

export const agentTelemetryOverlay = {
  apply: (cy, agentId, opts = {}) => {
    if (!cy || !agentId) return;
    const map = getBridgeTelemetryMap();
    const events = Array.isArray(map?.events)
      ? map.events.filter((ev) => ev?.agentId === agentId)
      : [];
    applyTelemetryEventsForAgent(cy, agentId, events, opts);
  },
  clear: (cy, agentId) => {
    if (!cy) return;
    if (!agentId) {
      clearAgentTelemetryOverlay(cy);
      return;
    }
    const nodes = cy.nodes().filter((n) => n.data('agentId') === agentId);
    nodes.removeClass(AGENT_TELEMETRY_CLASSES.novelty);
    nodes.removeClass(AGENT_TELEMETRY_CLASSES.contradiction);
  }
};

export function bindAgentTelemetryOverlayToggle(toggleEl, cy, getAgentTelemetryMap) {
  if (!toggleEl) return;
  toggleEl.addEventListener('change', () => {
    const enabled = Boolean(toggleEl.checked);
    if (typeof cy?.toggleAgentTelemetry === 'function') {
      cy.toggleAgentTelemetry(enabled);
      return;
    }
    const data = typeof getAgentTelemetryMap === 'function' ? getAgentTelemetryMap() : getBridgeTelemetryMap();
    if (!enabled) clearAgentTelemetryOverlay(cy);
    else applyAgentTelemetryOverlay(cy, data, true);
  });
}
