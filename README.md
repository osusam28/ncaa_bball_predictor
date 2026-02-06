# Case Study: Building an NCAA Predictor with an AI Coding Agent

This document traces the evolution of the "NCAA Predictor" project, demonstrating a collaborative "Pair Programming" workflow between a human (the User) and an AI Coding Agent (Antigravity).

---

## 🚀 The Initial Spark
**User**: "I want to create a system that helps me predict NCAA basketball games. I want it to use quantitative data from BartTorvik and my own qualitative notes."

**Agent's First Steps**:
1.  **Requirement Clarification**: Asked the user about storage (Markdown vs Database) and preferred data sources.
2.  **Infrastructure Setup**: Established a directory structure:
    - `/data/raw/` for JSON.
    - `/data/teams/` for Markdown "Team Documents".
    - `/src/` for the logic.

---

## 🛠️ Phase 1: The Quantitative Pipeline
The first goal was to turn raw stats into readable files.

1.  **The Fetcher**: Created `src/torvik_fetcher.py` to pull JSON from BartTorvik.
2.  **The Generator**: Created `src/team_doc_generator.py` to convert JSON into Markdown tables.
    - *Lesson*: By using Markdown, the data became "human-editable," allowing the user (and the agent) to easily see and modify team profiles.

---

## 🧠 Phase 2: Adding "Human" Insights
A predictor is only as good as its unique info. The system needed to "read" the user's notes.

1.  **Note Ingestion**: Created `src/note_ingester.py`.
2.  **The "Zags" Problem**: Teams often have nicknames (e.g., "UNC", "Zags"). 
    - *Agent's Solution*: Implemented `data/config/synonyms.json` to map nicknames to official names.
3.  **The Reviewer**: When a name wasn't recognized, the agent built `src/resolve_unprocessed.py`—an interactive script that asks the user to define new synonyms on the fly.

---

## 🔮 Phase 3: The Prediction Engine
With data and notes ready, we built the actual "Brain."

1.  **Agent Workflow**: Defined the `/predict` command.
2.  **Multimodal Analysis**:
    - **Step 1**: The Agent scrapes the web for real-time news (injuries, win streaks).
    - **Step 2**: The Agent reads the local Markdown docs (Stats + User Notes).
    - **Step 3**: The LLM synthesizes everything into a "Medium Detailed Report."

---

## 📈 Phase 4: Closing the Loop (Evaluation)
To ensure the system gets better, we needed a feedback loop.

1.  **The `/evaluate` Command**: After a game, the user asks the agent to check the results.
2.  **Learning Logic**: 
    - If the prediction was "Significantly Off" (Margin Error >= 10), the agent does a deep dive into *why*.
    - It provides **Passive Suggestions** (e.g., "We missed the turnover battle, consider adding that metric").

---

## 💾 Phase 5: Persistent Memory
A key breakthrough in the conversation: **"I want the qualitative field to be the 'memory' of the system."**

1.  **Write-Back Feature**: We updated the `/predict` workflow. Now, after every prediction, the Agent automatically *saves its web findings* back into the `Qualitative Notes` section of the team document.
2.  **Result**: Every time you use the system, it gets smarter.

---

## ⌨️ Phase 6: Operational UX (Slash Commands)
To make the codebase professional, we abstracted the scripts into simple commands:

| Command | Action |
| :--- | :--- |
| `/predict TeamA vs TeamB` | Scrapes, Analyzes, and Predicts. |
| `/update` | Full data refresh + Note ingestion. |
| `/note TeamName "Text"` | Adds a quick thought directly to a team doc. |
| `/evaluate Matchup` | Compares prediction to actual result. |

---

## 💡 Key Learning Points for Students

1.  **Iterative Engineering**: We didn't build the whole thing at once. We built a fetcher, then a log, then a brain, then a memory.
2.  **Data as Documentation**: Using Markdown files for team data allows both the Human and the AI to use the file system as a "shared whiteboard."
3.  **Nickname Resolution**: Real-world data is messy. Building a synonym layer is essential for mapping informal human language to rigid data schemas.
4.  **Agentic Workflows**: Instead of just running scripts, we defined *Workflows* that let the AI handle multi-step processes (Scrape → Read → Synthesis → Save).

---

## 🎓 Phase 7: The Learning System

The next evolution: **"How do we learn from our mistakes without over-indexing on single games?"**

### The Problem
After evaluating predictions, we had valuable insights scattered in evaluation files. But:
- How do we capture them systematically?
- How do we avoid biasing on single games? (e.g., "Kentucky came back once" ≠ "Kentucky is a comeback team")

### The Design Discussion

**User Insight**: *"If a team has a big comeback to win a game, don't automatically mark that team as great at comebacks. Make a note, but require more evidence before making it definitive."*

