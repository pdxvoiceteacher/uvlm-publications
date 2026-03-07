import { computeAtlasLayout } from './layoutEngine.js';
import { nodeStyles } from './nodeStyles.js';
import { bindSearchAndFilter, centerOnQuery } from './search.js';
import { renderMetadataPanel, setDefaultPanel } from './metadataPanel.js';
import { bindZoomController } from './zoomController.js';
import { timelineConfig } from './timelineConfig.js';
import { createTimelineEngine } from './timelineEngine.js';
import { bindTimelineControls } from './timelineControls.js';
import { edgeLabelMap } from './edgeLabels.js';
import { applyAttentionOverlay, loadAttentionOverlay } from './attentionOverlay.js';
import { applyDriftVisualization, loadDriftOverlay } from './driftVisualization.js';

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
const constellationSelectEl = document.getElementById('constellations');
const constellationClearEl = document.getElementById('constellation-clear');
const exportPngEl = document.getElementById('export-png');
const exportSvgEl = document.getElementById('export-svg');
const showOnboardingEl = document.getElementById('show-onboarding');
const onboardingEl = document.getElementById('onboarding');
const onboardingDismissEl = document.getElementById('onboarding-dismiss');

const timelineModeEl = document.getElementById('mode-toggle');
const timelinePlayEl = document.getElementById('timeline-play');
const timelinePauseEl = document.getElementById('timeline-pause');
const timelineResetEl = document.getElementById('timeline-reset');
const timelineSpeedEl = document.getElementById('timeline-speed');
const timelineSliderEl = document.getElementById('timeline-slider');
const timelineDateEl = document.getElementById('timeline-date');

const THEORY_EDGE_TYPES = ['contains', 'dependsOn', 'refines', 'extends', 'contrastsWith'];
const REFERENCE_EDGE_TYPES = ['cites', 'isReferencedBy'];

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
    const relatedEdges = cy
      .edges()
      .filter((edge) => THEORY_EDGE_TYPES.includes(edge.data('type')))
      .filter((edge) => edge.source().id() === node.id() || edge.target().id() === node.id());

    const relatedConcepts = relatedEdges.map((edge) => {
      const targetNode = edge.source().id() === node.id() ? edge.target() : edge.source();
      return {
        target: targetNode.id(),
        targetLabel: targetNode.data('value') || targetNode.id(),
        type: edge.data('type'),
        label: edgeLabelMap[edge.data('type')] ?? edge.data('type')
      };
    });

    node.data('relatedConceptCount', relatedConcepts.length);
    node.data('relatedConcepts', relatedConcepts);
  });
}

function isCurrentlyVisible(ele) {
  return !ele.hasClass('temporal-hidden') && !ele.hasClass('zoom-hidden') && !ele.hasClass('filter-hidden');
}

function clearSpotlight(cy) {
  cy.elements().removeClass('spotlight-dim spotlight-focus highlight');
}

function applyConceptSpotlight(cy, conceptId) {
  const concept = cy.getElementById(conceptId);
  if (!concept || !concept.length) {
    return;
  }

  clearSpotlight(cy);

  const keepNodes = new Set([conceptId]);
  const keepEdges = [];

  cy.edges().forEach((edge) => {
    const type = edge.data('type');
    const src = edge.source();
    const tgt = edge.target();

    const isConceptToConcept = THEORY_EDGE_TYPES.includes(type) && (src.id() === conceptId || tgt.id() === conceptId);
    const isConnectedPublication = type === 'mentionsConcept' && tgt.id() === conceptId;
    const isConnectedContext = ['authoredBy', 'taggedWith'].includes(type) && keepNodes.has(src.id());

    if (isConceptToConcept || isConnectedPublication || isConnectedContext) {
      keepNodes.add(src.id());
      keepNodes.add(tgt.id());
      keepEdges.push(edge);
    }
  });

  cy.nodes().forEach((node) => {
    if (!keepNodes.has(node.id()) && isCurrentlyVisible(node)) {
      node.addClass('spotlight-dim');
    } else if (keepNodes.has(node.id())) {
      node.addClass('spotlight-focus');
    }
  });

  cy.edges().forEach((edge) => {
    if (!keepEdges.includes(edge) && isCurrentlyVisible(edge)) {
      edge.addClass('spotlight-dim');
    }
  });
}

