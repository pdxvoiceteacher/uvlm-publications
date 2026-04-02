from pathlib import Path
import json
from fastapi import FastAPI
from atlas.agency import adjudicate_candidate, persist_candidate, load_existing_priors

app = FastAPI(title="Atlas Agency API", version="0.1.0")


@app.get("/health")
def health():
    return {"status": "ok", "service": "atlas"}


@app.post("/atlas/adjudicate")
def atlas_adjudicate():
    candidate_path = Path(r"C:\UVLM\CoherenceLattice\bridge\atlas_novelty_candidate.json")
    if not candidate_path.exists():
        return {"error": "atlas_novelty_candidate.json not found"}

    candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
    adjudication = adjudicate_candidate(candidate)

    out_path = Path(r"C:\UVLM\CoherenceLattice\bridge\atlas_adjudication.json")
    out_path.write_text(json.dumps(adjudication, indent=2), encoding="utf-8")

    return adjudication


@app.post("/atlas/persist")
def atlas_persist():
    candidate_path = Path(r"C:\UVLM\CoherenceLattice\bridge\atlas_novelty_candidate.json")
    if not candidate_path.exists():
        return {"error": "atlas_novelty_candidate.json not found"}

    candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
    stored_path = persist_candidate(candidate)

    result = {
        "stored": stored_path is not None,
        "path": stored_path,
    }

    out_path = Path(r"C:\UVLM\CoherenceLattice\bridge\atlas_persistence_result.json")
    out_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    return result


@app.get("/atlas/priors")
def atlas_priors():
    return {"atlas_priors": load_existing_priors()}
