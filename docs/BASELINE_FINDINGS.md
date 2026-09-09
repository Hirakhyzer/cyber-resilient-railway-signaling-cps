# Baseline Findings

These results come from the deterministic v0.1 synthetic benchmark (`seed=7`, 220 one-second steps, attack window steps 55-104). They are not measurements from a real railway.

| Scenario | Recall | False-positive rate | Completion ratio | Resilience score |
|---|---:|---:|---:|---:|
| Normal | n/a | 0.0% | 100% | 1.000 |
| Position spoof | 100% | 0.0% | 100% | 0.982 |
| Velocity spoof | 100% | 0.0% | 100% | 0.982 |
| Occupancy spoof | 100% | 0.0% | 100% | 0.980 |
| Replay | 100% | 0.0% | 100% | 0.982 |
| Rewritten replay | **0%** | 2.3% | 100% | 0.980 |
| Freeze | 98% | 0.0% | 100% | 0.982 |
| Signal falsification | 100% | 0.0% | 100% | 0.980 |
| Switch falsification | 100% | 0.0% | 100% | 0.980 |
| Packet loss | n/a | 0.0% | 100% | 1.000 |
| High latency | n/a | *superseded; re-benchmark after latency-queue fix* | — | — |

## What the baseline shows

Simple freshness metadata makes ordinary replay easy to detect, but **rewriting sequence/timestamp metadata defeats the v0.1 detector** because the replayed payload can remain physically plausible for short intervals. This is the main scientific limitation.

The small false-positive rate after rewritten replay reflects recovery/transient mismatch between the replayed telemetry and the digital twin. v0.2 should explicitly model recovery synchronization rather than treating that artifact as attack evidence.

## Latency-model correction

The original v0.1 `high_latency` row is no longer treated as a valid benchmark result. The network model sampled a delay value but the simulation processed the returned packet immediately, so the scenario did not actually delay telemetry. The network now queues packets until their simulated delivery time and the simulation reports mean T1 telemetry age. High-latency metrics must therefore be regenerated before publication or comparison with the original table.

This correction is a model-semantics fix, not evidence of improved detection performance.

## v0.2 questions

1. Can temporal change statistics detect valid-looking but repeated state trajectories?
2. Can occupancy, route, and train-position cross-sensor evidence expose rewritten replay?
3. Can a probabilistic twin distinguish attack, normal dwell/stoppage, communication delay, and model mismatch?
4. Can source isolation and reconstruction be evaluated with detection-delay and state-estimation error metrics?
