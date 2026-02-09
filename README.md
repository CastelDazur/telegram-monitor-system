# 📊 Telegram Monitor System

**AI-Powered Platform for Telegram Chat Monitoring, Analytics & Automated Lead Generation**

[![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)](https://www.python.org/)
[![Telethon](https://img.shields.io/badge/Telethon-Latest-orange)](https://github.com/LonamiWebs/Telethon)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?logo=postgresql)](https://www.postgresql.org/)
[![Heroku](https://img.shields.io/badge/Deploy-Heroku-430098?logo=heroku)](https://heroku.com)

---

## 🚀 Overview

A production-ready Telegram monitoring system that uses **AI (GPT-4o-mini & Claude 3.5 Sonnet)** to automatically classify, filter, and route messages from multiple Telegram channels. The system performs real-time user profiling, lead scoring, and automated invitation management.

**Built for:** Real estate, employment, beauty, and automotive industry lead generation

### 🎯 Key Features

- 🤖 **Dual AI Classification** - OpenAI GPT-4o-mini + Anthropic Claude 3.5 Sonnet with fallback
- 📊 **Multi-Category Routing** - Auto-route messages to specialized channels (real estate, jobs, beauty, cars)
- 👥 **Smart User Profiling** - Automatic user collection with scoring (activity, bio, photos)
- 🔍 **Advanced Spam Filtering** - Regex + AI-based spam detection with SpamGuard
- 📤 **Automated Invitations** - Smart invite system with FloodWait handling and rate limiting
- 🌙 **Night Mode** - Auto-pause during inactive hours (01:00-06:00)
- 📈 **Real-time Analytics** - PostgreSQL-backed user database with JSONB storage
- 💔 **Health Monitoring** - Heartbeat checks + daily health reports via Telegram bot

---

## 🏛️ Architecture

### System Components

```
Passive Bot (Telethon) 
    ↓
 Message Handler 
    ↓
 Keyword Filter → AI Classifier (OpenAI/Claude)
    ↓
 Category Router → Output Sender
    ↓
 User Collector → PostgreSQL
```

### Tech Stack

| Component | Technology |
|-----------|------------|
| **Framework** | [Telethon](https://github.com/LonamiWebs/Telethon) (Telegram MTProto API) |
| **AI** | OpenAI GPT-4o-mini, Anthropic Claude 3.5 Sonnet |
| **Database** | PostgreSQL 15 with JSONB |
| **Deployment** | Heroku Dyno (Worker + Scheduler) |
| **Language** | Python 3.10 |
| **Queue** | Heroku Scheduler (cron jobs) |

---

## 📚 Core Functionality

### 1. Message Classification

- **LLM-based routing**: Messages analyzed by AI to determine category
- **Supported categories**: Real estate, employment, beauty, automobiles, irrelevant
- **Confidence threshold**: 0.35 (configurable)
- **Fallback mode**: If AI fails, uses keyword/regex matching

### 2. User Collection

- **Automatic profiling**: Extracts user_id, username, bio, photo count
- **Smart scoring**: Activity score based on messages, username quality, bio presence
- **PostgreSQL storage**: JSONB format for flexible schema
- **Export**: Daily JSON exports for invitation pipeline

### 3. Spam Filtering

**Pre-filter (Regex)**:
- Blocks: metamask, trustwallet, usdt, keeper, chatkeeper

**AI SpamGuard**:
- Analyzes suspicious messages
- Actions: delete, warn, ban
- Dry-run mode for testing

### 4. Automated Invitations

- **Smart targeting**: Uses scored user database
- **Rate limiting**: Hourly (8-10) & daily (25-33) limits
- **FloodWait handling**: Automatic delays on Telegram rate limits
- **PID locking**: Prevents concurrent invitation jobs
- **Scheduling**: Runs via Heroku Scheduler at configured windows (23:00, 01:00, 03:00 UTC)

### 5. Night Mode

- **Auto-pause**: Bot stops during 01:00-06:00 (configurable timezone)
- **Graceful shutdown**: Sends summary before sleep
- **Auto-restart**: Resumes at 07:00

---

## 🔧 Configuration

### Environment Variables (Key)

```bash
# Telegram Bot
BOT1_API_ID=28884515
BOT1_SESSION_STRING=1ApWapzMBu...

# AI Providers
OPENAI_API_KEY=sk-proj-...
CLAUDE_API_KEY=sk-ant-...
OPENAI_MODEL=gpt-4o-mini
ANTHROPIC_MODEL=claude-3-5-sonnet-20240620

# Database
DATABASE_URL=postgres://...
PG_SSL_MODE=require

# Routing Channels
REALESTATE_CHAT_ID=-1002886864805
EMPLOYMENT_CHAT_ID=-1002708895240
BEAUTY_CHAT_ID=-1002517294239
AUTOMOBILES_CHAT_ID=-1002739633761

# Night Mode
NIGHT_MODE_ENABLED=true
NIGHT_MODE_START=01:00
NIGHT_MODE_END=06:00

# Inviter
INVITER_STRING_SESSION=1ApWapzMBu...
INVITE_HOURLY_LIMIT=8
INVITE_DAILY_LIMIT=25
INVITE_DELAY_MIN=60
INVITE_DELAY_MAX=180
```

---

## 💾 Database Schema

### PostgreSQL Table: `users_meta`

```sql
CREATE TABLE IF NOT EXISTS users_meta (
    user_id BIGINT PRIMARY KEY,
    meta JSONB NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_users_meta_updated_at 
ON users_meta (updated_at DESC);
```

**JSONB Structure**:
```json
{
  "user_id": 123456789,
  "username": "example_user",
  "sender_name": "John Doe",
  "bio": "Software Engineer",
  "photo_count": 3,
  "message_count": 42,
  "activity_score": 28,
  "last_seen": "2026-02-09T11:00:00Z"
}
```

---

## 🚀 Deployment (Heroku)

### 1. Procfile (Worker Dyno)

```bash
worker: bash -lc 'set -euo pipefail; ...; python src/bot_manager.py'
```

### 2. Heroku Scheduler Jobs

| Time (UTC) | Command | Purpose |
|------------|---------|----------|
| 23:00 | `python -m pg_export_users_file` | Export users to JSON |
| 23:00 | `python scheduled_invite.py` | Run invitations |
| 01:00 | `python scheduled_invite.py` | Run invitations |
| 03:00 | `python scheduled_invite.py` | Run invitations |

### 3. Deploy Commands

```bash
# Push to Heroku
git push heroku HEAD:main

# Scale worker
heroku ps:scale worker=1 -a your-app

# View logs
heroku logs -a your-app -t --ps worker
```

---

## 📊 Monitoring

### Health Check

- **Daily report**: Sent at 23:55 UTC to HEALTHCHECK_CHAT_ID
- **Metrics**: Message count, AI usage, errors, user stats
- **Bot status**: Uses HEALTHCHECK_BOT_TOKEN

### Log Analysis

```powershell
# View recent activity
heroku logs -a your-app -n 4000 --ps scheduler | Select-String -Pattern "Smart Inviter"

# Check errors
heroku logs -a your-app | Select-String -Pattern "ERROR|CRITICAL|FloodWait"

# Count invitations
heroku logs -a your-app | Select-String -Pattern "invited" | Measure-Object
```

---

## 🛡️ Security

- **Session Management**: Telethon StringSession (no file storage)
- **Rate Limiting**: Built-in FloodWait handler
- **PID Locking**: Prevents concurrent inviter runs
- **Spam Protection**: Pre-filter + AI-based detection
- **Database**: SSL-required PostgreSQL connection

---

## 📝 Project Structure

```
telegram-monitor-system/
├── src/
│   ├── bot_manager.py          # Main bot orchestrator
│   ├── passive_bot.py          # Telethon client
│   ├── message_handler.py      # Message processor
│   ├── ai_classifier.py        # AI routing logic
│   ├── keyword_filter.py       # Regex matching
│   ├── output_sender.py        # Message forwarder
│   ├── simple_user_collector.py # User profiler
│   ├── pg_user_store.py        # PostgreSQL ORM
│   ├── smart_inviter.py        # Invitation logic
│   └── moderation/
│       ├── spam_guard.py       # AI spam detection
│       └── adapter.py          # Moderation interface
├── scheduled_invite.py     # Cron job entrypoint
├── check_candidates.py     # Pre-filter users
├── config/                 # JSON configs
├── logs/                   # Runtime logs
├── requirements.txt        # Python deps
└── Procfile                # Heroku config
```

---

## 📈 Performance

- **Channels monitored**: 15+
- **Messages processed**: ~1000/day
- **AI classification**: 95%+ accuracy
- **Database size**: ~10 MB (1000+ users)
- **Uptime**: 99.5% (Heroku Essential Dyno)

---

## 👨‍💻 Author

**Dmytro Romanov** - Full-Stack Developer  
📧 casteldazur@gmail.com  
🔗 [LinkedIn](https://linkedin.com/in/casteldazur) | [GitHub](https://github.com/CastelDazur)

---

## 📝 License

MIT License - See LICENSE file for details

---

<p align="center">
  <i>Built with Python, AI, and ❤️ in Nice, France</i>
</p>
