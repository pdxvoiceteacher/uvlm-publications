export const AGENT_TELEMETRY_CLASSES = {
  novelty: 'telemetry-novelty',
  contradiction: 'telemetry-contradiction'
};

const TELEMETRY_CLASSES = AGENT_TELEMETRY_CLASSES;

export const AGENT_TELEMETRY_RESETTABLE_CLASSES = [
  TELEMETRY_CLASSES.novelty,
  TELEMETRY_CLASSES.contradiction
];

export function applyAgentTelemetryOverlay(cy, agentId) {
  if (!cy || !agentId) return;

  const telemetrySummary = window.__bridgeArtifacts?.agent_telemetry_event_map?.summary?.byAgent || {};
  const summary = telemetrySummary[agentId] || {};
  const eventCount = Number(summary.eventCount ?? 0);
  const contradictionCount = Number(summary.contradictionCount ?? 0);

  if (eventCount <= 0) return;

  cy.nodes().forEach((node) => {
    if (node.data('agentId') === agentId) {
      node.addClass(TELEMETRY_CLASSES.novelty);
      if (contradictionCount > 0) {
        node.addClass(TELEMETRY_CLASSES.contradiction);
      }
    }
  });
}

export function clearAgentTelemetryOverlay(cy) {
  if (!cy) return;
  cy.elements().removeClass(`${TELEMETRY_CLASSES.novelty} ${TELEMETRY_CLASSES.contradiction}`);
}

export function bindAgentTelemetryOverlayToggle(toggleElemId) {
  const toggleElem = document.getElementById(toggleElemId);
  if (!toggleElem) return;

  toggleElem.addEventListener('change', (e) => {
    const cy = window.cy;
    if (!cy) return;

    if (e.target.checked) {
      clearAgentTelemetryOverlay(cy);
      const artifacts = window.__bridgeArtifacts || {};
      const summary = artifacts.agent_telemetry_event_map?.summary?.byAgent || {};
      Object.keys(summary).forEach((agentId) => {
        if (Number(summary[agentId]?.eventCount ?? 0) > 0) {
          applyAgentTelemetryOverlay(cy, agentId);
        }
      });
    } else {
      clearAgentTelemetryOverlay(cy);
    }
  });
}

if (typeof window !== 'undefined') {
  window.bindAgentTelemetryOverlayToggle = bindAgentTelemetryOverlayToggle;
}
