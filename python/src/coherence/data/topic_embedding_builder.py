"""Topic embedding builder with optional sentence-transformers backend."""

from hashlib import sha256
from importlib.util import find_spec


def _fallback_embedding(text, dims=16):
    digest = sha256(text.encode('utf-8')).digest()
    values = []
    for idx in range(dims):
        byte = digest[idx % len(digest)]
        values.append(byte / 255.0)
    return values


def build_embeddings(nodes):
    """Build per-node topic embeddings keyed by node id."""
    valid_nodes = [node for node in nodes if node.get('id')]
    texts = [str(node.get('title', '')) for node in valid_nodes]

    if find_spec('sentence_transformers') is not None:
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer('all-MiniLM-L6-v2')
        vectors = model.encode(texts)
        return {
            node['id']: vector.tolist() if hasattr(vector, 'tolist') else list(vector)
            for node, vector in zip(valid_nodes, vectors)
        }

    return {
        node['id']: _fallback_embedding(text)
        for node, text in zip(valid_nodes, texts)
    }
