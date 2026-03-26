def build_triadic_loop_card(loop_result):
    return {
        "schema": "atlas.triadic.loop.v1",
        "initial_coherence": loop_result["initial_state"].get("true_coherence"),
        "final_coherence": loop_result["final_state"].get("true_coherence"),
        "intervention": loop_result["intervention"],
        "audit": loop_result["audit"],
        "delta_entropy": (
            loop_result["initial_state"]
            .get("entropy_extension", {})
            .get("total_entropy", 0.0)
            -
            loop_result["final_state"]
            .get("entropy_extension", {})
            .get("total_entropy", 0.0)
        ),
    }
