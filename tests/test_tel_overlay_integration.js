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

  function makeNode(id, agentId) {
    const classes = new Set();
    return {
      id,
      data(key) {
        if (key === 'agentId') return agentId;
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

  nodesById.set('n1', makeNode('n1', 'EchoAI'));
  nodesById.set('n2', makeNode('n2', 'OtherAI'));

  const api = {
    nodes() {
      return {
        forEach(fn) {
          nodesById.forEach((n) => fn(n));
        },
        removeClass(names) {
          nodesById.forEach((n) => n.removeClass(names));
        }
      };
    },
    elements() {
      return {
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
    'toggle-agent-telemetry': { addEventListener: (_evt, cb) => { listeners.telemetry = cb; } },
    'toggle-navigation': { addEventListener: (_evt, cb) => { listeners.navigation = cb; } }
  };

  const { api: cy, nodesById } = makeCy();
  const context = vm.createContext({
    window: {
      cy,
      __bridgeArtifacts: {
        agent_telemetry_event_map: {
          summary: {
            byAgent: {
              EchoAI: { eventCount: 2, contradictionCount: 1 },
              OtherAI: { eventCount: 0, contradictionCount: 0 }
            }
          }
        },
        navigation_state: {
          chosen_state: { n1: 'n2' },
          risk_by_node: { n1: 0.9 }
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

  listeners.telemetry({ target: { checked: true } });
  assert.ok(nodesById.get('n1').hasClass('telemetry-novelty'), 'Telemetry novelty class should be applied for active agent');
  assert.ok(nodesById.get('n1').hasClass('telemetry-contradiction'), 'Telemetry contradiction class should be applied when contradiction count exists');
  assert.ok(!nodesById.get('n2').hasClass('telemetry-novelty'), 'Telemetry class should not be applied when event count is zero');

  listeners.navigation({ target: { checked: true } });
  assert.ok(nodesById.get('n1').hasClass('nav-psi-high'), 'Navigation psi class should be applied to chosen node');
  assert.ok(nodesById.get('n1').hasClass('nav-risk-high'), 'Navigation risk class should be applied to high-risk chosen node');

  listeners.telemetry({ target: { checked: false } });
  listeners.navigation({ target: { checked: false } });
  assert.ok(!nodesById.get('n1').hasClass('telemetry-novelty'), 'Telemetry class should clear when toggle is off');
  assert.ok(!nodesById.get('n1').hasClass('nav-psi-high'), 'Navigation class should clear when toggle is off');

  console.log('Overlay toggle integration checks passed.');
})();
