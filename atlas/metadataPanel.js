function row(key, value) {
  return `<div class="meta-key">${key}</div><div class="meta-val">${value ?? '—'}</div>`;
}

export function renderMetadataPanel(container, data) {
  const preferred = ['class', 'type', 'title', 'name', 'value', 'abstract', 'doi', 'url', 'date', 'publication_type'];
  const keys = [...new Set([...preferred, ...Object.keys(data)])];

  container.innerHTML = keys
    .filter((k) => !['id', 'source', 'target'].includes(k) && data[k] !== undefined)
    .map((k) => row(k, Array.isArray(data[k]) ? data[k].join(', ') : data[k]))
    .join('');
}

export function setDefaultPanel(container) {
  container.innerHTML = '<p>Select a node or edge to inspect metadata.</p>';
}
