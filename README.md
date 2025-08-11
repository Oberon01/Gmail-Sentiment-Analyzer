# gmail\_poll

> Autonomous Gmail triage daemon that watches your inbox, scores every message for **signal‑to‑noise**, and then acts: *archive the junk, star the gold, surfacing only what truly matters*.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/status-beta-yellow)

---

## Why?

Your inbox should empower you, not bury you. *gmail\_poll* applies lightweight NLP to slice daily mail into three buckets:

| Bucket                       | Action                   | Definition                                    |
| ---------------------------- | ------------------------ | --------------------------------------------- |
| **Important & Urgent**       | **Star + Keep**        | Directly impacts your day; you must see this. |
| **Important but Not Urgent** | **Label / Review**   | Matters, but can wait until planned review.   |
| **Low Value**                | **Archive / Delete** | Ads, notifications, social clutter.           |

Run as a background daemon (systemd, Docker, or cron) and reclaim head‑space you can invest elsewhere.

---

## Features

* **Sentiment & priority scoring** powered by a distilled Transformer (≈40 MB, runs on CPU)
* **Rule overlay**: whitelist/blacklist domains or subjects for deterministic routing
* **Zero‑touch operation**: authenticates with Gmail via OAuth2 service account; token auto‑refresh
* **Observable**: JSON logs → stdout; integrate with Loki/Grafana in one line
* **Stateless**: keeps a local cache of processed message IDs to avoid re‑processing
* **Dry‑run mode**: see what *would* happen without touching your mail

---

## Architecture

```
┌───────────────┐      poll (1 min)
│   systemd     │────────────────┐
└──────┬────────┘                │
       │ ExecStart               │  Google API
┌──────▼────────┐   HTTP+OAuth   │
│  gmail_poll   │──────────────▶│ Gmail
│   daemon      │                │
└──────┬────────┘ <──────────────┘
       │ writes
┌──────▼────────┐    JSON log
│ local_cache   │───────────▶ Vector ➜ Loki ➜ Grafana
└───────────────┘
```

---

## Installation

### 1. Clone & install

```bash
git clone https://github.com/Oberon01/gmail_poll.git
cd gmail_poll
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Create a Google Cloud App

1. Go to [https://console.cloud.google.com/apis/credentials](https://console.cloud.google.com/apis/credentials)
2. **Create OAuth Client ID → Desktop App**
3. Download `credentials.json` into `~/.config/gmail_poll/`

### 3. Configure

Create `.env` (or systemd EnvironmentFile) with:

```ini
# .env
gmail_poll_LABEL_REVIEW="@Action/Review"
gmail_poll_POLL_INTERVAL=60          # seconds
gmail_poll_CACHE_PATH="/var/lib/gmail_poll/cache.db"
```

(Optional) tweak `config.yaml` to modify model threshold, rules, or labels.

### 4. First‑run authentication

```bash
python -m gmail_poll --auth
```

A browser will open; grant access once. Token is stored & auto‑refreshes.

### 5. Run

```bash
python -m gmail_poll --daemon          # foreground
# or install as service
sudo cp deploy/gmail_poll.service /etc/systemd/system/
sudo systemctl enable --now gmail_poll
```

---

## Usage

| Command                      | Description                               |
| ---------------------------- | ----------------------------------------- |
| `--auth`                     | Perform one‑time OAuth handshake          |
| `--once`                     | Process inbox once then exit              |
| `--daemon`                   | Start continuous polling loop             |
| `--dry-run`                  | Log planned actions without mutating mail |
| `--rules path/to/rules.yaml` | Load additional static routing rules      |

---

## Roadmap

* [ ] Plug‑in sentiment model hot‑swap (OpenAI, local LLM, spaCy)
* [ ] Web UI dashboard (FastAPI + React) to tweak rules live
* [ ] Multi‑account support (G‑suite + personal)
* [ ] Export daily triage metrics → Obsidian vault integration

---

## Contributing

PRs are welcome! Please:

1. Create a feature branch
2. Run `pre-commit run --all-files`
3. Submit your PR

---

## 🪪 License

`gmail_poll` is released under the MIT License. See [LICENSE](LICENSE) for details.


## Quick start

```bash
pip install -r requirements.txt
python gmail_poll.py init   # writes .env and rules.yaml in current dir
python gmail_poll.py --once --dry-run  # test once without changes
python gmail_poll.py --daemon          # run continuously
```

List available Gmail labels and IDs:

```bash
python gmail_poll.py labels
```

Config via `.env`:

```
LABEL_ID_REVIEW=Review
POLL_INTERVAL=600
GMAIL_POLL_CACHE=~/.cache/gmail_poll/cache.db
GSA_LOG_LEVEL=INFO
```
