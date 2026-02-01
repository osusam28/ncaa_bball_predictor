
import os
import json
import shutil
import glob

UNPROCESSED_DIR = "raw_notes/unprocessed"
RAW_NOTES_DIR = "raw_notes"
SYNONYM_PATH = "data/config/synonyms.json"

def load_synonyms():
    if os.path.exists(SYNONYM_PATH):
        with open(SYNONYM_PATH, 'r') as f:
            return json.load(f)
    return {}

def save_synonyms(data):
    with open(SYNONYM_PATH, 'w') as f:
        json.dump(data, f, indent=4)
        print("Updated synonyms.json.")

def main():
    if not os.path.exists(UNPROCESSED_DIR):
        print("No unprocessed folder found.")
        return

    files = glob.glob(os.path.join(UNPROCESSED_DIR, "*.txt"))
    if not files:
        print("No unprocessed notes found.")
        return

    print(f"Found {len(files)} unprocessed notes.")
    synonyms = load_synonyms()
    
    for filepath in files:
        filename = os.path.basename(filepath)
        with open(filepath, 'r') as f:
            content = f.read().strip()
            
        print(f"\n--- Note: {filename} ---")
        print(f"Content: \"{content}\"")
        
        print("\nOptions:")
        print("1. Add a synonym mapping (e.g. 'Hoos' -> 'Virginia')")
        print("2. Skip")
        print("3. Delete note")
        
        choice = input("Select (1/2/3): ").strip()
        
        if choice == '1':
            nickname = input("Enter the term/nickname used in the note: ").strip()
            official = input("Enter the Official Team Name (e.g. Virginia): ").strip()
            
            if nickname and official:
                synonyms[nickname] = official
                save_synonyms(synonyms)
                
                # Move back to raw_notes for reprocessing
                shutil.move(filepath, os.path.join(RAW_NOTES_DIR, filename))
                print(f"Moved {filename} back to queue for processing.")
            else:
                print("Invalid input. Skipping.")
                
        elif choice == '3':
            os.remove(filepath)
            print("Deleted.")
        else:
            print("Skipped.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
