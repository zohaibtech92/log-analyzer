import argparse
import csv
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

def top_ips(records, top_n=10):
    """
    Counts how many requests came from each IP address and return the most frequent ones. Useful for spotting bots/scrapers or your heaviesr traffic sources.
    """
    counter = Counter(r["ip"] for r in records)
    return counter.most_common(top_n)

def top_urls(records, top_n=10):
    """
    Counts how many times each requested path (URL) was hit and returns the most popular ones. Useful for understanding what content actually gets traffic.
    """
    counter = Counter(r["path"] for r in records)
    return counter.most_common(top_n)

def save_text_report(records, filepath="report.txt", top_n=10):
    """
    Writes the full analysis report to a plain text file, same content as what prints to the terminal.
    """
    with open(filepath, "w") as f:
        f.write("=" * 50 + "\n")
        f.write("TOP STATUS CODES\n")
        f.write("=" * 50 + "\n")
        for status, count in top_status_codes(records, top_n):
            f.write(f" {status}: {count} requests\n")

        f.write("\n" + "=" * 50 + "\n")
        f.write("BUSIEST HOURS (24-hour format)\n")
        f.write("=" * 50 + "\n")
        for hour, count in busiest_hours(records, top_n):
            f.write(f" {hour:02d}:00 - {count} requests\n")

        f.write("\n" + "=" * 50 + "\n")
        f.write(f"TOP {top_n} IP ADDRESSES\n")
        f.write("=" * 50 + "\n")
        for ip, count in top_ips(records, top_n):
            f.write(f" {ip}: {count} requests\n")

        f.write("\n" + "=" * 50 + "\n")
        f.write(f"TOP {top_n} REQUESTED URLS\n")
        f.write("=" * 50 + "\n")
        for url, count in top_urls(records, top_n):
            f.write(f" {url}: {count} requests\n")

    print(f"Text report saved to {filepath}")

def save_csv_report(records, filepath="report.csv", top_n=10):
    """
    Writes each analysis section to a single CSV file, with a 'category' column so all four sections coexist in one file.
    """
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["category", "key", "count"])

        for status, count in top_status_codes(records, top_n):
            writer.writerow(["status_code", status, count])

        for hour, count in busiest_hours(records, top_n):
            writer.writerow(["busiest_hour", f"{hour:02d}:00", count])

        for ip, count in top_ips(records, top_n):
            writer.writerow(["top_ip", ip, count])

        for url, count in top_urls(records, top_n):
            writer.writerow(["top_url", url, count])

    print(f"CSV report saved to {filepath}")

def print_report(records, top_n=10):
    print("=" * 50)
    print("TOP STATUS CODES")
    print("=" * 50)
    for status, count in top_status_codes(records, top_n):
        print(f"  {status}: {count} requests")

    print()
    print("=" * 50)
    print("BUSIEST HOURS (24-hour format)")
    print("=" * 50)
    for hour, count in busiest_hours(records, top_n):
        print(f"  {hour:02d}:00 - {count} requests")

    print()
    print("=" * 50)
    print(f"TOP {top_n} IP ADDRESSES")
    print("=" * 50)
    for ip, count in top_ips(records, top_n):
        print(f"  {ip}: {count} requests")

    print()
    print("=" * 50)
    print(f"TOP {top_n} REQUESTED URLS")
    print("=" * 50)
    for url, count in top_urls(records, top_n):
        print(f"  {url}: {count} requests")

def parse_args():
    """
    Defines and parses command-line arguments for the script.
    """
    parser = argparse.ArgumentParser(
        description="Analyze an Apache access log file: top status codes, "
                     "busiest hours, top IPs, and top URLs."
    )
    parser.add_argument(
        "--file",
        default="data/access.log",
        help="Path to the log file to analyze (default: data/access.log)"
    )
    parser.add_argument(
        "--top",
        type=int,
        default=10,
        help="Number of top results to show per category (default: 10)"
    )
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Skip saving report.txt and report.csv, only print to terminal"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    records = parse_log_file(args.file)
    print_report(records, top_n=args.top)

    if not args.no_save:
        save_text_report(records, top_n=args.top)
        save_csv_report(records, top_n=args.top)