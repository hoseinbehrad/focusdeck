// POST /api/sync
//
// Request:  { since: number, changes: [{ id, type, data, updatedAt, deleted }] }
// Response: { accepted, ignored, rejected: [{id, error}], changes: [...], cursor, hasMore, serverTime }
//
// 1. Pushed changes are stored only if newer than what the server has (per record, newest updatedAt wins).
// 2. Every stored change gets a new server sequence number (seq).
// 3. The response returns all records with seq > since, oldest first, so a device catches up
//    by calling again with the returned cursor while hasMore is true.

import {
  json, preflight, checkAuth, validateChange,
  MAX_CHANGES_PER_REQUEST, MAX_RECORD_BYTES, PULL_PAGE_SIZE
} from '../../lib/sync_shared.js';

const UPSERT_SQL = `
INSERT INTO records (id, type, data, updated_at, deleted, seq)
VALUES (?1, ?2, ?3, ?4, ?5, (SELECT value FROM counters WHERE name = 'seq'))
ON CONFLICT(id) DO UPDATE SET
  type = excluded.type,
  data = excluded.data,
  updated_at = excluded.updated_at,
  deleted = excluded.deleted,
  seq = excluded.seq
WHERE excluded.updated_at > records.updated_at`;

const BUMP_SQL = `UPDATE counters SET value = value + 1 WHERE name = 'seq'`;

export async function onRequestOptions() {
  return preflight();
}

export async function onRequestPost({ request, env }) {
  const denied = checkAuth(request, env);
  if (denied) return denied;

  let body;
  try {
    body = await request.json();
  } catch (e) {
    return json({ error: 'Body must be JSON' }, 400);
  }

  const since = Number.isFinite(body.since) && body.since >= 0 ? Math.floor(body.since) : 0;
  const changes = Array.isArray(body.changes) ? body.changes : [];
  if (changes.length > MAX_CHANGES_PER_REQUEST) {
    return json({ error: `Too many changes in one request (max ${MAX_CHANGES_PER_REQUEST})` }, 413);
  }

  // ---- push ----
  const rejected = [];
  const valid = [];
  for (const c of changes) {
    const err = validateChange(c);
    if (err) { rejected.push({ id: c && c.id, error: err }); continue; }
    const data = c.deleted === true ? null : JSON.stringify(c.data);
    if (data && data.length > MAX_RECORD_BYTES) { rejected.push({ id: c.id, error: 'record too large' }); continue; }
    valid.push({ id: c.id, type: c.type, data, updatedAt: Math.floor(c.updatedAt), deleted: c.deleted === true ? 1 : 0 });
  }

  let accepted = 0;
  const db = env.DB;
  // D1 runs each batch as one transaction and serializes writes, so seq numbers never interleave.
  const CHUNK = 50;
  for (let i = 0; i < valid.length; i += CHUNK) {
    const part = valid.slice(i, i + CHUNK);
    const stmts = [];
    for (const r of part) {
      stmts.push(db.prepare(BUMP_SQL));
      stmts.push(db.prepare(UPSERT_SQL).bind(r.id, r.type, r.data, r.updatedAt, r.deleted));
    }
    const results = await db.batch(stmts);
    for (let k = 1; k < results.length; k += 2) {
      if (results[k].meta && results[k].meta.changes > 0) accepted++;
    }
  }

  // ---- pull ----
  const { results: rows } = await db
    .prepare('SELECT id, type, data, updated_at, deleted, seq FROM records WHERE seq > ?1 ORDER BY seq LIMIT ?2')
    .bind(since, PULL_PAGE_SIZE + 1)
    .all();

  const hasMore = rows.length > PULL_PAGE_SIZE;
  const page = hasMore ? rows.slice(0, PULL_PAGE_SIZE) : rows;
  const out = page.map(r => ({
    id: r.id,
    type: r.type,
    data: r.deleted ? null : JSON.parse(r.data),
    updatedAt: r.updated_at,
    deleted: !!r.deleted
  }));

  let cursor = since;
  if (page.length) cursor = page[page.length - 1].seq;

  return json({
    accepted,
    ignored: valid.length - accepted,
    rejected,
    changes: out,
    cursor,
    hasMore,
    serverTime: Date.now()
  });
}
