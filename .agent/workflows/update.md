
---
description: Run the NCAA Predictor Data Pipeline (Fetch Stats + Ingest Notes)
---

1. Run the main pipeline script from the project root
// turbo
python3 src/run_pipeline.py

2. If there are unprocessed notes, run the resolver
python3 src/resolve_unprocessed.py
