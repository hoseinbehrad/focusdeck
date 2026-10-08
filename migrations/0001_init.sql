-- FocusDeck sync database (Cloudflare D1)

CREATE TABLE IF NOT EXISTS records (
  id          TEXT PRIMARY KEY,          -- "<type>:<item id>"
  type        TEXT NOT NULL,
  data        TEXT,                      -- JSON, NULL when deleted
  updated_at  INTEGER NOT NULL,          -- ms since epoch, set by the device that made the change
  deleted     INTEGER NOT NULL DEFAULT 0,
  seq         INTEGER NOT NULL           -- server sequence number, increases with every stored change
);

CREATE INDEX IF NOT EXISTS idx_records_seq ON records (seq);

CREATE TABLE IF NOT EXISTS counters (
  name   TEXT PRIMARY KEY,
  value  INTEGER NOT NULL
);

INSERT OR IGNORE INTO counters (name, value) VALUES ('seq', 0);
