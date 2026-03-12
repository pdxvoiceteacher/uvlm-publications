export const AGENT_TELEMETRY_CLASSES = ['telemetry-novelty', 'telemetry-contradiction'];

export const AGENT_TELEMETRY_RESETTABLE_CLASSES = [...AGENT_TELEMETRY_CLASSES];

export function applyAgentTelemetryOverlay(cy, agentId) {
  if (!cy || !agentId) return;
  const events = window.__bridgeArtifacts?.agent_telemetry_event_map?.summary?.byAgent || {};
  const count = (events[agentId]?.eventCount ?? events[agentId] ?? 0);
  if (count > 0) {
    cy.nodes(`[label = "${agentId}"]`).addClass(AGENT_TELEMETRY_CLASSES.join(' '));
  }
}

export function clearAgentTelemetryOverlay(cy) {
  if (!cy) return;
  cy.nodes().removeClass(AGENT_TELEMETRY_CLASSES.join(' '));
}

export function bindAgentTelemetryOverlayToggle(toggleElemId) {
  const toggleEl = document.getElementById(toggleElemId);
  if (!toggleEl) return;
  toggleEl.addEventListener('change', (e) => {
    if (window.cy) {
      clearAgentTelemetryOverlay(window.cy);
      if (e.target.checked) {
        const agents = Object.keys(window.__bridgeArtifacts?.agent_telemetry_event_map?.summary?.byAgent || {});
        agents.forEach((agentId) => applyAgentTelemetryOverlay(window.cy, agentId));
      }
    }
  });
}

if (typeof window !== 'undefined') {
  window.bindAgentTelemetryOverlayToggle = bindAgentTelemetryOverlayToggle;
}
