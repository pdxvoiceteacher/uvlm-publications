export const cascadeResettableClasses = () => ['cascade-strong'];
export const rebraidResettableClasses = () => ['rebraid-strong'];

export class TelCascadeOverlay {
  constructor(graph) {
    this.graph = graph;
  }

  apply(node) {
    const health = node.data('cascadeHealth');
    if (health !== undefined && Number(health) > 0.5) {
      node.addClass('cascade-strong');
    }
  }

  toggle(_enable) {
    // Toggling is handled by atlas bindings.
  }
}

export class TelRebraidOverlay {
  constructor(graph) {
    this.graph = graph;
  }

  apply(node) {
    const alert = node.data('rebraidAlert') || false;
    if (alert) {
      node.addClass('rebraid-strong');
    }
  }

  toggle(_enable) {
    // Toggling is handled by atlas bindings.
  }
}
