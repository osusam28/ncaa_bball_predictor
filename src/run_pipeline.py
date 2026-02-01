
import os
import subprocess

def run_step(script_name):
    print(f"\n>>> Running {script_name}...")
    subprocess.run(["python3", f"src/{script_name}"], check=True)

def main():
    print("Starting NCAA Predictor Pipeline...")
    
    # 1. Fetch latest Stats
    run_step("torvik_fetcher.py")
    
    # 2. Update/Generate Team docs (updates stats, preserves notes)
    run_step("team_doc_generator.py")
    
    # 3. Ingest new user notes
    run_step("note_ingester.py")
    
    print("\nPipeline Complete!")

if __name__ == "__main__":
    main()
