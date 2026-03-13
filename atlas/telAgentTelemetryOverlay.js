// Apply explicit novelty/contradiction classes to agent nodes
export const AGENT_TELEMETRY_CLASSES = ['telemetry-novelty', 'telemetry-contradiction'];
export const AGENT_TELEMETRY_RESETTABLE_CLASSES = [...AGENT_TELEMETRY_CLASSES];

export function applyAgentTelemetryOverlay(cy, agentId) {
  if (!cy || !agentId) return;

  // Clear previous overlay classes
  clearAgentTelemetryOverlay(cy);

  // Apply classes to nodes matching agentId in the telemetry event map
  const map = window.__bridgeArtifacts?.agent_telemetry_event_map;
  if (map && map.summary && map.summary.byAgent) {
    const events = map.summary.byAgent[agentId] || {};
    const node = cy.nodes(`[agentId = "${agentId}"]`);
    if (!node.empty()) {
      if (Number(events.novelty ?? 0) > 0) node.addClass('telemetry-novelty');
      if (Number(events.contradiction ?? 0) > 0) node.addClass('telemetry-contradiction');
    }
  }
}

export function clearAgentTelemetryOverlay(cy) {
  if (!cy) return;
  AGENT_TELEMETRY_CLASSES.forEach((cls) => {
    cy.elements(`.${cls}`).removeClass(cls);
  });
}

// Bind toggle button (expects element id)
export function bindAgentTelemetryOverlayToggle(toggleElemId) {
  const toggle = document.getElementById(toggleElemId);
  const cy = window.cy;
  if (!toggle || !cy) return;
  toggle.addEventListener('change', () => {
    if (toggle.checked) {
      const byAgent = window.__bridgeArtifacts?.agent_telemetry_event_map?.summary?.byAgent || {};
      Object.keys(byAgent).forEach((agentId) => {
        applyAgentTelemetryOverlay(cy, agentId);
      });
    } else {
      clearAgentTelemetryOverlay(cy);
    }
  });
}

if (typeof window !== 'undefined') {
  window.bindAgentTelemetryOverlayToggle = bindAgentTelemetryOverlayToggle;
}
