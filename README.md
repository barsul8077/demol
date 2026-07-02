# Instagram Profile Auto Update System

## Overview

This project refreshes Instagram profile data automatically and stores updates in a MySQL database. It also calculates engagement metrics from TheSocialCat and stores history for every refresh.

## Features

- Loads usernames from `Insta_Influencers`
- Scrapes Instagram profile fields
- Calculates engagement metrics from TheSocialCat
- Stores profile refresh history in `instagram_profile_history`
- Logs success, errors, and processing events
- Provides a live preview GUI using Tkinter
- Supports scheduled daily refresh and manual execution

## Requirements

- Python 3.12+
- Google Chrome installed
- ChromeDriver compatible with Chrome version
- MySQL database access

## Setup

1. Copy `.env.example` to `.env`
2. Update database credentials in `.env`
3. Install dependencies:

```bash
pip install -r requirements.txt
python -m playwright install chromium
```

4. Create the history table if not exists by running the project once.

## Running

- Manual refresh:

```bash
python main.py
```

- Run scheduler:

```bash
python main.py --schedule
```

## Project Structure

- `config/` configuration loader
- `database/` database manager
- `models/` data models
- `scrapers/` Instagram and engagement scrapers
- `scheduler/` job scheduler
- `history/` history management
- `gui/` live preview dashboard
- `utils/` shared utilities
- `main.py` entrypoint

## Notes

- Never hardcode credentials.
- The system retries failed profile fetches up to 3 times.
- The GUI updates in real time while profiles are processed.
