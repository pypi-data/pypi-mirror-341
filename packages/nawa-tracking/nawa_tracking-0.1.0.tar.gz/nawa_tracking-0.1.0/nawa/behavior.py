def analyze_behavior(movements: list) -> dict:
    """
    Simple rule‑based demo: detects if pilgrim exits allowed zones.
    movements = [("ARAFAT", "10:00"), ("MINA", "12:30"), ...]
    """
    flagged = any(zone not in {"HARAM", "MINA", "ARAFAT"} for zone, _ in movements)
    return {
        "status": "OK" if not flagged else "ANOMALY",
        "details": "Route valid" if not flagged else "Detected forbidden zone"
    }
