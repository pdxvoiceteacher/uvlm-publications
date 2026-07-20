# Local human-review decision UI — workstream A

The static Atlas page deliberately leaves the human decision `PENDING`; that
was insufficient for a person to record an accessible, bounded decision in the
product. This workstream adds a local loopback-only UI with a two-step
APPROVE/HOLD/REJECT confirmation flow.

The UI verifies the sealed run before serving it and writes one immutable,
hash-bound receipt outside the run root. It uses server-side CSRF tokens,
loopback Host/Origin checks, semantic HTML, labelled controls, visible text
errors, and no external resources. It invokes no model and performs no memory
or PMR action. Human authority remains binding, while the receipt is neither
truth certification nor publication authority.

The next product phase is Sonya system-tray ingress and launcher. A dialogue
AI remains deferred to the next bounded workstream.
