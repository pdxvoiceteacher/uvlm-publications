async function loadOperatorProposals() {
  const res = await fetch("/artifacts/operator_proposals.jsonl", { cache: "no-store" });
  const text = await res.text();

  const lines = text.trim().split("\n").filter(Boolean);
  const proposals = lines.map((line) => JSON.parse(line));

  let panel = document.getElementById("operator-proposal-panel");
  if (!panel) {
    panel = document.createElement("div");
    panel.id = "operator-proposal-panel";
    panel.className = "atlas-panel";
    document.body.appendChild(panel);
  }

  panel.innerHTML = "<h3>Operator Proposals</h3>";

  proposals.forEach((p) => {
    const div = document.createElement("div");
    div.innerHTML = `
      <strong>${p.title}</strong><br>
      Target: ${p.target_module}<br>
      Status: ${p.status}<br>
      Benefit: ${p.expected_benefit}<br><hr>
    `;
    panel.appendChild(div);
  });
}
