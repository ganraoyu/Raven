# AniAlert - Made with [discord.py](https://discordpy.readthedocs.io/en/stable/)

AniAlert is a Discord bot that helps anime fans track their favorite shows, get notified when episodes air, and discover seasonal anime.  

<img src="assets/list.png" alt="AniAlert UI" width="450"/>

## 🤖 Commands

| Command                     | Description                                           |
|-----------------------------|-------------------------------------------------------|
| `/search_anime`             | Search for anime by title with optional filters       |
| `/seasonal_anime`           | Browse this season's airing anime                    |
| `/random_anime_suggestion`  | Get random anime recommendations by genre            |
| `/list`                     | View your notification list                          |
| `/remove_anime`             | Remove an anime from your notification list          |
| `/clear`                    | Clear your entire notification list                  |
| `/guess_anime`              | Play a game where you guess the anime from a picture |
| `/schedule`                 | View the upcoming airing schedule of your anime      |
| `/search_image`             | Search anime by uploading a screenshot or image      |


## 🚀 Getting Started

# 1. Clone the AniAlert repository

```bash
git clone https://github.com/ganraoyu/AniAlert.git
```

### 2. Create and activate a virtual environment

```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Or Windows (cmd)
.\venv\Scripts\activate.bat
```

### 3. Install dependencies in editable mode

```bash
pip install -e .
```

> This installs AniAlert in “editable” mode so changes to the source code take effect immediately.

### 4. Create a `.env` file
```env
# Environment variables for AniAlert bot configuration

# Required for Discord bot authentication
DISCORD_TOKEN=your_discord_bot_token
CLIENT_ID=your_client_id

# Database configuration:
# By default, the bot uses a local SQLite database which requires no additional settings.
# To use PostgreSQL instead, set DB_TYPE to "postgres" and provide the connection details below.
DB_TYPE=sqlite          # Use "sqlite" for local DB (default) or "postgres" for remote

# PostgreSQL settings - only required if DB_TYPE=postgres
DB_HOST=               # PostgreSQL hostname or IP address
DB_NAME=               # PostgreSQL database name
DB_USER=               # PostgreSQL username
DB_PASSWORD=           # PostgreSQL password
DB_PORT=5432           # PostgreSQL port (default is 5432)
```

### 5. Run the bot

```bash
python bot.py
```

---

## 🗂 Project Structure

```
AniAlert/
├── bot.py                # Main entry point for the Discord bot
├── cogs/                 # Command modules (slash commands, etc.)
├── db/                   # DB connection and queries
├── providers/            # External API integrations (Anilist, Kitsu, etc.)
├── services/             # Business logic for searching, notifications, etc.
├── tasks/                # Background jobs and scheduled tasks that run independently 
├── utils/                # Helper functions and shared utilities
└──  views/               # Discord UI elements like buttons, views, menus
```

To run all tests using pytest:

```bash
pytest
```
