export const AGENT_TELEMETRY_CLASSES = ['agent-novelty-hotspot', 'agent-contradiction-hotspot'];

export const AGENT_TELEMETRY_RESETTABLE_CLASSES = [...AGENT_TELEMETRY_CLASSES];

export function applyAgentTelemetryOverlay(cy, agentId) {
  if (!cy || !agentId) return;
  cy.nodes().forEach((node) => {
    if (node.data('agent') === agentId || node.data('agentId') === agentId) {
      node.addClass('agent-novelty-hotspot agent-contradiction-hotspot');
    }
  });
}

export function clearAgentTelemetryOverlay(cy) {
  if (!cy) return;
  cy.nodes().forEach((node) => {
    AGENT_TELEMETRY_CLASSES.forEach((cls) => node.removeClass(cls));
  });
}

function toggleAgentTelemetry(toggleEl) {
  if (!toggleEl) return;
  toggleEl.addEventListener('change', () => {
    const artifacts = window.__bridgeArtifacts?.agent_telemetry_event_map;
    if (!artifacts && typeof window.toggleAgentTelemetry !== 'function') return;
    if (typeof window.toggleAgentTelemetry === 'function') {
      window.toggleAgentTelemetry(toggleEl.checked);
    }
  });
}

if (typeof window !== 'undefined') {
  window.bindAgentTelemetryOverlayToggle = toggleAgentTelemetry;
}

export const bindAgentTelemetryOverlayToggle = toggleAgentTelemetry;
