
---
description: Predict the outcome of a game between two teams. Auto-updates stats, searches web for insights, and saves a report.
---

1. Auto-Update Data (Quantitative)
// turbo
python3 src/run_pipeline.py

2. Web Search for Qualitative Context ("The Scraper")
    - Perform a web search for: `{{matchup}} basketball prediction analysis 2026` (or current year).
    - Read the content of 1-3 top search results to gather insights on:
        - Recent momentum/injuries.
        - Matchup specific history.
        - Strategic advantages (e.g. "Size mismatch", "Guard play").
    - **REMEMBER** the 1-2 most important insights for EACH team for Step 5.

2.5 Consult Prediction Lessons (Memory)
    - Read `data/memory/prediction_lessons.md` and apply relevant situational checks:
        - **Bounce-back?** Is either team coming off a 15+ point loss?
        - **Conference game?** Apply parity modifier (~20% reduction to predicted margin).
        - **Injury concerns?** Verify active roster via web search if needed.
    - Read `data/memory/metrics_priority.md` to know which stats to emphasize in analysis.
    - Read team docs and **weight insights by confidence level**:
        - `[PATTERN]` = Reliable, factor into prediction
        - `[TENDENCY]` = Consider, mention with caveat
        - `[OBSERVATION]` = Note for context, don't rely on
    - **If files don't exist**, skip this step.

3. Load Local Data
// turbo
python3 src/prepare_matchup.py {{matchup}}

4. Generate & Save Report
    - Synthesize the **Web Insights** (from Step 2) with the **Local Stats/Notes** (from Step 3).
    - Create a "Medium Detailed Report" in Markdown format.
    - **CRITICAL**: Save the report to `predictions/` before displaying it.
        - Filename: `predictions/YYYY-MM-DD_{TeamA}_vs_{TeamB}.md` (Use today's date).
        - Use the `write_to_file` tool.
    - Display the content to the user after saving.

5. Write Back Team Memory (NEW)
    - For **EACH team** in the matchup, append 1-2 key web insights to their team document.
    - Target files: `data/teams/{TeamName}.md`
    - Append format (add to end of file):
      ```
      ### Web Insight (YYYY-MM-DD)
      - {Insight 1}
      - {Insight 2}
      ```
    - Use the `replace_file_content` tool to append (or read file, then write full content).
    - This builds a persistent "memory" for future predictions.
