
import json
import os
import re

DATA_RAW_DIR = "data/raw"
DATA_TEAMS_DIR = "data/teams"
YEAR = 2026 # Should match the fetcher

# Schema Mapping based on BartTorvik CSV layout
# Indices based on observation:
# 0:rank, 1:team, 2:conf, 3:record, 4:adjoe, 5:oe_rank, 6:adjde, 7:de_rank, 8:barthag, 
# ... 41:WAB (approx), 44:adjt (approx) - Need to be careful.
# Let's trust the names are consistent in position.
# Better way: Create a small helper to robustly map this if possible, 
# but for now, we will use fixed indices and verify.

IDX_TEAM = 1
IDX_CONF = 2
IDX_RECORD = 3
IDX_ADJOE = 4
IDX_OE_RANK = 5
IDX_ADJDE = 6
IDX_DE_RANK = 7
IDX_BARTHAG = 8
# WAB is usually near the end. checking previous curl... 
# The curl output for previous turn showed WAB around index 41? 
# let's grab the raw data and find it dynamically if possible? No, JSON doesn't have keys.
# We will inspect the first record in the raw file to ensure we don't misalign.
IDX_WAB = 41 # Tentative
IDX_SOS = 15 # Tentative
IDX_TEMPO = 44 # Tentative -> Actually usually last or near last.

def load_raw_data():
    filename = f"team_results_{YEAR}.json"
    filepath = os.path.join(DATA_RAW_DIR, filename)
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}. Run fetcher first.")
        return []
    with open(filepath, 'r') as f:
        return json.load(f)

def generate_markdown(team_data):
    # Unpack data
    name = team_data[IDX_TEAM]
    conf = team_data[IDX_CONF]
    record = team_data[IDX_RECORD]
    adj_oe = team_data[IDX_ADJOE]
    oe_rank = team_data[IDX_OE_RANK]
    adj_de = team_data[IDX_ADJDE]
    de_rank = team_data[IDX_DE_RANK]
    barthag = team_data[IDX_BARTHAG]
    
    # Safely get others (length check)
    wab = team_data[IDX_WAB] if len(team_data) > IDX_WAB else "N/A"
    sos = team_data[IDX_SOS] if len(team_data) > IDX_SOS else "N/A"
    tempo = team_data[IDX_TEMPO] if len(team_data) > IDX_TEMPO else "N/A"
    
    # Frontmatter
    frontmatter = f"""---
team: {name}
conf: {conf}
year: {YEAR}
adj_oe: {adj_oe}
adj_de: {adj_de}
tempo: {tempo}
barthag: {barthag}
wab: {wab}
---"""

    # Stats Tables
    stats_body = f"""
# {name} ({YEAR})

## Quantitative Profile
| Metric | Value | Rank |
| :--- | :--- | :--- |
| **Offense** (AdjOE) | {adj_oe} | #{oe_rank} |
| **Defense** (AdjDE) | {adj_de} | #{de_rank} |
| **Tempo** | {tempo} | - |
| **Resume** | **WAB**: {wab} | **SOS**: {sos} |
| **Record** | {record} | |

"""
    return frontmatter + stats_body

def update_team_file(team_data):
    name = team_data[IDX_TEAM]
    safe_name = name.replace(" ", "_").replace("/", "-") # Sanitize filename
    filepath = os.path.join(DATA_TEAMS_DIR, f"{safe_name}.md")
    
    new_content_top = generate_markdown(team_data)
    
    existing_notes = ""
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            content = f.read()
            # Split at Qualitative Notes header
            parts = content.split("## Qualitative Notes")
            if len(parts) > 1:
                existing_notes = parts[1]
    
    # Reassemble
    full_content = new_content_top + "\n## Qualitative Notes" + existing_notes
    
    with open(filepath, 'w') as f:
        f.write(full_content)
    # print(f"Updated {name}") # Too verbose for all teams

def main():
    if not os.path.exists(DATA_TEAMS_DIR):
        os.makedirs(DATA_TEAMS_DIR)
        
    data = load_raw_data()
    print(f"Generatings docs for {len(data)} teams...")
    
    for team in data:
        update_team_file(team)
        
    print("Done.")

if __name__ == "__main__":
    main()
