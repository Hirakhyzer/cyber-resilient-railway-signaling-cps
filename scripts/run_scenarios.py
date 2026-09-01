import json
from pathlib import Path
from railcps.simulation import run_simulation

SCENARIOS=["normal","position_spoof","velocity_spoof","occupancy_spoof","replay","rewritten_replay","freeze","signal_falsification","switch_falsification","packet_loss","high_latency"]

if __name__ == "__main__":
    out={}
    for name in SCENARIOS:
        r=run_simulation(name)
        out[name]=r.metrics
        print(name, "recall=", round(r.metrics["recall"],3), "fpr=", round(r.metrics["false_positive_rate"],3), "resilience=", round(r.metrics["resilience_score"],3))
    Path("results").mkdir(exist_ok=True)
    Path("results/baseline_metrics.json").write_text(json.dumps(out,indent=2))
