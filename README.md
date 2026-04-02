# Logistics automation & dynamic vehicle routing system

A powerful automated logistics and dispatching system built with Python + FastAPI. Made with needs of administrators and real drivers in mind, prioritizing delivery time window integrity and driver comfort.

## Key features

* **Time window routing solver**: Utilizes Google OR-Tools to assign orders to drivers based on delivery timeframes, driver availability and shop requirements. *(Note: Further improvements to the routing engine are underway!)*
* **Optimal compute resource utilization**: A background loop runs an evaluation check every 60s to issue deliveries only when hitting dynamic internal urgency checks.
* **Data integrity**: Pydantic validation along with business logic checks prevent misinterpretations and ensure data integrity.
* **Integrations**: Connects with Yandex Maps API and OSRM for geocoding, order mapping, and distance matrix calculations.
* **Web User Interface (WIP)**: REST API compliant endpoints designed to serve an interactive user interface.
* **Containerization**: Containerized Web UI and SQL Server allow for a safe development environment and quick app startup.

## API modules

The API is divided into 6 modules in [api](./api):

* **`/controls`**: Toggle automatic routing engine modes (`/mode`).
* **`/direct`**: Commit manual dispatcher overrides (`/commit`).
* **`/home`**: Main dashboard, aggregate statistics, sitemap.
* **`/info`**: Basic system health checks (intended for background checks of modules).
* **`/map`**: Request route configurations (`/routes/{driver_id}`) and coordinates for order mapping (`/data`).
* **`/orders`**: Add new orders (`/add`), view unassigned orders (`/awaiting`), and update statuses (`/update-status`).

*View all up-to-date schemas in FastAPI's Swagger UI at `http://localhost:8000/docs`. Modules subject to change.*

## Installation

### Prerequisites
*   (With Docker): [Docker](https://www.docker.com/) and Docker Compose
*   (Without Docker): Python 3.11 and [Microsoft ODBC Driver 17](https://go.microsoft.com/fwlink/?linkid=2266337) for SQL Server.

### 1. Environment configuration
Copy the `.env.example` file and create a local `.env` file:
```bash
cp .env.example .env
```
Fill in the required variables:
```
DB_SERVER_NAME=db
DB_DATABASE_NAME=yourdbname
DB_DRIVER_NAME="ODBC Driver 17 for SQL Server"
DB_USER=sa
DB_PASSWORD=QWERTY123456!@#$%^
API_KEY_YANDEX_GEO=yandex-api-key
URL_YANDEX_GEO=https://geocode-maps.yandex.ru/v1/
URL_OSRM_TABLE=http://router.project-osrm.org/table/v1/driving/
```
*(Warning: The public OSRM demo server is for testing purposes only. Follow [guidelines](https://map.project-osrm.org/about.html) or consider [self-hosting](https://github.com/Project-OSRM/osrm-backend)).*

### 2. Run with Docker (Recommended)
Build and start the application and SQL Server database:
```bash
docker compose up --build
```
* By default the application will run at: `http://localhost:8000`
* Access the Swagger UI for endpoint testing: `http://localhost:8000/docs`

### 3. Local testing script *(Unsupported!)*
You can currently test data management and DB communication modules without running the Web Interface by executing the included sandbox script:
```bash
python sandbox.py
```

## Upcoming features (due May 2026)

* Developing `/map` and `/orders` endpoints, as well as basic HTML webpages using Bootstrap to enable a GUI connection to the backend.
* Further optimizing the routing engine by making a custom separate API-enabled server-based module.