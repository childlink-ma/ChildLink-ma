# Contributing to ChildLink-MA Assistant

Thank you for your interest. ChildLink-MA is a nonprofit, open-source initiative.
All contributions must align with our ethical and clinical quality standards.

---

## Who We Welcome

- Pediatricians, neurologists, psychologists, and neurodevelopment specialists
- AI/ML engineers focused on responsible, ethical AI
- Translators (our 6 target languages: EN · FR · AR · ES · PT · SW)
- Accessibility and UX experts
- Parents and educators with lived experience

---

## How to Contribute

### 1. Clinical guidelines (data/)

Only peer-reviewed or nationally recognized guidelines are accepted (NICE, HAS, CDC, AAP, WHO, DSM-5).
Open an Issue with the source reference before submitting.

### 2. Code contributions

```bash
# Fork the repo, then:
git checkout -b feature/your-feature-name
# Make your changes
git commit -m "feat: short description"
git push origin feature/your-feature-name
# Open a Pull Request against main
```

### 3. Bug reports

Use GitHub Issues. Include: steps to reproduce, expected behavior, actual behavior, environment.

---

## Code Standards

- Python: PEP 8, type hints encouraged
- No secrets or API keys in code or commits
- All new endpoints must have a test in `tests/`
- GDPR: no logging of raw questions or IP addresses (hashed IPs only)

---

## Clinical Content Standards

- Every claim must be traceable to a source in `data/`
- No diagnostic statements
- No content that could replace professional consultation
- Sources cited as `[Org, Year]` format only

---

## Contact

📩 admin@childlink-ma.org
🌐 childlink-ma.org
