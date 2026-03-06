import { computeAtlasLayout } from './layoutEngine.js';
import { nodeStyles } from './nodeStyles.js';
import { bindSearchAndFilter, centerOnQuery } from './search.js';
import { renderMetadataPanel, setDefaultPanel } from './metadataPanel.js';
import { bindZoomController } from './zoomController.js';

const graphContainer = document.getElementById('graph');
const detailEl = document.getElementById('details');
const searchEl = document.getElementById('search');
const typeFilterEl = document.getElementById('type-filter');
const resetEl = document.getElementById('reset');
const galaxyBtn = document.getElementById('view-galaxy');
const solarBtn = document.getElementById('view-solar');
const orbitBtn = document.getElementById('view-orbit');

function nodeColor(cls) {
  return (nodeStyles[cls] ?? nodeStyles.fallback).color;
}

function nodeSize(cls) {
  return (nodeStyles[cls] ?? nodeStyles.fallback).size;
}

function borderColor(cls) {
  return (nodeStyles[cls] ?? nodeStyles.fallback).borderColor;
}

function toElements(graph) {
  const nodes = graph.nodes.map((n) => ({ data: { ...n }, position: n.position }));
  const edges = graph.edges.map((e, i) => ({ data: { id: `e-${i}`, ...e } }));
  return [...nodes, ...edges];
}

function firstNodeByClass(cy, klass) {
  const matches = cy.nodes().filter((n) => n.data('class') === klass);
  return matches.length ? matches[0].id() : null;
}

async function main() {
  const response = await fetch('../registry/knowledge_graph.json');
  const sourceGraph = await response.json();
  const graph = computeAtlasLayout(sourceGraph);

  const cy = cytoscape({
    container: graphContainer,
    elements: toElements(graph),
    style: [
      {
        selector: 'node',
        style: {
          'background-color': (ele) => nodeColor(ele.data('class')),
          label: (ele) => ele.data('title') || ele.data('value') || ele.data('name') || ele.id(),
          color: '#eef3ff',
          'font-size': 9,
          'text-wrap': 'wrap',
          'text-max-width': 120,
          width: (ele) => nodeSize(ele.data('class')),
          height: (ele) => nodeSize(ele.data('class')),
          'border-width': 1.2,
          'border-color': (ele) => borderColor(ele.data('class')),
          'text-outline-width': 0.5,
          'text-outline-color': '#04060d'
        }
      },
      {
        selector: 'node[class = "concept"]',
        style: {
          'shadow-color': '#ffd700',
          'shadow-blur': 18,
          'shadow-opacity': 0.55
        }
      },
      {
        selector: 'edge',
        style: {
          width: 1.1,
          'line-color': '#626f89',
          'curve-style': 'bezier',
          'target-arrow-shape': 'triangle',
          'target-arrow-color': '#626f89',
          'arrow-scale': 0.65
        }
      },
      {
        selector: '.zoom-hidden',
        style: { display: 'none' }
      },
      {
        selector: '.filter-hidden',
        style: { display: 'none' }
      },
      {
        selector: '.highlight',
        style: { 'border-width': 3, 'border-color': '#ffffff' }
      }
    ],
    layout: {
      name: 'preset'
    }
  });

  cy.layout({
    name: 'fcose',
    animate: false,
    randomize: false,
    fit: true,
    gravity: 0.15,
    idealEdgeLength: 160,
    nodeRepulsion: 5000,
    numIter: 200
  }).run();

  setDefaultPanel(detailEl);
  const searchAPI = bindSearchAndFilter({ cy, searchEl, typeFilterEl });
  const zoomAPI = bindZoomController(cy);

  cy.on('tap', 'node, edge', (evt) => {
    cy.elements().removeClass('highlight');
    evt.target.addClass('highlight');
    renderMetadataPanel(detailEl, evt.target.data());

    if (evt.target.isNode()) {
      const cls = evt.target.data('class');
      if (cls === 'concept') {
        zoomAPI.toSolar(evt.target.id());
      }
      if (cls === 'publication') {
        zoomAPI.toOrbit(evt.target.id());
      }
    }
  });

  searchEl.addEventListener('keydown', (evt) => {
    if (evt.key === 'Enter') {
      centerOnQuery(cy, searchEl.value);
    }
  });

  galaxyBtn?.addEventListener('click', () => zoomAPI.toGalaxy());
  solarBtn?.addEventListener('click', () => zoomAPI.toSolar(firstNodeByClass(cy, 'concept')));
  orbitBtn?.addEventListener('click', () => zoomAPI.toOrbit(firstNodeByClass(cy, 'publication')));

  resetEl.addEventListener('click', () => {
    searchEl.value = '';
    typeFilterEl.value = 'all';
    cy.elements().removeClass('zoom-hidden filter-hidden highlight');
    cy.fit(cy.elements(), 60);
    setDefaultPanel(detailEl);
    searchAPI.apply();
  });
}

main().catch((err) => {
  detailEl.innerHTML = `<p>Failed to load atlas: ${err.message}</p>`;
});