This led to a **3-Tier Learning Architecture**:

| Tier | What | Where | Example |
|------|------|-------|---------|
| **1** | Team/Player Insights | `data/teams/{Team}.md` | "Otega Oweh: bounce-back performer" |
| **2** | Metrics to Prioritize | `data/memory/metrics_priority.md` | "Weight paint points higher" |
| **3** | Global Prediction Lessons | `data/memory/prediction_lessons.md` | "Conference games = reduce margin predictions" |

### Evidence Thresholds

To prevent single-game bias, we implemented confidence tiers:

| Observations | Confidence | Label | How to Use |
|-------------|------------|-------|------------|
| 1 game | Low | `[OBSERVATION]` | Note for context only |
| 2-3 games | Medium | `[TENDENCY]` | Mention with caveats |
| 4+ games | High | `[PATTERN]` | Reliable, factor into predictions |

**Example progression:**
```
2026-01-31: [OBSERVATION] Showed resilience, rallied from 10 down.
2026-02-05: [TENDENCY] Now 2-for-2 in comeback situations.
2026-02-15: [PATTERN] 4 consecutive comeback wins—treat as reliable.
```

### Workflow Separation

We deliberately separated two workflows:
- **`/evaluate`**: Creates detailed evaluations in `evaluations/`. Stays focused on one game.
- **`/learn`**: Periodically consolidates insights across ALL evaluations into the memory tiers.

This separation allows:
1. Evaluations to be thorough without worrying about persistence
2. Learning to apply cross-game pattern matching
3. Clear audit trail (evaluations are marked `<!-- LEARNED -->` after processing)

### The "Quantitative vs Qualitative" Discussion

**User Question**: *"Will the update workflow capture the new metrics?"*

**Answer**: No—and that's intentional.

| Type | Captured By | Storage |
|------|-------------|---------|
| **Automated Stats** | `/update` → BartTorvik API | Team doc frontmatter |
| **Priority Metrics** | `/predict` → Web search | Prediction report only |
| **Learned Insights** | `/learn` → Evaluation review | Team doc qualitative section |

We considered enhancing the fetcher to pull more stats (like paint points, rebounding), but decided:
- Many priority metrics aren't in the standard BartTorvik JSON
- Web research during `/predict` is more flexible
- This keeps the system lightweight

---

## 📋 Current Slash Commands

| Command | Action |
| :--- | :--- |
| `/predict TeamA vs TeamB` | Scrapes, Analyzes, and Predicts. |
| `/update` | Full data refresh + Note ingestion. |
| `/note TeamName "Text"` | Adds a quick thought directly to a team doc. |
| `/evaluate Matchup` | Compares prediction to actual result. |
| `/learn` | **NEW**: Consolidates learnings from evaluations into memory. |

---

## 🔑 Additional Learning Points (from Phase 7)

5. **Evidence Thresholds**: Don't let a single data point become a "rule." Require multiple observations before treating insights as reliable patterns.
6. **Separation of Concerns**: Evaluation (one game) and Learning (cross-game patterns) are different activities. Keep them separate.
7. **Confidence Labels**: Explicitly mark the reliability of insights (`[OBSERVATION]` vs `[PATTERN]`). This helps future users (and agents) know how much to trust an insight.
8. **Lightweight over Automated**: Sometimes it's better to research on-demand (web search during `/predict`) than to build complex automated data pipelines for metrics you rarely need.
9. **Audit Trails**: Using markers like `<!-- LEARNED -->` creates a clear record of what's been processed, preventing duplicate work.

---

## 🔬 Phase 8: Metric Refinement (The Four Factors) ("The Grail")

The User realized that "Resume" metrics (WAB, SOS) were confusing the prediction model. A team can have a great resume but be a "paper tiger." We needed the **Four Factors** (eFG%, TOV%, ORB%, FTR) to see the *actual* quality of play.

1.  **The Data Gap**: The standard JSON feed didn't have these specific advanced stats.
2.  **The Scraper Solution**:
    *   We built a **Browser-Based Scraper** to bypass API limits and extract the full 24-column dataset for all 365 teams.
    *   **Resiliency**: Implemented a "Bot Protection Fallback" in `src/torvik_fetcher.py`. If the script gets blocked, it pauses and provides a link for the user to manually download the CSV, ensuring the pipeline never breaks.
3.  **The "Scientific Spread"**:
    *   We split the Team Doc into **Predictive Profile** (Four Factors + Efficiency) and **Resume Profile** (WAB + Record).
    *   **New Logic**: "Use Four Factors to set the score. Use WAB only to break ties in close games."

4.  **Key Lesson**: **Data Source Agility**. When the easy API fails, use a scraper. When the scraper gets blocked, build a human-in-the-loop fallback. Don't let a blocked request stop the entire workflow.

