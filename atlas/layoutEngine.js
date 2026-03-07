import { preferredOrbitRadius } from './layoutConfig.js';

function stableHash(value) {
  let hash = 0;
  for (let i = 0; i < value.length; i += 1) {
    hash = (hash * 31 + value.charCodeAt(i)) >>> 0;
  }
  return hash;
}

function orbitalPosition(center, radius, seed) {
  const angle = ((stableHash(seed) % 3600) / 3600) * 2 * Math.PI;
  return {
    x: center.x + radius * Math.cos(angle),
    y: center.y + radius * Math.sin(angle)
  };
}

function evenlySpacedPosition(center, radius, index, total) {
  const angle = (2 * Math.PI * index) / Math.max(1, total);
  return {
    x: center.x + radius * Math.cos(angle),
    y: center.y + radius * Math.sin(angle)
  };
}

function barycenter(nodes) {
  if (!nodes.length) {
    return { x: 0, y: 0 };
  }
  const sum = nodes.reduce((acc, node) => ({ x: acc.x + node.position.x, y: acc.y + node.position.y }), { x: 0, y: 0 });
  return { x: sum.x / nodes.length, y: sum.y / nodes.length };
}

function indexById(nodes) {
  return new Map(nodes.map((n) => [n.id, n]));
}

function connectionsByTarget(edges) {
  const map = new Map();
  for (const edge of edges) {
    if (!map.has(edge.target)) {
      map.set(edge.target, []);
    }
    map.get(edge.target).push(edge.source);
  }
  return map;
}

function conceptAnchors(concepts) {
  const radius = Math.max(500, 300 + concepts.length * 45);
  concepts.forEach((concept, i) => {
    const angle = (2 * Math.PI * i) / Math.max(1, concepts.length);
    concept.position = {
      x: radius * Math.cos(angle),
      y: radius * Math.sin(angle)
    };
  });
}

export function computeAtlasLayout(graph) {
  const nodes = graph.nodes.map((n) => ({ ...n, position: { x: 0, y: 0 } }));
  const byId = indexById(nodes);

  const edges = graph.edges;
  const conceptNodes = nodes.filter((n) => n.class === 'concept').sort((a, b) => a.id.localeCompare(b.id));
  const publicationNodes = nodes.filter((n) => n.class === 'publication');

  conceptAnchors(conceptNodes);

  const conceptTargets = new Map();
  for (const edge of edges) {
    if (edge.type === 'mentionsConcept' && byId.has(edge.source) && byId.has(edge.target)) {
      if (!conceptTargets.has(edge.source)) {
        conceptTargets.set(edge.source, []);
      }
      conceptTargets.get(edge.source).push(byId.get(edge.target));
    }
  }

  for (const pub of publicationNodes) {
    const centers = conceptTargets.get(pub.id) ?? [];
    const center = centers.length ? barycenter(centers) : { x: 0, y: 0 };
    pub.position = orbitalPosition(center, preferredOrbitRadius.publication, pub.id);
  }

  const incoming = connectionsByTarget(edges);
  for (const node of nodes) {
    if (!['author', 'keyword', 'series'].includes(node.class)) {
      continue;
    }
    const connectedSourceIds = incoming.get(node.id) ?? [];
    const publications = connectedSourceIds
      .map((id) => byId.get(id))
      .filter((n) => n && n.class === 'publication');
    const center = publications.length ? barycenter(publications) : { x: 0, y: 0 };
    const radius = preferredOrbitRadius[node.class] ?? 260;
    node.position = orbitalPosition(center, radius, `${node.id}:${center.x}:${center.y}`);
  }

  return {
    nodes,
    edges
  };
}

export function applySolarSystemLayout(cy, conceptId) {
  const concept = cy.getElementById(conceptId);
  if (!concept || !concept.length) {
    return {};
  }

  const conceptPos = concept.position();
  const mentionsEdges = cy.edges('[type = "mentionsConcept"]').filter((edge) => edge.target().id() === conceptId);
  const publications = mentionsEdges.map((edge) => edge.source());

  const positions = {};
  publications.forEach((pub, index) => {
    positions[pub.id()] = evenlySpacedPosition(conceptPos, preferredOrbitRadius.publication, index, publications.length);
  });

  return positions;
}

export function applyOrbitDetailLayout(cy, publicationId) {
  const publication = cy.getElementById(publicationId);
  if (!publication || !publication.length) {
    return {};
  }

  const center = publication.position();
  const positions = {};

  const keywords = publication.connectedEdges('[type = "taggedWith"]').targets();
  keywords.forEach((node, index) => {
    positions[node.id()] = evenlySpacedPosition(center, preferredOrbitRadius.keyword, index, keywords.length);
  });

  const authors = publication.connectedEdges('[type = "authoredBy"]').targets();
  authors.forEach((node, index) => {
    positions[node.id()] = evenlySpacedPosition(center, preferredOrbitRadius.author, index, authors.length);
  });

  const series = publication.connectedEdges('[type = "publishedIn"]').targets();
  series.forEach((node, index) => {
    positions[node.id()] = evenlySpacedPosition(center, preferredOrbitRadius.series, index, series.length);
  });

  return positions;
}