function bindGuidedPaths(cy, paths, onNodeFocus) {
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

    clearSpotlight(cy);
    let idx = 0;
    const timer = setInterval(() => {
      const nodeId = selected.nodes[idx];
      const node = cy.getElementById(nodeId);
      if (node && node.length) {
        clearSpotlight(cy);
        node.addClass('highlight spotlight-focus');
        cy.animate({
          center: { eles: node },
          zoom: Math.max(cy.zoom(), 1.2)
        }, { duration: 500 });
        onNodeFocus(node);
      }
      idx += 1;
      if (idx >= selected.nodes.length) {
        clearInterval(timer);
      }
    }, 1000);
  });
}

function wireOnboarding() {
  const storageKey = 'uvlmAtlasOnboardingDismissed';
  const dismissed = localStorage.getItem(storageKey) === '1';
  if (!dismissed && onboardingEl) {
    onboardingEl.hidden = false;
  }

  onboardingDismissEl?.addEventListener('click', () => {
    onboardingEl.hidden = true;
    localStorage.setItem(storageKey, '1');
  });

  showOnboardingEl?.addEventListener('click', () => {
    onboardingEl.hidden = false;
    localStorage.removeItem(storageKey);
  });
}

function downloadDataUrl(dataUrl, filename) {
  const link = document.createElement('a');
  link.href = dataUrl;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  link.remove();
}

function bindExportControls(cy) {
  exportPngEl?.addEventListener('click', () => {
    const png = cy.png({ full: false, scale: 2, bg: '#02040d' });
    downloadDataUrl(png, 'uvlm-atlas-view.png');
  });

  exportSvgEl?.addEventListener('click', () => {
    if (typeof cy.svg === 'function') {
      const svg = cy.svg({ full: false, scale: 1 });
      const data = `data:image/svg+xml;charset=utf-8,${encodeURIComponent(svg)}`;
      downloadDataUrl(data, 'uvlm-atlas-view.svg');
      return;
    }
    window.alert('SVG export scaffold is present, but Cytoscape SVG extension is not loaded in this build.');
  });
}

function focusFromHash(cy, zoomAPI, focusNode) {
  const hash = window.location.hash ?? '';
  if (hash.startsWith('#constellation=')) {
    return;
  }
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

  focusNode(node);
}

function bindConstellations({ cy, constellations, renderConstellationInfo }) {
  let activeConstellation = null;

  function applyConstellation(constellation) {
    clearSpotlight(cy);
    activeConstellation = constellation;
    if (!constellation) {
      return;
    }

    const members = new Set(constellation.memberNodeIds || []);
    const visibleMembers = [];
    cy.nodes().forEach((node) => {
      const inCluster = members.has(node.id());
      if (inCluster && isCurrentlyVisible(node)) {
        node.addClass('spotlight-focus');
        visibleMembers.push(node.id());
      } else if (!inCluster && isCurrentlyVisible(node)) {
        node.addClass('spotlight-dim');
      }
    });

    cy.edges().forEach((edge) => {
      if (!isCurrentlyVisible(edge)) {
        return;
      }
      const inCluster = members.has(edge.source().id()) && members.has(edge.target().id());
      if (inCluster) {
        edge.addClass('spotlight-focus');
      } else {
        edge.addClass('spotlight-dim');
      }
    });

    const visibleEles = cy.elements('.spotlight-focus');
    if (visibleEles.length) {
      cy.fit(visibleEles, 70);
    }

    renderConstellationInfo({
      ...constellation,
      class: 'constellation',
      visibleMemberCount: visibleMembers.length
    });
    window.history.replaceState(null, '', `#constellation=${encodeURIComponent(constellation.id)}`);
  }

  function refresh() {
    if (activeConstellation) {
      applyConstellation(activeConstellation);
    }
  }

  if (!constellationSelectEl) {
    return { applyConstellation, clear: () => applyConstellation(null), refresh };
  }

  constellationSelectEl.innerHTML = '<option value="">Research constellations</option>';
  (constellations ?? []).forEach((c) => {
    const opt = document.createElement('option');
    opt.value = c.id;
    opt.textContent = c.title;
    constellationSelectEl.appendChild(opt);
  });

  constellationSelectEl.addEventListener('change', () => {
    const selected = (constellations ?? []).find((c) => c.id === constellationSelectEl.value) ?? null;
    applyConstellation(selected);
    if (!selected) {
      setDefaultPanel(detailEl);
      window.history.replaceState(null, '', window.location.pathname);
    }
  });

  constellationClearEl?.addEventListener('click', () => {
    constellationSelectEl.value = '';
    applyConstellation(null);
    setDefaultPanel(detailEl);
    window.history.replaceState(null, '', window.location.pathname);
  });

  const hash = window.location.hash ?? '';
  if (hash.startsWith('#constellation=')) {
    const id = decodeURIComponent(hash.slice('#constellation='.length));
    const selected = (constellations ?? []).find((c) => c.id === id) ?? null;
    if (selected) {
      constellationSelectEl.value = selected.id;
      applyConstellation(selected);
    }
  }

  return {
    applyConstellation,
    clear: () => {
      activeConstellation = null;
      clearSpotlight(cy);
    },
    refresh
  };
}

