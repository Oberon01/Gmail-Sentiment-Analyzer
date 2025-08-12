# GSA v0.9.0-beta — Acceptance

## Environments
- [ ] Windows 11 (PowerShell)
- [ ] Ubuntu 22.04 (or WSL)

## Prep (both)
- [ ] Create a clean working folder (outside the repo).
- [ ] Place `credentials.json` in that folder.

## CLI path A (installed project)
- [ ] From repo root: `pip install -e .`
- [ ] In working folder:
  - [ ] `gsa init` (creates `.env`, `rules.yaml`)
  - [ ] `gsa labels` (shows names + IDs)
  - [ ] `gsa --once --dry-run` (prints per-message actions)
  - [ ] `gsa --once` (live)
    - [ ] Gmail shows: `label:starred newer_than:10m`
    - [ ] Gmail shows: `in:trash newer_than:10m`
    - [ ] Gmail shows: `label:Review newer_than:10m`
  - [ ] `gsa --daemon` with `POLL_INTERVAL=90` (observe startup + per-cycle logs)

## CLI path B (script only)
- [ ] Repo root: `pip install -r requirements.txt`
- [ ] Working folder:
  - [ ] `python /path/to/gmail_poll.py init`
  - [ ] `python /path/to/gmail_poll.py --once --dry-run`
  - [ ] `python /path/to/gmail_poll.py --once`

## Resilience
- [ ] Kill network mid-loop → process retries and recovers (no crash).
- [ ] Restart app → previously processed IDs are not reprocessed.
- [ ] Delete cache DB → dry-run reprints classifications for the same messages.

## Docker (optional acceptance)
- [ ] `docker run --rm -it -v "$PWD:/app" docker.io/oberon01/gsa:0.9.0-beta gsa --once --dry-run` (macOS/Linux)
- [ ] Windows PowerShell equivalent works.
- [ ] Daemon: `docker run -d --name gsa --restart=unless-stopped -v "$PWD:/app" docker.io/oberon01/gsa:0.9.0-beta gsa --daemon`

## Docs & surface
- [ ] README shows both paths (A/B) and correct Windows venv line.
- [ ] Repo “About” description + topics set.
- [ ] CHANGELOG/PRIVACY/SECURITY present and linked.

## Release plumbing
- [ ] Tagging `v0.9.0-beta.*` builds artifacts and uploads to **TestPyPI**.
- [ ] Docker job builds/pushes `docker.io/oberon01/gsa:<tag>` (if secrets set).
