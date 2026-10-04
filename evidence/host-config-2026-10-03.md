# Host configuration and source snapshot — 2026-10-03

**Commands:**
```sh
hermes --version
hermes config get tools.tool_search
hermes config get memory.provider
git -C /home/hermes-pi/.hermes/hermes-agent rev-parse HEAD
git -C /home/hermes-pi/.hermes/hermes-agent status --short
git -C /home/hermes-pi/.hermes/hermes-agent log -1 --format='%H %cs %s'
```

**Observed output (secrets omitted; none were returned):**
```text
Hermes Agent v0.21.5+4699.g5f666db (2026.9.24) · upstream eb7e8620 · local 5f666db4 (+2 carried commits)
Install directory: /home/hermes-pi/.hermes/hermes-agent
Install method: git
Python: 3.14.7
Update available: 1527 commits behind — run 'hermes update'

tools.tool_search:
  enabled: auto
  threshold_pct: 5
  search_default_limit: 5
  max_search_limit: 25
  listing: auto
  listing_max_tokens: 4000
  defer: computer_use, session_search, image_generate, todo_list, process_manage,
         cronjob_manage, drive_preview, gui_tour, desktop_preview, annotate_preview,
         show_tip, desktop_project, close_terminal, apply_layout, read_terminal,
         read_window_below, focus_pane
memory.provider: mnemosyne
Local repo HEAD: 5f666db4e3af17142fa62b11e06ff377d5239a42
Local git status --short: empty
Last commit: 5f666db4e3af17142fa62b11e06ff377d5239a42 2026-09-29 address review: min=1 not 0, and cover the plain short-string path
```

The update-available count is context only. It does **not** authorize or recommend an Hermes update. `auto` and the deferral behavior were verified in the local code at this exact HEAD; current online docs are not the authority for what this older install does.
