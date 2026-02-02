
---
description: Consolidate learnings from evaluations into persistent memory (team docs, metrics, lessons).
---

## Evidence Thresholds

> [!IMPORTANT]
> **Avoid over-indexing on single games.** Use these confidence tiers:

| Observations | Confidence | Label Format | Action |
|-------------|------------|--------------|--------|
| 1 game | Low | `[OBSERVATION]` | Note it, don't treat as pattern |
| 2-3 games | Medium | `[TENDENCY]` | Mention in predictions with caveats |
| 4+ games | High | `[PATTERN]` | Treat as reliable insight |

**Examples:**
- ❌ Wrong: "Kentucky is great at comebacks" (1 game)
- ✅ Right: "[OBSERVATION] Kentucky showed resilience, rallying from 10 down vs Arkansas (2026-01-31)"
- ✅ Right: "[PATTERN] Kentucky has now won 4 straight bounce-back games after losses"

---

## Workflow Steps

1. Read All Unprocessed Evaluations
    - Scan `evaluations/` for all `*_eval.md` files.
    - **Skip** any file containing `<!-- LEARNED -->` (already processed).
    - For each unprocessed evaluation, extract:
        - Teams involved
        - Player-specific insights (from "Analysis" or "What Happened" sections)
        - Team tendencies discovered
        - Suggested metrics (from "Improvement Suggestions")
        - Generalizable lessons (patterns that apply beyond this game)

2. Summarize Learnings
    - Group insights by team for Tier 1 (team docs).
    - Compile metrics suggestions for Tier 2 (`data/memory/metrics_priority.md`).
    - Identify patterns/lessons that apply globally for Tier 3 (`data/memory/prediction_lessons.md`).
    - **Apply evidence thresholds**: Check existing team docs for prior observations before upgrading confidence.
    - Present a summary to the user before persisting.

3. Update Team Documents (Tier 1)
    - For EACH team with new insights:
        - Open `data/teams/{Team}.md`
        - Check for existing observations about the same trait
        - **If new observation matches existing one**: Upgrade from `[OBSERVATION]` → `[TENDENCY]` → `[PATTERN]`
        - **If first observation**: Add with `[OBSERVATION]` prefix
        - Include date attribution in format: `(YYYY-MM-DD)`
    - Example format:
      ```markdown
      ### Player Insights
      - **Otega Oweh**: [OBSERVATION] Bounce-back performance after loss—24 pts at Arkansas after 25-pt defeat. (2026-01-31)
      
      ### Team Tendencies
      - [OBSERVATION] Showed resilience coming back from early deficit vs Arkansas. (2026-01-31)
      - [TENDENCY] Dangerous after blowout losses—2nd straight bounce-back win. (2026-02-05)
      - [PATTERN] 4 consecutive bounce-back wins after losses > 15pts. (2026-02-15)
      ```

4. Update Metrics Priority (Tier 2)
    - Read `data/memory/metrics_priority.md`.
    - Add new metrics suggestions to appropriate priority tier.
    - Avoid duplicates—if metric already exists, update the source/reason if new info is more compelling.

5. Update Prediction Lessons (Tier 3)
    - Read `data/memory/prediction_lessons.md`.
    - Add new generalizable lessons with source attribution.
    - **Only add as definitive lesson if supported by 2+ games** (otherwise note as observation).
    - Group under appropriate category (Situational Factors, Pre-Game Checks, Margin Calibration).
    - Use GitHub alert syntax (NOTE/TIP/IMPORTANT/WARNING/CAUTION) for emphasis.

6. Mark Evaluations as Processed
    - For EACH evaluation file that was processed:
        - Append `<!-- LEARNED -->` marker at the END of the file.
    - This prevents reprocessing on future `/learn` runs.
