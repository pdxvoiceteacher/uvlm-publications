const APPROACHING_THRESHOLD = 0.65;
const CONVERGED_THRESHOLD = 0.85;
const LOW_PLURALITY_THRESHOLD = 0.35;

const TERRACE_RESETTABLE_CLASSES = [
  'terrace-approaching',
  'terrace-converged-orthodoxy',
  'terrace-caution-overlay',
];

function asNumber(value, fallback = 0) {
  if (typeof value === 'number' && Number.isFinite(value)) return value;
  if (typeof value === 'string') {
    const n = Number.parseFloat(value);
    return Number.isFinite(n) ? n : fallback;
  }
  return fallback;
}

function derivePluralityScore(node) {
  return asNumber(
    node.data('pluralityScore')
      ?? node.data('pluralityRetention')
      ?? node.data('pluralityRetentionScore')
      ?? node.data('pluralityDurability')
      ?? 1,
    1
  );
}

export function applyTerraceOverlay(cy, enabled = true) {
  cy.nodes().removeClass(TERRACE_RESETTABLE_CLASSES.join(' '));

  if (!enabled) {
    return;
  }

  cy.nodes().forEach((node) => {
    const theta = asNumber(node.data('terracePrecursorScore'), NaN);
    if (!Number.isFinite(theta)) {
      return;
    }

    const plurality = derivePluralityScore(node);
    const convergedOrthodoxy = theta >= CONVERGED_THRESHOLD && plurality <= LOW_PLURALITY_THRESHOLD;
    const approachingTerrace = theta >= APPROACHING_THRESHOLD;

    if (convergedOrthodoxy) {
      node.addClass('terrace-converged-orthodoxy terrace-caution-overlay');
      node.data('terraceReadinessState', 'converged-orthodoxy-watch');
      node.data('terraceReadinessAdvisory', 'Bounded guidance: watch this thread for plateau emergence and plurality contraction risk; no closure or finality implied.');
      return;
    }

    if (approachingTerrace) {
      node.addClass('terrace-approaching');
      node.data('terraceReadinessState', 'approaching-terrace');
      node.data('terraceReadinessAdvisory', 'Bounded guidance: watch this thread for plateau emergence; keep-open stewardship recommended.');
      return;
    }

    node.data('terraceReadinessState', 'bounded');
    node.data('terraceReadinessAdvisory', 'Bounded guidance only; no governance claim or final map inference.');
  });
}

export function bindTerraceOverlayToggle(cy, toggleEl, reapply) {
  if (!toggleEl) {
    return;
  }
  toggleEl.addEventListener('change', () => {
    applyTerraceOverlay(cy, Boolean(toggleEl.checked));
    if (typeof reapply === 'function') {
      reapply();
    }
  });
}

export function terraceResettableClasses() {
  return [...TERRACE_RESETTABLE_CLASSES];
}
