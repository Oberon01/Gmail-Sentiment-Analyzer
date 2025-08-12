# Gmail Sentiment Analyzer (GSA) — v0.9.0-beta

Autonomous Gmail triage daemon that watches your inbox, scores new mail, and automatically **stars**, **routes for review**, or **silences** the noise.

---

## Why?

Your inbox should empower you, not bury you. GSA applies lightweight NLP to slice daily mail into three buckets:

| Bucket                     | Action            | Definition                                    |
|---------------------------|-------------------|-----------------------------------------------|
| **Important & Urgent**    | **Star**          | Directly impacts your day; must see this.     |
| **Important, Not Urgent** | **Add to Review** | Matters, but can wait until planned review.   |
| **Low Value**             | **Trash/Archive** | Ads, notifications, social clutter.           |

Run as a background daemon (systemd, Task Scheduler, or Docker) and reclaim head-space.

---

## Features

- **Lightweight NLP**: sentiment proxy via TextBlob (CPU-only; no big model).
- **Rules overlay**: whitelist/blacklist or always-star specific senders/subjects.
- **Resilient**: exponential backoff for Gmail API calls; won’t crash on blips.
- **Observable**: logs to console and rotating file `gsa.log`.
- **Idempotent**: caches processed message IDs to avoid reprocessing.
- **Dry-run**: see exactly what would happen without changing Gmail.

---

## Installation

### 1) Clone & install

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
python -m venv .venv

# Windows:
.venv\Scripts\activate

# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) Enable Gmail API and create credentials
1. In Google Cloud Console, enable Gmail API.
2. Create an OAuth Client ID → Desktop App.
3. Download the client secret as `credentials.json` and place it in the project folder (same directory you run the script from).

4. First run will open a browser to authorize; a `token.pickle` will be stored locally.

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