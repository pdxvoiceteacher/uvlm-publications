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

  function makeNode(id, agent) {
    const classes = new Set();
    return {
      id,
      data(key) {
        if (key === 'agent' || key === 'agentId') return agent;
        return undefined;
      },
      addClass(names) {
        String(names).split(/\s+/).filter(Boolean).forEach((n) => classes.add(n));
      },
      removeClass(names) {
        String(names).split(/\s+/).filter(Boolean).forEach((n) => classes.delete(n));
      },
      hasClass(name) {
        return classes.has(name);
      },
      empty() {
        return false;
      }
    };
  }

  nodesById.set('A', makeNode('A', 'X'));
  nodesById.set('B', makeNode('B', 'Y'));

  const api = {
    nodes(selector) {
      if (typeof selector === 'string' && selector.startsWith('.')) {
        const names = selector.replace(/\./g, ' ').replace(/,/g, ' ').trim().split(/\s+/).filter(Boolean);
        return {
          removeClass(remove) {
            nodesById.forEach((n) => {
              if (names.some((cls) => n.hasClass(cls))) n.removeClass(remove);
            });
          }
        };
      }
      return {
        forEach(fn) {
          nodesById.forEach((n) => fn(n));
        },
        removeClass(names) {
          nodesById.forEach((n) => n.removeClass(names));
        }
      };
    },
    getElementById(id) {
      const node = nodesById.get(id);
      return node || { empty: () => true, addClass() {}, removeClass() {} };
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
              X: { eventCount: 5, novelty: 2, contradiction: 1 },
              Y: { eventCount: 1, novelty: 0, contradiction: 3 }
            }
          }
        },
        navigation_state: {
          chosen_state: 'B',
          risk_by_node: { B: 0.91 }
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
  listeners.telemetry({ target: toggles['toggle-agent-telemetry'] });
  assert.ok(!nodesById.get('A').hasClass('telemetry-contradiction'), 'Novelty-dominant node should not be contradiction class');
  assert.ok(nodesById.get('B').hasClass('telemetry-contradiction'), 'Contradiction-dominant node should be contradiction class');

  toggles['toggle-navigation'].checked = true;
  listeners.navigation({ target: toggles['toggle-navigation'] });
  assert.ok(nodesById.get('B').hasClass('nav-psi-high'), 'Chosen state should be highlighted');
  assert.ok(nodesById.get('B').hasClass('nav-risk-high'), 'High risk chosen state should be marked');

  toggles['toggle-agent-telemetry'].checked = false;
  listeners.telemetry({ target: toggles['toggle-agent-telemetry'] });
  toggles['toggle-navigation'].checked = false;
  listeners.navigation({ target: toggles['toggle-navigation'] });
  assert.ok(!nodesById.get('B').hasClass('nav-psi-high'), 'Navigation class should clear when toggle is off');

  console.log('Overlay toggle integration checks passed.');
})();
