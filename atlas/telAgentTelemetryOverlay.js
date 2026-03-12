export const AGENT_TELEMETRY_CLASSES = {
  novelty: 'agent-novelty-hotspot',
  contradiction: 'agent-contradiction-hotspot'
};

export const AGENT_TELEMETRY_RESETTABLE_CLASSES = [
  AGENT_TELEMETRY_CLASSES.novelty,
  AGENT_TELEMETRY_CLASSES.contradiction
];

export function applyAgentTelemetryOverlay(cy, agentId) {
  if (!cy || !agentId) return;
  cy.nodes().forEach((node) => {
    if (node.data('agentId') === agentId) {
      node.addClass(AGENT_TELEMETRY_CLASSES.novelty);
      node.addClass(AGENT_TELEMETRY_CLASSES.contradiction);
    }
  });
}

export function clearAgentTelemetryOverlay(cy) {
  if (!cy) return;
  cy.nodes().forEach((node) => {
    node.removeClass(AGENT_TELEMETRY_CLASSES.novelty);
    node.removeClass(AGENT_TELEMETRY_CLASSES.contradiction);
  });
}

export const agentTelemetryOverlay = {
  apply: applyAgentTelemetryOverlay,
  clear: clearAgentTelemetryOverlay
};

function toggleAgentTelemetry(toggleEl, cy) {
  if (!toggleEl) return;
  toggleEl.addEventListener('change', (evt) => {
    if (evt.target.checked) {
      const artifacts = window.__bridgeArtifacts?.agent_telemetry_event_map;
      const byAgent = artifacts?.summary?.byAgent ?? {};
      Object.entries(byAgent).forEach(([agent, info]) => {
        if ((info?.eventCount ?? 0) > 0) {
          applyAgentTelemetryOverlay(cy, agent);
        }
      });
    } else {
      clearAgentTelemetryOverlay(cy);
    }
  });
}

// Backwards-compatible alias.
export const bindAgentTelemetryOverlayToggle = toggleAgentTelemetry;
