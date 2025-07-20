# DawnBot

**DawnBot** is a personal Discord bot project written in Python. Its primary feature is to **celebrate user birthdays** by automatically posting a birthday message in a designated server channel. The bot is containerized using Docker and uses PostgreSQL for persistent data storage.

---

## Features

- Slash command to set your birthday
- Slash command to get another member's birthday
- Daily automatic birthday announcements in a specific channel
- PostgreSQL backend for storing birthday data
- Dockerized for easy deployment

---

## Technologies

- Python 3.11
- [Pycord](https://docs.pycord.dev/)
- PostgreSQL
- Docker + Docker Compose
- dotenv for secrets

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/dawnbot.git
cd dawnbot
```

### 2. Add a `.env` File

Create a `.env` file in the root with the following:

```env
DISCORD_TOKEN=your_token_here
DB_NAME=database_name
DB_USER=database_user
DB_PASSWORD=database_pw
DB_HOST=postgres
DB_PORT=5432
BIRTHDAY_CHANNEL_ID=your_discord_channel_id
```

### 3. Build and Run with Docker

```bash
docker-compose up --build
```

This will start the bot and a locally hosted PostgreSQL container.


## Slash Commands


These are the main commands that aren't test commands (which will be removed someday)
|Command|Description  |
|--|--|
|`/setbirthday` | Set your birthday (month, day) |
| `/getbirthday` | Get a member's birthday |
| `/testbirthday` | Simulate today instead of waiting 24 hours to get birthday message|

---
