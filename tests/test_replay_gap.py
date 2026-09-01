from railcps.simulation import run_simulation

def test_rewritten_replay_is_documented_baseline_gap():
    r = run_simulation("rewritten_replay")
    assert r.metrics["recall"] < 0.2
