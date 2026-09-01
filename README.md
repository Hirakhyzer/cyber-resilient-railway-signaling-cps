# Cyber-Resilient Railway Signaling Cyber-Physical System

[![CI](https://github.com/Hirakhyzer/cyber-resilient-railway-signaling-cps/actions/workflows/ci.yml/badge.svg)](https://github.com/Hirakhyzer/cyber-resilient-railway-signaling-cps/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Status](https://img.shields.io/badge/status-research%20prototype-orange)

A reproducible **railway signaling + cybersecurity + cyber-physical systems** research platform for studying how digital twins, safety invariants, telemetry trust, and resilient supervision can distinguish cyber anomalies from faults and operational disturbances.

> **Safety and research boundary:** this repository is simulation-only. It is not a certified interlocking, train-control system, route-setting product, operational IDS, or exploitation toolkit. No real railway protocol, credentials, infrastructure addresses, or live-system attack procedures are implemented.

## Core research question

**Can a railway CPS identify when reported signaling state is physically or logically inconsistent, isolate untrusted telemetry, reconstruct a conservative state estimate, and preserve service without violating modeled safety constraints?**

```text
Trains / Blocks / Junction
          ↓
Signals + Switch + Occupancy
          ↓
Synthetic faults / cyber manipulation
          ↓
Telemetry network
          ↓
Railway Digital Twin
          ↓
Safety invariants + residuals + freshness
          ↓
Trust / diagnosis
          ↓
Resilience supervisor
          ↓
Restrict / reconstruct / recover
          ↓
Simulated railway operation
```

## Implemented in v0.1

- two-train corridor with a shared junction;
- block occupancy and reduced-order train kinematics;
- signals, switches, abstract routes and interlocking;
- train position, velocity, block, occupancy, signal and switch telemetry;
- packet loss, delay and jitter;
- synthetic position/velocity/occupancy manipulation;
- signal/switch-state falsification;
- replay, rewritten replay and sensor freeze;
- railway digital twin with explicit uncertainty;
- physics/kinematic residuals and freshness checks;
- safety-invariant monitoring;
- per-source trust;
- `NORMAL`, `DIAGNOSE`, `ISOLATE_SOURCE`, `RESTRICT_OPERATION`, `RECOVERY`, `SAFE_STOP`;
- state-reconstruction foundation;
- service, cyber, safety and resilience metrics;
- tests, CI and standardized scenario runner.

## Quick start

```bash
git clone https://github.com/Hirakhyzer/cyber-resilient-railway-signaling-cps.git
cd cyber-resilient-railway-signaling-cps
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e '.[dev]'
pytest
python scripts/run_demo.py
python scripts/run_scenarios.py
```

## Baseline scenarios

| Scenario | Research purpose |
|---|---|
| Normal | false-alarm baseline |
| Position spoof | kinematic integrity |
| Velocity spoof | speed consistency |
| Occupancy spoof | train-vs-block consistency |
| Replay | temporal integrity |
| Rewritten replay | stealthy temporal integrity |
| Freeze | stale telemetry |
| Signal falsification | safety-state consistency |
| Switch falsification | route/topology consistency |
| Packet loss | availability resilience |
| High latency | delayed-state discrimination |

## Why safety invariants matter

The framework deliberately combines cyber evidence with independent railway state. Examples include conflicting-route attempts, contradictory green-signal/occupied-block states, block identity mismatches, and train kinematics that disagree with the digital twin.

This is intended to support research on **attack-vs-fault-vs-operational-disturbance discrimination**, not only network intrusion classification.

## Scientific integrity

All parameters are illustrative. No result should be described as evidence about a real operator, train, signaling system, route, protocol, or certified safety case. Publications should report the exact commit, scenario, random seed, uncertainty parameters, detector threshold, attack window, and benchmark protocol.

See `docs/` for architecture, railway model, interlocking/safety, digital twin, threat model, detection, trust/diagnosis, resilience/recovery, benchmark protocol, reproducibility, references and roadmap.
