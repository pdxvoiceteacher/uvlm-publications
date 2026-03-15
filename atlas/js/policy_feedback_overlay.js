function renderPolicyFeedbackPanel(data) {
  const panel = document.getElementById('policy-panel');
  if (!panel) return;

  const policyPressure = Array.isArray(data?.policy_pressure) ? data.policy_pressure : [];

  panel.innerHTML = `
    Policy Pressure:<br>
    ${policyPressure.join(', ')}
  `;
}

function loadPolicyFeedback() {
  return fetch('/bridge/policy_feedback_map.json', { cache: 'no-store' })
    .then((r) => r.json())
    .then((data) => {
      renderPolicyFeedbackPanel(data);
    });
}

document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('toggle-policy-feedback');
  if (!btn || btn.dataset.bound === 'true') return;

  btn.dataset.bound = 'true';
  btn.addEventListener('click', loadPolicyFeedback);
});
