# Resilience and Recovery

The supervisor states are `NORMAL`, `DIAGNOSE`, `ISOLATE_SOURCE`, `RESTRICT_OPERATION`, `RECOVERY`, and `SAFE_STOP`. Restriction changes only the simulated speed cap.

Research sequence: detect -> diagnose -> isolate -> reconstruct -> restrict -> verify -> recover. No state is permitted to intentionally override a modeled safety conflict.
