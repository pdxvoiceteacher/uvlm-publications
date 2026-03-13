const fs = require('fs');
const path = require('path');
const vm = require('vm');
const assert = require('assert');

function loadOverlayModule(relativePath, context) {
  const sourcePath = path.join(__dirname, '..', relativePath);
  const source = fs.readFileSync(sourcePath, 'utf8').replace(/export\s+/g, '');
  vm.runInContext(source, context, { filename: sourcePath });
}

function makeCy() {
  const nodesById = new Map();

  function makeNode(id, agentId, navRiskScore = 0) {
    const classes = new Set();
    const values = { id, agentId, nav_risk_score: navRiskScore };
    return {
      id,
      data(key) {
        if (!key) return values;
        return values[key];
      },
      addClass(names) {
        String(names).split(/\s+/).filter(Boolean).forEach((n) => classes.add(n));
      },
      removeClass(names) {
        String(names).split(/\s+/).filter(Boolean).forEach((n) => classes.delete(n));
      },
      hasClass(name) {
        return classes.has(name);
      }
    };
  }

  nodesById.set('A', makeNode('A', 'X', 0.3));
  nodesById.set('B', makeNode('B', 'Y', 1.2));

  const emptyCollection = {
    addClass() {},
    removeClass() {},
    empty() { return true; }
  };

  const api = {
    nodes(selector) {
      if (!selector) {
        return {
          forEach(fn) { nodesById.forEach((n) => fn(n)); },
          removeClass(name) { nodesById.forEach((n) => n.removeClass(name)); }
        };
      }

      const classMatch = selector.match(/^\.(.+)$/);
      if (classMatch) {
        const cls = classMatch[1];
        const matched = [...nodesById.values()].filter((n) => n.hasClass(cls));
        return {
          removeClass(name) { matched.forEach((n) => n.removeClass(name)); },
          addClass(name) { matched.forEach((n) => n.addClass(name)); },
          empty() { return matched.length === 0; }
        };
      }

      const agentMatch = selector.match(/^\[agentId\s*=\s*"([^"]+)"\]$/);
      if (agentMatch) {
        const agentId = agentMatch[1];
        const matched = [...nodesById.values()].filter((n) => n.data('agentId') === agentId);
        return {
          removeClass(name) { matched.forEach((n) => n.removeClass(name)); },
          addClass(name) { matched.forEach((n) => n.addClass(name)); },
          empty() { return matched.length === 0; }
        };
      }

      const idMatch = selector.match(/^\[id\s*=\s*"([^"]+)"\]$/);
      if (idMatch) {
        const node = nodesById.get(idMatch[1]);
        return node ? {
          addClass(name) { node.addClass(name); },
          removeClass(name) { node.removeClass(name); },
          empty() { return false; }
        } : emptyCollection;
      }

      return emptyCollection;
    },
    elements(selector) {
      return this.nodes(selector);
    }
  };

  return { api, nodesById };
}

(function run() {
  const listeners = {};
  const toggles = {
    'toggle-agent-telemetry': { addEventListener: (_evt, cb) => { listeners.telemetry = cb; }, checked: false },
    'toggle-navigation': { addEventListener: (_evt, cb) => { listeners.navigation = cb; }, checked: false }
  };

  const { api: cy, nodesById } = makeCy();
  const context = vm.createContext({
    window: {
      cy,
      __bridgeArtifacts: {
        agent_telemetry_event_map: {
          summary: {
            byAgent: {
              X: { novelty: 0.8, contradiction: 0.1 },
              Y: { novelty: 0.3, contradiction: 0.5 }
            }
          }
        },
        navigation_state: {
          chosen_state: 'B'
        }
      }
    },
    document: {
      getElementById(id) {
        return toggles[id] || null;
      }
    },
    console
  });

  loadOverlayModule('atlas/telAgentTelemetryOverlay.js', context);
  loadOverlayModule('atlas/telNavigationOverlay.js', context);

  context.window.bindAgentTelemetryOverlayToggle('toggle-agent-telemetry');
  context.window.bindNavigationToggle('toggle-navigation');

  assert.ok(typeof listeners.telemetry === 'function', 'Telemetry toggle should register a change listener');
  assert.ok(typeof listeners.navigation === 'function', 'Navigation toggle should register a change listener');

  toggles['toggle-agent-telemetry'].checked = true;
  listeners.telemetry();
  assert.ok(nodesById.get('B').hasClass('telemetry-contradiction'), 'Contradiction class should be applied to matching agent node');

  toggles['toggle-navigation'].checked = true;
  listeners.navigation();
  assert.ok(nodesById.get('B').hasClass('nav-psi-high'), 'Chosen node should receive nav-psi-high');
  assert.ok(nodesById.get('B').hasClass('nav-risk-high'), 'High nav_risk_score nodes should receive nav-risk-high');

  toggles['toggle-agent-telemetry'].checked = false;
  listeners.telemetry();
  toggles['toggle-navigation'].checked = false;
  listeners.navigation();
  assert.ok(!nodesById.get('B').hasClass('telemetry-contradiction'), 'Telemetry class should clear when toggle is off');
  assert.ok(!nodesById.get('B').hasClass('nav-psi-high'), 'Navigation class should clear when toggle is off');

  console.log('Overlay toggle integration checks passed.');
})();
