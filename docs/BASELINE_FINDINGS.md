# Baseline Findings

These are deterministic synthetic benchmark results (`seed=7`, 220 one-second steps, attack window steps 55-104). They are not measurements from a real railway and do not establish signaling-system safety certification or standards compliance.

## Corrected post-maintenance baseline

The table below was regenerated in GitHub Actions from commit `255aa435b4421e2aa7d4b4ce3aa8efd52100144a`. It includes four important model-semantics corrections: network delay is applied to packet arrival, replay/freeze state is isolated per telemetry source, resilience decisions persist into the next train-control update, and delayed telemetry is compared with timestamp-aligned twin/signaling reference state.

| Scenario | Recall | False-positive rate | Completion ratio | Resilience score | Mean T1 telemetry age (s) |
|---|---:|---:|---:|---:|---:|
| Normal | n/a | 0.0% | 100% | 1.000 | 0.000 |
| Position spoof | 100% | 0.0% | 100% | 0.880 | 0.000 |
| Velocity spoof | 100% | 0.0% | 100% | 0.880 | 0.000 |
| Occupancy spoof | 100% | 0.0% | 100% | 0.861 | 0.000 |
| Replay | 100% | 0.0% | 100% | 0.880 | 9.161 |
| Rewritten replay | 100% | 0.0% | 100% | 0.880 | 0.000 |
| Freeze | 98% | 0.0% | 100% | 0.881 | 7.656 |
| Signal falsification | 100% | 0.0% | 100% | 0.861 | 0.000 |
| Switch falsification | 100% | 0.0% | 100% | 0.861 | 0.000 |
| Packet loss | n/a | 0.0% | 100% | 1.000 | 0.000 |
| High latency | n/a | 0.0% | 100% | 1.000 | 2.470 |

For scenarios with no cyberattack positives (`normal`, `packet_loss`, `high_latency`), recall is not a meaningful attack metric even though the raw metrics object reports `0.0`.

## Closed-loop resilience correction

Earlier versions computed `DIAGNOSE`, `ISOLATE_SOURCE`, `RESTRICT_OPERATION`, or `SAFE_STOP` decisions after telemetry processing but did not reliably carry the resulting speed cap into the next physical train update. The simulator now stores the most recent control decision per train and applies that decision on the next movement update. Discrete signaling/occupancy alarms can conservatively restrict active trains, and safety conflicts can impose a safe stop.

`restriction_fraction` is now defined over **train control updates**, not arbitrary telemetry packets. The lower attack-scenario resilience scores in the table therefore reflect actual simulated speed restrictions being applied in the closed loop rather than only counting diagnostic decisions.

## Replay-model correction

The original replay injector used one global replay buffer for all telemetry sources. Replay and freeze state are now isolated per source. The earlier finding that rewritten replay had 0% recall was therefore an artifact of incorrect replay semantics and has been withdrawn.

The current reduced-order rewritten-replay scenario reaches 100% recall. This does **not** establish that realistic metadata-rewritten replay is generally easy to detect. Future work should introduce trajectory-aligned and temporally plausible replay windows that preserve cross-sensor consistency.

## Latency-model and timestamp-alignment correction

A previous `high_latency` implementation first failed to delay packet arrival at all. After real queuing was added, delayed telemetry was initially compared against the **current** twin/signaling state, which produced artificial cyber residuals and unnecessary restrictions.

The detector now compares a delayed packet with the digital-twin or discrete signaling reference associated with that packet's timestamp. In the deterministic high-latency benchmark, mean T1 telemetry age is about 2.47 seconds while false-positive rate remains 0%, both trains complete, and resilience remains 1.0.

This is still a simplified simulator. Timestamp alignment does not solve all communication-security problems; future experiments should include out-of-order delivery, longer burst delays, packet corruption, uncertainty growth with age, and delayed state reconstruction.

## v0.2 questions

1. Can trajectory-aligned and temporally plausible replay remain stealthy after source-correct replay semantics?
2. Can occupancy, route, and train-position cross-sensor evidence distinguish replay from legitimate dwell, delay, and model mismatch?
3. How should twin uncertainty grow with telemetry age and communication mode?
4. Can source isolation and reconstruction be evaluated with detection delay, reconstruction error, service delay, and route-utilization metrics?
5. How does the closed-loop restriction policy trade service availability against modeled safety margins under mixed cyber and communication faults?
