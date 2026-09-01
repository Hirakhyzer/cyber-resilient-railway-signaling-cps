# Architecture

The platform is a reduced-order, simulation-only railway CPS: physical trains and blocks feed signaling state, telemetry and network effects, a railway digital twin, safety invariants, hybrid detection and trust, then a resilience supervisor that can reconstruct state and restrict simulated operation.

The design intentionally separates physical truth from reported telemetry so experiments can compare cyber evidence with independent safety and kinematic evidence.
