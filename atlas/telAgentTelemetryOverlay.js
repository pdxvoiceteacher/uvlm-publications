export const AGENT_TELEMETRY_CLASSES = ['telemetry-novelty', 'telemetry-contradiction'];
export const AGENT_TELEMETRY_RESETTABLE_CLASSES = [...AGENT_TELEMETRY_CLASSES];

export function clearAgentTelemetryOverlay(cy) {
  if (!cy) return;
  cy.nodes().removeClass(AGENT_TELEMETRY_CLASSES.join(' '));
}

export function applyAgentTelemetryOverlay(cy, agentId) {
  if (!cy || !agentId) return;

  clearAgentTelemetryOverlay(cy);

  const map = window.__bridgeArtifacts?.agent_telemetry_event_map;
  if (!map) return;

  const summary = map.summary?.byAgent || {};
  const info = summary[agentId] || {};
  const nodes = cy.nodes(`[agentId="${agentId}"]`);
  if (Number(info.novelty ?? 0) > Number(info.contradiction ?? 0)) {
    nodes.addClass('telemetry-novelty');
  }
  if (Number(info.contradiction ?? 0) > Number(info.novelty ?? 0)) {
    nodes.addClass('telemetry-contradiction');
  }
}

export function bindAgentTelemetryOverlayToggle(toggleId) {
  const toggle = document.getElementById(toggleId);
  if (!toggle) return;

  toggle.addEventListener('change', (e) => {
    const isChecked = e?.target?.checked ?? toggle.checked;
    if (isChecked) {
      const map = window.__bridgeArtifacts?.agent_telemetry_event_map;
      if (!map) return;
      const agents = Object.keys(map.summary?.byAgent || {});
      agents.forEach((agentId) => applyAgentTelemetryOverlay(window.cy, agentId));
    } else {
      clearAgentTelemetryOverlay(window.cy);
    }
  });
}

if (typeof window !== 'undefined') {
  window.bindAgentTelemetryOverlayToggle = bindAgentTelemetryOverlayToggle;
}
