
---
description: Evaluate a prediction against actual results.
---

1. Find the Prediction File
    - Search `predictions/` for files matching `{{matchup}}`.
    - Read the prediction file to extract:
        - **Predicted Winner**
        - **Predicted Score** (e.g., "Kansas 78 - BYU 74")
        - **Predicted Margin** (calculated from score)

2. Get Actual Game Result
    - Web search: `{{matchup}} final score basketball 2026`
    - Extract **Actual Winner** and **Actual Score**.

3. Calculate Accuracy
    - `Predicted Margin = Predicted Winner Score - Predicted Loser Score`
    - `Actual Margin = Actual Winner Score - Actual Loser Score`
    - `Margin Error = |Predicted Margin - Actual Margin|`
    - `Correct Winner? = (Predicted Winner == Actual Winner)`

4. Evaluate
    - **Accurate Prediction**: `Margin Error < 10` AND `Correct Winner`.
        - Log as "Good prediction".
    - **Significantly Off**: `Margin Error >= 10` OR `Wrong Winner`.
        - Perform deeper web search for game recap/analysis.
        - Identify factors that were missed (injuries, hot shooting, turnovers, etc.).
        - Suggest improvements (passively):
            - "Consider adding turnover rate to team docs"
            - "Weight recent form higher"
            - etc.

5. Save Evaluation
    - Use `write_to_file` to save to `evaluations/YYYY-MM-DD_{TeamA}_vs_{TeamB}_eval.md`.
    - Include:
        - Prediction Summary
        - Actual Result
        - Margin Error
        - Analysis (if significantly off)
        - Improvement Suggestions (if applicable)
