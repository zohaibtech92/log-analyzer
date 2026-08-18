import re

LOG_PATTERN = re.compile(
    r'^(\S+) \S+ \S+ \[(.*?)\] "(\S+) (.*?) (\S+)" (\d+) (\S+) "(.*?)" "(.*?)"$'
)

def parse_log_line(line):
    """
    Takes one raw log line and return a dictionary of structured fields, or None if the line doesn't match the expected format.
    """
    match = LOG_PATTERN.match(line)
    if not match:
        return None

    ip, timestamp, method, path, protocol, status,size, referer, user_agent = match.groups()

    return {
        "ip": ip,
        "timestamp": timestamp,
        "method": method,
        "path": path,
        "protocol": protocol,
        "status": int(status),
        "size": size,
        "referer": referer,
        "user_agent": user_agent
    }

def parse_log_file(filepath):
    """
    Reads the file line by line and return a list of parsed records. Skips and counts any lines that fail to parse.
    """
    records = []
    failed = 0

    with open(filepath, "r") as f:
        for line in f:
            parsed = parse_log_line(line.strip())
            if parsed:
                records.append(parsed)
            else:
                failed += 1

    print(f"Parsed {len(records)} lines successfully, {failed} failed")
    return records

if __name__ == "__main__":
    logs = parse_log_file("data/access.log")

    print("\nSample parsed record:")
    print(logs[0])