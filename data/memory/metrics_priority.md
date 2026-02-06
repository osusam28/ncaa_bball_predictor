# Metrics Priority Guide

Tracks which quantitative metrics should be prioritized based on evaluation feedback.

---

## Predictive Metrics (The "Scientific Spread")
*These metrics set the base expectation for the game score.*

| Metric | Priority | Impact |
|--------|--------|--------|
| **Adj Efficiency** (OE/DE) | **Critical** | Sets the baseline strength (Talent Adjusted). |
| **Effective FG%** (Target/Allowed) | **High** | Primary driver of offensive success. |
| **Turnover Rate** (Tor/Def) | **High** | Critical for possession volume control. |
| **Offensive Rebounding** (ORB%) | **High** | Second-chance points generator. |
| **Free Throw Rate** (FTR) | **Medium** | Can swing close games, dependent on officiating. |

---

## Resume Metrics (The "Contextual Adjustment")
*Do NOT use these to predict the score. Use them to predict the WINNER in close games.*

| Metric | Role | When to Use |
|--------|-------------|--------|
| **Wins Above Bubble (WAB)** | Tie-Breaker | Use when spread is < 3 points. Trust the high-WAB team. |
| **Record** | Context | Ignore for prediction. High record w/ low efficiency = "Luck". |
| **SOS** | Calibration | Already baked into AdjOE/DE. Use only to spot "battle-tested" teams. |

---

## Qualitative Adjustments (The "Human Element")
*Apply these shifts AFTER the model sets the spread.*

| Factor | Shift Magnitude | Example |
|--------|--------|--------|
| **Star Injury** | 3-5 Points | Key scorer out (e.g., Kansas w/o Dickinson). |
| **Home Court** | 2-4 Points | "Phog Allen Fieldhouse" effect. |
| **Revenge/Motivation** | 1-2 Points | Lost previous matchup; fighting for bubble. |

---

## Metrics TO ADD (Not Currently Tracked)

| Metric | Why | Priority |
|--------|-----|----------|
| Individual Defensive Assignments | Fland shut down opposing PG (8 steals) | Medium |
| Bench Scoring Depth | Drop-off when stars are out is non-linear | Medium |
| Tempo Trends (Last 5 Games) | BYU/Kansas went way over predicted total | Low |
