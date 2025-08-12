# Gmail Sentiment Analyzer (GSA) — v0.9.0-beta

Autonomous Gmail triage daemon that watches your inbox, scores new mail, and automatically **stars**, **routes for review**, or **silences** the noise.

**Repo:** https://github.com/Oberon01/Gmail-Sentiment-Analyzer

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Release CI](https://github.com/Oberon01/Gmail-Sentiment-Analyzer/actions/workflows/release.yml/badge.svg)](https://github.com/Oberon01/Gmail-Sentiment-Analyzer/actions/workflows/release.yml)
[![Release](https://img.shields.io/github/v/release/Oberon01/Gmail-Sentiment-Analyzer?include_prereleases&sort=semver)](https://github.com/Oberon01/Gmail-Sentiment-Analyzer/releases)


---

## Why?

Your inbox should empower you, not bury you. GSA applies lightweight NLP and simple rules to bucket daily mail:

| Bucket                     | Action            | Definition                                    |
|---------------------------|-------------------|-----------------------------------------------|
| **Important & Urgent**    | **Star**          | Directly impacts your day; must see this.     |
| **Important, Not Urgent** | **Add to Review** | Matters, but can wait until planned review.   |
| **Low Value**             | **Trash/Archive** | Ads, notifications, social clutter.           |

Runs as a background daemon (systemd, Task Scheduler, or Docker) so you can reclaim focus.

---

## Quick Start (choose one path)

> **Heads-up:** `pip install -r requirements.txt` only installs third-party libraries.  
> It does **not** install the `gsa` command. For `gsa`, you must also install **this project** (Path A).  
> If you don’t want to install the project, use the **direct script** (Path B).

### ✅ Path A — Use the `gsa` CLI (recommended)
1) From the repo root (where `pyproject.toml` lives):

```bash
# Clone & enter the repo
git clone https://github.com/Oberon01/Gmail-Sentiment-Analyzer.git
cd Gmail-Sentiment-Analyzer

# Create/activate a virtual env (optional but recommended)
python -m venv .venv

# Windows:
.venv\Scripts\activate

# macOS/Linux:
source .venv/bin/activate

# Install the project so the `gsa` command is available
pip install -e .          # or: pip install .
```
Now place your `credentials.json` in a working folder of your choice (not necessarily the repo), cd into that folder, and run:
```bash
gsa init          # creates .env and rules.yaml in *this* working folder
gsa labels        # lists Gmail labels and IDs
gsa --once --dry-run
# later: gsa --daemon
```
#### Troubleshooting:
If `gsa` is not found, you’re likely outside your virtual env.
  - Windows: where gsa
  - macOS/Linux: which gsa
Re-activate your env and retry.


### 🟨 Path B — Run the script directly (no project install)
If you prefer not to install the project, you can run the script with Python:
```bash
# Clone & enter the repo
git clone https://github.com/Oberon01/Gmail-Sentiment-Analyzer.git
cd Gmail-Sentiment-Analyzer

# (Optional) create/activate a venv, then:
pip install -r requirements.txt
```

Put `credentials.json` in your current working folder (where you want .env, rules.yaml, and gsa.log to live), then run:
```bash
python gmail_poll.py init
python gmail_poll.py labels
python gmail_poll.py --once --dry-run
# later: python gmail_poll.py --daemon
```

Gmail API credentials
  1. In Google Cloud Console, enable Gmail API.
  2. Create an OAuth Client ID → Desktop App.
  3. Download as credentials.json and place it in the working folder you’ll run from.
    - First run will open a browser for OAuth and save token.pickle locally.

#### Configuration (.env)
Created by init in your working folder:
```ini
LABEL_ID_REVIEW=Review
POLL_INTERVAL=600
GMAIL_POLL_CACHE=~/.cache/gmail_poll/cache.db
GSA_LOG_LEVEL=INFO
```

- `LABEL_ID_REVIEW` can be a label name (e.g., `Review`) or a label ID (`gsa labels` shows both).
> Tip while testing: set POLL_INTERVAL=90 for quicker feedback.
Usage reference
Dry-run once (no Gmail changes):
```bash
gsa --once --dry-run
# or: python gmail_poll.py --once --dry-run
```

Live once (applies actions; verify in Gmail after):
```bash
gsa --once
# or: python gmail_poll.py --once

# Gmail searches to verify:
#   label:starred newer_than:10m
#   in:trash newer_than:10m
#   label:Review newer_than:10m
```

Daemon mode (continuous):
```bash
gsa --daemon
# or: python gmail_poll.py --daemon
```

Custom rules file:
```bash
gsa --once --dry-run --rules rules.yaml
# or: python gmail_poll.py --once --dry-run --rules rules.yaml
```

---

### Docker (no local Python needed)
Put credentials.json in your working directory first; it’s mounted into the container.

macOS/Linux
```bash
docker run --rm -it -v "$PWD:/app" docker.io/oberon01/gsa:0.9.0-beta gsa --once --dry-run
```

Windows PowerShell
```powershell
docker run --rm -it -v "${PWD}:/app" docker.io/oberon01/gsa:0.9.0-beta gsa --once --dry-run
```

Windows CMD
```bat
docker run --rm -it -v "%cd%:/app" docker.io/oberon01/gsa:0.9.0-beta gsa --once --dry-run
```

Daemon via Docker
```bash
docker run -d --name gsa --restart=unless-stopped -v "$PWD:/app" docker.io/oberon01/gsa:0.9.0-beta gsa --daemon
```

Rules (rules.yaml)
Created by init. Example:
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
---

### Logging & Cache
- Console + rotating file log: gsa.log (in the working folder you run from).
- Cache DB for seen message IDs: ~/.cache/gmail_poll/cache.db.
To re-test the same messages in dry-run, delete or rename the cache DB.

---

### Run as a service
Linux (systemd user service)
Use the included `SYSTEMD-gsa.service` as a starting point.

Windows (Task Scheduler)
Create a basic task that runs:
```powershell
gsa --daemon
```

Set “Start in” to your working folder so logs/config resolve correctly.

#### Security & Privacy
- Gmail scope: `https://www.googleapis.com/auth/gmail.modify`
- Local files: `credentials.json`, `token.pickle`, `.env`, `rules.yaml`, cache DB, `gsa.log`.
- GSA sends data only to Gmail API under your authorization; no telemetry.

---

### Troubleshooting
- `gsa` not found: you didn’t install the project. Run `pip install -e .` (Path A), or use `python gmail_poll.py` … (Path B).
- No daemon output: set `POLL_INTERVAL=90` while testing.
- Review label not applied: ensure label exists; use `gsa labels` and set its name or ID in `.env`.
- Dry-run shows nothing after first time: cached IDs skip reprocessing; remove the cache DB.
- Want chatty live logs: look for `LIVE:` lines in console/`gsa.log` during actions.

---

### Roadmap
- Pluggable sentiment backends (spaCy/LLM)
- Minimal web UI for rules/thresholds
- Multi-account support
- Export daily triage metrics

---

### License
MIT — see `LICENSE`.
