from railcps.simulation import run_simulation


def test_rewritten_replay_preserves_target_source_semantics():
    r = run_simulation("rewritten_replay")
    assert r.records
    assert all(record["source"] == "train:T1" for record in r.records)
    assert 0.0 <= r.metrics["recall"] <= 1.0
