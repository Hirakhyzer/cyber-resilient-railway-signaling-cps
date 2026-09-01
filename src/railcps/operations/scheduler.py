def priority_order(trains) -> list[str]:
    return sorted((t.train_id for t in trains if not t.completed), key=lambda x: x)
