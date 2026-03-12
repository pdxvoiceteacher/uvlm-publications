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
import { applyTerraceOverlay, bindTerraceOverlayToggle, terraceResettableClasses } from './telTerraceOverlay.js';
import { applyOrthodoxyCorridorOverlay, bindOrthodoxyCorridorToggles, orthodoxyResettableClasses } from './telOrthodoxyOverlay.js';
import { applySchismOverlay, bindSchismOverlayToggle, schismResettableClasses } from './telSchismOverlay.js';
import { applyRebraidOverlay, clearRebraidOverlay, bindRebraidOverlayToggle, rebraidResettableClasses } from './telRebraidOverlay.js';
import { applyCorridorOverlay, bindCorridorOverlayToggle, corridorResettableClasses } from './telCorridorOverlay.js';
import { applyRiverOverlay, clearRiverOverlay, bindRiverOverlayToggle, riverResettableClasses } from './telRiverOverlay.js';
import { applyDeltaOverlay, clearDeltaOverlay, bindDeltaOverlayToggle, deltaResettableClasses } from './telDeltaOverlay.js';
import { applyRuptureOverlay, clearRuptureOverlay, bindRuptureOverlayToggle, ruptureResettableClasses } from './telRuptureOverlay.js';
import { applyCascadeOverlay, clearCascadeOverlay, bindCascadeOverlayToggle, cascadeResettableClasses } from './telCascadeOverlay.js';
import { applyAgentTelemetryOverlay, clearAgentTelemetryOverlay, AGENT_TELEMETRY_RESETTABLE_CLASSES } from './telAgentTelemetryOverlay.js';
import { applyNavigationOverlay, clearNavigationOverlay, bindNavigationToggle, NAVIGATION_RESETTABLE_CLASSES } from './telNavigationOverlay.js';

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
const showTerraceReadinessEl = document.getElementById('show-terrace-readiness');
const showOrthodoxyRiskEl = document.getElementById('show-orthodoxy-risk');
const showDiscoveryCorridorEl = document.getElementById('show-discovery-corridor');
const showSchismRiskEl = document.getElementById('show-schism-risk');
const showRebraidSignalsEl = document.getElementById('toggle-rebraid') || document.getElementById('show-rebraid-signals');
const showCorridorPathsEl = document.getElementById('toggle-corridor');
const showRiverFlowEl = document.getElementById('toggle-river');
const showKnowledgeDeltasEl = document.getElementById('toggle-delta');
const showRuptureSignalsEl = document.getElementById('toggle-rupture');
const showCascadeHealthEl = document.getElementById('toggle-cascade');
const showAgentTelemetryEl = document.getElementById('toggle-agent-telemetry');
const showNavigationEl = document.getElementById('toggle-navigation');
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
  const [graphResponse, timelineResponse, pathsResponse, constellationsResponse, attentionOverlay, driftOverlay, agentTelemetryResponse, aiGuidanceResponse, navigationStateResponse] = await Promise.all([
    fetch('../registry/knowledge_graph.json'),
    fetch('../registry/atlas_timeline.json'),
    fetch('../registry/atlas_paths.json').catch(() => null),
    fetch('../registry/constellations.json').catch(() => null),
    loadAttentionOverlay().catch(() => ({})),
    loadDriftOverlay().catch(() => ({})),
    fetch('../bridge/agent_telemetry_event_map.json').catch(() => null),
    fetch('../bridge/ai_guidance.json').catch(() => null),
    fetch('../bridge/navigation_state.json').catch(() => null)
  ]);

  const sourceGraph = await graphResponse.json();
  const timeline = await timelineResponse.json();
  const pathsData = pathsResponse ? await pathsResponse.json() : { paths: [] };
  const constellationsData = constellationsResponse ? await constellationsResponse.json() : { constellations: [] };
  const agentTelemetryMap = agentTelemetryResponse ? await agentTelemetryResponse.json().catch(() => ({})) : {};
  const aiGuidance = aiGuidanceResponse ? await aiGuidanceResponse.json().catch(() => ({})) : {};
  const navigationState = navigationStateResponse ? await navigationStateResponse.json().catch(() => ({})) : {};
  window.__bridgeArtifacts = {
    ...(window.__bridgeArtifacts ?? {}),
    agentTelemetryMap,
    agent_telemetry_event_map: agentTelemetryMap,
    aiGuidance,
    navigation_state: navigationState
  };
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
        selector: '.terrace-approaching',
        style: {
          'background-color': 'rgba(255,165,0,0.8)',
          'border-color': '#ffd199',
          'border-width': 2.4
        }
      },
      {
        selector: '.terrace-converged-orthodoxy',
        style: {
          'background-color': 'rgba(200,50,50,0.8)',
          'border-color': '#ff9fa7',
          'border-width': 2.8
        }
      },
      {
        selector: '.terrace-caution-overlay',
        style: {
          'overlay-color': 'rgba(200,50,50,0.25)',
          'overlay-opacity': 0.14,
          'overlay-padding': 2
        }
      },

      {
        selector: '.orthodoxy-alert',
        style: {
          'background-color': 'rgba(185, 22, 22, 0.82)',
          'border-color': '#ff8a8a',
          'border-width': 2.9
        }
      },
      {
        selector: '.orthodoxy-caution-overlay',
        style: {
          'overlay-color': 'rgba(220, 40, 40, 0.32)',
          'overlay-opacity': 0.16,
          'overlay-padding': 2
        }
      },
      {
        selector: '.corridor-forming',
        style: {
          'background-color': 'rgba(66, 190, 119, 0.82)',
          'border-color': '#8fffc3',
          'border-width': 2.6
        }
      },
      {
        selector: '.corridor-reopening-overlay',
        style: {
          'overlay-color': 'rgba(66, 190, 119, 0.3)',
          'overlay-opacity': 0.16,
          'overlay-padding': 2
        }
      },

      {
        selector: '.schism-branch',
        style: {
          'background-color': 'rgba(172, 62, 222, 0.8)',
          'border-color': '#d9a5ff',
          'border-width': 2.8
        }
      },
      {
        selector: '.schism-coupling-overlay',
        style: {
          'overlay-color': 'rgba(172, 62, 222, 0.28)',
          'overlay-opacity': 0.18,
          'overlay-padding': 3,
          'border-style': 'dashed'
        }
      },

      {
        selector: '.rebraid-node',
        style: {
          'background-color': 'rgba(84, 193, 212, 0.82)',
          'border-color': '#b8f7ff',
          'border-width': 2.7
        }
      },
      {
        selector: '.rebraid-coupling-overlay',
        style: {
          'overlay-color': 'rgba(84, 193, 212, 0.28)',
          'overlay-opacity': 0.18,
          'overlay-padding': 3
        }
      },

      {
        selector: '.corridor-node, .corridor-highlight',
        style: {
          'background-color': 'rgba(255, 160, 64, 0.86)',
          'border-color': '#ffd4a2',
          'border-width': 2.5
        }
      },
      {
        selector: '.river-node, .river-highlight, .river-flowing',
        style: {
          'background-color': 'rgba(88, 221, 255, 0.84)',
          'border-color': '#bcf4ff',
          'border-width': 2.5
        }
      },
      {
        selector: '.delta-node, .delta-highlight, .delta-forming',
        style: {
          'background-color': 'rgba(225, 98, 255, 0.84)',
          'border-color': '#f1b1ff',
          'border-width': 2.5
        }
      },
      {
        selector: '.rupture-node, .rupture-highlight, .rupture-looming',
        style: {
          'background-color': 'rgba(255, 165, 0, 0.22)',
          'border-color': '#ffa500',
          'border-width': 2.7
        }
      },

      {
        selector: '.cascade-strong',
        style: {
          'background-color': '#00ffff',
          'line-color': '#00ffff',
          'target-arrow-color': '#00ffff',
          'width': 3.4,
          'border-color': '#00ffff',
          'border-width': 4,
          'overlay-color': 'rgba(0, 255, 255, 0.25)',
          'overlay-opacity': 0.18,
          'overlay-padding': 3
        }
      },
      {
        selector: '.cascade-risk',
        style: {
          'border-style': 'dashed',
          'border-color': '#ff00ff',
          'border-width': 3,
          'overlay-color': 'rgba(255, 0, 255, 0.18)',
          'overlay-opacity': 0.14,
          'overlay-padding': 2
        }
      },
      {
        selector: '.cascade-safe',
        style: {
          'border-style': 'solid',
          'border-color': '#00ff00',
          'border-width': 3,
          'overlay-color': 'rgba(0, 255, 0, 0.14)',
          'overlay-opacity': 0.1,
          'overlay-padding': 2
        }
      },
      {
        selector: '.rebraid-strong',
        style: {
          'background-color': '#ff00ff',
          'border-color': '#ff00ff',
          'border-style': 'dashed',
          'border-width': 2.8,
          'overlay-color': 'rgba(255, 0, 255, 0.24)',
          'overlay-opacity': 0.18,
          'overlay-padding': 3
        }
      },


      {
        selector: '.agent-novelty-hotspot',
        style: {
          'border-width': 4,
          'border-style': 'double',
          'border-color': '#00bcd4',
          'background-color': '#e0f7fa'
        }
      },
      {
        selector: '.agent-contradiction-hotspot',
        style: {
          'border-width': 4,
          'border-style': 'dashed',
          'border-color': '#ff00aa',
          'background-color': '#ffe6f2'
        }
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
      },
      {
        selector: '.queue-health-actionable',
        style: {
          'border-color': '#b8e2ff'
        }
      },
      {
        selector: '.backlog-pressure-watch',
        style: {
          'overlay-color': '#b8e2ff',
          'overlay-opacity': 0.08,
          'overlay-padding': 2
        }
      },
      {
        selector: '.review-fatigue-watch',
        style: {
          'border-width': 2,
          'border-color': '#ffd8a4'
        }
      },
      {
        selector: '.metric-gaming-watch',
        style: {
          'border-width': 2,
          'border-color': '#ffc4de'
        }
      },
      {
        selector: '.load-shedding-recommended',
        style: {
          'shadow-color': '#b8e2ff',
          'shadow-opacity': 0.12,
          'shadow-blur': 14
        }
      },
      {
        selector: '.priority-actionable',
        style: {
          'border-color': '#c7d6ff'
        }
      },
      {
        selector: '.triage-watch',
        style: {
          'overlay-color': '#c7d6ff',
          'overlay-opacity': 0.08,
          'overlay-padding': 2
        }
      },
      {
        selector: '.urgency-high',
        style: {
          'border-width': 2,
          'border-color': '#ffd3aa'
        }
      },
      {
        selector: '.priority-critical',
        style: {
          'shadow-color': '#c7d6ff',
          'shadow-opacity': 0.14,
          'shadow-blur': 14
        }
      },
      {
        selector: '.triage-conflict',
        style: {
          'border-width': 2,
          'border-color': '#ffccda'
        }
      },
      {
        selector: '.closure-active',
        style: {
          'border-color': '#cfe7dc'
        }
      },
      {
        selector: '.closure-provisional',
        style: {
          'overlay-color': '#cfe7dc',
          'overlay-opacity': 0.08,
          'overlay-padding': 2
        }
      },
      {
        selector: '.repair-urgent',
        style: {
          'border-width': 2,
          'border-color': '#ffd9b8'
        }
      },
      {
        selector: '.reopened-watch',
        style: {
          'shadow-color': '#ffd7e4',
          'shadow-opacity': 0.14,
          'shadow-blur': 14
        }
      },
      {
        selector: '.symbolic-field-active',
        style: {
          'border-color': '#d5d8ff'
        }
      },
      {
        selector: '.regime-shift-watch',
        style: {
          'overlay-color': '#d5d8ff',
          'overlay-opacity': 0.08,
          'overlay-padding': 2
        }
      },
      {
        selector: '.lambda-warning',
        style: {
          'border-width': 2,
          'border-color': '#ffd6be'
        }
      },
      {
        selector: '.architecture-hint',
        style: {
          'shadow-color': '#d5d8ff',
          'shadow-opacity': 0.14,
          'shadow-blur': 14
        }
      },
      {
        selector: '.verification-active',
        style: {
          'border-color': '#d5ebdf'
        }
      },
      {
        selector: '.claim-typed',
        style: {
          'overlay-color': '#d5ebdf',
          'overlay-opacity': 0.08,
          'overlay-padding': 2
        }
      },
      {
        selector: '.entity-ambiguity',
        style: {
          'border-width': 2,
          'border-color': '#ffd8c8'
        }
      },
      {
        selector: '.verification-urgent',
        style: {
          'shadow-color': '#d5ebdf',
          'shadow-opacity': 0.14,
          'shadow-blur': 14
        }
      },
      {
        selector: '.public-record-active',
        style: {
          'border-color': '#d4e6f5'
        }
      },
      {
        selector: '.entity-graph-linked',
        style: {
          'overlay-color': '#d4e6f5',
          'overlay-opacity': 0.08,
          'overlay-padding': 2
        }
      },
      {
        selector: '.relationship-ambiguous',
        style: {
          'border-width': 2,
          'border-color': '#ffd7c7'
        }
      },
      {
        selector: '.custody-fragile',
        style: {
          'shadow-color': '#ffd7c7',
          'shadow-opacity': 0.14,
          'shadow-blur': 14
        }
      },
      {
        selector: '.machine-readable-record',
        style: {
          'border-style': 'dashed',
          'border-width': 2
        }
      },

      {
        selector: '.investigation-active',
        style: {
          'border-color': '#cde8ff'
        }
      },
      {
        selector: '.investigation-stage-mid',
        style: {
          'overlay-color': '#cde8ff',
          'overlay-opacity': 0.08,
          'overlay-padding': 2
        }
      },
      {
        selector: '.investigation-stage-late',
        style: {
          'border-width': 2,
          'border-color': '#ffd8ae'
        }
      },
      {
        selector: '.investigation-plan-progressing',
        style: {
          'shadow-color': '#cde8ff',
          'shadow-opacity': 0.14,
          'shadow-blur': 14
        }
      },
      {
        selector: '.investigation-blocked',
        style: {
          'border-width': 2,
          'border-color': '#ffc8d8'
        }
      },
      {
        selector: '.dependency-graph-linked',
        style: {
          'border-style': 'double',
          'border-width': 2
        }
      },

      {
        selector: '.authority-gated',
        style: {
          'border-color': '#d7e8ff'
        }
      },
      {
        selector: '.weak-evidence-signal',
        style: {
          'overlay-color': '#d7e8ff',
          'overlay-opacity': 0.07,
          'overlay-padding': 2
        }
      },
      {
        selector: '.authority-mismatch',
        style: {
          'border-width': 2,
          'border-color': '#ffd8d8'
        }
      },
      {
        selector: '.propagation-restricted',
        style: {
          'shadow-color': '#d7e8ff',
          'shadow-opacity': 0.12,
          'shadow-blur': 13
        }
      },
      {
        selector: '.maturity-gated',
        style: {
          'border-style': 'dotted',
          'border-width': 2
        }
      },

      {
        selector: '.review-packet-ready',
        style: {
          'border-color': '#dcecff'
        }
      },
      {
        selector: '.review-packet-watch',
        style: {
          'overlay-color': '#dcecff',
          'overlay-opacity': 0.08,
          'overlay-padding': 2
        }
      },
      {
        selector: '.packet-ambiguity-high',
        style: {
          'border-width': 2,
          'border-color': '#ffd7cc'
        }
      },
      {
        selector: '.uncertainty-disclosed',
        style: {
          'shadow-color': '#dcecff',
          'shadow-opacity': 0.12,
          'shadow-blur': 13
        }
      },
      {
        selector: '.synthesis-bounded',
        style: {
          'border-style': 'dashed',
          'border-width': 2
        }
      },

      {
        selector: '.pattern-cluster-active',
        style: {
          'border-color': '#dce7ff'
        }
      },
      {
        selector: '.cross-case-hints',
        style: {
          'overlay-color': '#dce7ff',
          'overlay-opacity': 0.08,
          'overlay-padding': 2
        }
      },
      {
        selector: '.pattern-maturity-stable',
        style: {
          'shadow-color': '#dce7ff',
          'shadow-opacity': 0.12,
          'shadow-blur': 13
        }
      },
      {
        selector: '.pattern-conflict',
        style: {
          'border-width': 2,
          'border-color': '#ffd5d5'
        }
      },

      {
        selector: '.pattern-timeline-active',
        style: {
          'border-color': '#dfe7ff'
        }
      },
      {
        selector: '.persistence-stable',
        style: {
          'shadow-color': '#dfe7ff',
          'shadow-opacity': 0.12,
          'shadow-blur': 13
        }
      },
      {
        selector: '.temporal-conflict-marker',
        style: {
          'border-width': 2,
          'border-color': '#ffd3d3'
        }
      },
      {
        selector: '.causal-bundle-active',
        style: {
          'border-color': '#dfeeff'
        }
      },
      {
        selector: '.mechanism-candidate',
        style: {
          'overlay-color': '#dfeeff',
          'overlay-opacity': 0.08,
          'overlay-padding': 2
        }
      },
      {
        selector: '.explanatory-gap-high',
        style: {
          'border-width': 2,
          'border-color': '#ffd6d6'
        }
      },
      {
        selector: '.prohibited-conclusion',
        style: {
          'shadow-color': '#dfeeff',
          'shadow-opacity': 0.12,
          'shadow-blur': 13
        }
      },
      {
        selector: '.causal-conflict-marker',
        style: {
          'border-style': 'dotted',
          'border-width': 2
        }
      },
      {
        selector: '.collaborative-review-active',
        style: {
          'border-color': '#e5f4ff'
        }
      },
      {
        selector: '.consensus-provisional',
        style: {
          'overlay-color': '#e5f4ff',
          'overlay-opacity': 0.08,
          'overlay-padding': 2
        }
      },
      {
        selector: '.dissent-present',
        style: {
          'border-style': 'dashed',
          'border-width': 2
        }
      },
      {
        selector: '.collaborative-maturity-bound',
        style: {
          'shadow-color': '#e5f4ff',
          'shadow-opacity': 0.1,
          'shadow-blur': 12
        }
      },
      {
        selector: '.telemetry-field-active',
        style: {
          'border-color': '#edf8ff'
        }
      },
      {
        selector: '.lattice-transition',
        style: {
          'border-style': 'dashed',
          'border-width': 2
        }
      },
      {
        selector: '.donor-pattern-active',
        style: {
          'overlay-color': '#edf8ff',
          'overlay-opacity': 0.08,
          'overlay-padding': 2
        }
      },
      {
        selector: '.taf-elevated',
        style: {
          'shadow-color': '#edf8ff',
          'shadow-opacity': 0.1,
          'shadow-blur': 12
        }
      },
      {
        selector: '.branch-novel',
        style: {
          'border-width': 2,
          'border-color': '#d8ebff'
        }
      },
      {
        selector: '.branch-maturity-bound',
        style: {
          'border-style': 'dotted'
        }
      },
      {
        selector: '.branch-lifecycle-active',
        style: {
          'border-color': '#eef6ff'
        }
      },
      {
        selector: '.branch-conflict-graph',
        style: {
          'border-style': 'dashed',
          'border-width': 2
        }
      },
      {
        selector: '.branch-decay-indicator',
        style: {
          'border-color': '#ffe0e0',
          'border-width': 2
        }
      },
      {
        selector: '.branch-reinforcement-trend',
        style: {
          'shadow-color': '#eef6ff',
          'shadow-opacity': 0.12,
          'shadow-blur': 12
        }
      },
      {
        selector: '.branch-contradiction-trend',
        style: {
          'overlay-color': '#ffe0e0',
          'overlay-opacity': 0.08,
          'overlay-padding': 2
        }
      },
      {
        selector: '.forecast-accuracy-high',
        style: {
          'border-color': '#eaf6ff'
        }
      },
      {
        selector: '.calibration-improving',
        style: {
          'shadow-color': '#eaf6ff',
          'shadow-opacity': 0.1,
          'shadow-blur': 12
        }
      },
      {
        selector: '.branch-reliability-stable',
        style: {
          'border-width': 2,
          'border-color': '#dcebff'
        }
      },
      {
        selector: '.prediction-timeline-active',
        style: {
          'overlay-color': '#eaf6ff',
          'overlay-opacity': 0.08,
          'overlay-padding': 2
        }
      },
      {
        selector: '.experimental-active',
        style: {
          'border-color': '#f1f7ff'
        }
      },
      {
        selector: '.falsification-ready',
        style: {
          'shadow-color': '#f1f7ff',
          'shadow-opacity': 0.1,
          'shadow-blur': 11
        }
      },
      {
        selector: '.replication-defined',
        style: {
          'overlay-color': '#f1f7ff',
          'overlay-opacity': 0.08,
          'overlay-padding': 2
        }
      },
      {
        selector: '.theory-gate-hold',
        style: {
          'border-style': 'dotted',
          'border-width': 2
        }
      },

      {
        selector: '.theory-corpus-active',
        style: {
          'border-color': '#eef1ff'
        }
      },
      {
        selector: '.theory-negative-results',
        style: {
          'overlay-color': '#ffeef2',
          'overlay-opacity': 0.08,
          'overlay-padding': 2
        }
      },
      {
        selector: '.theory-revision-lineage',
        style: {
          'shadow-color': '#eef1ff',
          'shadow-opacity': 0.1,
          'shadow-blur': 10
        }
      },
      {
        selector: '.theory-competition-open',
        style: {
          'border-style': 'dashed',
          'border-width': 2,
          'border-color': '#e5e9ff'
        }
      },

      {
        selector: '.agency-mode-active',
        style: {
          'border-color': '#f3f0ff'
        }
      },
      {
        selector: '.agency-volitional-edge',
        style: {
          'shadow-color': '#f3f0ff',
          'shadow-opacity': 0.1,
          'shadow-blur': 10
        }
      },
      {
        selector: '.agency-deterministic-edge',
        style: {
          'overlay-color': '#f3f0ff',
          'overlay-opacity': 0.08,
          'overlay-padding': 2
        }
      },
      {
        selector: '.agency-vhat-provisional',
        style: {
          'border-style': 'dashed',
          'border-width': 2,
          'border-color': '#ece6ff'
        }
      },
      {
        selector: '.agency-governance-bounded',
        style: {
          'border-color': '#eee8ff'
        }
      },
      {
        selector: '.agency-consent-required',
        style: {
          'overlay-color': '#f6f2ff',
          'overlay-opacity': 0.08,
          'overlay-padding': 2
        }
      },
      {
        selector: '.agency-blame-suppressed',
        style: {
          'shadow-color': '#f0e9ff',
          'shadow-opacity': 0.08,
          'shadow-blur': 9
        }
      },

      {
        selector: '.responsibility-active',
        style: {
          'border-color': '#f0f7f1'
        }
      },
      {
        selector: '.support-pathway-defined',
        style: {
          'shadow-color': '#eef8f0',
          'shadow-opacity': 0.1,
          'shadow-blur': 10
        }
      },
      {
        selector: '.consent-required',
        style: {
          'overlay-color': '#eef8f0',
          'overlay-opacity': 0.08,
          'overlay-padding': 2
        }
      },
      {
        selector: '.coercion-ceiling-strict',
        style: {
          'border-style': 'dashed',
          'border-width': 2,
          'border-color': '#e6f2e9'
        }
      },
      {
        selector: '.sanction-suppressed',
        style: {
          'shadow-color': '#edf6ef',
          'shadow-opacity': 0.08,
          'shadow-blur': 9
        }
      },
      {
        selector: '.intervention-bounded',
        style: {
          'border-color': '#e9f4ec'
        }
      },

      {
        selector: '.transfer-active',
        style: {
          'border-color': '#f1f3ff'
        }
      },
      {
        selector: '.transfer-asymmetry-high',
        style: {
          'overlay-color': '#fff0f4',
          'overlay-opacity': 0.08,
          'overlay-padding': 2
        }
      },
      {
        selector: '.transfer-replication-gated',
        style: {
          'border-style': 'dashed',
          'border-width': 2,
          'border-color': '#ecefff'
        }
      },
      {
        selector: '.transfer-prohibited-claims',
        style: {
          'shadow-color': '#f3f4ff',
          'shadow-opacity': 0.1,
          'shadow-blur': 10
        }
      },
      {
        selector: '.transfer-risk-elevated',
        style: {
          'border-color': '#ecefff'
        }
      },

      {
        selector: '.system-forecast-active',
        style: {
          'border-color': '#eef5ff'
        }
      },
      {
        selector: '.regime-transition-probable',
        style: {
          'shadow-color': '#edf4ff',
          'shadow-opacity': 0.1,
          'shadow-blur': 10
        }
      },
      {
        selector: '.entropy-accumulating',
        style: {
          'overlay-color': '#eef4ff',
          'overlay-opacity': 0.08,
          'overlay-padding': 2
        }
      },
      {
        selector: '.branch-ecosystem-fragile',
        style: {
          'border-style': 'dashed',
          'border-width': 2,
          'border-color': '#e7f0ff'
        }
      },
      {
        selector: '.trajectory-divergent',
        style: {
          'border-color': '#e8f1ff'
        }
      },

      {
        selector: '.curiosity-active',
        style: {
          'border-color': '#f0f9f6'
        }
      },
      {
        selector: '.uncertainty-gradient-high',
        style: {
          'overlay-color': '#f2faf7',
          'overlay-opacity': 0.08,
          'overlay-padding': 2
        }
      },
      {
        selector: '.information-gain-high',
        style: {
          'shadow-color': '#eef8f4',
          'shadow-opacity': 0.1,
          'shadow-blur': 10
        }
      },
      {
        selector: '.experiment-priority-high',
        style: {
          'border-style': 'dashed',
          'border-width': 2,
          'border-color': '#e7f3ee'
        }
      },
      {
        selector: '.entropy-reduction-positive',
        style: {
          'border-color': '#e8f4ef'
        }
      },

      {
        selector: '.value-alignment-active',
        style: {
          'border-color': '#f7f7ef'
        }
      },
      {
        selector: '.knowledge-priority-top',
        style: {
          'border-style': 'dashed',
          'border-width': 2,
          'border-color': '#f0efdd'
        }
      },
      {
        selector: '.welfare-impact-positive',
        style: {
          'shadow-color': '#f5f5ea',
          'shadow-opacity': 0.1,
          'shadow-blur': 10
        }
      },
      {
        selector: '.fairness-impact-watch',
        style: {
          'overlay-color': '#f7f7ed',
          'overlay-opacity': 0.08,
          'overlay-padding': 2
        }
      },
      {
        selector: '.value-risk-flagged',
        style: {
          'border-color': '#f1f1e1'
        }
      },

      {
        selector: '.meta-active',
        style: {
          'border-color': '#f6f2fb'
        }
      },
      {
        selector: '.reasoning-efficiency-high',
        style: {
          'shadow-color': '#f4effc',
          'shadow-opacity': 0.1,
          'shadow-blur': 10
        }
      },
      {
        selector: '.donor-reliability-high',
        style: {
          'border-style': 'dashed',
          'border-width': 2,
          'border-color': '#eee7f8'
        }
      },
      {
        selector: '.governance-constraint-strong',
        style: {
          'overlay-color': '#f6f1fb',
          'overlay-opacity': 0.08,
          'overlay-padding': 2
        }
      },
      {
        selector: '.discovery-productive',
        style: {
          'border-color': '#f0e9f9'
        }
      },

      {
        selector: '.architecture-active',
        style: {
          'border-color': '#f1f6fa'
        }
      },
      {
        selector: '.module-performance-strong',
        style: {
          'shadow-color': '#eef4f9',
          'shadow-opacity': 0.1,
          'shadow-blur': 10
        }
      },
      {
        selector: '.architecture-discovery-productive',
        style: {
          'border-style': 'dashed',
          'border-width': 2,
          'border-color': '#e7eef6'
        }
      },
      {
        selector: '.safeguard-performance-strong',
        style: {
          'overlay-color': '#f0f5fa',
          'overlay-opacity': 0.08,
          'overlay-padding': 2
        }
      },
      {
        selector: '.architecture-proposal-queued',
        style: {
          'border-color': '#e8eff7'
        }
      },

      {
        selector: '.social-entropy-active',
        style: {
          'border-color': '#f7f3f2'
        }
      },
      {
        selector: '.social-status-fraying',
        style: {
          'overlay-color': '#f8f4f3',
          'overlay-opacity': 0.08,
          'overlay-padding': 2
        }
      },
      {
        selector: '.cohesion-fragile',
        style: {
          'border-style': 'dashed',
          'border-width': 2,
          'border-color': '#f1e8e5'
        }
      },
      {
        selector: '.legitimacy-drift-elevated',
        style: {
          'shadow-color': '#f6efed',
          'shadow-opacity': 0.1,
          'shadow-blur': 10
        }
      },
      {
        selector: '.reviewer-concentration-high',
        style: {
          'border-color': '#eee4e1'
        }
      },
      {
        selector: '.reviewer-fatigue-high',
        style: {
          'border-color': '#ece2df'
        }
      },
      {
        selector: '.repair-priority-high',
        style: {
          'border-color': '#ebdfdc'
        }
      },

      {
        selector: '.federation-active',
        style: {
          'border-color': '#f4f6f2'
        }
      },
      {
        selector: '.federation-status-coherent',
        style: {
          'overlay-color': '#f5f7f3',
          'overlay-opacity': 0.08,
          'overlay-padding': 2
        }
      },
      {
        selector: '.stewardship-node-distributed',
        style: {
          'border-style': 'dashed',
          'border-width': 2,
          'border-color': '#eaeee6'
        }
      },
      {
        selector: '.dissent-portable',
        style: {
          'shadow-color': '#f2f5ef',
          'shadow-opacity': 0.1,
          'shadow-blur': 10
        }
      },
      {
        selector: '.capture-risk-elevated',
        style: {
          'border-color': '#e7ebe2'
        }
      },
      {
        selector: '.mitigation-required',
        style: {
          'border-color': '#e5e9df'
        }
      },

      {
        selector: '.emergent-domain-active',
        style: {
          'border-color': '#f3f6f8'
        }
      },
      {
        selector: '.domain-status-emergent',
        style: {
          'overlay-color': '#f4f7f9',
          'overlay-opacity': 0.08,
          'overlay-padding': 2
        }
      },
      {
        selector: '.invariant-pattern-convergent',
        style: {
          'border-style': 'dashed',
          'border-width': 2,
          'border-color': '#e8edf1'
        }
      },
      {
        selector: '.field-birth-pressure-high',
        style: {
          'shadow-color': '#eff3f6',
          'shadow-opacity': 0.1,
          'shadow-blur': 10
        }
      },
      {
        selector: '.domain-boundary-failure-active',
        style: {
          'border-color': '#e4eaee'
        }
      },
      {
        selector: '.commons-legibility-required',
        style: {
          'border-color': '#e2e8ed'
        }
      },
      {
        selector: '.trust-presentation-degraded',
        style: {
          'border-style': 'dotted',
          'border-width': 2,
          'border-color': '#e6dcda'
        }
      },

      {
        selector: '.commons-sovereignty-active',
        style: {
          'border-color': '#f3f5f3'
        }
      },
      {
        selector: '.commons-integrity-fragile',
        style: {
          'overlay-color': '#f4f6f4',
          'overlay-opacity': 0.08,
          'overlay-padding': 2
        }
      },
      {
        selector: '.institutional-capture-risk-elevated',
        style: {
          'border-style': 'dashed',
          'border-width': 2,
          'border-color': '#e8ede8'
        }
      },
      {
        selector: '.public-trust-unstable',
        style: {
          'shadow-color': '#eef2ee',
          'shadow-opacity': 0.1,
          'shadow-blur': 10
        }
      },
      {
        selector: '.epistemic-diversity-high',
        style: {
          'border-color': '#e6ece6'
        }
      },
      {
        selector: '.civilizational-dissent-portable',
        style: {
          'border-color': '#e4ebe4'
        }
      },

      {
        selector: '.civilizational-memory-active',
        style: {
          'border-color': '#f5f3f7'
        }
      },
      {
        selector: '.preservation-criticality-high',
        style: {
          'overlay-color': '#f6f4f8',
          'overlay-opacity': 0.08,
          'overlay-padding': 2
        }
      },
      {
        selector: '.legibility-drifting',
        style: {
          'border-style': 'dashed',
          'border-width': 2,
          'border-color': '#ece8f0'
        }
      },
      {
        selector: '.vocabulary-drift-risk-high',
        style: {
          'shadow-color': '#f2eff5',
          'shadow-opacity': 0.1,
          'shadow-blur': 10
        }
      },
      {
        selector: '.notation-fragility-high',
        style: {
          'border-color': '#e9e4ef'
        }
      },
      {
        selector: '.memory-recoverability-strong',
        style: {
          'border-color': '#e7e2ee'
        }
      },
      {
        selector: '.custody-diversity-high',
        style: {
          'border-color': '#e5dfec'
        }
      },
      {
        selector: '.operationalization-active',
        style: {
          'border-color': '#f4f5f8'
        }
      },
      {
        selector: '.operational-status-bounded-ready',
        style: {
          'overlay-color': '#f5f6f9',
          'overlay-opacity': 0.08,
          'overlay-padding': 2
        }
      },
      {
        selector: '.maturity-class-field-tested',
        style: {
          'border-style': 'dashed',
          'border-width': 2,
          'border-color': '#e9ebf0'
        }
      },
      {
        selector: '.deployment-readiness-bounded',
        style: {
          'shadow-color': '#f0f1f5',
          'shadow-opacity': 0.1,
          'shadow-blur': 10
        }
      },
      {
        selector: '.dead-zone-adjacent',
        style: {
          'border-color': '#e5e7ee'
        }
      },
      {
        selector: '.translation-risk-watch',
        style: {
          'border-color': '#e2e5ec'
        }
      },
      {
        selector: '.safeguards-required',
        style: {
          'border-color': '#e0e3ea'
        }
      },
      {
        selector: '.commons-review-required',
        style: {
          'border-color': '#dde1e8'
        }
      },

      {
        selector: '.discovery-navigation-active',
        style: {
          'border-color': '#f3f6f5'
        }
      },
      {
        selector: '.discovery-status-active',
        style: {
          'overlay-color': '#f4f7f6',
          'overlay-opacity': 0.08,
          'overlay-padding': 2
        }
      },
      {
        selector: '.discovery-vector-cross-domain',
        style: {
          'border-style': 'dashed',
          'border-width': 2,
          'border-color': '#e7eee9'
        }
      },
      {
        selector: '.discovery-bridge-emergent',
        style: {
          'shadow-color': '#eef4f0',
          'shadow-opacity': 0.1,
          'shadow-blur': 10
        }
      },
      {
        selector: '.discovery-corridor-bounded',
        style: {
          'border-color': '#e4ebe6'
        }
      },
      {
        selector: '.discovery-dead-zone-adjacent',
        style: {
          'border-color': '#e2e9e4'
        }
      },
      {
        selector: '.discovery-memory-supported',
        style: {
          'border-color': '#e0e7e2'
        }
      },
      {
        selector: '.discovery-commons-review-required',
        style: {
          'border-color': '#dde5df'
        }
      },
      {
        selector: '.discovery-risk-watch',
        style: {
          'border-color': '#dae2dc'
        }
      },
      {
        selector: '.discovery-repair-corridor',
        style: {
          'border-style': 'dashed',
          'border-width': 2,
          'border-color': '#d7e1da'
        }
      },
      {
        selector: '.discovery-distortion-risk',
        style: {
          'border-color': '#d5dfd8'
        }
      },
      {
        selector: '.discovery-river-seed',
        style: {
          'shadow-color': '#eaf2ed',
          'shadow-opacity': 0.1,
          'shadow-blur': 10
        }
      },
      {
        selector: '.discovery-river-formation',
        style: {
          'overlay-color': '#eef5f1',
          'overlay-opacity': 0.08,
          'overlay-padding': 2
        }
      },
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

  window.cy = cy;

  function toggleAgentTelemetry(enabled) {
    const summary = window.__bridgeArtifacts?.agent_telemetry_event_map;
    if (!summary || !window.cy) return;
    if (enabled) {
      Object.keys(summary.summary?.byAgent || {}).forEach((id) => {
        if ((summary.summary.byAgent[id]?.eventCount ?? 0) > 0) {
          applyAgentTelemetryOverlay(window.cy, id);
        }
      });
    } else {
      clearAgentTelemetryOverlay(window.cy);
    }
  }

  window.toggleAgentTelemetry = toggleAgentTelemetry;
  cy.toggleAgentTelemetry = toggleAgentTelemetry;

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


  function resetOverlays() {
    clearRiverOverlay(cy);
    clearDeltaOverlay(cy);
    clearRuptureOverlay(cy);
    clearCascadeOverlay(cy);
    clearRebraidOverlay(cy);
    clearAgentTelemetryOverlay(cy);
    clearNavigationOverlay(cy);
  }

  function reapplyPublisherOverlays() {
    applyAttentionOverlay(cy, attentionOverlay);
    timelineEngine.refreshConceptVisuals();
    applyDriftVisualization(cy, driftOverlay);
    applyTerraceOverlay(cy, showTerraceReadinessEl ? Boolean(showTerraceReadinessEl.checked) : true);
    applyOrthodoxyCorridorOverlay(cy, {
      orthodoxyEnabled: showOrthodoxyRiskEl ? Boolean(showOrthodoxyRiskEl.checked) : true,
      corridorEnabled: showDiscoveryCorridorEl ? Boolean(showDiscoveryCorridorEl.checked) : true
    });
    applySchismOverlay(cy, showSchismRiskEl ? Boolean(showSchismRiskEl.checked) : true);
    applyRebraidOverlay(cy, showRebraidSignalsEl ? Boolean(showRebraidSignalsEl.checked) : true);
    applyCorridorOverlay(cy, showCorridorPathsEl ? Boolean(showCorridorPathsEl.checked) : true);
    clearRiverOverlay(cy);
    if (showRiverFlowEl ? Boolean(showRiverFlowEl.checked) : true) applyRiverOverlay(cy);
    clearDeltaOverlay(cy);
    if (showKnowledgeDeltasEl ? Boolean(showKnowledgeDeltasEl.checked) : true) applyDeltaOverlay(cy);
    clearRuptureOverlay(cy);
    if (showRuptureSignalsEl ? Boolean(showRuptureSignalsEl.checked) : true) applyRuptureOverlay(cy);
    applyCascadeOverlay(cy, showCascadeHealthEl ? Boolean(showCascadeHealthEl.checked) : true);
    if (showAgentTelemetryEl ? Boolean(showAgentTelemetryEl.checked) : false) {
      toggleAgentTelemetry(true);
    } else {
      toggleAgentTelemetry(false);
    }
    if (showNavigationEl ? Boolean(showNavigationEl.checked) : false) {
      applyNavigationOverlay(cy, window.__bridgeArtifacts?.navigation_state?.result);
    } else {
      clearNavigationOverlay(cy);
    }
  }

  reapplyPublisherOverlays();

  bindGuidedPaths(cy, pathsData?.paths ?? [], (node) => focusNode(node));

  bindTerraceOverlayToggle(cy, showTerraceReadinessEl, () => {
    applyTerraceOverlay(cy, showTerraceReadinessEl ? Boolean(showTerraceReadinessEl.checked) : true);
  });

  bindOrthodoxyCorridorToggles(cy, showOrthodoxyRiskEl, showDiscoveryCorridorEl, () => {
    applyOrthodoxyCorridorOverlay(cy, {
      orthodoxyEnabled: showOrthodoxyRiskEl ? Boolean(showOrthodoxyRiskEl.checked) : true,
      corridorEnabled: showDiscoveryCorridorEl ? Boolean(showDiscoveryCorridorEl.checked) : true
    });
    applySchismOverlay(cy, showSchismRiskEl ? Boolean(showSchismRiskEl.checked) : true);
  });

  bindRebraidOverlayToggle(cy, showRebraidSignalsEl, () => {
    applyRebraidOverlay(cy, showRebraidSignalsEl ? Boolean(showRebraidSignalsEl.checked) : true);
  });

  bindCorridorOverlayToggle(cy, showCorridorPathsEl, () => {
    applyCorridorOverlay(cy, showCorridorPathsEl ? Boolean(showCorridorPathsEl.checked) : true);
  });

  bindRiverOverlayToggle(cy, showRiverFlowEl, () => {
    clearRiverOverlay(cy);
    if (showRiverFlowEl ? Boolean(showRiverFlowEl.checked) : true) applyRiverOverlay(cy);
  });

  bindDeltaOverlayToggle(cy, showKnowledgeDeltasEl, () => {
    clearDeltaOverlay(cy);
    if (showKnowledgeDeltasEl ? Boolean(showKnowledgeDeltasEl.checked) : true) applyDeltaOverlay(cy);
  });

  bindRuptureOverlayToggle(cy, showRuptureSignalsEl, () => {
    clearRuptureOverlay(cy);
    if (showRuptureSignalsEl ? Boolean(showRuptureSignalsEl.checked) : true) applyRuptureOverlay(cy);
  });

  bindCascadeOverlayToggle(cy, showCascadeHealthEl, () => {
    applyCascadeOverlay(cy, showCascadeHealthEl ? Boolean(showCascadeHealthEl.checked) : true);
    if (showAgentTelemetryEl ? Boolean(showAgentTelemetryEl.checked) : false) {
      toggleAgentTelemetry(true);
    } else {
      toggleAgentTelemetry(false);
    }
    if (showNavigationEl ? Boolean(showNavigationEl.checked) : false) {
      applyNavigationOverlay(cy, window.__bridgeArtifacts?.navigation_state?.result);
    } else {
      clearNavigationOverlay(cy);
    }
  });

  if (showAgentTelemetryEl) {
    document.getElementById('toggle-agent-telemetry').addEventListener('change', (evt) => window.toggleAgentTelemetry(evt.target.checked));
  }

  bindNavigationToggle();

  const constellationApi = bindConstellations({
    cy,
    constellations: constellationsData?.constellations ?? [],
    renderConstellationInfo: (constellationData) => renderMetadataPanel(detailEl, constellationData, { edgeLabelMap })
  });

  timelineEngine.onStateChange(() => {
    resetOverlays();
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
    cy.elements().removeClass('zoom-hidden filter-hidden highlight spotlight-dim spotlight-focus sonya-candidate reasoning-thread reasoning-watch stability-positive stability-watch multimodal-donation multimodal-watch review-candidate watch-queue governance-review governance-watch constitutional-watch constitutional-freeze deliberation-docket deliberation-watch deliberation-urgent anti-capture-watch continuity-docket continuity-watch continuity-fragile continuity-freeze recovery-docket recovery-watch escrow-ready recovery-fragile attestation-docket attestation-watch witness-sufficient attestation-sensitive precedent-docket precedent-watch precedent-divergent precedent-strong scenario-docket scenario-watch scenario-freeze scenario-rehearse-recovery institutional-status-indicator chamber-conflict-indicator system-health-overview queue-health-actionable backlog-pressure-watch review-fatigue-watch metric-gaming-watch load-shedding-recommended priority-actionable triage-watch urgency-high priority-critical triage-conflict investigation-active investigation-stage-mid investigation-stage-late investigation-plan-progressing investigation-blocked dependency-graph-linked authority-gated weak-evidence-signal authority-mismatch propagation-restricted maturity-gated review-packet-ready review-packet-watch packet-ambiguity-high uncertainty-disclosed synthesis-bounded pattern-cluster-active cross-case-hints pattern-maturity-stable pattern-conflict pattern-timeline-active persistence-stable temporal-conflict-marker causal-bundle-active mechanism-candidate explanatory-gap-high prohibited-conclusion causal-conflict-marker collaborative-review-active consensus-provisional dissent-present collaborative-maturity-bound telemetry-field-active lattice-transition donor-pattern-active taf-elevated branch-novel branch-maturity-bound branch-lifecycle-active branch-conflict-graph branch-decay-indicator branch-reinforcement-trend branch-contradiction-trend forecast-accuracy-high calibration-improving branch-reliability-stable prediction-timeline-active experimental-active falsification-ready replication-defined theory-gate-hold theory-corpus-active theory-negative-results theory-revision-lineage theory-competition-open agency-mode-active agency-volitional-edge agency-deterministic-edge agency-vhat-provisional agency-governance-bounded agency-consent-required agency-blame-suppressed responsibility-active support-pathway-defined consent-required coercion-ceiling-strict sanction-suppressed intervention-bounded transfer-active transfer-asymmetry-high transfer-replication-gated transfer-prohibited-claims transfer-risk-elevated system-forecast-active regime-transition-probable entropy-accumulating branch-ecosystem-fragile trajectory-divergent uncertainty-gradient-high information-gain-high experiment-priority-high entropy-reduction-positive curiosity-active value-alignment-active knowledge-priority-top welfare-impact-positive fairness-impact-watch value-risk-flagged meta-active reasoning-efficiency-high donor-reliability-high governance-constraint-strong discovery-productive architecture-active module-performance-strong architecture-discovery-productive safeguard-performance-strong architecture-proposal-queued social-entropy-active social-status-fraying cohesion-fragile legitimacy-drift-elevated reviewer-concentration-high reviewer-fatigue-high repair-priority-high federation-active federation-status-coherent stewardship-node-distributed dissent-portable capture-risk-elevated mitigation-required emergent-domain-active domain-status-emergent invariant-pattern-convergent field-birth-pressure-high domain-boundary-failure-active commons-legibility-required trust-presentation-degraded commons-sovereignty-active commons-integrity-fragile institutional-capture-risk-elevated public-trust-unstable epistemic-diversity-high civilizational-dissent-portable civilizational-memory-active preservation-criticality-high legibility-drifting vocabulary-drift-risk-high notation-fragility-high memory-recoverability-strong custody-diversity-high operationalization-active operational-status-bounded-ready maturity-class-field-tested deployment-readiness-bounded dead-zone-adjacent translation-risk-watch safeguards-required commons-review-required discovery-navigation-active discovery-status-active discovery-vector-cross-domain discovery-bridge-emergent discovery-corridor-bounded discovery-dead-zone-adjacent discovery-memory-supported discovery-commons-review-required discovery-risk-watch discovery-repair-corridor discovery-distortion-risk discovery-river-seed discovery-river-formation ' + terraceResettableClasses().concat(orthodoxyResettableClasses(), schismResettableClasses(), rebraidResettableClasses(), corridorResettableClasses(), riverResettableClasses, deltaResettableClasses, ruptureResettableClasses, cascadeResettableClasses, AGENT_TELEMETRY_RESETTABLE_CLASSES, NAVIGATION_RESETTABLE_CLASSES).join(' '));
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
