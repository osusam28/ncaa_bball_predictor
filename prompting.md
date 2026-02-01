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
