from railcps.twin.estimator import reconstruct_train_state

def reconstruct(source: str, payload: dict, twin_state, trust: float) -> dict:
    return reconstruct_train_state(twin_state, payload, trust)