async function main() {
  const [graphResponse, timelineResponse, pathsResponse, constellationsResponse, attentionOverlay, driftOverlay] = await Promise.all([
    fetch('../registry/knowledge_graph.json'),
    fetch('../registry/atlas_timeline.json'),
    fetch('../registry/atlas_paths.json').catch(() => null),
    fetch('../registry/constellations.json').catch(() => null),
    loadAttentionOverlay().catch(() => ({})),
    loadDriftOverlay().catch(() => ({}))
  ]);

  const sourceGraph = await graphResponse.json();
  const timeline = await timelineResponse.json();
  const pathsData = pathsResponse ? await pathsResponse.json() : { paths: [] };
  const constellationsData = constellationsResponse ? await constellationsResponse.json() : { constellations: [] };
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
          'shadow-blur': 20,
          'shadow-opacity': 0.6
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
          'line-style': 'solid',
          opacity: 1
        }
      },
      {
        selector: 'edge[type = "cites"], edge[type = "isReferencedBy"], edge[type = "isVersionOf"]',
        style: {
          'line-style': 'dashed',
          'line-color': '#91a2c4',
          'target-arrow-color': '#91a2c4'
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
      },
      {
        selector: '.spotlight-dim',
        style: { opacity: 0.15 }
      },
      {
        selector: '.spotlight-focus',
        style: { opacity: 1 }
      },

      {
        selector: '.attention-priority',
        style: {
          'border-width': 2.3,
          'border-color': '#f7d24d'
        }
      },
      {
        selector: '.attention-secondary',
        style: {
          'border-width': 1.8,
          'border-color': '#7dcfff'
        }
      },
      {
        selector: '.drift-high',
        style: {
          'overlay-color': '#ff5d73',
          'overlay-opacity': 0.2,
          'overlay-padding': 3
        }
      },
      {
        selector: '.sonya-candidate',
        style: {
          'border-style': 'double',
          'border-width': 2.6,
          'border-color': '#b6ffce'
        }
      },
      {
        selector: '.reasoning-thread',
        style: {
          'border-color': '#c2a6ff'
        }
      },
      {
        selector: '.reasoning-watch',
        style: {
          'overlay-color': '#ffd37f',
          'overlay-opacity': 0.12,
          'overlay-padding': 2
        }
      },
      {
        selector: '.stability-positive',
        style: {
          'shadow-color': '#73ffa4',
          'shadow-blur': 22,
          'shadow-opacity': 0.28
        }
      },
      {
        selector: '.stability-watch',
        style: {
          'overlay-color': '#ffcc66',
          'overlay-opacity': 0.14,
          'overlay-padding': 3
        }
      },
      {
        selector: '.multimodal-donation',
        style: {
          'border-color': '#8ff3ff'
        }
      },
      {
        selector: '.multimodal-watch',
        style: {
          'overlay-color': '#7fd3ff',
          'overlay-opacity': 0.12,
          'overlay-padding': 3
        }
      },
      {
        selector: '.review-candidate',
        style: {
          'border-color': '#ff9ad9',
          'border-width': 2.4
        }
      },
      {
        selector: '.watch-queue',
        style: {
          'overlay-color': '#d9a6ff',
          'overlay-opacity': 0.12,
          'overlay-padding': 2
        }
      },
      {
        selector: '.governance-review',
        style: {
          'border-color': '#ffb36b'
        }
      },
      {
        selector: '.governance-watch',
        style: {
          'overlay-color': '#ffc27a',
          'overlay-opacity': 0.1,
          'overlay-padding': 2
        }
      },
      {
        selector: '.constitutional-watch',
        style: {
          'border-color': '#94d3ff',
          'border-width': 2
        }
      },
      {
        selector: '.constitutional-freeze',
        style: {
          'overlay-color': '#85b7ff',
          'overlay-opacity': 0.12,
          'overlay-padding': 3
        }
      },
      {
        selector: '.deliberation-docket',
        style: {
          'border-color': '#8ac5ff'
        }
      },
      {
        selector: '.deliberation-watch',
        style: {
          'overlay-color': '#8ac5ff',
          'overlay-opacity': 0.08,
          'overlay-padding': 2
        }
      },
      {
        selector: '.deliberation-urgent',
        style: {
          'border-width': 2.2,
          'border-color': '#ffd28f'
        }
      },
      {
        selector: '.anti-capture-watch',
        style: {
          'shadow-color': '#ff9b9b',
          'shadow-opacity': 0.18,
          'shadow-blur': 20
        }
      },
      {
        selector: '.continuity-docket',
        style: {
          'border-color': '#9be7b1'
        }
      },
      {
        selector: '.continuity-watch',
        style: {
          'overlay-color': '#9be7b1',
          'overlay-opacity': 0.08,
          'overlay-padding': 2
        }
      },
      {
        selector: '.continuity-fragile',
        style: {
          'border-width': 2,
          'border-color': '#ffd9a0'
        }
      },
      {
        selector: '.continuity-freeze',
        style: {
          'overlay-color': '#b7a6ff',
          'overlay-opacity': 0.12,
          'overlay-padding': 3
        }
      },
      {
        selector: '.recovery-docket',
        style: {
          'border-color': '#a6f2ff'
        }
      },
      {
        selector: '.recovery-watch',
        style: {
          'overlay-color': '#a6f2ff',
          'overlay-opacity': 0.08,
          'overlay-padding': 2
        }
      },
      {
        selector: '.escrow-ready',
        style: {
          'shadow-color': '#9cf6e0',
          'shadow-opacity': 0.2,
          'shadow-blur': 18
        }
      },
      {
        selector: '.recovery-fragile',
        style: {
          'border-width': 2,
          'border-color': '#ffd8a4'
        }
      },
      {
        selector: '.attestation-docket',
        style: {
          'border-color': '#b9f0ff'
        }
      },
      {
        selector: '.attestation-watch',
        style: {
          'overlay-color': '#b9f0ff',
          'overlay-opacity': 0.08,
          'overlay-padding': 2
        }
      },
      {
        selector: '.witness-sufficient',
        style: {
          'shadow-color': '#8ff0cc',
          'shadow-opacity': 0.18,
          'shadow-blur': 18
        }
      },
      {
        selector: '.attestation-sensitive',
        style: {
          'border-width': 2,
          'border-color': '#ffd3a0'
        }
      },
      {
        selector: '.precedent-docket',
        style: {
          'border-color': '#d4c2ff'
        }
      },
      {
        selector: '.precedent-watch',
        style: {
          'overlay-color': '#d4c2ff',
          'overlay-opacity': 0.08,
          'overlay-padding': 2
        }
      },
      {
        selector: '.precedent-divergent',
        style: {
          'border-width': 2,
          'border-color': '#ffc79a'
        }
      },
      {
        selector: '.precedent-strong',
        style: {
          'shadow-color': '#cab4ff',
          'shadow-opacity': 0.18,
          'shadow-blur': 18
        }
      },

      {
        selector: '.scenario-docket',
        style: {
          'border-color': '#b9d7ff'
        }
      },
      {
        selector: '.scenario-watch',
        style: {
          'overlay-color': '#b9d7ff',
          'overlay-opacity': 0.08,
          'overlay-padding': 2
        }
      },
      {
        selector: '.scenario-freeze',
        style: {
          'border-width': 2,
          'border-color': '#ffd1b0'
        }
      },
      {
        selector: '.scenario-rehearse-recovery',
        style: {
          'shadow-color': '#b9d7ff',
          'shadow-opacity': 0.12,
          'shadow-blur': 14
        }
      },
      {
        selector: '.institutional-status-indicator',
        style: {
          'border-color': '#b7ecd1'
        }
      },
      {
        selector: '.chamber-conflict-indicator',
        style: {
          'border-width': 2,
          'border-color': '#ffd9a8'
        }
      },
      {
        selector: '.system-health-overview',
        style: {
          'shadow-color': '#b7ecd1',
          'shadow-opacity': 0.12,
          'shadow-blur': 14
        }
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

  function focusNode(node) {
    clearSpotlight(cy);
    cy.elements().removeClass('highlight');
    node.addClass('highlight');
    renderMetadataPanel(detailEl, node.data(), { edgeLabelMap });
  }

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

  function reapplyPublisherOverlays() {
    applyAttentionOverlay(cy, attentionOverlay);
    timelineEngine.refreshConceptVisuals();
    applyDriftVisualization(cy, driftOverlay);
  }

  reapplyPublisherOverlays();

  bindGuidedPaths(cy, pathsData?.paths ?? [], (node) => focusNode(node));

  const constellationApi = bindConstellations({
    cy,
    constellations: constellationsData?.constellations ?? [],
    renderConstellationInfo: (constellationData) => renderMetadataPanel(detailEl, constellationData, { edgeLabelMap })
  });

  timelineEngine.onStateChange(() => {
    reapplyPublisherOverlays();
    constellationApi.refresh();
  });

  detailEl.addEventListener('click', (evt) => {
    const btn = evt.target.closest('.concept-relation-link');
    if (!btn) {
      return;
    }
    const targetId = btn.getAttribute('data-concept-target');
    const target = cy.getElementById(targetId);
    if (!target || !target.length) {
      return;
    }
    zoomAPI.toSolar(targetId);
    focusNode(target);
  });

  cy.on('tap', 'node, edge', (evt) => {
    constellationApi.clear();
    focusNode(evt.target);

    if (evt.target.isNode()) {
      const cls = evt.target.data('class');
      if (cls === 'concept') {
        zoomAPI.toSolar(evt.target.id());
        applyConceptSpotlight(cy, evt.target.id());
      }
      if (cls === 'publication') {
        zoomAPI.toOrbit(evt.target.id());
      }
      const encoded = encodeURIComponent(evt.target.id());
      window.history.replaceState(null, '', `#node=${encoded}`);
    }
  });

  cy.on('tap', (evt) => {
    if (evt.target === cy) {
      clearSpotlight(cy);
      cy.elements().removeClass('highlight');
      setDefaultPanel(detailEl);
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
    cy.elements().removeClass('zoom-hidden filter-hidden highlight spotlight-dim spotlight-focus sonya-candidate reasoning-thread reasoning-watch stability-positive stability-watch multimodal-donation multimodal-watch review-candidate watch-queue governance-review governance-watch constitutional-watch constitutional-freeze deliberation-docket deliberation-watch deliberation-urgent anti-capture-watch continuity-docket continuity-watch continuity-fragile continuity-freeze recovery-docket recovery-watch escrow-ready recovery-fragile attestation-docket attestation-watch witness-sufficient attestation-sensitive precedent-docket precedent-watch precedent-divergent precedent-strong scenario-docket scenario-watch scenario-freeze scenario-rehearse-recovery institutional-status-indicator chamber-conflict-indicator system-health-overview');
    constellationApi.clear();
    cy.fit(cy.elements(':visible'), 60);
    setDefaultPanel(detailEl);
    searchAPI.apply();
    window.history.replaceState(null, '', window.location.pathname);
    reapplyPublisherOverlays();
  });

  wireOnboarding();
  bindExportControls(cy);
  focusFromHash(cy, zoomAPI, focusNode);
}

main().catch((err) => {
  detailEl.innerHTML = `<p>Failed to load atlas: ${err.message}</p>`;
});
