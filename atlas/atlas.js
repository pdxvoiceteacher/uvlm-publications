import { computeAtlasLayout } from './layoutEngine.js';
import { nodeStyles } from './nodeStyles.js';
import { bindSearchAndFilter, centerOnQuery } from './search.js';
import { renderMetadataPanel, setDefaultPanel } from './metadataPanel.js';
import { bindZoomController } from './zoomController.js';
import { timelineConfig } from './timelineConfig.js';
import { createTimelineEngine } from './timelineEngine.js';
import { bindTimelineControls } from './timelineControls.js';

const graphContainer = document.getElementById('graph');
const detailEl = document.getElementById('details');
const searchEl = document.getElementById('search');
const typeFilterEl = document.getElementById('type-filter');
const resetEl = document.getElementById('reset');
const galaxyBtn = document.getElementById('view-galaxy');
const solarBtn = document.getElementById('view-solar');
const orbitBtn = document.getElementById('view-orbit');

const timelineModeEl = document.getElementById('mode-toggle');
const timelinePlayEl = document.getElementById('timeline-play');
const timelinePauseEl = document.getElementById('timeline-pause');
const timelineResetEl = document.getElementById('timeline-reset');
const timelineSpeedEl = document.getElementById('timeline-speed');
const timelineSliderEl = document.getElementById('timeline-slider');
const timelineDateEl = document.getElementById('timeline-date');

function nodeColor(cls) {
  return (nodeStyles[cls] ?? nodeStyles.fallback).color;
}

function nodeSize(cls) {
  return (nodeStyles[cls] ?? nodeStyles.fallback).size;
}

function borderColor(cls) {
  return (nodeStyles[cls] ?? nodeStyles.fallback).borderColor;
}

function edgeTimelineId(edge) {
  return `${edge.source}->${edge.target}:${edge.type}`;
}

function toElements(graph, timeline) {
  const nodeDates = timeline?.nodes ?? {};
  const edgeDates = timeline?.edges ?? {};

  const nodes = graph.nodes.map((n) => ({
    data: {
      ...n,
      appearanceDate: nodeDates[n.id]?.appearanceDate ?? null
    },
    position: n.position
  }));

  const edges = graph.edges.map((e, i) => {
    const timelineId = edgeTimelineId(e);
    return {
      data: {
        id: `e-${i}`,
        ...e,
        timelineId,
        appearanceDate: edgeDates[timelineId]?.appearanceDate ?? null
      }
    };
  });

  return [...nodes, ...edges];
}

function firstNodeByClass(cy, klass) {
  const matches = cy.nodes().filter((n) => n.data('class') === klass);
  return matches.length ? matches[0].id() : null;
}

async function main() {
  const [graphResponse, timelineResponse] = await Promise.all([
    fetch('../registry/knowledge_graph.json'),
    fetch('../registry/atlas_timeline.json')
  ]);

  const sourceGraph = await graphResponse.json();
  const timeline = await timelineResponse.json();
  const graph = computeAtlasLayout(sourceGraph);

  const cy = cytoscape({
    container: graphContainer,
    elements: toElements(graph, timeline),
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
          'text-outline-color': '#04060d',
          opacity: 1
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
          'arrow-scale': 0.65,
          opacity: 1
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
        selector: '.temporal-hidden',
        style: { display: 'none' }
      },
      {
        selector: '.newly-visible',
        style: { opacity: 1 }
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

  const timelineEngine = createTimelineEngine({
    cy,
    timeline,
    config: timelineConfig
  });

  bindTimelineControls({
    engine: timelineEngine,
    modeEl: timelineModeEl,
    playEl: timelinePlayEl,
    pauseEl: timelinePauseEl,
    resetEl: timelineResetEl,
    speedEl: timelineSpeedEl,
    sliderEl: timelineSliderEl,
    dateLabelEl: timelineDateEl,
    maxIndex: timeline.events.length - 1
  });

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
    cy.fit(cy.elements(':visible'), 60);
    setDefaultPanel(detailEl);
    searchAPI.apply();
  });
}

main().catch((err) => {
  detailEl.innerHTML = `<p>Failed to load atlas: ${err.message}</p>`;
});
