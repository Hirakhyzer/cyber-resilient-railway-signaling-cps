from railcps.simulation import run_simulation

def test_normal_service_completes_without_safety_violations():
    r = run_simulation("normal")
    assert r.metrics["completion_ratio"] == 1.0
    assert r.metrics["duplicate_occupancy"] == 0
    assert r.metrics["route_conflicts"] == 0
    assert r.metrics["signal_conflicts"] == 0
