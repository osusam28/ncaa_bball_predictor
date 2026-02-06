# Evaluation of NCAA Prediction Process

## Executive Summary
**Current Status:** B- (Solid Foundation, Missing Detail)
**Verdict:** Your current process uses **highly correlated "Result" metrics** (Adjusted Efficiency, WAB) but lacks the **"Causal" metrics** (Four Factors) that explain *how* those results happen. You are effectively predicting games based on "who is better overall" rather than "how do they match up style-wise."

A "Significantly Off" prediction like Kansas vs Texas Tech often happens because top-level efficiency metrics hide fatal flaws (e.g., turnover proneness, reliance on 3-point variance) that get exposed tactical matchups.

---

## 1. What You Are Doing Well (The Foundation)
You are using the "Big Three" of predictive signals. These are excellent and should remain the core of your model:
-   **Adjusted Efficiency (AdjOE/AdjDE):** This is the single most predictive metric in college basketball. It normalizes for pace and opponent, which is critical.
-   **Tempo:** Crucial for setting the "Total" and understanding variance (fewer possessions = higher variance).
-   **Wins Above Bubble (WAB):** An excellent resume metric for determining "proven" quality vs "inflated" records.

## 2. What Is Missing (The "Blind Spots")
The following metrics are the "DNA" of basketball efficiency. They are currently **missing** from your `teams/*.md` files and prediction logic, yet they correlate highly with winning, especially in the NCAA Tournament.

### A. The "Four Factors" (Critical Gaps)
Dean Oliver’s Four Factors are the standard for component-based prediction.
1.  **Effective Field Goal % (eFG%)**: The most important factor (40% weight). You are treating all "120 AdjOE" teams as equal, but a team that gets there via dunks/layups is more consistent than one relying on 40% 3PT shooting.
2.  **Turnover Rate (TOV%)**: (25% weight). **Major Miss.** High-pressure defenses (like Houston/Iowa State types) wreak havoc on high-turnover offenses, even if the offense is "efficient" against average teams.
3.  **Offensive Rebounding % (ORB%)**: (20% weight). "Possession Volume" indicator. Teams that shoot poorly but rebound 35%+ of misses (like Purdue/UNC often do) have a high floor.
4.  **Free Throw Rate (FTR)**: (15% weight). Indicates ability to generate "free" points and put opponents in foul trouble.

### B. Variance Indicators
-   **3-Point Reliance (3PA/FGA):** Teams that take 45%+ of shots from 3 (like Alabama often does) are high-variance. They can beat #1 or lose to #100. Your model currently treats them the same as balanced teams.
-   **Home/Away Splits:** "The Lubbock Factor" you noted manually is backed by data. Some teams are 10 points worse on the road. Your model currently uses a flat home court advantage (implied), but specific home/road efficiency splits are better.

---

## 3. Data Availability Check
**Good News:** You are *already downloading* this data.
Your `src/torvik_fetcher.py` saves a massive JSON file (`team_results_2026.json`) that contains ~46 data points per team. Your `src/team_doc_generator.py` currently only reads indices 4, 6, 41, 44 (Efficiency, WAB, Tempo).
The "Four Factors" are almost certainly sitting in indices 10-40 of that file, waiting to be mapped.

## 4. Recommendations
1.  **Map the Raw Data:** Update `team_doc_generator.py` to extract eFG%, TOV%, ORB%, and FTR.
2.  **Update Team Docs:** Display these in the `teams/{Team}.md` files so your LLM context sees them.
3.  **Refine "Prediction Lessons":**
    *   *Old:* "Check for injuries."
    *   *New:* "Check if High Turnover Offense vs High Steal Defense." (e.g., If TOV% > 20% and DefTOV% > 22%, predict a blowout loss for the offense).

**Would you like me to create an Implementation Plan to map these new metrics and add them to your pipeline?**
