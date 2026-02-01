
import requests
import json
import os
import datetime

# Configuration
DATA_DIR = "data/raw"
YEAR = datetime.datetime.now().year 
# Logic to handle "early season" if needed (e.g. in Nov/Dec, use current year+1)
# For now, default to current calendar year but allow override.
# In Jan 2026 -> 2026 season. In Nov 2025 -> 2026 season.
current_month = datetime.datetime.now().month
if current_month > 10:
    YEAR += 1

URL_TEAM_RESULTS = f"https://barttorvik.com/{YEAR}_team_results.json"
URL_ADVANCED_STATS = f"https://barttorvik.com/getadvstats.php?year={YEAR}&csv=1" # Returns CSV, might need parsing or just raw save.

def fetch_json(url, filename):
    print(f"Fetching from {url}...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        # Parse standard JSON response
        data = response.json()
        
        filepath = os.path.join(DATA_DIR, filename)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Saved {len(data)} records to {filepath}")
        return data
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def main():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        
    print(f"--- BartTorvik Fetcher for Season {YEAR} ---")
    
    # Fetch Core Team Results (Efficiency, W-L, etc.)
    fetch_json(URL_TEAM_RESULTS, f"team_results_{YEAR}.json")
    
    # Additional fetches can be added here (e.g. player stats)
    
if __name__ == "__main__":
    main()
