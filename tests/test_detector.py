from railcps.security.detector import HybridDetector

def test_large_position_residual_alarms():
    d=HybridDetector(); r=d.evaluate_train("t",{"position_z":5,"speed_z":0,"block_mismatch":0},{"sequence_stale":False,"timestamp_stale":False}); assert r.alarm
