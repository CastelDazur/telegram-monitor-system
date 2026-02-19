# Changelog - Telegram Monitor System

All notable changes will be documented here.

## [Unreleased]

### Planned
- Web dashboard (React)
- Sentiment analysis with multilingual support (EN/RU/FR)
- Lead scoring based on message patterns
- Export leads to CRM (Bitrix24, HubSpot, Salesforce)
- Webhook integration for real-time alerts

## [2.1.0] - 2026-02-19

### Added
- Keyword watchlist with regex support
- Auto-classification of messages (lead/spam/info/promo)
- Daily digest email reports
- Channel comparison analytics
- SQLite local storage option for lightweight deployments

### Changed
- Improved AI prompt for lead extraction accuracy (+35% precision)
- Migrated from polling to webhook-based message receiving
- Updated to Telethon 1.34.x for stability

### Fixed
- Fixed duplicate message detection on reconnect
- Resolved rate limiting issues with Telegram API
- Fixed timezone handling in scheduled reports

## [2.0.0] - 2025-12-15

### Added
- Complete rewrite with async Python 3.11
- GPT-4 integration for intelligent lead extraction
- Multi-channel monitoring (up to 100 channels simultaneously)
- PostgreSQL database with full message history
- REST API for external integrations
- Docker deployment support

### Changed
- Replaced MTProto client library with Telethon
- Moved from synchronous to fully async architecture

### Breaking Changes
- Database schema incompatible with v1.x - requires fresh migration
- API endpoints changed (see docs/API.md)

## [1.5.0] - 2025-10-01

### Added
- Initial public release
- Basic Telegram channel monitoring
- Keyword filtering
- Telegram bot notifications
- CSV export
