
# NCAA Predictor Agent Guide

This document outlines the operational procedures for the NCAA Predictor system.

## System Overview
The system aggregates quantitative data from BartTorvik and qualitative user notes into markdown-based "Team Documents". It also features a "Smart Prediction Engine" that combines this data with real-time web analysis.

**Project Root**: `/Users/samuelhall/Documents/ncaa_predictor`

## Common Operations

### 1. Predict a Game (Smart Workflow)
**Context**: To generate a comprehensive AI analysis of a matchup, including web research.
**Action**:
```bash
/predict TeamA vs TeamB
```
**Process**:
1.  **Auto-Update**: Runs the pipeline to fetch the latest BartTorvik stats.
2.  **Scrape**: The Agent searches the web for recent analysis/injuries.
3.  **Synthesize**: Combines Web Insights + Local Stats + Local Notes.
4.  **Save**: Generates a report and saves it to `predictions/YYYY-MM-DD_{Matchup}.md`.
5.  **Memory**: Key insights are written back to each team's document for future use.

### 2. Evaluate a Prediction
**Context**: After a game is played, compare your prediction to the actual result.
**Action**:
```bash
/evaluate TeamA vs TeamB
```
**Process**:
1.  **Find Prediction**: Searches `predictions/` for the matching file.
2.  **Get Actual**: Searches the web for the final score.
3.  **Compare**: Calculates margin error and winner accuracy.
4.  **Analyze**: If significantly off (margin error >= 10), performs a deep dive.
5.  **Save**: Writes evaluation to `evaluations/YYYY-MM-DD_{Matchup}_eval.md`.

### 3. Run Full Update Pipeline (Manual)
**Context**: Run this if you just added new notes manually and want to process them without generating a prediction.
**Action**:
```bash
/update
```
**What it does**:
- Fetches latest stats from BartTorvik.
- Refreshes Team Markdown files with new stats.
- Ingests any new notes from `raw_notes/` into the Team Documents.

### 3. Handle Unprocessed Notes
**Context**: If notes contain nicknames or abbreviations the system doesn't know, they are moved to `raw_notes/unprocessed/`.
**Action**:
```bash
python3 src/resolve_unprocessed.py
```
**Interactive Mode**:
The script shows you the unknown note and asks you to define a mapping (e.g., "Zags" -> "Gonzaga"). It then auto-moves the note back to the queue for processing.

### 4. Add a Quick Note to a Team
**Context**: You have an insight about a specific team (e.g., after watching a game).
**Action**:
```bash
/note TeamName "Your insight here"
```
**Example**:
```bash
/note Nebraska "Interior defense looks dominant with Mast healthy"
```
**Result**: The note is appended to `data/teams/Nebraska.md` under `## Qualitative Notes`.

### 5. Add Notes via Drop Folder (Alternative)
**Action**:
1. Create a text file in `raw_notes/` (e.g., `raw_notes/game_recap.txt`).
2. Write your notes plain text. Mention team names (e.g., "Duke", "UConn") or known nicknames.
3. Run the pipeline (Method 2) or a Prediction (Method 1).

### 6. Consolidate Learnings
**Context**: Periodically process evaluation files to extract and persist learnings.
**Action**:
```bash
/learn
```
**Process**:
1.  **Scan**: Reads all unprocessed evaluations (those without `<!-- LEARNED -->` marker).
2.  **Extract**: Pulls player insights, team tendencies, metrics suggestions, and global lessons.
3.  **Persist**: Updates team docs (Tier 1), `metrics_priority.md` (Tier 2), and `prediction_lessons.md` (Tier 3).
4.  **Mark**: Adds `<!-- LEARNED -->` to processed evaluation files.

---

## Learning System

The system learns from prediction evaluations through three tiers:

### How It Works
```
/evaluate → evaluations/*.md → /learn → persistent memory → /predict
```
1. `/evaluate` creates evaluation files with embedded insights in `evaluations/`
2. `/learn` periodically consolidates those insights into persistent memory
3. `/predict` consults the memory when generating new predictions

### Tier 1: Team/Player Insights
**Location**: `data/teams/{Team}.md` under `### Player Insights` and `### Team Tendencies`

Stores player-specific performances (ceiling games, defensive matchups) and team-level patterns (bounce-back behavior, road resilience).

### Tier 2: Metrics Priorities  
**Location**: `data/memory/metrics_priority.md`

Tracks which quantitative metrics should be weighted higher or lower based on evaluation feedback (e.g., "Paint Points Per Game" is high priority).

### Tier 3: Prediction Lessons
**Location**: `data/memory/prediction_lessons.md`

Global rules and situational checks that apply to all predictions (e.g., "Apply 20% parity modifier to SEC games").

---

## Component-Level Operations

### Fetch Data Only
Refreshes `data/raw/team_results_{YEAR}.json`.
```bash
python3 src/torvik_fetcher.py
```

### Regenerate Docs Only
Updates the Markdown stats tables in `data/teams/` without fetching new web data. Preserves existing notes.
```bash
python3 src/team_doc_generator.py
```

### Process Notes Only
Scans `raw_notes/`, matches team names, appends to docs, and cleans up files.
```bash
python3 src/note_ingester.py
```

### Prepare Matchup Context
Use this if you just want to see the raw data for two teams without generating a full prediction.
```bash
python3 src/prepare_matchup.py "Team A vs Team B"
```

## Directory Structure
- `src/`: Python source code.
- `data/raw/`: Raw JSON fetched from BartTorvik.
- `data/teams/`: Generated Markdown files per team (The main output).
- `data/memory/`: Persistent learning artifacts (metrics priorities, prediction lessons).
- `raw_notes/`: Drop folder for unprocessed notes.
- `predictions/`: Archive of generated prediction reports.
- `evaluations/`: Archive of prediction evaluations.

## Configuration
- `data/config/synonyms.json`: Maps nicknames to official team names.

