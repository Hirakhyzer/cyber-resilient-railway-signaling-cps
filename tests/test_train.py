from railcps.physical.train import Train

def test_stopping_distance_positive():
    t=Train("T",["A"]); t.speed_mps=10; assert 40 < t.stopping_distance_m() < 45
