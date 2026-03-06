function parseDate(value) {
  return new Date(`${value}T00:00:00Z`).getTime();
}

function isModeVisible(nodeOrEdge) {
  return !nodeOrEdge.hasClass('temporal-hidden') && !nodeOrEdge.hasClass('zoom-hidden') && !nodeOrEdge.hasClass('filter-hidden');
}

function visibleConceptPublicationCount(cy, conceptId) {
  return cy
    .edges('[type = "mentionsConcept"]')
    .filter((edge) => isModeVisible(edge) && edge.target().id() === conceptId && isModeVisible(edge.source()))
    .length;
}

function conceptScale(config, count) {
  const growth = Math.log1p(count);
  return {
    size: config.conceptScaling.baseSize + config.conceptScaling.sizeFactor * growth,
    glow: config.conceptScaling.baseGlow + config.conceptScaling.glowFactor * growth,
    importanceScore: growth
  };
}

function updateConceptVisuals(cy, config) {
  cy.nodes('[class = "concept"]').forEach((node) => {
    if (!isModeVisible(node)) {
      return;
    }
    const count = visibleConceptPublicationCount(cy, node.id());
    const { size, glow, importanceScore } = conceptScale(config, count);
    const coherenceWeight = Number(node.data('coherenceWeight') ?? 1);
    const weightedSize = size * (0.85 + coherenceWeight * 0.3);
    const weightedGlow = glow * (0.8 + coherenceWeight * 0.45);
    node.style('width', weightedSize);
    node.style('height', weightedSize);
    node.style('shadow-blur', weightedGlow);
    node.style('shadow-opacity', 0.45 + Math.min(0.45, count * 0.08));
    node.style('font-size', 9 + Math.min(5, importanceScore * 1.6 + coherenceWeight));
    node.data('visiblePublicationCount', count);
    node.data('importanceScore', importanceScore * coherenceWeight);
  });
}

function setVisibleState(cy, visibleNodeIds, visibleEdgeIds) {
  cy.nodes().forEach((node) => {
    node.toggleClass('temporal-hidden', !visibleNodeIds.has(node.id()));
  });
  cy.edges().forEach((edge) => {
    edge.toggleClass('temporal-hidden', !visibleEdgeIds.has(edge.data('timelineId')));
  });
}

function buildVisibilitySets(timeline, index) {
  const visibleNodes = new Set();
  const visibleEdges = new Set();

  for (let i = 0; i <= index; i += 1) {
    const event = timeline.events[i];
    if (!event) {
      continue;
    }
    if (event.type === 'node-appear') {
      visibleNodes.add(event.id);
    }
    if (event.type === 'edge-appear') {
      visibleEdges.add(event.id);
    }
  }

  return { visibleNodes, visibleEdges };
}

export function createTimelineEngine({ cy, timeline, config }) {
  const state = {
    mode: config.defaultMode,
    currentIndex: 0,
    currentDate: timeline.timeRange.start,
    isPlaying: false,
    speedKey: '1x'
  };

  let timer = null;
  const listeners = new Set();

  function emit() {
    const snapshot = {
      mode: state.mode,
      currentIndex: state.currentIndex,
      currentDate: state.currentDate,
      isPlaying: state.isPlaying,
      speedKey: state.speedKey
    };
    listeners.forEach((fn) => fn(snapshot));
  }

  function stopTimer() {
    if (timer) {
      clearInterval(timer);
      timer = null;
    }
  }

  function showStatic() {
    cy.elements().removeClass('temporal-hidden newly-visible');
    updateConceptVisuals(cy, config);
  }

  function applyTemporalAt(index) {
    const bounded = Math.max(0, Math.min(index, timeline.events.length - 1));
    const prevVisible = new Set(
      cy.nodes().filter((n) => !n.hasClass('temporal-hidden')).map((n) => n.id())
    );

    const { visibleNodes, visibleEdges } = buildVisibilitySets(timeline, bounded);
    setVisibleState(cy, visibleNodes, visibleEdges);

    visibleNodes.forEach((id) => {
      if (!prevVisible.has(id)) {
        const node = cy.getElementById(id);
        if (node && node.length) {
          node.addClass('newly-visible');
          node.animate({ style: { opacity: 1 } }, { duration: config.animation.nodeFadeMs });
        }
      }
    });

    cy.edges().forEach((edge) => {
      const isVisible = !edge.hasClass('temporal-hidden');
      edge.style('opacity', isVisible ? 1 : 0);
      if (isVisible) {
        edge.animate({ style: { opacity: 1 } }, { duration: config.animation.edgeFadeMs });
      }
    });

    updateConceptVisuals(cy, config);

    state.currentIndex = bounded;
    state.currentDate = timeline.events[bounded]?.date ?? timeline.timeRange.start;
    emit();
  }

  function setMode(mode) {
    state.mode = mode;
    if (mode === 'static') {
      stopTimer();
      state.isPlaying = false;
      state.currentDate = timeline.timeRange.end;
      state.currentIndex = timeline.events.length - 1;
      showStatic();
      emit();
      return;
    }

    reset();
  }

  function play() {
    if (state.mode !== 'temporal') {
      return;
    }
    stopTimer();
    state.isPlaying = true;
    timer = setInterval(() => {
      if (state.currentIndex >= timeline.events.length - 1) {
        pause();
        return;
      }
      applyTemporalAt(state.currentIndex + 1);
    }, config.playbackSpeeds[state.speedKey]);
    emit();
  }

  function pause() {
    stopTimer();
    state.isPlaying = false;
    emit();
  }

  function reset() {
    pause();
    if (timeline.events.length === 0) {
      state.currentIndex = 0;
      state.currentDate = timeline.timeRange.start;
      emit();
      return;
    }
    applyTemporalAt(0);
  }

  function seekToIndex(index) {
    pause();
    applyTemporalAt(index);
  }

  function seekToDate(dateString) {
    const target = parseDate(dateString);
    let idx = 0;
    for (let i = 0; i < timeline.events.length; i += 1) {
      if (parseDate(timeline.events[i].date) <= target) {
        idx = i;
      } else {
        break;
      }
    }
    seekToIndex(idx);
  }

  function setSpeed(speedKey) {
    state.speedKey = speedKey;
    if (state.isPlaying) {
      play();
    } else {
      emit();
    }
  }

  function getCurrentState() {
    return {
      mode: state.mode,
      currentIndex: state.currentIndex,
      currentDate: state.currentDate,
      isPlaying: state.isPlaying,
      speedKey: state.speedKey
    };
  }

  function onStateChange(fn) {
    listeners.add(fn);
    fn(getCurrentState());
    return () => listeners.delete(fn);
  }

  setMode(config.defaultMode);

  return {
    setMode,
    play,
    pause,
    reset,
    seekToIndex,
    seekToDate,
    setSpeed,
    getCurrentState,
    onStateChange,
    refreshConceptVisuals: () => updateConceptVisuals(cy, config)
  };
}
