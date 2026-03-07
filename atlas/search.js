export function bindSearchAndFilter({ cy, searchEl, typeFilterEl }) {
  function apply() {
    const q = searchEl.value.trim().toLowerCase();
    const selectedClass = typeFilterEl.value;

    cy.nodes().forEach((node) => {
      const text = `${node.data('title') ?? ''} ${node.data('value') ?? ''} ${node.data('name') ?? ''} ${node.id()}`.toLowerCase();
      const classOk = selectedClass === 'all' || node.data('class') === selectedClass;
      const textOk = !q || text.includes(q);
      node.toggleClass('filter-hidden', !(classOk && textOk));
    });

    cy.edges().forEach((edge) => {
      const hideByFilter = edge.source().hasClass('filter-hidden') || edge.target().hasClass('filter-hidden');
      edge.toggleClass('filter-hidden', hideByFilter);
    });

    const visible = cy.elements(':visible');
    if (visible.length > 0) {
      cy.fit(visible, 60);
    }
  }

  searchEl.addEventListener('input', apply);
  typeFilterEl.addEventListener('change', apply);
  return { apply };
}

export function centerOnQuery(cy, query) {
  if (!query) {
    return;
  }
  const q = query.trim().toLowerCase();
  if (!q) {
    return;
  }
  const match = cy.nodes().find((node) => {
    const text = `${node.data('title') ?? ''} ${node.data('value') ?? ''} ${node.data('name') ?? ''} ${node.id()}`.toLowerCase();
    return text.includes(q);
  });
  if (match) {
    cy.center(match);
    cy.zoom(Math.max(cy.zoom(), 1.1));
    cy.elements().removeClass('highlight');
    match.addClass('highlight');
  }
}
