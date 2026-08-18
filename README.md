cat > README.md << 'EOF'
# Log File Analyzer

A terminal + Python project that parses Apache server access logs and answers
questions like "what are the top error codes" and "what times get the most traffic."

Built to practice Linux terminal tools (grep, awk) and translating that logic
into a proper Python parsing/analysis workflow.

## Dataset

Sample Apache Combined Log Format data (10,000 requests), sourced from the
Elastic examples repo: https://github.com/elastic/examples

## Project Structure

log-analyzer/
- data/access.log      -> sample log data
- parser.py             -> parses raw log lines into structured records
- README.md

## Progress Log

- Step 1-2: Set up project inside WSL (had to switch from Windows PowerShell,
  since grep/awk/wc aren't available there). Explored the log using
  grep, awk, sort, uniq -c to get quick answers directly in the terminal.
- Step 3-4: Designed a regex to parse the Apache Combined Log Format properly
  (needed instead of plain awk splitting, since quoted fields like the user agent
  string contain spaces). Wrote parser.py to turn raw log lines into structured
  Python dictionaries.

## How to Run

python3 parser.py

## Status

In progress - parsing works, analysis (top error codes, busiest hours) coming next.
EOF
