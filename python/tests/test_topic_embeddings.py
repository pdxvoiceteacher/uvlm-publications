from coherence.data.topic_embedding_builder import build_embeddings


def test_embeddings_structure():
    nodes = [
        {'id': 'a', 'title': 'Relativity and electromagnetism'},
        {'id': 'b', 'title': 'Lorentz transformations'},
    ]

    emb = build_embeddings(nodes)

    assert 'a' in emb
    assert 'b' in emb
    assert isinstance(emb['a'], list)
    assert isinstance(emb['b'], list)
    assert len(emb['a']) > 0
    assert len(emb['b']) > 0
