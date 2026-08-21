# Log File Analyzer

A terminal + Python project that parses Apache server access logs and answers
real questions like "what are the top error codes" and "what times get the
most traffic."

Built to practice core Linux terminal tools (grep, awk, sort, uniq) and
translate that same logic into a reusable Python parsing and analysis
workflow with a proper command-line interface.

## What This Project Does

1. Takes a raw Apache server access log (plain text file)
2. Explores it using Linux terminal commands (grep, awk)
3. Parses every log line into structured data using Python + regex
4. Analyzes the structured data to answer:
   - What are the most common HTTP status codes (200, 404, 500, etc.)?
   - What hours of the day get the most traffic?
   - Which IP addresses send the most requests?
   - Which URLs/pages are requested most often?
5. Saves the report to both a plain text file and a CSV file
6. Accepts command-line arguments so it can analyze any log file, not just
   the sample data

## Dataset

Sample Apache Combined Log Format data (10,000 requests), sourced from the
Elastic examples repo: https://github.com/elastic/examples

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
- analyzer.py         -> runs analysis, handles CLI args, saves reports
- README.md

## How to Run

Make sure Python 3 is installed, then from the project folder run:

python3 analyzer.py

This parses the log file and prints a report of top status codes, busiest
hours, top IPs, and top URLs directly to the terminal, then saves the same
report to report.txt and report.csv.

### Command-Line Options

python3 analyzer.py --file data/access.log   # analyze a specific log file
python3 analyzer.py --top 5                  # show top 5 results per category instead of 10
python3 analyzer.py --no-save                # print to terminal only, skip saving files
python3 analyzer.py --help                   # show all available options

## Development Environment Notes

This project was originally started in Windows PowerShell, but core Linux
tools (grep, awk, wc, touch, curl) don't exist there. The project was
migrated to run inside WSL (Windows Subsystem for Linux) with Ubuntu, so
all terminal commands behave exactly as they would on a real Linux server.

Project files live inside the Linux filesystem (~/log-analyzer), not the
Windows filesystem (C:\Users\...). Editing or running files through the
Windows-side path (\\wsl.localhost\...) caused real problems during
development (permission errors, unreliable terminal output) and is avoided
in favor of working directly inside the native Ubuntu terminal.

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
- Verified results matched the earlier terminal-only awk/sort/uniq output
  exactly, confirming the Python parsing logic was correct.
- Found 1 malformed line out of 10,000 (a truncated Googlebot user agent
  string missing its closing quote) that correctly fails the regex and
  gets skipped. Left as an intentionally-skipped edge case rather than
  loosening the regex, since a stricter regex correctly flags genuinely
  malformed data instead of silently mis-parsing it.

### Step 6: Top IPs & Top URLs
- Added top_ips() and top_urls(), using the same Counter-based
  "extract field -> count -> sort" pattern as status codes and busiest
  hours.
- Cross-checked both against raw awk/sort/uniq terminal commands to
  confirm the Python output matched exactly.

### Step 7: Save Reports to File
- Added save_text_report() and save_csv_report() to write the full
  analysis to report.txt and report.csv instead of only printing to
  the terminal.
- Fixed a typo bug (f.wirte instead of f.write).
- Added report.txt and report.csv to .gitignore since they're generated
  output, not source code.

### Step 8: Command-Line Interface & Final Polish
- Added argparse support: --file (analyze any log file), --top (control
  how many results per category), --no-save (terminal-only mode), and
  --help (auto-generated usage docs).
- Debugged a PermissionError caused by accessing WSL files through the
  Windows-side path (\\wsl.localhost\...) instead of the native Ubuntu
  terminal; fixed with sudo chown to restore correct file ownership.
- Fixed a bug where --top wasn't actually being passed through to the
  saved report files (report.txt/report.csv always showed top 10
  regardless of the --top value) - required threading the top_n
  parameter consistently through every report-generating function.

## Status

Complete. Core features working: terminal-based log exploration, regex
parsing, status code analysis, busiest-hour analysis, top IPs, top URLs,
text/CSV export, and a full command-line interface.

## Skills Demonstrated

- Linux terminal fluency: grep, awk, sort, uniq, wc
- Regular expressions for structured text parsing
- Python data processing (collections.Counter, datetime parsing)
- Building a command-line interface with argparse
- Translating terminal-based exploration into a reusable Python workflow
- Debugging real-world issues: malformed data, typos, file permissions,
  environment configuration (WSL vs native Windows)
