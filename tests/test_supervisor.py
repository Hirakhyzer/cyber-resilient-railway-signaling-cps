from railcps.resilience.supervisor import ResilienceSupervisor

def test_safety_conflict_safe_stop():
    d=ResilienceSupervisor().decide(1.0,False,True,False); assert d.state=="SAFE_STOP" and d.speed_cap_mps==0
