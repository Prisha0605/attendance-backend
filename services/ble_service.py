def detect_classroom_from_ble(ble_readings):
    if not ble_readings:
        return None, None

    strongest = max(ble_readings, key=lambda x: x["rssi"])
    return strongest["minor"], strongest["rssi"]