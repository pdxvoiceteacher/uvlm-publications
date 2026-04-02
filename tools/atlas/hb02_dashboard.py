def build_dashboard_entry(result):
    return {
        "model": result["model_name"],
        "coherence": result["true_coherence"],
        "entropy_delta": result["entropy_reduction"],
        "classification": result["classification"],
        "summary": result["summary"],
    }
