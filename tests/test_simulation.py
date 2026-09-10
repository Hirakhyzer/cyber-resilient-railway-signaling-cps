from railcps.simulation import run_simulation

def test_normal_runs():
    r=run_simulation("normal",steps=50); assert r.metrics["duplicate_occupancy"]==0

def test_position_spoof_detectable():
    r=run_simulation("position_spoof"); assert r.metrics["recall"]>0.5

def test_detected_train_attack_changes_next_control_decision():
    normal=run_simulation("normal")
    attacked=run_simulation("position_spoof")
    assert normal.metrics["restriction_fraction"] == 0.0
    assert attacked.metrics["restriction_fraction"] > 0.0
    assert attacked.metrics["restricted_train_updates"] > 0
    assert any(r["applied_control_state"] != "NORMAL" for r in attacked.records if r["step"] > 55)
