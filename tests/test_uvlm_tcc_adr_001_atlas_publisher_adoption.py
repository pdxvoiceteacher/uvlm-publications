"""Local, deterministic checks for the Atlas/Publisher architecture adoption."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ADR = ROOT / "docs/architecture/UVLM_TCC_ADR_001_ATLAS_PUBLISHER_ADOPTION.md"
README = ROOT / "README.md"
AGENTS = ROOT / "AGENTS.md"
ATLAS_HANDOFF = ROOT / "CONTINUITY_HANDOFF_ATLAS_2026-04-02.md"
TRIADIC_HANDOFF = ROOT / "TRIADIC_BRAIN_CONTINUITY_HANDOFF_2026-04-02.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_local_adoption_architecture_lock():
    assert ADR.is_file()
    adr = read(ADR)
    readme = read(README)
    agents = read(AGENTS)

    assert "UVLM_TCC_ADR_001_ATLAS_PUBLISHER_ADOPTION.md" in readme
    assert "approved local model → Sonya → CoherenceLattice → Sophia → Atlas/Publisher → Human → PMR only when separately authorized" in adr
    assert "Sonya → approved local model backend → Sonya" in adr
    assert "Atlas posture and publication execution are separate namespaces and separate authority grants." in adr
    for prohibition in ("not permission to write memory", "canonize", "publish", "mint a DOI", "deposit Crossref metadata"):
        assert prohibition in adr
    assert "PMR performs governed provenance retention only when separately authorized" in adr
    assert "UCC is a cross-cutting control plane" in adr
    assert "Human final authority remains binding" in adr
    assert "complete live route is not accepted or green" in adr
    assert "Formal drift** = CoherenceLattice truth" not in readme
    assert "Publisher memory storage" not in readme
    assert "HISTORICAL CONTINUITY RECORD" in read(ATLAS_HANDOFF)
    assert "HISTORICAL CONTINUITY RECORD" in read(TRIADIC_HANDOFF)
    for rule in (
        "Do not implement CoherenceLattice or Sophia behavior here",
        "Do not call a model or accept raw model output",
        "Do not write memory automatically",
        "Do not mutate publication, DOI, catalog, graph, or Crossref state",
    ):
        assert rule in agents
    assert "source_commit: null" in adr
    assert "document_sha256: null" in adr
    assert "verification_status: deferred_to_three_repository_consistency_gate" in adr
