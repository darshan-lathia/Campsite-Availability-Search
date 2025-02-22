import subprocess
import argparse
import time
from datetime import datetime

def run_camping_wrapper(args):
    """
    Runs camping_wrapper.py with the given arguments and returns the output.
    """
    command = [
        "python", "camping_wrapper.py",
        "--start-date", args.start_date,
        "--end-date", args.end_date,
        "--parks", *args.parks,
        "--nights", str(args.nights),
        "--show-campsite-info"
    ]

    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Error running camping_wrapper.py: {result.stderr}")
    
    return result.stdout

def parse_results(output):
    """
    Parses the output of camping_wrapper.py to create a structured result.
    Returns a dictionary of sections (priority, regular, ignored) with their date ranges and site counts.
    """
    results = {"priority": {}, "regular": {}, "ignored": {}}
    lines = output.splitlines()
    current_section = None

    for line in lines:
        if "**Priority Results:**" in line:
            current_section = "priority"
        elif "**Regular Results:**" in line:
            current_section = "regular"
        elif "**Ignored Results:**" in line:
            current_section = "ignored"
        elif current_section and " --> " in line:
            date_range, site_info = line.split(" --> ")
            site_count = int(site_info.split(" site(s)")[0].strip())
            results[current_section][date_range] = site_count

    return results

def filter_results_by_type(results, types):
    """
    Filters results by the specified types (priority, regular, ignored).
    """
    filtered_results = {}
    for result_type in types:
        filtered_results.update(results.get(result_type, {}))
    return filtered_results

def detect_changes(old_results, new_results):
    """
    Detects changes between the old and new results.
    Returns a list of changes and a boolean indicating if changes occurred.
    """
    changes = []
    all_keys = set(old_results.keys()).union(new_results.keys())

    for key in all_keys:
        old_count = old_results.get(key, 0)
        new_count = new_results.get(key, 0)

        if old_count == 0 and new_count > 0:
            changes.append(f"🟢 New availability: {key} --> {new_count} site(s) available")
        elif old_count > 0 and new_count == 0:
            changes.append(f"🔴 No longer available: {key}")

    return changes, bool(changes)

def camping_notification(args):
    """
    Main function to run camping_wrapper.py periodically and detect changes.
    """
    if args.frequency == 0:
        print("Running one-time check...")
    else:
        print(f"Starting camping notifications with frequency: {args.frequency} minute(s)")
    
    print(f"Filtering results: {', '.join(args.filters)}")

    try:
        print(f"\n[{datetime.now()}] Checking campsite availability...")
        try:
            output = run_camping_wrapper(args)
            parsed_results = parse_results(output)
            filtered_results = filter_results_by_type(parsed_results, args.filters)

            print("\n=== Full Results for Reference ===")
            print(output)

            # If frequency is 0, exit immediately after printing results
            if args.frequency == 0:
                return

        except RuntimeError as e:
            print(f"Error: {e}")
            if args.frequency == 0:
                return
            print("Skipping this check. Retaining previous results for future comparisons.")

        # Only continue with loop if frequency > 0
        if args.frequency > 0:
            old_results = filtered_results
            while True:
                time.sleep(args.frequency * 60)
                try:
                    output = run_camping_wrapper(args)
                    parsed_results = parse_results(output)
                    filtered_results = filter_results_by_type(parsed_results, args.filters)

                    changes, has_changes = detect_changes(old_results, filtered_results)
                    if has_changes:
                        print("\n=== Changes Detected ===")
                        for change in changes:
                            print(change)

                    print("\n=== Full Results for Reference ===")
                    print(output)

                    old_results = filtered_results

                except RuntimeError as e:
                    print(f"Error: {e}")
                    print("Skipping this check. Retaining previous results for future comparisons.")

    except KeyboardInterrupt:
        print("\nExiting. Goodbye!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Camping Notification Wrapper")
    parser.add_argument("--start-date", required=True, help="Start date in YYYY-MM-DD format")
    parser.add_argument("--end-date", required=True, help="End date in YYYY-MM-DD format")
    parser.add_argument("--parks", required=True, nargs="+", help="List of park IDs")
    parser.add_argument("--nights", type=int, required=True, help="Minimum number of nights required")
    parser.add_argument("--frequency", type=int, default=30, help="Frequency to check in minutes (default: 30, 0 for one-time check)")
    parser.add_argument(
        "--filters",
        nargs="+",
        choices=["priority", "regular", "ignored"],
        default=["priority", "regular", "ignored"],
        help="Specify which result types to include in changes detected (default: all types)."
    )

    args = parser.parse_args()

    camping_notification(args)

