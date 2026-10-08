# FocusDeck

Focus timer, daily time-block planner, 10,000-hours tracker and reports. One self-contained `index.html`.

## Build

The source is in `modules/`. Do not edit `index.html` by hand.

```
python assemble.py
```

This writes `index.html`.

## Storage

- Data lives in the browser's IndexedDB (database `focusdeck`), one record per item:
  `{ id, type, data, updatedAt, deleted }`.
- Record types: session, tag, skill, backlog, template, thought, block, dayplan, setting, config.
- Deleting an item writes a tombstone (`deleted: true`) so deletes can sync.
- Every write is also queued in the `outbox` store for cloud sync (phase 4).
- Device-only state (running timer, last export/import time) is in localStorage key `focusdeck.device.v1`.
- Safety snapshots (last 3, before import or wipe) are device-only and never exported.
- The old localStorage key `focusdeck.v1` is read once on first open and left untouched as a fallback copy.

## Modules

| File | Contents |
|---|---|
| modules/css.py | Styles |
| modules/markup.py | HTML body |
| modules/js_state_and_timer.py | Defaults, migration, timer engine |
| modules/js_storage.py | IndexedDB record storage |
| modules/js_timeblock.py | Time-block planner |
| modules/js_skills.py | 10,000 hours |
| modules/js_backup.py | Export, import, snapshots |
| modules/js_views_and_charts.py | Views, log, reports, settings |
| modules/js_main.py | Startup |
