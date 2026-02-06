
import re
import json
import sys
from bs4 import BeautifulSoup

INPUT_FILE = "data/raw/torvik_2026.html"
OUTPUT_FILE = "data/raw/team_stats_2026_scraped.json"

def clean_val(text):
    """Extracts the first number/value from a cell like '127.6 5' -> '127.6'"""
    if not text: return ""
    # Split by newlines or spaces if needed, but usually just taking the first token is enough
    # But names like "New Mexico St." have spaces.
    # Efficiency values have space + rank: "127.6 5"
    if re.search(r'\d+\.\d+\s+\d+', text):
       return text.split()[0]
    return text.strip()

def parse_html():
    print(f"Reading {INPUT_FILE}...")
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except FileNotFoundError:
        print(f"Error: {INPUT_FILE} not found. Run curl first.")
        sys.exit(1)

    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find the main table. Usually has class 'table' or similar.
    # We can look for a table with 'AdjOE' in the header.
    tables = soup.find_all('table')
    target_table = None
    
    for t in tables:
        if "AdjOE" in t.get_text():
            target_table = t
            break
            
    if not target_table:
        print("Error: Could not find stats table in HTML.")
        sys.exit(1)
        
    print("Found stats table. Parsing rows...")
    
    data = []
    # Identify Header Indices mapping (Manual based on Browser analysis)
    # 0:RK, 1:Team, 2:Conf, 3:G, 4:Rec, 5:AdjOE, 6:AdjDE, 7:Barthag, 8:EFG, 9:EFGD, 10:TOR, 11:TORD, 12:ORB, 13:DRB, 14:FTR, 15:FTRD
    
    # Skip header rows (thead)
    tbody = target_table.find('tbody')
    if tbody:
        rows = tbody.find_all('tr')
    else:
        rows = target_table.find_all('tr')
        
    for tr in rows:
        tds = tr.find_all('td')
        if not tds or len(tds) < 16:
            continue
            
        # Extract Team Name (can be messy with <a> tags)
        team_cell = tds[1]
        team_name = team_cell.get_text(strip=True).split('(')[0].strip() # Remove seed/record if appended
        # Remove trailing info if any
        if "\n" in team_name:
            team_name = team_name.split("\n")[0]
            
        row_data = {
            "Team": team_name,
            "Conf": clean_val(tds[2].get_text()),
            "AdjOE": clean_val(tds[5].get_text()),
            "AdjDE": clean_val(tds[6].get_text()),
            "EFG%": clean_val(tds[8].get_text()),
            "EFGD%": clean_val(tds[9].get_text()),
            "TOR": clean_val(tds[10].get_text()),
            "TORD": clean_val(tds[11].get_text()),
            "ORB": clean_val(tds[12].get_text()),
            "DRB": clean_val(tds[13].get_text()),
            "FTR": clean_val(tds[14].get_text()),
            "FTRD": clean_val(tds[15].get_text()),
            "WAB": clean_val(tds[23].get_text()) if len(tds) > 23 else "0.0",
            "AdjT": clean_val(tds[22].get_text()) if len(tds) > 22 else "65.0"
        }
        
        # Valid row check (Rank should be number)
        if tds[0].get_text(strip=True).isdigit():
            data.append(row_data)
            
    print(f"Parsed {len(data)} teams.")
    
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    parse_html()
