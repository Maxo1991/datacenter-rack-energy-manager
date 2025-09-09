def create_rack(conn, rack):
    validate_rack(rack);

    cursor = conn.cursor()
    sql = """
        INSERT INTO racks (name, description, serial_number, capacity_units, max_power) 
        VALUES (%s, %s, %s, %s, %s)
    """
    values = (rack.name, rack.description, rack.serial_number, rack.capacity_units, rack.max_power)
    cursor.execute(sql, values)
    conn.commit()
    return cursor.lastrowid

def update_rack(conn, rack_id, rack):
    validate_rack(rack);

    cursor = conn.cursor()
    sql = """
        UPDATE racks
        SET name=%s, description=%s, serial_number=%s, capacity_units=%s, max_power=%s
        WHERE id=%s
    """
    values = (rack.name, rack.description, rack.serial_number, rack.capacity_units, rack.max_power, rack_id)
    cursor.execute(sql, values)
    conn.commit()
    return cursor.rowcount > 0

def delete_rack(conn, rack_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM racks WHERE id=%s", (rack_id,))
    conn.commit()
    return cursor.rowcount > 0

def get_all_racks(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, description, serial_number, capacity_units, max_power FROM racks")
    return cursor.fetchall()

def get_rack_with_devices(conn, rack_id):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name, description, serial_number, capacity_units, max_power FROM racks WHERE id = %s",
        (rack_id,)
    )
    row = cursor.fetchone()
    if not row:
        return None

    return build_rack_with_devices(conn, row)


def get_racks_with_devices(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, description, serial_number, capacity_units, max_power FROM racks")
    rack_rows = cursor.fetchall()

    return [build_rack_with_devices(conn, row) for row in rack_rows]

def build_rack_with_devices(conn, row):
    cursor = conn.cursor()
    rack_id = row[0]

    capacity_units = row[4] or 0
    max_power = row[5] or 0

    rack = {
        "id": rack_id,
        "name": row[1],
        "description": row[2],
        "serial_number": row[3],
        "capacity_units": capacity_units,
        "max_power": max_power,
        "devices": [],
        "used_units": 0,
        "used_power": 0,
        "used_units_percent": 0.0,
        "used_power_percent": 0.0
    }

    cursor.execute(
        "SELECT id, name, description, serial_number, units, power FROM devices WHERE rack_id = %s",
        (rack_id,)
    )
    device_rows = cursor.fetchall()

    total_units = 0
    total_power = 0
    devices = []

    for d in device_rows:
        units = int(d[4] or 0)
        power = int(d[5] or 0)

        devices.append({
            "id": d[0],
            "name": d[1],
            "description": d[2],
            "serial_number": d[3],
            "units": units,
            "power": power
        })

        total_units += units
        total_power += power

    rack["devices"] = devices
    rack["used_units"] = total_units
    rack["used_power"] = total_power
    rack["used_units_percent"] = round((total_units / capacity_units) * 100, 2) if capacity_units else 0
    rack["used_power_percent"] = round((total_power / max_power) * 100, 2) if max_power else 0

    return rack

def validate_rack(rack):
    errors = []
    if rack.capacity_units <= 0:
        errors.append("Rack capacity_units must be greater than 0")
    if rack.max_power <= 0:
        errors.append("Rack max_power must be greater than 0")
    if errors:
        raise ValueError("; ".join(errors))
