import { computeAtlasLayout } from './layoutEngine.js';
import { nodeStyles } from './nodeStyles.js';
import { bindSearchAndFilter, centerOnQuery } from './search.js';
import { renderMetadataPanel, setDefaultPanel } from './metadataPanel.js';
import { bindZoomController } from './zoomController.js';
import { timelineConfig } from './timelineConfig.js';
import { createTimelineEngine } from './timelineEngine.js';
import { bindTimelineControls } from './timelineControls.js';
import { edgeLabelMap } from './edgeLabels.js';

const graphContainer = document.getElementById('graph');
const detailEl = document.getElementById('details');
const searchEl = document.getElementById('search');
const typeFilterEl = document.getElementById('type-filter');
const resetEl = document.getElementById('reset');
const galaxyBtn = document.getElementById('view-galaxy');
const solarBtn = document.getElementById('view-solar');
const orbitBtn = document.getElementById('view-orbit');
const pathSelectEl = document.getElementById('guided-paths');
const pathPlayEl = document.getElementById('guided-play');

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
        label: edgeLabelMap[e.type] ?? e.type,
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

function annotateConceptStats(cy) {
  cy.nodes('[class = "concept"]').forEach((node) => {
    const relatedConceptCount = cy
      .edges('[type = "contains"], [type = "dependsOn"], [type = "refines"], [type = "extends"], [type = "contrastsWith"]')
      .filter((edge) => edge.source().id() === node.id() || edge.target().id() === node.id())
      .length;
    node.data('relatedConceptCount', relatedConceptCount);
  });
}

function bindGuidedPaths(cy, paths) {
  if (!pathSelectEl || !pathPlayEl) {
    return;
  }

  pathSelectEl.innerHTML = '<option value="">Guided paths</option>';
  (paths ?? []).forEach((path) => {
    const opt = document.createElement('option');
    opt.value = path.id;
    opt.textContent = path.title;
    pathSelectEl.appendChild(opt);
  });

  pathPlayEl.addEventListener('click', () => {
    const selected = (paths ?? []).find((p) => p.id === pathSelectEl.value);
    if (!selected || !Array.isArray(selected.nodes) || selected.nodes.length === 0) {
      return;
    }

    cy.elements().removeClass('highlight');
    let idx = 0;
    const timer = setInterval(() => {
      const nodeId = selected.nodes[idx];
      const node = cy.getElementById(nodeId);
      if (node && node.length) {
        cy.elements().removeClass('highlight');
        node.addClass('highlight');
        cy.animate({
          center: { eles: node },
          zoom: Math.max(cy.zoom(), 1.2)
        }, { duration: 500 });
        renderMetadataPanel(detailEl, node.data(), { edgeLabelMap });
      }
      idx += 1;
      if (idx >= selected.nodes.length) {
        clearInterval(timer);
      }
    }, 1000);
  });
}

function focusFromHash(cy, zoomAPI) {
  const hash = window.location.hash ?? '';
  if (!hash.startsWith('#node=')) {
    return;
  }
  const nodeId = decodeURIComponent(hash.slice('#node='.length));
  const node = cy.getElementById(nodeId);
  if (!node || !node.length) {
    return;
  }

  const cls = node.data('class');
  if (cls === 'concept') {
    zoomAPI.toSolar(nodeId);
  } else if (cls === 'publication') {
    zoomAPI.toOrbit(nodeId);
  } else {
    cy.animate({ center: { eles: node }, zoom: 1.2 }, { duration: 600 });
  }

  cy.elements().removeClass('highlight');
  node.addClass('highlight');
  renderMetadataPanel(detailEl, node.data(), { edgeLabelMap });
}

async function main() {
  const [graphResponse, timelineResponse, pathsResponse] = await Promise.all([
    fetch('../registry/knowledge_graph.json'),
    fetch('../registry/atlas_timeline.json'),
    fetch('../registry/atlas_paths.json').catch(() => null)
  ]);

  const sourceGraph = await graphResponse.json();
  const timeline = await timelineResponse.json();
  const pathsData = pathsResponse ? await pathsResponse.json() : { paths: [] };
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

  annotateConceptStats(cy);
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

  bindGuidedPaths(cy, pathsData?.paths ?? []);

  cy.on('tap', 'node, edge', (evt) => {
    cy.elements().removeClass('highlight');
    evt.target.addClass('highlight');
    renderMetadataPanel(detailEl, evt.target.data(), { edgeLabelMap });

    if (evt.target.isNode()) {
      const cls = evt.target.data('class');
      if (cls === 'concept') {
        zoomAPI.toSolar(evt.target.id());
      }
      if (cls === 'publication') {
        zoomAPI.toOrbit(evt.target.id());
      }
      const encoded = encodeURIComponent(evt.target.id());
      window.history.replaceState(null, '', `#node=${encoded}`);
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
    window.history.replaceState(null, '', window.location.pathname);
  });

  focusFromHash(cy, zoomAPI);
}

main().catch((err) => {
  detailEl.innerHTML = `<p>Failed to load atlas: ${err.message}</p>`;
});
