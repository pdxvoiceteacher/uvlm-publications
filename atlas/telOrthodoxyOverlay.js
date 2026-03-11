const ORTHODOXY_ALERT_THRESHOLD = 0.72;
const CORRIDOR_FORMING_THRESHOLD = 0.68;

const ORTHODOXY_RESETTABLE_CLASSES = [
  'orthodoxy-alert',
  'orthodoxy-caution-overlay',
  'corridor-forming',
  'corridor-reopening-overlay',
];

function asNumber(value, fallback = 0) {
  if (typeof value === 'number' && Number.isFinite(value)) return value;
  if (typeof value === 'string') {
    const n = Number.parseFloat(value);
    return Number.isFinite(n) ? n : fallback;
  }
  return fallback;
}

export function applyOrthodoxyCorridorOverlay(cy, options = {}) {
  const {
    orthodoxyEnabled = true,
    corridorEnabled = true,
  } = options;

  cy.nodes().removeClass(ORTHODOXY_RESETTABLE_CLASSES.join(' '));

  if (!orthodoxyEnabled && !corridorEnabled) {
    return;
  }

  cy.nodes().forEach((node) => {
    const orthodoxyScore = asNumber(node.data('orthodoxyScore'), NaN);
    const corridorPotential = asNumber(node.data('corridorPotential'), NaN);

    if (orthodoxyEnabled && Number.isFinite(orthodoxyScore) && orthodoxyScore >= ORTHODOXY_ALERT_THRESHOLD) {
      node.addClass('orthodoxy-alert orthodoxy-caution-overlay');
      node.data('orthodoxyRiskLabel', 'Orthodoxy Alert');
      node.data('orthodoxyRiskAdvisory', 'Advisory indicator (non-final): High narrative-coercion indicator; supportive overlay, not a final conclusion.');
    }

    if (corridorEnabled && Number.isFinite(corridorPotential) && corridorPotential >= CORRIDOR_FORMING_THRESHOLD) {
      node.addClass('corridor-forming corridor-reopening-overlay');
      node.data('corridorSignalLabel', 'Corridor Forming');
      node.data('corridorSignalAdvisory', 'Advisory indicator (non-final): Preliminary plural exploration zone, watch for new threads.');
    }
  });
}

export function bindOrthodoxyCorridorToggles(cy, orthodoxyToggleEl, corridorToggleEl, reapply) {
  const handler = () => {
    applyOrthodoxyCorridorOverlay(cy, {
      orthodoxyEnabled: orthodoxyToggleEl ? Boolean(orthodoxyToggleEl.checked) : true,
      corridorEnabled: corridorToggleEl ? Boolean(corridorToggleEl.checked) : true,
    });
    if (typeof reapply === 'function') {
      reapply();
    }
  };

  orthodoxyToggleEl?.addEventListener('change', handler);
  corridorToggleEl?.addEventListener('change', handler);
}

export function orthodoxyResettableClasses() {
  return [...ORTHODOXY_RESETTABLE_CLASSES];
}
