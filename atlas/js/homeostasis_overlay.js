function classifyHomeostasis(hValue) {
  if (hValue >= 0.7) {
    return {
      state: 'Healthy Discovery',
      band: 'green = stable discovery',
      color: '#78ff9a'
    };
  }

  if (hValue >= 0.4) {
    return {
      state: 'Exploration Regime',
      band: 'yellow = exploration',
      color: '#ffd24d'
    };
  }

  return {
    state: 'Collapse Risk',
    band: 'red = collapse',
    color: '#ff7a7a'
  };
}

function setLine(label, value) {
  return `${label}: ${Number(value ?? 0).toFixed(2)}`;
}

function renderHomeostasis(data) {
  const panel = document.getElementById('homeostasis-panel');
  if (!panel) {
    return;
  }

  const psi = Number(data?.psi ?? 0.82);
  const p = Number(data?.p ?? 0.67);
  const t = Number(data?.t ?? 0.73);
  const deltaS = Number(data?.delta_s ?? 0.18);
  const lambda = Number(data?.lambda ?? 0.21);
  const h = Number(data?.h ?? data?.homeostasis ?? 0.76);

  const classification = classifyHomeostasis(h);

  panel.innerHTML = `
    <h3>Triadic Brain Homeostasis</h3>
    <div>${setLine('Ψ', psi)}</div>
    <div>${setLine('P', p)}</div>
    <div>${setLine('T', t)}</div>
    <div>${setLine('ΔS', deltaS)}</div>
    <div>${setLine('Λ', lambda)}</div>
    <div style="margin-top:0.35rem;">H = ${h.toFixed(2)}</div>
    <div>State: ${classification.state}</div>
    <div style="margin-top:0.35rem;font-weight:600;color:${classification.color};">${classification.band}</div>
    <div style="font-size:0.82rem;color:#d8deea;">green = stable discovery • yellow = exploration • red = collapse</div>
  `;
}

async function loadHomeostasisOverlay() {
  let payload = null;

  try {
    const response = await fetch('/bridge/homeostasis_map.json', { cache: 'no-store' });
    if (response.ok) {
      payload = await response.json();
    }
  } catch (_error) {
    payload = null;
  }

  renderHomeostasis(payload ?? {});
}

document.addEventListener('DOMContentLoaded', () => {
  const button = document.getElementById('toggle-homeostasis');
  if (button) {
    button.addEventListener('click', loadHomeostasisOverlay);
  }

  loadHomeostasisOverlay();
});
