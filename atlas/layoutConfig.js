export const nodeMass = {
  concept: 10,
  publication: 4,
  series: 6,
  author: 2,
  keyword: 1
};

export const preferredOrbitRadius = {
  publication: 150,
  keyword: 250,
  author: 300,
  series: 420
};

export const edgeStrength = {
  mentionsConcept: 1.0,
  contains: 0.9,
  cites: 0.7,
  isVersionOf: 0.85,
  isPartOf: 0.7,
  isReferencedBy: 0.7,
  publishedIn: 0.45,
  authoredBy: 0.35,
  taggedWith: 0.25
};

export const edgeLength = {
  mentionsConcept: 140,
  contains: 120,
  cites: 180,
  isVersionOf: 110,
  isPartOf: 160,
  isReferencedBy: 180,
  publishedIn: 260,
  authoredBy: 280,
  taggedWith: 240
};
