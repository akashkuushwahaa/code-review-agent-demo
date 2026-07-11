# UserLookup (Demo Repo)

A deliberately tiny internal user-lookup service, built **only** to serve
as a test target for an automated PR security review agent. Not a real
product — don't deploy this anywhere.

## What's here

- `main` branch — a small, clean Flask app with a parameterized SQL query
  (i.e. no vulnerabilities, this is the "before" state)
- `feature/search-endpoint` branch — adds a search endpoint that
  introduces several intentional security issues, meant to be opened as
  a pull request against `main` so a security-review agent has something
  real to flag

## Running it

```bash
pip install -r requirements.txt
python app.py
```

## Purpose

This repo exists to demo a scoped, security-focused AI code review agent.
The `feature/search-endpoint` branch intentionally contains:

- A hardcoded API key
- A SQL injection vulnerability (string-concatenated query)
- Unsafe use of `eval()` on user input
- A command injection vulnerability (`os.system` with unsanitized input)
- A missing input validation check

These are present on purpose, for demo purposes only.
