import random

from railcps.cyber.network import Network
from railcps.cyber.telemetry import TelemetryPacket
from railcps.simulation import run_simulation


def test_packet_loss_is_not_mislabeled_attack_in_baseline():
    r = run_simulation("packet_loss")
    assert r.metrics["false_positive_rate"] == 0.0


def test_network_queue_applies_delay_before_delivery():
    net=Network(base_delay_s=2.0,jitter_s=0.0,rng=random.Random(1))
    packet=TelemetryPacket("train:T1",1,0.0,{"speed_mps":1.0})
    assert net.send(packet,0.0)
    assert net.receive(0.0) == []
    assert net.receive(1.0) == []
    assert net.receive(2.0) == [packet]


def test_high_latency_uses_timestamp_aligned_reference_state():
    normal=run_simulation("normal")
    delayed=run_simulation("high_latency")
    assert normal.metrics["mean_t1_telemetry_age_s"] == 0.0
    assert delayed.metrics["mean_t1_telemetry_age_s"] >= 1.0
    assert delayed.metrics["false_positive_rate"] == 0.0
    assert delayed.metrics["completion_ratio"] == 1.0
