async function loadEmbeddingDrift() {
  const res = await fetch("/artifacts/embedding_drift_map.json", { cache: "no-store" });
  const data = await res.json();

  console.log("Embedding Drift:", data);
}
