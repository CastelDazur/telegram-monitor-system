# Telegram Monitor System

> Лёгкая система мониторинга Telegram для поиска сигналов, лидов и аналитики в реальном времени. Основа — Telethon, конфигурация — через .env, развёртывание — локально или на Heroku.

[English version below ⬇](#english)

---

## Содержание

- [Кратко](#кратко)
- [Мини-баннер и бейджи](#мини-баннер-и-бейджи)
- [Ключевые возможности](#ключевые-возможности)
- [Архитектура](#архитектура)
- [Применение для бизнеса](#применение-для-бизнеса)
- [Структура проекта](#структура-проекта)
- [Установка и запуск локально](#установка-и-запуск-локально)
- [Конфигурация окружения](#конфигурация-окружения)
- [Деплой на Heroku](#деплой-на-heroku)
- [Работа с данными и аналитикой](#работа-с-данными-и-аналитикой)
- [Дорожная карта](#дорожная-карта)
- [Безопасность и соответствие](#безопасность-и-соответствие)
- [Вклад и обратная связь](#вклад-и-обратная-связь)
- [Лицензия](#лицензия)
- [Скриншоты](#скриншоты)

---

## Кратко

- **Назначение:** фильтрация сообщений из указанных чатов/каналов Telegram по ключевым словам и маршрутизация в «чистые» закрытые каналы команды.
- **Фокус:** поиск лидов, мониторинг ключевых сигналов, первичная аналитика активности.
- **Подход:** модульная архитектура (filters, router, monitor), простое конфигурирование через .env, минимальные зависимости.

---

## Мини-баннер и бейджи

- **Проект:** Telegram Monitor System • v1.0
- **Платформа:** Python 3.11+ • Telethon • Heroku-ready
- **Лицензия:** MIT
- **Статус:** Active development
---

## Ключевые возможности

- **Мониторинг:** подписка на чаты/каналы, чтение новых сообщений в реальном времени.
- **Фильтрация:** отбор по ключевым словам, фразам и хэштегам с регистронезависимым сравнением.
- **Маршрутизация:** публикация совпадений в закрытые каналы для командной работы.
- **Конфигурация:** параметры проекта — через .env и config/settings.py.
- **Расширяемость:** отдельные модули для фильтров, роутера, обработчиков событий.

---

## Архитектура

```
Telegram чаты/каналы
   │
Telethon Client (Session)
   │
События новых сообщений
   │
Filters (ключевые слова, правила)
   │
Router (куда отправить совпадения)
   │
Целевые закрытые каналы / Логи / Экспорт
```

---

## Применение для бизнеса

- **Лиды:** отслеживание «ищу», «нанимаем», «нужен подрядчик», «ищем фаундера».
- **Маркетинг/PR:** упоминания бренда, запросы «рекомендйте», тренды тем.
- **HR:** публикации о вакансиях, активности специалистов в нишевых сообществах.
- **Аналитика:** динамика сообщений, плотность тем, «горячие» часы активности.

---

## Структура проекта

```
.
├── app
│   ├── __init__.py
│   ├── filters.py
│   ├── monitor.py
│   └── router.py
├── config
│   └── settings.py
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
└── main.py        ← точка входа (см. пример ниже)
```

---

## Установка и запуск локально

1. **Клонирование**
   - **Команда:**
     ```
     git clone https://github.com/CastleDazur/telegram-monitor-system.git
     cd telegram-monitor-system
     ```

2. **Зависимости**
   - **Установка:**
     ```
     python -m venv venv
     source venv/bin/activate   # Windows: venv\Scripts\activate
     pip install -r requirements.txt
     ```

3. **Конфигурация**
   - **Действия:** скопируйте .env.example → .env и заполните значения (см. ниже).

4. **Запуск**
   - **Команда:**
     ```
     python main.py
     ```

---

## Конфигурация окружения

> Все переменные читаются из .env через python-dotenv и доступны в config/settings.py.

| Переменная           | Описание                                     | Пример                        |
|----------------------|--------------------------------------------- |-------------------------------|
| TELEGRAM_API_ID      | API ID Telegram                              | 123456                        |
| TELEGRAM_API_HASH    | API Hash Telegram                            | abcdef0123456789abcdef0123    |
| TELEGRAM_SESSION_NAME| Имя сессии Telethon                          | monitor_session               |
| KEYWORDS             | Список ключевых слов (через запятую)         | crypto,project,launch         |
| TARGET_CHANNEL_IDS   | Целевые каналы для публикации (через запятую)| -1001234,-1005678             |

Пример .env.example:
```
TELEGRAM_API_ID=123456
TELEGRAM_API_HASH=your_api_hash_here
TELEGRAM_SESSION_NAME=monitor_session
KEYWORDS=crypto,project,launch
TARGET_CHANNEL_IDS=-1001234567890
```

---

## Деплой на Heroku

1. **Подготовка**
   - **Файлы:**
     ```
     Procfile
     runtime.txt
     ```
   - **Procfile (пример):**
     ```
     worker: python main.py
     ```
   - **runtime.txt (пример):**
     ```
     python-3.11.6
     ```

2. **Развёртывание**
   - **Команды:**
     ```
     heroku create
     heroku buildpacks:set heroku/python
     git push heroku main
     ```

3. **Переменные окружения**
   - **Действия:** установите TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_SESSION_NAME, KEYWORDS, TARGET_CHANNEL_IDS в Heroku Config Vars.

4. **Запуск воркера**
   - **Команда:**
     ```
     heroku ps:scale worker=1
     ```

---

## Работа с данными и аналитикой

- **Логи:** вывод совпадений в stdout (Heroku — в логи), опционально — в файл.
- **Экспорт:** при необходимости — CSV/JSON экспортер (можно добавить в app/router.py).
- **Сводки:** периодические дайджесты (по cron/планировщику) в отдельный канал.

---

## Дорожная карта

- **v1.1:** расширенные фильтры (регулярные выражения, стоп-слова), экспорт CSV/JSON, конфиг через YAML.
- **v1.2:** статистика по каналам (частота, «горячие часы»), простые графики, отправка дневных дайджестов.
- **v1.3:** интеграции (Webhook для CRM), тегирование категорий, список исключений.
- **v2.0:** масштабируемая обработка (очереди), хранение событий (PostgreSQL), панель аналитики (внешний BI).

---

## Безопасность и соответствие

- **Ограничение:** проект не аффилирован с Telegram, использует только доступные API.
- **Данные:** работает с публичным контентом; не предназначен для спама и нарушений приватности.
- **Юрисдикция:** соблюдайте местные законы и правила платформы.

---

## Вклад и обратная связь

- **Issues:** создавайте задачи и предложения по улучшениям.
- **PRs:** приветствуются — придерживайтесь стиля кода и линтинга.
- **Идеи:** открыты к новым сценариям мониторинга и аналитики.

---

## Лицензия

- **Тип:** MIT — свободное использование, модификация и распространение с сохранением уведомления об авторстве.

---

## Скриншоты

- **Чистая лента совпадений:** docs/screenshots/clean_feed.png
- **Пример настройки .env:** docs/screenshots/env_example.png

---

## Пример точки входа (main.py)

```python
from app.monitor import run

if __name__ == "__main__":
    run()
```
## 📬 Контакты
- **LinkedIn:** [Dmytro Romanov](https://www.linkedin.com/in/casteldazur/)
- **GitHub:** [CastleDazur](https://github.com/CastleDazur)
- **Email:** castledazur@gmail.com
- **TG:** https://t.me/casteldazur
---

# English

> Lightweight Telegram monitoring system for real-time signal detection, lead discovery, and analytics. Built on Telethon, configured via .env, deployable locally or on Heroku.

[Перейти к русской версии ⬆](#кратко)

---

## Contents

- [At a glance](#at-a-glance)
- [Mini banner and badges](#mini-banner-and-badges)
- [Key features](#key-features)
- [Architecture](#architecture-1)
- [Business use cases](#business-use-cases)
- [Project structure](#project-structure)
- [Local setup](#local-setup)
- [Environment configuration](#environment-configuration)
- [Deploy to Heroku](#deploy-to-heroku)
- [Data and analytics](#data-and-analytics)
- [Roadmap](#roadmap)
- [Safety and compliance](#safety-and-compliance)
- [Contributing](#contributing)
- [License](#license)
- [Screenshots](#screenshots-1)

---

## At a glance

- **Purpose:** filter messages from selected Telegram chats/channels by keywords and route matches to “clean” team channels.
- **Focus:** lead discovery, key-signal tracking, basic activity analytics.
- **Approach:** modular design (filters, router, monitor), .env configuration, minimal dependencies.

---

## Mini banner and badges

- **Project:** Telegram Monitor System • v1.0
- **Platform:** Python 3.11+ • Telethon • Heroku-ready
- **License:** MIT
- **Status:** Active development

---

## Key features

- **Monitoring:** subscribe to chats/channels and read new messages in real time.
- **Filtering:** case-insensitive keyword/phrase/hashtag filtering.
- **Routing:** post matches to private team channels for focused workflows.
- **Configuration:** .env variables wired via config/settings.py.
- **Extensibility:** dedicated modules for filters, routing, and event handlers.

---

## Architecture

```
Telegram chats/channels
   │
Telethon Client (Session)
   │
New message events
   │
Filters (keywords, rules)
   │
Router (targets and outputs)
   │
Private target channels / Logs / Export
```

---

## Business use cases

- **Leads:** “looking for”, “hiring”, “need contractor”, early-demand signals.
- **Marketing/PR:** brand mentions, “recommend please” requests, topic trends.
- **HR:** vacancy posts and expert activity in niche communities.
- **Analytics:** message dynamics, topic density, “hot” activity hours.

---

## Project structure

```
.
├── app
│   ├── __init__.py
│   ├── filters.py
│   ├── monitor.py
│   └── router.py
├── config
│   └── settings.py
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
└── main.py
```

---

## Local setup

1. **Clone**
   - **Command:**
     ```
     git clone https://github.com/CastleDazur/telegram-monitor-system.git
     cd telegram-monitor-system
     ```

2. **Dependencies**
   - **Install:**
     ```
     python -m venv venv
     source venv/bin/activate   # Windows: venv\Scripts\activate
     pip install -r requirements.txt
     ```

3. **Config**
   - **Action:** copy .env.example → .env and fill in required values (see below).

4. **Run**
   - **Command:**
     ```
     python main.py
     ```

---

## Environment configuration

> Variables are loaded from .env via python-dotenv and exposed in config/settings.py.

| Variable             | Description                                  | Example                       |
|---------------------|---------------------------------------------- |-------------------------------|
| TELEGRAM_API_ID     | Telegram API ID                               | 123456                        |
| TELEGRAM_API_HASH   | Telegram API Hash                             | abcdef0123456789abcdef0123    |
| TELEGRAM_SESSION_NAME| Telethon session name                        | monitor_session               |
| KEYWORDS            | Comma-separated keywords                      | crypto,project,launch         |
| TARGET_CHANNEL_IDS  | Comma-separated target channel IDs            | -1001234,-1005678             |

Sample .env.example:
```
TELEGRAM_API_ID=123456
TELEGRAM_API_HASH=your_api_hash_here
TELEGRAM_SESSION_NAME=monitor_session
KEYWORDS=crypto,project,launch
TARGET_CHANNEL_IDS=-1001234567890
```

---

## Deploy to Heroku

1. **Prepare**
   - **Files:**
     ```
     Procfile
     runtime.txt
     ```
   - **Procfile:**
     ```
     worker: python main.py
     ```
   - **runtime.txt:**
     ```
     python-3.11.6
     ```

2. **Deploy**
   - **Commands:**
     ```
     heroku create
     heroku buildpacks:set heroku/python
     git push heroku main
     ```

3. **Config Vars**
   - **Action:** set TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_SESSION_NAME, KEYWORDS, TARGET_CHANNEL_IDS.

4. **Scale worker**
   - **Command:**
     ```
     heroku ps:scale worker=1
     ```

---

## Data and analytics

- **Logs:** matches printed to stdout (Heroku logs), optional file logging.
- **Export:** CSV/JSON exporter can be added in app/router.py if needed.
- **Digest:** periodic digests (cron/scheduler) to a dedicated channel.

---

## Roadmap

- **v1.1:** enhanced filters (regex, stop words), CSV/JSON export, YAML config.
- **v1.2:** per-channel stats (frequency, hot hours), simple charts, daily digests.
- **v1.3:** integrations (CRM webhook), category tagging, exclusion lists.
- **v2.0:** scalable processing (queues), event storage (PostgreSQL), BI dashboard.

---

## Safety and compliance

- **Disclaimer:** not affiliated with Telegram; uses publicly available APIs.
- **Data:** intended for public content; not for spam or privacy violations.
- **Jurisdiction:** comply with local laws and platform rules.

---

## Contributing

- **Issues:** open feature requests and bug reports.
- **PRs:** welcome; follow code style and lint rules.
- **Ideas:** open to new monitoring and analytics scenarios.

---

## License

- **Type:** MIT — free to use, modify, and distribute with attribution.

---

## Screenshots

- **Clean matches feed:** docs/screenshots/clean_feed.png
- **.env setup example:** docs/screenshots/env_example.png


## 📬 Contacts
- **LinkedIn:** [Dmytro Romanov](https://www.linkedin.com/in/casteldazur/)
- **GitHub:** [CastleDazur](https://github.com/CastleDazur)
- **Email:** castledazur@gmail.com
- **TG:** https://t.me/casteldazur
