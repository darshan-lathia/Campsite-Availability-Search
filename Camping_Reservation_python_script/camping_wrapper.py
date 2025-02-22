import subprocess
import argparse
from datetime import datetime, timedelta

def run_camping_script(args):
    # Prepare the command
    command = [
        "python", "camping.py",
        "--start-date", args.start_date,
        "--end-date", args.end_date,
        "--parks", *args.parks,
        "--nights", str(args.nights),
    ]
    if args.show_campsite_info:
        command.append("--show-campsite-info")
    
    # Run the script
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Error running camping.py: {result.stderr}")
    
    return result.stdout

def parse_camping_output(output):
    # Parse the output of camping.py
    parsed_data = {}
    lines = output.splitlines()
    current_park = None
    for line in lines:
        line = line.strip()
        if line.startswith("🏕"):
            park_info = line.split(":")[0]
            current_park = park_info.split("(")[0].strip()
            parsed_data[current_park] = {}
        elif line.startswith("* Site"):
            site_id = line.split()[2]
            parsed_data[current_park][site_id] = []
        elif line.startswith("* 202"):
            date_range = line.strip("* ").split(" -> ")
            parsed_data[current_park][site_id].append(tuple(date_range))
    return parsed_data

def filter_by_days(parsed_data, min_nights):
    priority_results = {}
    regular_results = {}
    ignored_results = {}

    for park, sites in parsed_data.items():
        park_priority = {}
        park_regular = {}
        park_ignored = {}
        for site_id, date_ranges in sites.items():
            for date_range in date_ranges:
                start_date = datetime.strptime(date_range[0], "%Y-%m-%d")
                end_date = datetime.strptime(date_range[1], "%Y-%m-%d")
                num_nights = (end_date - start_date).days

                range_key = format_date_range(date_range[0], date_range[1])

                if num_nights < min_nights:
                    continue

                # Logic for 1-night stays (no changes)
                if min_nights == 1:
                    if start_date.weekday() in [4, 5]:  # Friday or Saturday
                        if range_key not in park_priority:
                            park_priority[range_key] = 0
                        park_priority[range_key] += 1
                    elif start_date.weekday() in [3, 6]:  # Thursday or Sunday
                        if range_key not in park_regular:
                            park_regular[range_key] = 0
                        park_regular[range_key] += 1
                    else:
                        if range_key not in park_ignored:
                            park_ignored[range_key] = 0
                        park_ignored[range_key] += 1

                # Logic for 2-night stays (no changes)
                elif min_nights == 2:
                    if start_date.weekday() == 4 and (start_date + timedelta(days=1)).weekday() == 5:  # Fri and Sat
                        if range_key not in park_priority:
                            park_priority[range_key] = 0
                        park_priority[range_key] += 1
                    elif (
                        start_date.weekday() in [3, 4, 5, 6]
                        and end_date.weekday() in [5, 6, 0]
                    ):  # Thurs-Sun or ends on Mon
                        if range_key not in park_regular:
                            park_regular[range_key] = 0
                        park_regular[range_key] += 1
                    else:
                        if range_key not in park_ignored:
                            park_ignored[range_key] = 0
                        park_ignored[range_key] += 1

                # Logic for 3-night stays
                elif min_nights == 3:
                    if start_date.weekday() in [3, 4]:  # Thurs or Fri
                        if range_key not in park_priority:
                            park_priority[range_key] = 0
                        park_priority[range_key] += 1
                    else:
                        if range_key not in park_ignored:
                            park_ignored[range_key] = 0
                        park_ignored[range_key] += 1

                # Logic for 4-night stays
                elif min_nights == 4:
                    if start_date.weekday() == 3:  # Starts on Thurs
                        if range_key not in park_priority:
                            park_priority[range_key] = 0
                        park_priority[range_key] += 1
                    else:
                        if range_key not in park_ignored:
                            park_ignored[range_key] = 0
                        park_ignored[range_key] += 1

                # Logic for 5 or more nights (everything is priority)
                else:
                    if range_key not in park_priority:
                        park_priority[range_key] = 0
                    park_priority[range_key] += 1

        priority_results[park] = park_priority
        regular_results[park] = park_regular
        ignored_results[park] = park_ignored

    return priority_results, regular_results, ignored_results


def format_date_range(start, end):
    start_date = datetime.strptime(start, "%Y-%m-%d")
    end_date = datetime.strptime(end, "%Y-%m-%d")
    start_str = f"{start} ({start_date.strftime('%a')})"
    end_str = f"{end} ({end_date.strftime('%a')})"
    return f"{start_str} -> {end_str}"

def display_results(priority_results, regular_results, ignored_results):
    for park, date_ranges in priority_results.items():
        print(f"🏕 {park}")
        print("  **Priority Results:**")
        for date_range, site_count in date_ranges.items():
            print(f"  \033[1m{date_range} --> {site_count} site(s) available\033[0m")  # Bold text

    for park, date_ranges in regular_results.items():
        print(f"🏕 {park}")
        print("  **Regular Results:**")
        for date_range, site_count in date_ranges.items():
            print(f"  {date_range} --> {site_count} site(s) available")

    for park, date_ranges in ignored_results.items():
        print(f"🏕 {park}")
        print("  **Ignored Results:**")
        for date_range, site_count in date_ranges.items():
            print(f"  {date_range} --> {site_count} site(s) available")

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Wrapper for camping.py")
    parser.add_argument("--start-date", required=True, help="Start date in YYYY-MM-DD format")
    parser.add_argument("--end-date", required=True, help="End date in YYYY-MM-DD format")
    parser.add_argument("--parks", required=True, nargs="+", help="List of park IDs")
    parser.add_argument("--nights", type=int, required=True, help="Minimum number of nights required")
    parser.add_argument("--show-campsite-info", action="store_true", help="Show detailed campsite info")

    args = parser.parse_args()
    
    # Run camping.py and process its output
    try:
        output = run_camping_script(args)
        parsed_data = parse_camping_output(output)
        priority_results, regular_results, ignored_results = filter_by_days(parsed_data, args.nights)
        display_results(priority_results, regular_results, ignored_results)
    except Exception as e:
        print(f"Error: {e}")

