# OneClickAllResultsBot

A small Python/BeautifulSoup project that demonstrates how a semester-specific RMLAU result page can be requested and parsed for basic result information.

> **Project history:** originally built in November 2024. Code and documentation refreshed in August 2026 to improve error handling, reproducibility, and project context. The target university page is external and may change independently of this repository.

## What it demonstrates

- HTTP requests with `requests`
- Base64 encoding of the roll-number query value expected by the legacy portal
- HTML parsing with BeautifulSoup
- Defensive handling of changed/missing page structures
- Sequential processing with a delay rather than concurrent scraping

## Important use note

Result pages contain personal academic information. Use this project only for records you are authorized to access, respect the university portal's terms and rate limits, and do not use it to collect or republish student data without an appropriate basis.

## Current scope

The URL template in the script points to the historical RMLAU BCA Semester 3 result path used when this project was created. If the university changes its host, semester path, query parameters, or HTML structure, update `RESULT_URL_TEMPLATE` and the parser selectors before use.

## Setup

```bash
git clone https://github.com/chandanpandeys/OneClickAllResultsBot.git
cd OneClickAllResultsBot
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python OneClickAllResultBot.py
```

The program asks for:

1. the first roll number, and
2. the number of students in the small authorized range you want to check.

Requests are performed sequentially with a short delay. There is intentionally no concurrency or bulk-export feature.

## Improvements in the 2026 refresh

- Fixed an unsafe parser check that could access the 10th table cell without first confirming it existed
- Added request timeout and HTTP-error handling
- Reused a `requests.Session`
- Added basic input validation
- Added a `__main__` guard so the module can be imported safely
- Added a conservative delay between sequential requests
- Added the missing `requirements.txt`
- Corrected setup instructions to reference the actual script name

## Limitations

- Portal-specific and semester-specific
- Relies on HTML selectors owned by an external website
- Does not attempt CAPTCHA/authentication bypasses
- Does not guarantee current portal compatibility

## Status

**Legacy educational scraper / maintenance mode.** Useful as a compact parsing and defensive-request example; not presented as a production data-collection service.
