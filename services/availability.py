from datetime import time


def generate_time_slots():
    slots = []

    for hour in range(8, 17):
        slots.append({
            "start_time": time(hour, 0),
            "end_time": time(hour + 1, 0)
        })

    return slots