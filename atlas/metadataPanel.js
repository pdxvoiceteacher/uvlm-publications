function row(key, value) {
  return `<div class="meta-key">${key}</div><div class="meta-val">${value ?? '—'}</div>`;
}

function asList(values) {
  if (!Array.isArray(values) || values.length === 0) {
    return '—';
  }
  return values.join(', ');
}

function renderPublication(data) {
  const doiLink = data.doi && data.doi !== 'pending'
    ? `<a href="https://doi.org/${data.doi}" target="_blank" rel="noopener noreferrer">${data.doi}</a>`
    : (data.doi ?? 'pending');

  const pageLink = data.url
    ? `<a href="${data.url}" target="_blank" rel="noopener noreferrer">Open publication</a>`
    : '—';

  return [
    row('Node Class', 'publication'),
    row('Title', data.title),
    row('Authors', asList(data.authors)),
    row('Date', data.date),
    row('DOI', doiLink),
    row('Abstract', data.abstract),
    row('Concepts', asList(data.concepts)),
    row('Keywords', asList(data.keywords)),
    row('Series', data.series),
    row('Type', data.type ?? data.publication_type),
    row('Publication Page', pageLink)
  ].join('');
}

function renderConcept(data) {
  return [
    row('Node Class', 'concept'),
    row('Concept', data.value),
    row('First Appearance', data.appearanceDate),
    row('Related Papers', data.visiblePublicationCount ?? 0),
    row('Related Concepts', data.relatedConceptCount ?? 0)
  ].join('');
}

function renderEdge(data, edgeLabelMap = {}) {
  return [
    row('Edge Type', edgeLabelMap[data.type] ?? data.type ?? '—'),
    row('Source', data.source),
    row('Target', data.target),
    row('Date', data.appearanceDate)
  ].join('');
}

export function renderMetadataPanel(container, data, options = {}) {
  const edgeLabelMap = options.edgeLabelMap ?? {};
  if (data.source && data.target) {
    container.innerHTML = renderEdge(data, edgeLabelMap);
    return;
  }

  if (data.class === 'publication') {
    container.innerHTML = renderPublication(data);
    return;
  }

  if (data.class === 'concept') {
    container.innerHTML = renderConcept(data);
    return;
  }

  const preferred = ['class', 'type', 'title', 'name', 'value', 'doi', 'url', 'date'];
  const keys = [...new Set([...preferred, ...Object.keys(data)])];
  container.innerHTML = keys
    .filter((k) => !['id', 'source', 'target'].includes(k) && data[k] !== undefined)
    .map((k) => row(k, Array.isArray(data[k]) ? data[k].join(', ') : data[k]))
    .join('');
}

export function setDefaultPanel(container) {
  container.innerHTML = '<p>Select a node or edge to inspect metadata.</p>';
}
