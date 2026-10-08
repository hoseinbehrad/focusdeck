// Shared helpers for the FocusDeck sync API (Cloudflare Pages Functions).

export const RECORD_TYPES = new Set([
  'session', 'tag', 'skill', 'backlog', 'template', 'thought',
  'block', 'dayplan', 'setting', 'config', 'review'
]);

export const MAX_CHANGES_PER_REQUEST = 500;
export const MAX_RECORD_BYTES = 100 * 1024;
export const PULL_PAGE_SIZE = 500;

export const CORS_HEADERS = {
  // Auth is a bearer token (no cookies), so allowing any origin is safe and
  // lets the Android wrapper and local file:// copies reach the API.
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Authorization, Content-Type',
  'Access-Control-Max-Age': '86400'
};

export function json(body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store', ...CORS_HEADERS }
  });
}

export function preflight() {
  return new Response(null, { status: 204, headers: CORS_HEADERS });
}

// Constant-time string comparison
function safeEqual(a, b) {
  if (typeof a !== 'string' || typeof b !== 'string') return false;
  const enc = new TextEncoder();
  const x = enc.encode(a);
  const y = enc.encode(b);
  let diff = x.length ^ y.length;
  const n = Math.max(x.length, y.length);
  for (let i = 0; i < n; i++) diff |= (x[i] || 0) ^ (y[i] || 0);
  return diff === 0;
}

// Returns a Response if the request is NOT allowed, otherwise null.
export function checkAuth(request, env) {
  const expected = env.SYNC_TOKEN;
  if (!expected || expected.length < 24) {
    return json({ error: 'Server not configured: set a SYNC_TOKEN secret of at least 24 characters' }, 500);
  }
  const header = request.headers.get('Authorization') || '';
  const token = header.startsWith('Bearer ') ? header.slice(7).trim() : '';
  if (!safeEqual(token, expected)) return json({ error: 'Unauthorized' }, 401);
  if (!env.DB) return json({ error: 'Server not configured: D1 binding "DB" is missing' }, 500);
  return null;
}

// Validates one incoming change. Returns an error string or null.
export function validateChange(c) {
  if (!c || typeof c !== 'object') return 'change must be an object';
  if (typeof c.id !== 'string' || c.id.length < 3 || c.id.length > 200) return 'bad id';
  if (!RECORD_TYPES.has(c.type)) return 'unknown type: ' + c.type;
  if (!c.id.startsWith(c.type + ':')) return 'id must start with its type';
  if (typeof c.updatedAt !== 'number' || !Number.isFinite(c.updatedAt) || c.updatedAt < 0) return 'bad updatedAt';
  // Reject clocks more than 1 day in the future; they would win every conflict forever.
  if (c.updatedAt > Date.now() + 86400000) return 'updatedAt is in the future (check device clock)';
  if (c.deleted !== true && (c.data === null || typeof c.data !== 'object')) return 'data required unless deleted';
  return null;
}
