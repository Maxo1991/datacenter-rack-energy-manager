# Data Center Management API

This project is an API for managing devices and racks in a data center.  
It is built with **FastAPI** and uses MySQL as the database.

## Installation & Run

**Prerequisites:**  
- Docker (version 20.10+ recommended)  
- Docker Compose v2 (version 2.39.2 or newer)

```bash
git clone https://github.com/Maxo1991/datacenter-rack-energy-manager.git
cd datacenter-rack-energy-manager
docker compose up --build
```

## Features

- **Device management** – full CRUD operations for devices  
- **Rack management** – full CRUD operations for racks  
- **Device allocation** – assign devices to racks  
- **Monitoring** – track rack capacity usage and power consumption  

## API Documentation

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Postman Collection

A Postman collection with example requests is included in the project.  
You can import it into Postman by following these steps:

1. Open Postman  
2. Go to **File → Import**  
3. Select the file: `postman/DataCenterAPI.postman_collection.json`  
4. The collection will appear in your Postman workspace

## Documentation

Detailed functional documentation about how devices and racks are managed,
as well as the allocation logic, can be found in [DOCUMENTATION.md](DOCUMENTATION.md).

