# Load Balancer Demo with Nginx, Workers, and PostgreSQL

This project demonstrates a **basic load-balanced system** using **Nginx**, **multiple worker services**, and **PostgreSQL** to log incoming requests.
It also simulates **processing delay** and supports **concurrent load testing**.

---

## Architecture Overview

```
Client
  │
  ▼
Nginx (Load Balancer)
  │
  ├── Worker 1 (Flask)
  ├── Worker 2 (Flask)
  └── Worker 3 (Flask)
        │
        ▼
   PostgreSQL (Request Logs)
```

---

## Tech Stack

- **Nginx** – Reverse proxy & load balancer  
- **Python + Flask** – Worker service  
- **PostgreSQL** – Persistent request logging  
- **Docker & Docker Compose** – Containerization & orchestration  

---

## Features

- Load balancing across **multiple worker containers**
- Simulated processing delay (**3 seconds per request**)
- Logs each request to PostgreSQL:
  - `worker_id`
  - `path`
  - `status`
  - `message_received`
  - `created_at`
- Supports **concurrent load testing**
- Demonstrates **threaded behavior** of Flask dev server

---

## Database Schema

```sql
CREATE TABLE requests (
  id BIGSERIAL PRIMARY KEY,
  worker_id TEXT NOT NULL,
  path TEXT NOT NULL,
  status TEXT NOT NULL,
  message_received TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

---

## Running the Project

### Build and start services (3 workers)
```bash
docker compose up -d --build --scale worker=3 nginx worker
```

### Verify services
```bash
docker ps
```

---

## Making a Request

```bash
curl "http://localhost:8080/?message=hello"
```

Response:
```
✅ Written to DB by worker <worker_id>
```

---

## Load Testing (Simple)

Simulate **200 requests with 50 concurrent clients**:
```bash
seq 1 200 | xargs -n1 -P50 curl -s "http://localhost:8080/?message=test" > /dev/null
```

Measure total execution time:
```bash
time seq 1 200 | xargs -n1 -P50 curl -s "http://localhost:8080/?message=test" > /dev/null
```

---

## Inspect Logs in PostgreSQL

```bash
docker exec -it load-balancer-demo-db-1 psql -U app -d appdb -c "SELECT worker_id, COUNT(*) FROM requests GROUP BY worker_id;"
```

---

## Key Learnings

- **Concurrency ≠ capacity** — throughput is limited by worker configuration
- Flask dev server is **multi-threaded by default**
- Nginx handles request fan-in; workers determine processing speed
- Proper DB logging helps verify load distribution

---

## Notes

- Flask dev server is **not production-ready**
- In production, use **Gunicorn/Uvicorn** with explicit worker & thread limits
- PostgreSQL volume data is excluded via `.gitignore`

---

## Possible Enhancements

- Switch workers to **Gunicorn**
- Add request metrics (latency, throughput)
- Use `wrk` or `k6` for advanced load testing
- Add health checks and timeouts in Nginx
