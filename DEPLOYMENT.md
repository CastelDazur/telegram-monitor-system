# Deployment Guide

Step-by-step instructions for deploying the Telegram Monitor System in production.

## Prerequisites

- Python 3.10+
- PostgreSQL 14+
- Redis 7+
- Docker & Docker Compose (recommended)
- A Telegram API account (`api_id` + `api_hash` from [my.telegram.org](https://my.telegram.org))
- A Telegram Bot token (from [@BotFather](https://t.me/BotFather))

---

## Option 1: Docker Compose (Recommended)

### 1. Clone and configure

```bash
git clone https://github.com/CastelDazur/telegram-monitor-system.git
cd telegram-monitor-system
cp .env.example .env
```

### 2. Edit `.env`

```env
# Telegram API Credentials
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_PHONE=+33600000000

# Database
DATABASE_URL=postgresql://monitor:password@postgres:5432/telegram_monitor
REDIS_URL=redis://redis:6379/0

# AI Settings
OPENAI_API_KEY=your_openai_key
AI_MODEL=gpt-4o-mini
SENTIMENT_THRESHOLD=0.6

# Application
APP_SECRET_KEY=your-secret-key-here
DEBUG=false
LOG_LEVEL=INFO
MAX_CHANNELS=50
MESSAGE_BATCH_SIZE=100
```

### 3. Start services

```bash
docker-compose up -d
```

This starts:
- `monitor` — main Python monitoring service
- `api` — FastAPI REST interface
- `postgres` — PostgreSQL database
- `redis` — message queue and caching
- `celery` — background task workers
- `flower` — Celery task monitor (port 5555)
- `nginx` — reverse proxy (port 80/443)

### 4. Run migrations

```bash
docker-compose exec api alembic upgrade head
```

### 5. Create admin user

```bash
docker-compose exec api python manage.py create_admin --email admin@example.com
```

---

## Option 2: Manual Installation

### 1. System dependencies

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y python3.10 python3-pip postgresql redis-server

# Install Python deps
pip install -r requirements.txt
```

### 2. PostgreSQL setup

```sql
CREATE DATABASE telegram_monitor;
CREATE USER monitor WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE telegram_monitor TO monitor;
```

### 3. Run migrations

```bash
alembic upgrade head
```

### 4. Start services

```bash
# Terminal 1: Main monitor
python -m src.monitor.main

# Terminal 2: API server
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --workers 4

# Terminal 3: Celery workers
celery -A src.tasks worker --loglevel=info --concurrency=4

# Terminal 4: Celery Beat (scheduler)
celery -A src.tasks beat --loglevel=info
```

---

## Production Checklist

### Security
- [ ] Change all default passwords in `.env`
- [ ] Set `DEBUG=false`
- [ ] Configure SSL/TLS certificates (Let's Encrypt recommended)
- [ ] Set up firewall rules (allow only 80, 443, 22)
- [ ] Enable fail2ban for SSH protection
- [ ] Rotate `APP_SECRET_KEY` on first deployment
- [ ] Store credentials in secrets manager (not `.env` files)

### Performance
- [ ] Set PostgreSQL connection pool size: `DB_POOL_SIZE=20`
- [ ] Configure Redis maxmemory policy: `maxmemory-policy allkeys-lru`
- [ ] Enable Celery worker autoscaling
- [ ] Set up Nginx rate limiting for API endpoints

### Monitoring
- [ ] Set up health check endpoint: `GET /health`
- [ ] Configure uptime monitoring (e.g., UptimeRobot)
- [ ] Enable Sentry error tracking: `SENTRY_DSN=your_dsn`
- [ ] Set up log aggregation (e.g., Papertrail, Datadog)
- [ ] Configure alerts for channel analysis failures

### Backup
- [ ] Automated PostgreSQL backups (daily minimum)
- [ ] Redis RDB/AOF persistence enabled
- [ ] Store Telethon session files safely

---

## Scaling

### Horizontal scaling (multiple monitor instances)

```yaml
# docker-compose.override.yml
services:
  monitor:
    deploy:
      replicas: 3
  celery:
    deploy:
      replicas: 5
```

### Channel limits per instance

| Instance Type | Max Channels | Messages/day |
|---------------|-------------|---------------|
| Small (2 CPU, 4GB) | 20 | ~100K |
| Medium (4 CPU, 8GB) | 50 | ~500K |
| Large (8 CPU, 16GB) | 150 | ~2M |

---

## Troubleshooting

### Monitor not connecting to Telegram
```bash
# Check session file
docker-compose exec monitor python -c "from telethon import TelegramClient; print('OK')"

# Re-authenticate
docker-compose exec monitor python -m src.auth.setup
```

### Database connection errors
```bash
docker-compose exec postgres psql -U monitor -d telegram_monitor -c "SELECT 1"
```

### View logs
```bash
docker-compose logs -f monitor
docker-compose logs -f celery
```

---

*For issues, open a GitHub Issue or contact [casteldazur@gmail.com](mailto:casteldazur@gmail.com)*
