
import os
import json
import shutil
import glob

RAW_NOTES_DIR = "raw_notes"
UNPROCESSED_DIR = "raw_notes/unprocessed"
DATA_TEAMS_DIR = "data/teams"
DATA_RAW_DIR = "data/raw"
YEAR = 2026

def load_team_map():
    # Returns a map of "Team Name" -> "Filename"
    # Or just a list of valid team names
    data_path = os.path.join(DATA_RAW_DIR, f"team_results_{YEAR}.json")
    if not os.path.exists(data_path):
        return {}
    
    with open(data_path, 'r') as f:
        data = json.load(f)
        
    # JSON schema: index 1 is Team Name
    # We want to match "Duke" -> "Duke.md"
    # But filenames are sanitized. So we reconstruct the filename logic.
    team_map = {}
    for row in data:
        name = row[1]
        safe_name = name.replace(" ", "_").replace("/", "-")
        team_map[name] = f"{safe_name}.md"
        
    return team_map

def process_notes():
    if not os.path.exists(UNPROCESSED_DIR):
        os.makedirs(UNPROCESSED_DIR)

    team_map = load_team_map()
    note_files = glob.glob(os.path.join(RAW_NOTES_DIR, "*.txt"))
    
    print(f"Found {len(note_files)} note files to process.")
    
    
    # Load Synonyms from JSON
    SYNONYM_MAP = {}
    synonym_path = "data/config/synonyms.json"
    if os.path.exists(synonym_path):
        with open(synonym_path, 'r') as f:
            SYNONYM_MAP = json.load(f)
    else:
        print("Warning: data/config/synonyms.json not found.")

    for note_path in note_files:
        with open(note_path, 'r') as f:
            content = f.read()
            
        # Entity Resolution (Enhanced)
        matched_teams = set() # Use set to avoid duplicates
        
        # 1. Check Exact Matches
        sorted_names = sorted(team_map.keys(), key=len, reverse=True)
        for name in sorted_names:
            if name in content:
                matched_teams.add(name)
                
        # 2. Check Synonyms
        for nickname, official_name in SYNONYM_MAP.items():
            if nickname in content:
                # Use word boundary check or naive check? Naive for now, but careful with short abbr.
                # "TAM" is safe. "A&M" is safe.
                if official_name in team_map:
                    matched_teams.add(official_name)
        
        if matched_teams:
            print(f"Matched {len(matched_teams)} teams in {os.path.basename(note_path)}: {list(matched_teams)}")
            # Append to each matched team
            for team_name in matched_teams:
                filename = team_map[team_name]
                filepath = os.path.join(DATA_TEAMS_DIR, filename)
                
                if os.path.exists(filepath):
                    with open(filepath, 'a') as f: # Append mode
                        f.write(f"\n\n### Note ({os.path.basename(note_path)})\n")
                        f.write(content.strip() + "\n")
                else:
                    print(f"Warning: Team file {filename} not found despite match.")
            
            # Delete processed file
            os.remove(note_path)
            print(f"Processed and deleted: {note_path}")
            
        else:
            print(f"No match found for {note_path}. Moving to unprocessed.")
            shutil.move(note_path, os.path.join(UNPROCESSED_DIR, os.path.basename(note_path)))

if __name__ == "__main__":
    process_notes()
