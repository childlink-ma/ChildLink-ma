# Security Policy

## Supported Versions

| Version | Supported |
|---|---|
| v0.4.x (current) | ✅ |
| v0.3.x | ⚠️ security fixes only |
| < v0.3 | ❌ |

## Reporting a Vulnerability

**Do not open a public GitHub Issue for security vulnerabilities.**

Email: admin@childlink-ma.org
Subject: `[SECURITY] ChildLink-assistant — <brief description>`

We will respond within 72 hours and coordinate a fix before any public disclosure.

## Security Design

- Hashed IPs only (SHA-256, 12-char prefix) — raw IPs never logged
- Rate limiting: 3 requests/day/IP by default
- No user accounts, no personal data stored
- Azure DPA signed (francecentral region)
- CORS restricted to declared origins only
- API key required for non-origin requests
- FAISS index and metadata excluded from version control
