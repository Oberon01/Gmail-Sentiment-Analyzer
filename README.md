# Gmail Sentiment Analyzer (GSA) — v0.9.0-beta

Autonomous Gmail triage daemon that watches your inbox, scores new mail, and automatically **stars**, **routes for review**, or **silences** the noise.

**Repo:** https://github.com/Oberon01/Gmail-Sentiment-Analyzer

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Release](https://img.shields.io/github/v/tag/Oberon01/Gmail-Sentiment-Analyzer?label=release)](https://github.com/Oberon01/Gmail-Sentiment-Analyzer/releases)

---

## Why?

Your inbox should empower you, not bury you. GSA applies lightweight NLP and simple rules to bucket daily mail:

| Bucket                     | Action            | Definition                                    |
|---------------------------|-------------------|-----------------------------------------------|
| **Important & Urgent**    | **Star**          | Directly impacts your day; must see this.     |
| **Important, Not Urgent** | **Add to Review** | Matters, but can wait until planned review.   |
| **Low Value**             | **Trash/Archive** | Ads, notifications, social clutter.           |

Run as a background daemon (systemd, Task Scheduler, or Docker) and reclaim head-space.

---

## Features

- **Lightweight NLP**: sentiment proxy via TextBlob (CPU-only; no big model).
- **Rules overlay**: `rules.yaml` supports `whitelist`, `blacklist`, `always_star`.
- **Resilient**: exponential backoff for Gmail API calls; won’t crash on blips.
- **Observable**: logs to console and rotating file `gsa.log`.
- **Idempotent**: caches processed message IDs; no double-processing.
- **Dry-run**: see actions without touching Gmail.

---

## Installation

### 1) Clone & install

```bash
git clone https://github.com/Oberon01/Gmail-Sentiment-Analyzer.git
cd Gmail-Sentiment-Analyzer
python -m venv .venv

# Windows:
.venv\Scripts\activate

# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

### 2) nable Gmail API and create credentials
  1. In Google Cloud Console, enable Gmail API.
  2. Create an OAuth Client ID → Desktop App.
  3. Download as credentials.json and place it in the folder you will run GSA from (a working folder you choose).
  4. On first run, a browser opens for OAuth and token.pickle is saved locally.

### 3) First-time setup
```bash
python gmail_poll.py init           # writes .env and rules.yaml in current dir
python gmail_poll.py labels         # list Gmail labels and their IDs
```

## Edit `.env` (created by `init`) to set your review label (name or ID):
```env
LABEL_ID_REVIEW=Review
POLL_INTERVAL=600
GMAIL_POLL_CACHE=~/.cache/gmail_poll/cache.db
GSA_LOG_LEVEL=INFO
```
> Tip: While testing, set `POLL_INTERVAL=90` for quicker feedback.

## Usage
### **Dry-run once** (no changes to Gmail):
```bash
python gmail_poll.py --once --dry-run
```

### **Live once** (applies actions, good for verification):
```bash
python gmail_poll.py --once
# Then check Gmail:
#   label:starred newer_than:10m
#   in:trash newer_than:10m
#   label:Review newer_than:10m   (or your chosen review label)
```

### **Daemon mode** (continuous):
```bash
python gmail_poll.py --daemon
```

### **Custom rules file**:
```bash
python gmail_poll.py --once --dry-run --rules rules.yaml
```

## **Rules** (`rules.yaml`)
Created by `init`. Example:

```yaml
whitelist:
  - "@yourcompany.com"
  - "vip.client@example.com"

blacklist:
  - "@examplemailer.com"

always_star:
  - "boss@yourcompany.com"
  - "spouse@example.com"
  ```

## **Logging & Cache**
- Console + rotating file log: `gsa.log` (created in the working directory).
- Cache DB for seen message IDs: `~/.cache/gmail_poll/cache.db`.

To re-test the same messages in dry-run, delete or rename the cache DB.

## Run as a service
### Linux (systemd user service)
Use the sample unit `SYSTEMD-gsa.service`:
```bash
# Example layout (user service)
mkdir -p ~/gsa && cp -r <repo>/* ~/gsa
systemctl --user enable --now gsa@$(whoami).service
```

### Windows (Task Scheduler)
Create a basic task that runs:
```bash
python <path>\gmail_poll.py --daemon
```
### Docker Run
```bash
docker run --rm -it -v "%cd%:/app" oberon01/gsa:/0.9.0-beta gsa dry-run
```

Set **Start in** to the project folder so logs/config resolve correctly.

## Security & Privacy
- Scope used: `https://www.googleapis.com/auth/gmail.modify`
- Tokens are stored locally as `token.pickle` next to your `credentials.json`.
- Single-user, local tool. No data leaves your machine beyond Gmail API calls you authorize.

## Troubleshooting
- No output in daemon: lower `POLL_INTERVAL` to `90` for faster feedback.

- Review label not applied: ensure it exists in Gmail; use `python gmail_poll.py labels` and set `LABEL_ID_REVIEW` to that name or ID.

- Dry-run shows nothing after first time: cached IDs are skipping; remove the cache DB to re-process.

- Want chatty live logs: look for `LIVE`: lines in console/`gsa.log` during actions.

## Roadmap
- Hot-swap sentiment backends (spaCy/LLM).
- Minimal web UI to tweak rules and thresholds.
- Multi-account support.
- Export daily triage metrics for journaling/Obsidian.

## License
MIT — see LICENSE.
