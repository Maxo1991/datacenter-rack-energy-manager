import itertools

def allocate_devices(devices, racks) -> dict:
    if not racks and not devices:
        return {
            "allocations": [],
            "unallocated_devices": []
        }
    
    rack_data = [
        {
            "id": r[0],
            "name": r[1],
            "max_power": r[5],
            "capacity_units": r[4],
        }
        for r in racks
    ]

    device_data = devices
    unallocated_devices = []

    possible_racks_per_device = []
    for device in device_data:
        valid_racks = []
        for idx, rack in enumerate(rack_data):
            if device.units <= rack["capacity_units"] and device.power <= rack["max_power"]:
                valid_racks.append(idx)

        if not valid_racks:
            unallocated_devices.append(device.name)
            possible_racks_per_device.append([-1])
        else:
            possible_racks_per_device.append(valid_racks)

    if all(r == [-1] for r in possible_racks_per_device):
        return {
            "allocations": [
                {
                    "rack_id": r["id"],
                    "rack_name": r["name"],
                    "devices": [],
                    "used_units": 0,
                    "used_power": 0,
                    "used_units_percent": 0,
                    "power_usage_percent": 0
                } for r in rack_data
            ],
            "unallocated_devices": unallocated_devices
        }

    filtered_devices = [d for d, choices in zip(device_data, possible_racks_per_device) if choices != [-1]]
    filtered_choices = [c for c in possible_racks_per_device if c != [-1]]

    all_combinations = list(itertools.product(*filtered_choices))

    best_allocation = None
    best_score = None

    for combination in all_combinations:
        racks_copy = [ 
            {
                "id": r["id"],
                "name": r["name"],
                "max_power": r["max_power"],
                "capacity_units": r["capacity_units"],
                "used_power": 0,
                "used_capacity": 0,
                "devices": []
            } 
            for r in rack_data
        ]

        valid = True
        for device, rack_idx in zip(filtered_devices, combination):
            rack = racks_copy[rack_idx]
            if rack["used_capacity"] + device.units <= rack["capacity_units"] and \
               rack["used_power"] + device.power <= rack["max_power"]:
                rack["devices"].append(device.name)
                rack["used_capacity"] += device.units
                rack["used_power"] += device.power
            else:
                valid = False
                break

        if not valid:
            continue

        usage_percents = [
            (r["used_power"] / r["max_power"] * 100) if r["max_power"] > 0 else 0
            for r in racks_copy
        ]
        score = max(usage_percents) - min(usage_percents)

        if best_score is None or score < best_score:
            best_score = score
            best_allocation = racks_copy

    if best_allocation is None:
        best_allocation = [
            {
                "id": r["id"],
                "name": r["name"],
                "devices": [],
                "used_capacity": 0,
                "used_power": 0,
                "max_power": r["max_power"],
                "capacity_units": r["capacity_units"]
            } 
            for r in rack_data
        ]

    result = []
    for rack in best_allocation:
        usage_percent = (rack["used_power"] / rack["max_power"] * 100) if rack["max_power"] > 0 else 0
        result.append({
            "rack_id": rack["id"],
            "rack_name": rack["name"],
            "devices": rack["devices"],
            "used_units": rack["used_capacity"],
            "used_power": rack["used_power"],
            "used_units_percent": round(rack["used_capacity"] / rack["capacity_units"] * 100, 2) if rack["capacity_units"] > 0 else 0,
            "power_usage_percent": round(usage_percent, 2)
        })

    return {
        "allocations": result,
        "unallocated_devices": unallocated_devices
    }
