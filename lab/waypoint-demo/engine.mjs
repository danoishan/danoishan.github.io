// A local, deterministic policy model. No Braze SDK, network or message delivery.
export const POLICY = Object.freeze({ delayMs: 2 * 60 * 60 * 1000, freshnessMs: 24 * 60 * 60 * 1000 });
const TYPES = new Set(['search_completed', 'booking_completed', 'consent_changed', 'identify']);
const timestamp = value => typeof value === 'string' ? Date.parse(value) : NaN;
const identifier = value => typeof value === 'string' && /^[a-zA-Z0-9_-]{1,80}$/.test(value);
const fingerprint = event => JSON.stringify([event.type, event.userId, event.at, event.searchId, event.emailConsent, event.customerId]);

export function evaluateScenario(input) {
  if (!input || !Number.isFinite(timestamp(input.now))) throw new Error('A valid evaluation time is required.');
  if (!Array.isArray(input.profiles ?? []) || !Array.isArray(input.events ?? [])) throw new Error('Profiles and events must be arrays.');
  const now = timestamp(input.now);
  const profiles = new Map();
  const aliases = new Map();
  const searches = new Map();
  const bookings = new Set();
  const ledger = new Map();
  const trace = [];
  const rejected = [];
  let duplicates = 0;
  for (const profile of input.profiles ?? []) {
    if (!identifier(profile.id) || typeof profile.emailConsent !== 'boolean' || typeof profile.identified !== 'boolean' || !Number.isFinite(timestamp(profile.consentAt)) || timestamp(profile.consentAt) > now) {
      throw new Error('Profiles require a valid ID, identity state, consent and consent timestamp.');
    }
    if (profiles.has(profile.id)) throw new Error('Duplicate profile ID.');
    profiles.set(profile.id, { ...profile });
  }
  const resolve = id => {
    const visited = new Set();
    while (aliases.has(id)) {
      if (visited.has(id)) throw new Error('Identity alias cycle.');
      visited.add(id);
      id = aliases.get(id);
    }
    return id;
  };
  const profileFor = id => {
    id = resolve(id);
    if (!profiles.has(id)) profiles.set(id, { id, identified: false, emailConsent: false, consentAt: '1970-01-01T00:00:00Z' });
    return profiles.get(id);
  };
  for (const event of input.events ?? []) {
    let problem;
    if (!event || typeof event !== 'object') problem = 'invalid_event';
    else if (!identifier(event.id) || !identifier(event.userId)) problem = 'invalid_identifier';
    else if (!TYPES.has(event.type)) problem = 'unsupported_event';
    else if (!Number.isFinite(timestamp(event.at))) problem = 'invalid_timestamp';
    else if (timestamp(event.at) > now) problem = 'future_event';
    else if (['search_completed', 'booking_completed'].includes(event.type) && !identifier(event.searchId)) problem = 'missing_search_id';
    else if (event.type === 'consent_changed' && typeof event.emailConsent !== 'boolean') problem = 'invalid_consent';
    else if (event.type === 'identify' && (!identifier(event.customerId) || !profiles.get(resolve(event.customerId))?.identified)) problem = 'unknown_identified_customer';
    if (problem) {
      rejected.push({ eventId: event?.id ?? null, reason: problem });
      trace.push({ eventId: event?.id ?? null, action: 'reject', reason: problem });
      continue;
    }
    if (ledger.has(event.id)) {
      if (ledger.get(event.id) === fingerprint(event)) {
        duplicates++;
        trace.push({ eventId: event.id, action: 'ignore_duplicate' });
      } else {
        rejected.push({ eventId: event.id, reason: 'event_id_conflict' });
        trace.push({ eventId: event.id, action: 'reject', reason: 'event_id_conflict' });
      }
      continue;
    }
    const userId = resolve(event.userId);
    const profile = profileFor(userId);
    if (event.type === 'identify') {
      const customerId = resolve(event.customerId);
      if (userId !== customerId && profile.identified) {
        rejected.push({ eventId: event.id, reason: 'cannot_merge_identified_customers' });
        trace.push({ eventId: event.id, action: 'reject', reason: 'cannot_merge_identified_customers' });
        continue;
      }
      if (userId !== customerId) {
        aliases.set(userId, customerId);
        // Keep an equally recent or newer anonymous opt-out. Never grant consent from it.
        const customer = profileFor(customerId);
        if (!profile.emailConsent && timestamp(profile.consentAt) >= timestamp(customer.consentAt)) {
          customer.emailConsent = false;
          customer.consentAt = profile.consentAt;
        }
        for (const [key, search] of [...searches]) {
          if (search.customerId !== userId) continue;
          searches.delete(key);
          const newKey = `${customerId}|${search.searchId}`;
          const existing = searches.get(newKey);
          if (!existing || timestamp(search.at) > timestamp(existing.at)) searches.set(newKey, { ...search, customerId });
        }
        for (const key of [...bookings]) {
          if (key.startsWith(`${userId}|`)) {
            bookings.delete(key);
            bookings.add(`${customerId}|${key.split('|')[1]}`);
          }
        }
      }
      trace.push({ eventId: event.id, action: 'identity_resolved', customerId });
    } else if (event.type === 'consent_changed') {
      if (timestamp(event.at) > timestamp(profile.consentAt)) {
        profile.emailConsent = event.emailConsent;
        profile.consentAt = event.at;
        trace.push({ eventId: event.id, action: 'consent_updated', customerId: userId });
      } else if (timestamp(event.at) === timestamp(profile.consentAt) && !event.emailConsent) {
        // A conflicting equal-time opt-out wins conservatively.
        profile.emailConsent = false;
        trace.push({ eventId: event.id, action: 'equal_time_opt_out', customerId: userId });
      } else {
        trace.push({ eventId: event.id, action: 'ignore_stale_consent', customerId: userId });
      }
    } else if (event.type === 'booking_completed') {
      bookings.add(`${userId}|${event.searchId}`);
      trace.push({ eventId: event.id, action: 'booking_recorded', customerId: userId, searchId: event.searchId });
    } else {
      const key = `${userId}|${event.searchId}`;
      const previous = searches.get(key);
      if (!previous || timestamp(event.at) > timestamp(previous.at)) searches.set(key, { customerId: userId, searchId: event.searchId, at: event.at });
      trace.push({ eventId: event.id, action: 'search_recorded', customerId: userId, searchId: event.searchId });
    }
    ledger.set(event.id, fingerprint(event));
  }
  const decisions = [...searches.values()].map(search => {
    const profile = profileFor(search.customerId);
    const age = now - timestamp(search.at);
    let decision = 'eligible', reason = 'eligible_abandoned_search';
    if (!profile.identified) { decision = 'suppressed'; reason = 'unresolved_identity'; }
    else if (bookings.has(`${search.customerId}|${search.searchId}`)) { decision = 'suppressed'; reason = 'matched_booking'; }
    else if (age > POLICY.freshnessMs) { decision = 'expired'; reason = 'stale_search'; }
    else if (!profile.emailConsent) { decision = 'suppressed'; reason = 'no_email_consent'; }
    else if (age < POLICY.delayMs) { decision = 'waiting'; reason = 'delay_not_elapsed'; }
    return { customerId: search.customerId, searchId: search.searchId, decision, reason, dueAt: new Date(timestamp(search.at) + POLICY.delayMs).toISOString() };
  }).sort((a, b) => `${a.customerId}|${a.searchId}`.localeCompare(`${b.customerId}|${b.searchId}`));
  return { decisions, duplicates, rejected, trace };
}

