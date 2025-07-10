import re

# Path to your ckpool log
log_path = "/home/ckpool/ckpool-solo/logs/ckpool.log"

# Regular expression to match bestshare line
bestshare_pattern = r'bestshare":\s*(\d+)'

def extract_latest_bestshare(log_file):
    bestshare = None
    try:
        with open(log_file, "r") as f:
            for line in reversed(f.readlines()):
                match = re.search(bestshare_pattern, line)
                if match:
                    bestshare = int(match.group(1))
                    break
    except FileNotFoundError:
        print(f"Log file not found: {log_file}")
    except Exception as e:
        print(f"Error reading log file: {e}")

    return bestshare

if __name__ == "__main__":
    bestshare = extract_latest_bestshare(log_path)
    if bestshare is not None:
        print(f"Latest bestshare: {bestshare}")
    else:
        print("No bestshare found in log.")

