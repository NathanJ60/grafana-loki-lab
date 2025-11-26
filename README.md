# Grafana Loki Lab

A complete observability lab using Grafana, Loki, Promtail, and a fake log generator. Perfect for learning log aggregation and visualization.

## Architecture

```
┌─────────────────┐     ┌──────────────┐     ┌─────────────┐
│  Fake Generator │────▶│   Promtail   │────▶│    Loki     │
│  (Python/Faker) │     │ (log shipper)│     │ (log store) │
└─────────────────┘     └──────────────┘     └─────────────┘
                                                    │
                                                    ▼
                                             ┌─────────────┐
                                             │   Grafana   │
                                             │   (WebUI)   │
                                             └─────────────┘
```

## Stack

| Service | Port | Description |
|---------|------|-------------|
| Grafana | 3000 | Visualization & Dashboards |
| Loki | 3100 | Log aggregation & storage |
| Promtail | 9080 | Log collection agent |
| Fakeapp | - | Fake log generator |

## Quick Start

### Prerequisites

- Docker
- Docker Compose

### Installation

```bash
git clone https://github.com/NathanJ60/grafana-loki-lab.git
cd grafana-loki-lab
docker-compose up -d
```

### Access Grafana

1. Open http://localhost:3000 (or http://YOUR_SERVER_IP:3000)
2. Login with `admin` / `admin`
3. Go to **Connections** → **Data Sources** → **Add data source**
4. Select **Loki**
5. Set URL to `http://loki:3100`
6. Click **Save & Test**

### Explore Logs

Go to **Explore** and run:

```logql
{job="fakeapp"}
```

Filter by log level:

```logql
{job="fakeapp"} |= "ERROR"
```

```logql
{job="fakeapp"} | logfmt | level="CRITICAL"
```

## Project Structure

```
grafana-loki-lab/
├── docker-compose.yml
├── loki/
│   └── loki-config.yaml
├── promtail/
│   └── promtail-config.yaml
├── generator/
│   ├── Dockerfile
│   ├── generate_logs.py
│   └── requirements.txt
├── logs/
│   └── .gitkeep
└── README.md
```

## Log Format

The fake log generator produces logs in this format:

```
[2024-01-15 10:30:45] INFO - User john_doe logged in successfully
[2024-01-15 10:30:46] ERROR - Failed to connect to database: Connection refused
[2024-01-15 10:30:47] WARNING - High memory usage detected: 85%
```

Log levels distribution:
- DEBUG: 10%
- INFO: 50%
- WARNING: 20%
- ERROR: 15%
- CRITICAL: 5%

Every ~100 logs, there's a 30% chance of an "incident" burst (20-50 ERROR/CRITICAL logs).

## Commands

```bash
# Start the stack
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the stack
docker-compose down

# Rebuild after changes
docker-compose up -d --build

# View specific service logs
docker-compose logs -f fakeapp
docker-compose logs -f loki
```

## Configuration

### Loki

Edit `loki/loki-config.yaml` to modify:
- Retention period
- Storage settings
- Ingestion limits

### Promtail

Edit `promtail/promtail-config.yaml` to modify:
- Log paths
- Labels
- Pipeline stages

### Log Generator

Modify `generator/generate_logs.py` to:
- Add custom log messages
- Change log level distribution
- Adjust incident frequency

## License

MIT
