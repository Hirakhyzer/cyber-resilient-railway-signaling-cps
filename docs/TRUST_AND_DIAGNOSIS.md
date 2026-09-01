# Trust and Diagnosis

Each telemetry source receives a dynamic trust score in `[0,1]`. Low-trust sources can be isolated while the digital twin supplies a conservative reconstructed train state.

The long-term research goal is to distinguish `OPERATIONAL_DISTURBANCE`, `SENSOR_FAULT`, `COMMUNICATION_FAULT`, `MODEL_MISMATCH`, `CYBER_ANOMALY`, and `SAFETY_CONFLICT` instead of using one binary alarm.
