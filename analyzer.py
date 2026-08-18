from collections import Counter
from datetime import datetime
from parser import parse_log_file

def top_status_codes(records, top_n=10):
    """
    Counts occurences of each HTTP status code in and returns the most common ones.
    """
    counter = Counter(r['status'] for r in records)
    return counter.most_common(top_n)

def busiest_hours(records, top_n=10):
    """
    Extracts the hour (0-23) from each timestamp and counts the number of requests per hour, returning the busiest hours.
    """
    counter = Counter()

    for r in records:
        dt = datetime.strptime(r["timestamp"].split()[0], "%d/%b/%Y:%H:%M:%S")
        counter[dt.hour] += 1

    return counter.most_common(top_n)

def print_report(records):
    print("=" * 50)
    print("TOP STATUS CODES")
    print("=" * 50)
    for status, count in top_status_codes(records):
        print(f" {status}: {count} requests")

    print()
    print("=" * 50)
    print("BUSIEST HOURS (24-hour format)")
    print("=" * 50)
    for hour, count in busiest_hours(records):
        print(f" {hour:02d}:00 - {count} requests")

if __name__ == "__main__":
    records = parse_log_file("data/access.log")
    print_report(records)