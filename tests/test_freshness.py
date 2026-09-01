from railcps.cyber.freshness import FreshnessChecker
from railcps.cyber.telemetry import TelemetryPacket

def test_replay_stale():
    f=FreshnessChecker(); p=TelemetryPacket("x",1,1.0,{}) ; assert not any(f.check(p).values()); assert all(f.check(p).values())
