from railcps.simulation import run_simulation

def test_normal_runs():
    r=run_simulation("normal",steps=50); assert r.metrics["duplicate_occupancy"]==0

def test_position_spoof_detectable():
    r=run_simulation("position_spoof"); assert r.metrics["recall"]>0.5
