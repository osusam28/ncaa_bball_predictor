
---
description: Add a quick note to a team's document.
---

1. Resolve Team Name
    - Parse the command for `{{team}}` and `{{note}}`.
    - Resolve the team name using `data/config/synonyms.json` if needed.
    - Determine the target file: `data/teams/{TeamName}.md`
        - Use underscores for spaces (e.g., "Texas A&M" -> "Texas_A&M.md").

2. Read Existing File
    - Read the content of `data/teams/{TeamName}.md`.

3. Append Note
    - Add the following to the END of the file:
      ```
      ### User Note (YYYY-MM-DD)
      {{note}}
      ```
    - Use `write_to_file` with Overwrite=true (write full content with note appended).

4. Confirm
    - Tell the user: "Added note to {TeamName}."
