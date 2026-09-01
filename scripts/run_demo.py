from railcps.simulation import run_simulation

if __name__ == "__main__":
    result=run_simulation("position_spoof")
    print("Scenario:", result.scenario)
    for k,v in result.metrics.items(): print(f"{k}: {v}")
