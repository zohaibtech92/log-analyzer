# Log File Analyzer

A terminal + Python project that parses Apache server access logs and answers
real questions like "what are the top error codes" and "what times get the
most traffic."

This project was built to practice core Linux terminal tools (grep, awk,
sort, uniq) and then translate that same logic into a proper, reusable
Python parsing and analysis workflow.

## What This Project Does

1. Takes a raw Apache server access log (plain text file)
2. Explores it using Linux terminal commands (grep, awk)
3. Parses every log line into structured data using Python + regex
4. Analyzes the structured data to answer:
   - What are the most common HTTP status codes (200, 404, 500, etc.)?
   - What hours of the day get the most traffic?

## Dataset

Sample Apache Combined Log Format data (10,000 real-world-style requests),
sourced from the Elastic examples repo:
https://github.com/elastic/examples

Each log line looks like this:

83.149.9.216 - - [17/May/2015:10:05:03 +0000] "GET /path/to/page HTTP/1.1" 200 203023 "http://referrer.com/" "Mozilla/5.0 ..."

Field breakdown:
- IP address of the client
- Timestamp of the request
- HTTP method, path, and protocol (e.g. GET /page HTTP/1.1)
- HTTP status code (200, 404, 500, etc.)
- Response size in bytes
- Referer URL
- User agent string

## Project Structure

log-analyzer/
- data/access.log   -> sample log data (10,000 lines)
- parser.py          -> parses raw log lines into structured Python records
- analyzer.py         -> runs analysis on parsed records (status codes, busiest hours)
- README.md

## How to Run

Make sure Python 3 is installed, then from the project folder run:

python3 analyzer.py

This will parse the log file and print a report of top status codes and
busiest hours directly to the terminal.

## Development Environment Notes

This project was originally started in Windows PowerShell, but core Linux
tools (grep, awk, wc, touch, curl) don't exist there. The project was
migrated to run inside WSL (Windows Subsystem for Linux) with Ubuntu, so
all terminal commands behave exactly as they would on a real Linux server.

Project files live inside the Linux filesystem (~/log-analyzer), not the
Windows filesystem (C:\Users\...), for correct and fast tool behavior.

## How It Was Built (Progress Log)

### Step 1-2: Project Setup
- Initialized a git repo and downloaded the sample Apache log dataset.
- Hit an early setup issue: ran commands in Windows PowerShell, where
  grep/awk/wc/touch/curl aren't available.
- Solved this by installing WSL (Ubuntu) and rebuilding the project inside
  the Linux filesystem (~/log-analyzer), separate from the Windows
  filesystem (C:\Users\...).
- Explored the raw log directly in the terminal before writing any code:
  - grep '" 404 ' data/access.log        -> find 404 errors
  - grep -E '" 5[0-9]{2} ' data/access.log -> find 5xx server errors
  - awk '{print $9}' data/access.log | sort | uniq -c | sort -rn
    -> quick terminal-only version of "top status codes"

### Step 3: Understanding the Log Format
- Broke down the Apache Combined Log Format field by field.
- Decided plain awk (space-splitting) isn't reliable for full parsing,
  since quoted fields like the user agent contain spaces.
- Designed a regex to properly extract each field while respecting quoted
  sections.

### Step 4: Python Parser (parser.py)
- Wrote parse_log_line() to apply the regex to a single line and return a
  structured dictionary (ip, timestamp, method, path, protocol, status,
  size, referer, user_agent).
- Wrote parse_log_file() to read the whole file, parse every line, and
  gracefully skip and count any lines that fail to match, instead of
  crashing.

### Step 5: Analysis (analyzer.py)
- Used Python's collections.Counter to count status code occurrences and
  find the busiest hours (extracted from each request's timestamp using
  datetime.strptime).
- Verified the results matched the earlier terminal-only awk/sort/uniq
  output exactly, confirming the Python parsing logic was correct.
- Found 1 malformed line out of 10,000 (a truncated Googlebot user agent
  string missing its closing quote) that correctly fails the regex and
  gets skipped. This was left as an intentionally-skipped edge case rather
  than loosening the regex, since a stricter regex correctly flags
  genuinely malformed data instead of silently mis-parsing it.

### Step 6: Top IPs & Top URLs
- Added top_ips() and top_urls() to analyzer.py, using the same
  Counter-based "extract field -> count -> sort" pattern as status codes
  and busiest hours.
- Cross-checked both against raw awk/sort/uniq terminal commands to
  confirm the Python output matched exactly.

## Status

In progress. Working: log exploration, parsing, status code analysis,
busiest-hour analysis. Coming next: a cleaner final report output.

## Skills Demonstrated

- Linux terminal fluency: grep, awk, sort, uniq, wc
- Regular expressions for structured text parsing
- Python data processing (collections.Counter, datetime parsing)
- Translating terminal-based exploration into a reusable Python workflow
- Debugging real-world malformed data instead of assuming clean input
