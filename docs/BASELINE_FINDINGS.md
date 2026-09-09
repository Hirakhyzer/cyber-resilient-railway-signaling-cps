# Baseline Findings

These are deterministic synthetic benchmark results (`seed=7`, 220 one-second steps, attack window steps 55-104). They are not measurements from a real railway.

## Corrected post-maintenance baseline

The table below was regenerated from commit `7edf76296b30a714e920578b0256210694fea0d3` after two model-semantics fixes: network delay is now applied to packet arrival, and replay/freeze state is isolated per telemetry source.

| Scenario | Recall | False-positive rate | Completion ratio | Resilience score | Mean T1 telemetry age (s) |
|---|---:|---:|---:|---:|---:|
| Normal | n/a | 0.0% | 100% | 1.000 | 0.000 |
| Position spoof | 100% | 0.0% | 100% | 0.982 | 0.000 |
| Velocity spoof | 100% | 0.0% | 100% | 0.982 | 0.000 |
| Occupancy spoof | 100% | 0.0% | 100% | 0.980 | 0.000 |
| Replay | 100% | 0.0% | 100% | 0.982 | 10.688 |
| Rewritten replay | 100% | 0.0% | 100% | 0.982 | 0.000 |
| Freeze | 98% | 0.0% | 100% | 0.982 | 8.877 |
| Signal falsification | 100% | 0.0% | 100% | 0.980 | 0.000 |
| Switch falsification | 100% | 0.0% | 100% | 0.980 | 0.000 |
| Packet loss | n/a | 0.0% | 100% | 1.000 | 0.000 |
| High latency | n/a | 3.8% | 100% | 0.792 | 2.471 |

For scenarios with no cyberattack positives (`normal`, `packet_loss`, `high_latency`), recall is not a meaningful attack metric even though the raw metrics object reports `0.0`.

## Replay-model correction

The original replay injector used one global replay buffer for all telemetry sources. Because the source loop includes train, occupancy, signal, and switch telemetry, a replay aimed at `train:T1` could reuse a packet buffered from a different source. The old simulation loop then continued to interpret that packet using the pre-attack source/type variable, masking the semantic mismatch.

Replay and freeze state are now isolated per telemetry source. The earlier finding that rewritten replay had 0% recall was therefore an artifact of incorrect replay semantics and has been withdrawn. With the corrected source-specific replay model in the deterministic benchmark above, rewritten replay recall is 100%.

This does **not** establish that realistic metadata-rewritten replay is generally easy to detect. It only states the result for this reduced-order simulator, current replay construction, detector, seed, and attack window. Future work should introduce more physically plausible replay windows and trajectory-aligned replay to test genuinely stealthy cases.

## Latency-model correction

The original `high_latency` scenario sampled a delay value but processed the returned packet immediately. The network now queues packets until their simulated delivery time. Under the corrected deterministic scenario, T1 telemetry age averages about 2.47 seconds and the detector produces a 3.8% false-positive rate while service completion remains 100%.

This exposes a more meaningful research problem: distinguishing delayed-but-benign telemetry from cyber manipulation without over-restricting service. The lower resilience score (0.792) reflects those additional restrictions in the current simplified supervisor metric.

## v0.2 questions

1. Can trajectory-aligned and temporally plausible replay remain stealthy after source-correct replay semantics?
2. Can occupancy, route, and train-position cross-sensor evidence distinguish replay from legitimate dwell and delay?
3. Can a probabilistic twin distinguish attack, normal dwell/stoppage, communication delay, and model mismatch?
4. Can source isolation and reconstruction be evaluated with detection-delay and state-estimation error metrics?
