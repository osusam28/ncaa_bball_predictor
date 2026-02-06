
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
URL_ADVANCED_STATS = f"https://barttorvik.com/trank.php?year={YEAR}&csv=1" # Correct Team CSV Endpoint

def fetch_json(url, filename):
    print(f"Fetching from {url}...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
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
    
    # Fetch Advanced Stats (CSV with headers) to get Four Factors reliably
    print(f"Fetching CSV from {URL_ADVANCED_STATS}...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        r = requests.get(URL_ADVANCED_STATS, headers=headers)
        r.raise_for_status()
        
        # Check if we got a valid CSV (not HTML error page)
        if "<!DOCTYPE html>" in r.text or "Verifying your browser" in r.text:
            raise ValueError("Bot protection detected.")
            
        csv_path = os.path.join(DATA_DIR, f"team_stats_{YEAR}.csv")
        with open(csv_path, 'w') as f:
            f.write(r.text)
        print(f"Success! Saved CSV to {csv_path}")
        
    except Exception as e:
        print(f"\n[WARNING] Automatic CSV download failed: {e}")
        print(f"ACTION REQUIRED: Please visit this URL manually:")
        print(f"  {URL_ADVANCED_STATS}")
        print(f"Save the file as: data/raw/team_stats_{YEAR}.csv")
        print("Then run the pipeline again.\n")
        # Don't re-raise; allow pipeline to continue if data already exists
    
    # Additional fetches can be added here (e.g. player stats)
    
if __name__ == "__main__":
    main()
