// GET /api/status
// Without a token: { ok: true } (use it to test that the server is reachable).
// With a valid token: also returns record counts per type and the current sequence number.

import { json, preflight, checkAuth } from '../../lib/sync_shared.js';

export async function onRequestOptions() {
  return preflight();
}

export async function onRequestGet({ request, env }) {
  if (!request.headers.get('Authorization')) {
    return json({ ok: true, serverTime: Date.now() });
  }
  const denied = checkAuth(request, env);
  if (denied) return denied;

  const { results } = await env.DB
    .prepare('SELECT type, SUM(CASE WHEN deleted = 0 THEN 1 ELSE 0 END) AS live, SUM(deleted) AS deleted FROM records GROUP BY type ORDER BY type')
    .all();
  const seqRow = await env.DB.prepare("SELECT value FROM counters WHERE name = 'seq'").first();

  return json({ ok: true, serverTime: Date.now(), seq: seqRow ? seqRow.value : 0, types: results });
}
