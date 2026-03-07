const graphContainer = document.getElementById('graph');
const detailEl = document.getElementById('details');
const searchEl = document.getElementById('search');
const typeFilterEl = document.getElementById('type-filter');
const resetEl = document.getElementById('reset');

function toElements(graph) {
  const nodes = graph.nodes.map((n) => ({ data: { ...n } }));
  const edges = graph.edges.map((e, i) => ({ data: { id: `e-${i}`, ...e } }));
  return [...nodes, ...edges];
}

function item(key, value) {
  return `<div class="meta-key">${key}</div><div class="meta-val">${value ?? '—'}</div>`;
}

function renderDetails(data) {
  const preferred = ['class', 'title', 'value', 'name', 'doi', 'doi_suffix', 'publication_type', 'date', 'url'];
  const keys = [...new Set([...preferred, ...Object.keys(data)])];
  detailEl.innerHTML = keys
    .filter((k) => !['id', 'source', 'target', 'type'].includes(k) && data[k] !== undefined)
    .map((k) => item(k, Array.isArray(data[k]) ? data[k].join(', ') : data[k]))
    .join('');
}

function styleForClass(cls) {
  const map = {
    concept: '#f4c542',
    publication: '#4a90e2',
    author: '#f8f9ff',
    keyword: '#9b59b6',
    series: '#42d4b8'
  };
  return map[cls] ?? '#a4b2cc';
}

async function main() {
  const response = await fetch('../registry/knowledge_graph.json');
  const graph = await response.json();

  const cy = cytoscape({
    container: graphContainer,
    elements: toElements(graph),
    style: [
      {
        selector: 'node',
        style: {
          'background-color': (ele) => styleForClass(ele.data('class')),
          label: (ele) => ele.data('title') || ele.data('value') || ele.data('name') || ele.id(),
          color: '#e8edf7',
          'font-size': 9,
          'text-wrap': 'wrap',
          'text-max-width': 120,
          width: (ele) => (ele.data('class') === 'concept' ? 34 : ele.data('class') === 'publication' ? 22 : 14),
          height: (ele) => (ele.data('class') === 'concept' ? 34 : ele.data('class') === 'publication' ? 22 : 14),
          'border-width': 1,
          'border-color': '#24324f'
        }
      },
      {
        selector: 'edge',
        style: {
          width: 1.2,
          'line-color': '#5e6980',
          'curve-style': 'bezier',
          'target-arrow-shape': 'triangle',
          'target-arrow-color': '#5e6980',
          'arrow-scale': 0.7
        }
      },
      {
        selector: '.hidden',
        style: { display: 'none' }
      },
      {
        selector: '.highlight',
        style: { 'border-width': 3, 'border-color': '#ffffff' }
      }
    ],
    layout: {
      name: 'cose',
      animate: false,
      nodeRepulsion: 6500,
      idealEdgeLength: 100,
      gravity: 0.4
    }
  });

  cy.on('tap', 'node, edge', (evt) => {
    cy.elements().removeClass('highlight');
    evt.target.addClass('highlight');
    renderDetails(evt.target.data());
  });

  function applyFilters() {
    const q = searchEl.value.trim().toLowerCase();
    const cls = typeFilterEl.value;

    cy.nodes().forEach((node) => {
      const label = `${node.data('title') ?? ''} ${node.data('value') ?? ''} ${node.data('name') ?? ''} ${node.id()}`.toLowerCase();
      const classOk = cls === 'all' || node.data('class') === cls;
      const searchOk = !q || label.includes(q);
      node.toggleClass('hidden', !(classOk && searchOk));
    });

    cy.edges().forEach((edge) => {
      edge.toggleClass('hidden', edge.source().hasClass('hidden') || edge.target().hasClass('hidden'));
    });

    cy.fit(cy.elements(':visible'), 60);
  }

  searchEl.addEventListener('input', applyFilters);
  typeFilterEl.addEventListener('change', applyFilters);
  resetEl.addEventListener('click', () => {
    searchEl.value = '';
    typeFilterEl.value = 'all';
    cy.elements().removeClass('hidden highlight');
    cy.fit(cy.elements(), 60);
    detailEl.innerHTML = '<p>Select a node to inspect metadata.</p>';
  });
}

main().catch((err) => {
  detailEl.innerHTML = `<p>Failed to load graph: ${err.message}</p>`;
});
