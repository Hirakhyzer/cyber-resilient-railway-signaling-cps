from railcps.simulation import run_simulation

def test_packet_loss_is_not_mislabeled_attack_in_baseline():
    r = run_simulation("packet_loss")
    assert r.metrics["false_positive_rate"] == 0.0
