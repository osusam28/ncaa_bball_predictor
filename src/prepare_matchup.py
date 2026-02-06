
import sys
import os
import json
import re

DATA_RAW_DIR = "data/raw"
DATA_TEAMS_DIR = "data/teams"
SYNONYM_PATH = "data/config/synonyms.json"
YEAR = 2026

def load_team_map():
    # 1. Load Official Names from CSV Scrape
    data_path = os.path.join(DATA_RAW_DIR, f"team_stats_{YEAR}.csv")
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found.")
        return {}
    
    team_map = {}
    import csv
    with open(data_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row: continue
            name = row[0] # Team is index 0 in our CSV
            safe_name = name.replace(" ", "_").replace("/", "-")
            team_map[name.lower()] = f"{safe_name}.md" # Key by lowercase for easier matching
        
    # 2. Layer on Synonyms
    if os.path.exists(SYNONYM_PATH):
        with open(SYNONYM_PATH, 'r') as f:
            synonyms = json.load(f)
            for nick, official in synonyms.items():
                if official.lower() in team_map:
                    team_map[nick.lower()] = team_map[official.lower()]
    
    return team_map

def get_team_content(query_name, team_map):
    query_u = query_name.lower().strip()
    
    # Exact match check
    if query_u in team_map:
        filename = team_map[query_u]
        filepath = os.path.join(DATA_TEAMS_DIR, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return f.read()
    
    # Fuzzy/Contains check if exact fails
    # This might be dangerous if queries are short, but useful for "State" vs "Ohio State" if careful.
    # For now, let's stick to strict map matching to avoid "Iowa" matching "Iowa State".
    
    return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 src/prepare_matchup.py 'Team A vs Team B'")
        sys.exit(1)
        
    matchup_str = " ".join(sys.argv[1:])
    
    # Heuristic split by "vs" or "vs."
    parts = re.split(r'\s+vs\.?\s+', matchup_str, flags=re.IGNORECASE)
    
    if len(parts) != 2:
        print(f"Error: Could not parse matchup '{matchup_str}'. Use format 'Team A vs Team B'.")
        sys.exit(1)
        
    team1_query = parts[0].strip()
    team2_query = parts[1].strip()
    
    print(f"Resolving: '{team1_query}' and '{team2_query}'...\n")
    
    team_map = load_team_map()
    
    content1 = get_team_content(team1_query, team_map)
    content2 = get_team_content(team2_query, team_map)
    
    if not content1:
        print(f"❌ Could not find team: {team1_query}")
    if not content2:
        print(f"❌ Could not find team: {team2_query}")
        
    if not content1 or not content2:
        print("\nTry using exact official names or adding synonyms in data/config/synonyms.json")
        sys.exit(1)
        
    print(f"✅ Found data for both teams.\n")
    print("="*40)
    print(f"CONTEXT FOR LLM ANALYSIS")
    print("="*40)
    print("\n")
    print(f"--- DATA FOR {team1_query.upper()} ---")
    print(content1)
    print("\n")
    print("-" * 40)
    print("\n")
    print(f"--- DATA FOR {team2_query.upper()} ---")
    print(content2)
    print("\n")
    print("="*40)

if __name__ == "__main__":
    main()
