# Baseline Findings

These results come from the deterministic v0.1 synthetic benchmark (`seed=7`, 220 one-second steps, attack window steps 55-104). They are not measurements from a real railway.

| Scenario | Recall | False-positive rate | Completion ratio | Resilience score |
|---|---:|---:|---:|---:|
| Normal | n/a | 0.0% | 100% | 1.000 |
| Position spoof | 100% | 0.0% | 100% | 0.982 |
| Velocity spoof | 100% | 0.0% | 100% | 0.982 |
| Occupancy spoof | 100% | 0.0% | 100% | 0.980 |
| Replay | *superseded; re-benchmark after source-isolated replay fix* | — | — | — |
| Rewritten replay | *superseded; re-benchmark after source-isolated replay fix* | — | — | — |
| Freeze | 98% | 0.0% | 100% | 0.982 |
| Signal falsification | 100% | 0.0% | 100% | 0.980 |
| Switch falsification | 100% | 0.0% | 100% | 0.980 |
| Packet loss | n/a | 0.0% | 100% | 1.000 |
| High latency | n/a | *superseded; re-benchmark after latency-queue fix* | — | — |

## What remains valid

The unchanged rows above remain the original deterministic v0.1 synthetic baseline. They should still be re-run before publication if compared against any post-maintenance result because the repository now contains corrected network/replay semantics.

## Replay-model correction

The original replay injector used one global replay buffer for all telemetry sources. Because the source loop includes train, occupancy, signal, and switch telemetry, a replay aimed at `train:T1` could reuse a packet buffered from a different source. The old simulation loop then continued to interpret that packet using the pre-attack source/type variable, masking the semantic mismatch.

Replay and freeze state are now isolated per telemetry source. As a result, the previous claim that rewritten replay had 0% recall is **not a valid research finding** and has been withdrawn from the baseline table. Corrected replay metrics must be regenerated before they are cited.

## Latency-model correction

The original v0.1 `high_latency` row is also no longer treated as a valid benchmark result. The network model sampled a delay value but the simulation processed the returned packet immediately, so the scenario did not actually delay telemetry. The network now queues packets until their simulated delivery time and the simulation reports mean T1 telemetry age. High-latency metrics must therefore be regenerated before publication or comparison with the original table.

These corrections are model-semantics fixes, not evidence of improved detection performance.

## v0.2 questions

1. Can temporal change statistics detect valid-looking but repeated state trajectories after source-correct replay is used?
2. Can occupancy, route, and train-position cross-sensor evidence distinguish replay from legitimate dwell and delay?
3. Can a probabilistic twin distinguish attack, normal dwell/stoppage, communication delay, and model mismatch?
4. Can source isolation and reconstruction be evaluated with detection-delay and state-estimation error metrics?
