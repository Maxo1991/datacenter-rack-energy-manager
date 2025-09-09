from models.devices import Device

def create_device(conn, device):
    validate_device(device)
    
    cursor = conn.cursor()
    if device.rack_id is not None:
        cursor.execute(
            "SELECT capacity_units, max_power FROM racks WHERE id = %s",
            (device.rack_id,)
        )
        rack = cursor.fetchone()
        if not rack:
            raise ValueError("Rack not found")

        capacity_units, max_power = rack

        cursor.execute(
            "SELECT COALESCE(SUM(units), 0), COALESCE(SUM(power), 0) FROM devices WHERE rack_id = %s",
            (device.rack_id,)
        )
        used_units, used_power = cursor.fetchone()

        if used_units + device.units > capacity_units:
            raise ValueError("Not enough rack units available")
        if used_power + device.power > max_power:
            raise ValueError("Not enough power capacity available")
    
    sql = """
        INSERT INTO devices (name, description, serial_number, units, power, rack_id)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (device.name, device.description, device.serial_number, device.units, device.power,  device.rack_id)
    cursor.execute(sql, values)
    conn.commit()
    return cursor.lastrowid

def get_devices(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, description, serial_number, units, power, rack_id FROM devices")
    rows = cursor.fetchall()
    devices = [Device(id=row[0], name=row[1], description=row[2], serial_number=row[3], units=row[4], power=row[5], rack_id=row[6]) for row in rows]
    return devices

def get_device(conn, device_id):
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, description, serial_number, units, power, rack_id FROM devices WHERE id = %s", (device_id,))
    row = cursor.fetchone()
    if row:
        return Device(id=row[0], name=row[1], description=row[2], serial_number=row[3], units=row[4], power=row[5], rack_id=row[6])
    return None

def update_device(conn, device_id, device):
    validate_device(device)
    
    cursor = conn.cursor()

    if device.rack_id is not None:
        cursor.execute(
            "SELECT capacity_units, max_power FROM racks WHERE id = %s",
            (device.rack_id,)
        )
        rack = cursor.fetchone()
        if not rack:
            raise ValueError("Rack not found")

        capacity_units, max_power = rack

        cursor.execute(
            "SELECT COALESCE(SUM(units),0), COALESCE(SUM(power),0) FROM devices WHERE rack_id = %s AND id != %s",
            (device.rack_id, device_id)
        )
        used_units, used_power = cursor.fetchone()
        if used_units + device.units > capacity_units:
            raise ValueError("Not enough rack units available")
        if used_power + device.power > max_power:
            raise ValueError("Not enough power capacity available")
    
    sql = """
        UPDATE devices
        SET name=%s, description=%s, serial_number=%s, units=%s, power=%s, rack_id=%s
        WHERE id=%s
    """
    values = (device.name, device.description, device.serial_number, device.units, device.power, device.rack_id, device_id)
    cursor.execute(sql, values)
    conn.commit()
    return cursor.rowcount

def delete_device(conn, device_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM devices WHERE id=%s", (device_id,))
    conn.commit()
    return cursor.rowcount

def validate_device(device):
    errors = []
    if device.units <= 0:
        errors.append("Device units must be greater than 0")
    if device.power <= 0:
        errors.append("Device power must be greater than 0")
    if errors:
        raise ValueError("; ".join(errors))