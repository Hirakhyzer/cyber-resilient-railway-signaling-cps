from railcps.simulation import build_demo

def test_conflicting_route_not_lockable():
    rail,i=build_demo(); assert i.lock("R1",for_train="T1"); rail.switches["SW1"].set_position("DIVERGE"); assert not i.lock("R2",for_train="T2")
