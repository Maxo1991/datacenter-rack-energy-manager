# Data Center Rack Energy Manager – Documentation

## Overview
This application simulates the allocation of devices (servers, network equipment, etc.) to racks in a data center.  
The main goal is to balance the energy usage across racks, ensuring that each rack operates with a similar power utilization.

## Core Entities

### Rack
- **Attributes:**  
  - `id` – unique identifier  
  - `name`
  - `description`
  - `serial_number`  
  - `capacity_units` – total number of slots available  
  - `max_power` – maximum power that the rack can handle  

- **Operations (CRUD):**  
  - Create, get all, get by id, update, delete

---

### Device
- **Attributes:**  
  - `id` – unique identifier  
  - `name`
  - `description`
  - `serial_number`  
  - `power` – power consumption of the device  
  - `units` – number of rack units it occupies  
  - `rack_id` – nullable 

- **Operations (CRUD):**  
  - Create, get all, get by id, update, delete

---

## Allocation Logic

### `/allocate` Endpoint
- Generates a proposed distribution of devices across racks.  
- Response contains two main sections:
  - **`allocations`** – racks with their assigned devices  
  - **`unallocated_devices`** – devices that cannot be placed in any rack  

### Reasons for Unallocated Devices
- More devices exist than available rack slots  
- Device requires more units than available in the rack  
- Device requires more power than the rack can provide  

---

## Example

**Request:**  
```http
GET /allocate

## Device Placement Rules
1. When creating or updating a device:  
   - If `rack_id` is set, the system checks:  
     - Is there enough free rack units?  
     - Is there enough available power?  
   - If the check fails → operation is rejected.  

2. If `rack_id = null`, the device remains unassigned until allocation.  

3. Allocation tries to balance power usage across racks as evenly as possible.  
```

