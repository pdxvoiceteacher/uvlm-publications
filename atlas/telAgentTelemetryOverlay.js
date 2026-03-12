export const AGENT_TELEMETRY_CLASSES = ['agent-novelty-hotspot', 'agent-contradiction-hotspot'];

export const AGENT_TELEMETRY_RESETTABLE_CLASSES = [...AGENT_TELEMETRY_CLASSES];

/** Apply telemetry hotspots for a given agent */
export function applyAgentTelemetryOverlay(cy, agentId) {
  if (!cy || !agentId) return;
  const nodes = cy.nodes().filter((node) => node.data('agentId') === agentId || node.data('agent') === agentId);
  nodes.forEach((node) => {
    node.addClass(AGENT_TELEMETRY_CLASSES.join(' '));
  });
}

/** Clear all agent telemetry overlays from the graph */
export function clearAgentTelemetryOverlay(cy) {
  if (!cy) return;
  cy.nodes().removeClass(AGENT_TELEMETRY_CLASSES.join(' '));
}

function toggleAgentTelemetry(toggleEl) {
  if (!toggleEl) return;
  toggleEl.addEventListener('change', () => {
    const summary = window.__bridgeArtifacts?.agent_telemetry_event_map;
    if (!summary && typeof window.toggleAgentTelemetry !== 'function') return;
    if (typeof window.toggleAgentTelemetry === 'function') {
      window.toggleAgentTelemetry(toggleEl.checked);
    }
  });
}

if (typeof window !== 'undefined') {
  window.bindAgentTelemetryOverlayToggle = toggleAgentTelemetry;
}

/** Bind toggle element for agent telemetry (for backward compatibility) */
export const bindAgentTelemetryOverlayToggle = toggleAgentTelemetry;
