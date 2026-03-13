const TELEMETRY_CLASSES = ['telemetry-novelty', 'telemetry-contradiction'];

export const AGENT_TELEMETRY_CLASSES = TELEMETRY_CLASSES;
export const AGENT_TELEMETRY_RESETTABLE_CLASSES = [...TELEMETRY_CLASSES];

function clearTelemetryClasses(cy) {
  if (!cy) return;
  cy.nodes(`.${TELEMETRY_CLASSES.join(', .')}`).removeClass(TELEMETRY_CLASSES.join(' '));
}

export function applyAgentTelemetryOverlay(cy, agentId) {
  if (!cy || !agentId) return;

  clearTelemetryClasses(cy);

  const events = window.__bridgeArtifacts?.agent_telemetry_event_map?.summary?.byAgent || {};
  const ev = events[agentId];
  if (!ev || Number(ev.eventCount ?? 0) <= 0) return;

  const novelty = Number(ev.novelty ?? 0);
  const contradiction = Number(ev.contradiction ?? ev.contradictionCount ?? 0);
  const cls = novelty >= contradiction ? 'telemetry-novelty' : 'telemetry-contradiction';

  cy.nodes().forEach((node) => {
    const agent = node.data('agent') ?? node.data('agentId');
    if (agent === agentId) {
      node.addClass(cls);
    }
  });
}

export function clearAgentTelemetryOverlay(cy) {
  clearTelemetryClasses(cy);
}

export function bindAgentTelemetryOverlayToggle(toggleElemId) {
  const toggle = document.getElementById(toggleElemId);
  if (!toggle) return;

  toggle.addEventListener('change', () => {
    if (!window.cy) return;

    if (toggle.checked) {
      const byAgent = window.__bridgeArtifacts?.agent_telemetry_event_map?.summary?.byAgent || {};
      Object.keys(byAgent).forEach((agentId) => {
        applyAgentTelemetryOverlay(window.cy, agentId);
      });
    } else {
      window.cy.nodes().removeClass(TELEMETRY_CLASSES.join(' '));
    }
  });
}

if (typeof window !== 'undefined') {
  window.bindAgentTelemetryOverlayToggle = bindAgentTelemetryOverlayToggle;
}
