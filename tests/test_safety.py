from railcps.simulation import build_demo
from railcps.safety.invariants import evaluate_safety

def test_demo_starts_without_invariant_violation():
    r,i=build_demo(); assert sum(evaluate_safety(r,i).values())==0
