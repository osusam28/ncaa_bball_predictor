
import csv
import os

DATA_RAW_DIR = "data/raw"
DATA_TEAMS_DIR = "data/teams"
YEAR = 2026

# CSV Indices (Based on our custom scrape)
# Team,AdjOE,AdjDE,EFG,EFGD,TOR,TORD,ORB,DRB,FTR,FTRD,WAB
IDX_TEAM = 0
IDX_ADJOE = 1
IDX_ADJDE = 2
IDX_EFG = 3
IDX_EFGD = 4
IDX_TOR = 5
IDX_TORD = 6
IDX_ORB = 7
IDX_DRB = 8
IDX_FTR = 9
IDX_FTRD = 10
IDX_WAB = 11

def load_raw_data():
    filename = f"team_stats_{YEAR}.csv"
    filepath = os.path.join(DATA_RAW_DIR, filename)
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}. Run torvik_fetcher/scraper first.")
        return []
        
    data = []
    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row: continue
            data.append(row)
    return data

def generate_markdown(team_data):
    # Unpack
    name = team_data[IDX_TEAM]
    adj_oe = team_data[IDX_ADJOE]
    adj_de = team_data[IDX_ADJDE]
    wab = team_data[IDX_WAB]
    
    # Four Factors
    efg = team_data[IDX_EFG]
    efgd = team_data[IDX_EFGD]
    tor = team_data[IDX_TOR]
    tord = team_data[IDX_TORD]
    orb = team_data[IDX_ORB]
    drb = team_data[IDX_DRB] # Opp ORB % (Defensive Rebounding quality is inverse of this)
    ftr = team_data[IDX_FTR]
    ftrd = team_data[IDX_FTRD]

    # Frontmatter
    frontmatter = f"""---
team: {name}
conf: N/A
year: {YEAR}
adj_oe: {adj_oe}
adj_de: {adj_de}
barthag: N/A
wab: {wab}
---"""

    # Stats Tables
    stats_body = f"""
# {name} ({YEAR})

## Predictive Profile (Four Factors)
*Use these metrics to predict the game spread and flow.*

| Category | Metric | Offense | Defense |
| :--- | :--- | :--- | :--- |
| **Efficiency** | Adj. Efficiency | {adj_oe} | {adj_de} |
| **Shooting** | Effective FG% | {efg}% | {efgd}% |
| **Ball Security** | Turnover Rate | {tor}% | {tord}% |
| **Rebounding** | Off. Rebound % | {orb}% | {drb}% |
| **Free Throws** | Free Throw Rate | {ftr} | {ftrd} |

## Resume Profile (Context Only)
*Non-predictive metrics. Use only to judge "clutch" factor or proven record.*

| Metric | Value |
| :--- | :--- |
| **Wins Above Bubble** | {wab} |
| **Record** | (Check Web) |

"""
    return frontmatter + stats_body

def update_team_file(team_data):
    name = team_data[IDX_TEAM]
    safe_name = name.replace(" ", "_").replace("/", "-")
    filepath = os.path.join(DATA_TEAMS_DIR, f"{safe_name}.md")
    
    new_content_top = generate_markdown(team_data)
    
    existing_notes = ""
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            content = f.read()
            parts = content.split("## Qualitative Notes")
            if len(parts) > 1:
                existing_notes = parts[1]
    
    full_content = new_content_top + "\n## Qualitative Notes" + existing_notes
    
    with open(filepath, 'w') as f:
        f.write(full_content)

def main():
    if not os.path.exists(DATA_TEAMS_DIR):
        os.makedirs(DATA_TEAMS_DIR)
        
    data = load_raw_data()
    print(f"Generating docs for {len(data)} teams...")
    
    for team in data:
        update_team_file(team)
        
    print("Done.")

if __name__ == "__main__":
    main()
