# Privacy Policy

**Project:** Gmail Sentiment Analyzer (GSA)  
**Version:** v0.9.0-beta  
**Last updated:** 2025-08-12

GSA runs locally on your machine. It does not send your data to any server other than Google’s Gmail API endpoints that you explicitly authorize via OAuth.

## What data is processed
- **Email metadata:** sender, recipients, subject, Gmail label IDs.
- **Email content:** snippet and/or body text used for local classification.
- **Rules:** `rules.yaml` may contain email addresses or domains you add.
- **Logs:** local operational logs (`gsa.log`) with message IDs and actions.

## What is stored locally
- **OAuth tokens:** `token.pickle` (refresh/access tokens for Gmail).
- **Credentials:** `credentials.json` (OAuth client secret you provide).
- **Cache:** SQLite DB storing processed Gmail message IDs.
- **Configuration:** `.env`, `rules.yaml`, and logs in your working directory.

> GSA does **not** collect telemetry or transmit analytics to the authors.

## Third parties and scopes
- **Google Gmail API** with scope: `https://www.googleapis.com/auth/gmail.modify`
- All Gmail requests are performed under your OAuth consent and identity.

## Retention and control
- You control all local files (logs, cache, tokens, rules).  
- Remove or rotate:
  - Delete `gsa.log` for logs.
  - Delete the cache DB to reprocess messages in dry-run.
  - Delete `token.pickle` to revoke the local session (you’ll re-auth on next run).
  - Regenerate `credentials.json` as needed.

## Security of local data
- Files are stored in plain form on your machine. Rely on OS permissions and full-disk encryption where appropriate.
- **Recommendation:** keep repo private or ensure you never commit `credentials.json` / `token.pickle` / cache DB.

## Contact
- Open an issue for general questions or feedback.
- For sensitive security/privacy reports, follow the instructions in `SECURITY.md`.