export async function ingestWithRetry(payload, send, { maxAttempts = 3, sleep = ms => new Promise(resolve => setTimeout(resolve, ms)) } = {}) {
  if (!Number.isInteger(maxAttempts) || maxAttempts < 1 || maxAttempts > 5) throw new Error('maxAttempts must be between 1 and 5.');
  const attempts = [];
  for (let number = 1; number <= maxAttempts; number++) {
    let response;
    try { response = await send(payload); }
    catch { response = { status: 503, transportError: true }; }
    if (!Number.isInteger(response?.status) || response.status < 100 || response.status > 599) throw new Error('Mock adapter must return a valid HTTP status.');
    attempts.push({ number, status: response.status });
    if (response.transportError) attempts.at(-1).transportError = true;
    if (response.status >= 200 && response.status < 300) {
      const errors = response.body?.errors ?? [];
      return { state: errors.length ? 'partial' : 'accepted', attempts, errors, accepted: response.body?.accepted ?? [] };
    }
    const retryable = response.status === 429 || response.status >= 500;
    if (!retryable || number === maxAttempts) return { state: 'failed', attempts, errors: [{ reason: retryable ? 'retry_exhausted' : 'non_retryable' }] };
    // This short local exercise defers long server waits instead of retrying early.
    if (Number.isFinite(response.retryAfterMs) && response.retryAfterMs > 1000) return { state: 'deferred', attempts, retryAfterMs: response.retryAfterMs, errors: [{ reason: 'server_wait_exceeds_demo_budget' }] };
    const waitMs = Number.isFinite(response.retryAfterMs) && response.retryAfterMs >= 0 ? response.retryAfterMs : Math.min(100 * 2 ** (number - 1), 1000);
    attempts.at(-1).waitMs = waitMs;
    await sleep(waitMs);
  }
}
