# Security Policy

**Project:** Gmail Sentiment Analyzer (GSA)  
**Version:** v0.9.0-beta  
**Last updated:** 2025-08-12

## Supported versions
Security fixes are provided for the latest beta/stable release tags (e.g., `v0.9.x-*` and the most recent `v1.x.y` once available).

## Reporting a vulnerability
Please **do not** file public GitHub issues for security reports.

Use **GitHub Security Advisories** to report privately:
1. Go to the repository on GitHub.
2. Click **Security** → **Advisories** → **Report a vulnerability**.
3. Provide steps to reproduce, environment details, and potential impact.

If Security Advisories are unavailable in your fork, you may email the maintainer privately (replace with your contact):
- **Security contact:** _[add your email or contact form link]_  

We aim to acknowledge within **72 hours** and provide a remediation plan or fix timeline within **7 days**.

## Handling sensitive data
- GSA stores OAuth tokens and logs locally. Do **not** attach these files to public issues.
- Redact message IDs, addresses, or subjects when sharing logs.

## Hardening recommendations (users)
- Use a dedicated machine user or separate Google account where appropriate.
- Ensure OS-level protections: user account isolation, disk encryption, and regular updates.
- Keep `credentials.json` and `token.pickle` outside of version control.
