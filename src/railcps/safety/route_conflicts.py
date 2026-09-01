def conflicting_locked_routes(interlocking) -> list[tuple[str, str]]:
    locked = sorted(interlocking.locked)
    conflicts = []
    for i, a in enumerate(locked):
        ra = interlocking.routes[a]
        for b in locked[i+1:]:
            rb = interlocking.routes[b]
            if b in ra.conflicts or a in rb.conflicts or set(ra.blocks) & set(rb.blocks):
                conflicts.append((a, b))
    return conflicts
