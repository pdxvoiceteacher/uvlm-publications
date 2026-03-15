const VISUAL_FIELD_CLASS = 'visual-field-gradient';
const VISUAL_FIELD_SCALED_PREFIX = 'visual-field-gradient-';

let visualFieldActive = false;

function clearVisualFieldOverlay() {
  if (window.cy) {
    const classesToClear = [VISUAL_FIELD_CLASS];
    for (let idx = 0; idx <= 9; idx += 1) {
      classesToClear.push(`${VISUAL_FIELD_SCALED_PREFIX}${idx}`);
    }
    window.cy.elements().removeClass(classesToClear.join(' '));
  }

  document
    .querySelectorAll(
      `.${VISUAL_FIELD_CLASS}, [class*="${VISUAL_FIELD_SCALED_PREFIX}"]`
    )
    .forEach((node) => {
      node.classList.remove(VISUAL_FIELD_CLASS);
      for (let idx = 0; idx <= 9; idx += 1) {
        node.classList.remove(`${VISUAL_FIELD_SCALED_PREFIX}${idx}`);
      }
    });
}

function normalizeGradientValues(data) {
  if (!Array.isArray(data)) {
    return [];
  }

  const values = data
    .map((item) => Number(item?.gradient ?? item?.magnitude ?? item?.value ?? 0))
    .filter((value) => Number.isFinite(value));

  const max = values.length ? Math.max(...values) : 0;
  if (max <= 0) {
    return data.map((item) => ({
      node: item?.node ?? item?.node_id,
      scaled: 0
    }));
  }

  return data.map((item) => {
    const raw = Number(item?.gradient ?? item?.magnitude ?? item?.value ?? 0);
    const bounded = Number.isFinite(raw) ? Math.max(raw, 0) : 0;
    const scaled = Math.min(9, Math.floor((bounded / max) * 9));

    return {
      node: item?.node ?? item?.node_id,
      scaled
    };
  });
}

function applyVisualFieldGradient(gradients) {
  const normalized = normalizeGradientValues(gradients);

  normalized.forEach((entry) => {
    const nodeId = entry.node;
    if (!nodeId) {
      return;
    }

    const scaledClass = `${VISUAL_FIELD_SCALED_PREFIX}${entry.scaled}`;

    const cyNode = window.cy?.getElementById(nodeId);
    if (cyNode && cyNode.length) {
      cyNode.addClass(VISUAL_FIELD_CLASS);
      cyNode.addClass(scaledClass);
    }

    const domNode =
      document.querySelector(`[data-node="${nodeId}"]`) ||
      document.getElementById(nodeId);

    if (domNode) {
      domNode.classList.add(VISUAL_FIELD_CLASS);
      domNode.classList.add(scaledClass);
    }
  });
}

async function toggleVisualFieldOverlay() {
  const panel = document.getElementById('visual-field-panel');

  if (visualFieldActive) {
    clearVisualFieldOverlay();
    visualFieldActive = false;
    if (panel) {
      panel.textContent = 'Visual input heatmap is inactive.';
    }
    return;
  }

  const response = await fetch('/bridge/visual_field_map.json', { cache: 'no-store' });
  const data = await response.json();
  const gradients = data?.gradients ?? data?.nodes ?? [];

  clearVisualFieldOverlay();
  applyVisualFieldGradient(gradients);
  visualFieldActive = true;

  if (panel) {
    panel.innerHTML = `Visual heatmap active.<br>Gradient nodes: ${gradients.length}`;
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const button = document.getElementById('toggle-visual-field');

  if (!button || button.dataset.bound === 'true') {
    return;
  }

  button.dataset.bound = 'true';
  button.addEventListener('click', toggleVisualFieldOverlay);
});
