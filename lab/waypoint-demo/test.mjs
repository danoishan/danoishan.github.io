import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { evaluateScenario, ingestWithRetry } from './engine.mjs';

const fixtures = JSON.parse(await readFile(new URL('./fixtures.json', import.meta.url), 'utf8'));
for (const fixture of fixtures) {
  test(fixture.title, () => {
    const actual = evaluateScenario(fixture.input);
    assert.deepEqual(actual.decisions.map(({ customerId, searchId, decision, reason }) => ({ customerId, searchId, decision, reason })), fixture.expected.decisions);
    assert.equal(actual.duplicates, fixture.expected.duplicates ?? 0);
    assert.deepEqual(actual.rejected.map(item => item.reason), fixture.expected.rejected ?? []);
  });
}
test('Evaluation does not mutate its input', () => {
  const input = structuredClone(fixtures[0].input), before = structuredClone(input);
  evaluateScenario(input);
  assert.deepEqual(input, before);
});
test('Unknown evaluation time fails explicitly', () => assert.throws(() => evaluateScenario({ now: 'bad' }), /evaluation time/));
test('Malformed initial consent fails closed', () => assert.throws(() => evaluateScenario({ now: fixtures[0].input.now, profiles: [{ id: 'cust_01', identified: true, emailConsent: 'yes', consentAt: 'bad' }] }), /Profiles require/));
test('Equal-time consent conflict favors opt-out', () => {
  const input = structuredClone(fixtures[0].input);
  input.events.push({ id: 'optout_equal', type: 'consent_changed', userId: 'cust_01', at: input.profiles[0].consentAt, emailConsent: false });
  assert.equal(evaluateScenario(input).decisions[0].reason, 'no_email_consent');
});
test('429 respects a bounded wait, then succeeds', async () => {
  const waits = [], responses = [{ status: 429, retryAfterMs: 50 }, { status: 200, body: { accepted: ['evt_1'] } }];
  const actual = await ingestWithRetry({}, async () => responses.shift(), { sleep: async ms => waits.push(ms) });
  assert.equal(actual.state, 'accepted'); assert.deepEqual(waits, [50]); assert.equal(actual.attempts.length, 2);
});
test('Transient failure uses a bounded retry count', async () => {
  const waits = []; const actual = await ingestWithRetry({}, async () => ({ status: 503 }), { sleep: async ms => waits.push(ms) });
  assert.equal(actual.state, 'failed'); assert.equal(actual.attempts.length, 3); assert.equal(actual.errors[0].reason, 'retry_exhausted'); assert.deepEqual(waits, [100, 200]);
});
test('200 with record errors is partial, not complete', async () => {
  let calls = 0;
  const actual = await ingestWithRetry({}, async () => { calls++; return { status: 200, body: { accepted: ['evt_1'], errors: [{ eventId: 'evt_2', reason: 'invalid_identity' }] } }; });
  assert.equal(actual.state, 'partial'); assert.equal(calls, 1); assert.equal(actual.errors[0].eventId, 'evt_2');
});
test('400 is not retried', async () => {
  const actual = await ingestWithRetry({}, async () => ({ status: 400 }));
  assert.equal(actual.state, 'failed'); assert.equal(actual.attempts.length, 1);
});
test('A long server wait is deferred, never shortened', async () => {
  let calls = 0;
  const actual = await ingestWithRetry({}, async () => { calls++; return { status: 429, retryAfterMs: 5000 }; });
  assert.equal(actual.state, 'deferred'); assert.equal(actual.retryAfterMs, 5000); assert.equal(calls, 1);
});
test('A transport failure can recover within the retry budget', async () => {
  let calls = 0;
  const actual = await ingestWithRetry({}, async () => { if (++calls === 1) throw new Error('offline'); return { status: 200 }; }, { sleep: async () => {} });
  assert.equal(actual.state, 'accepted'); assert.equal(actual.attempts[0].transportError, true); assert.equal(calls, 2);
});
test('Delay and freshness boundaries are explicit', () => {
  const input = structuredClone(fixtures[0].input);
  input.events[0].at = '2026-10-09T12:00:00Z';
  assert.equal(evaluateScenario(input).decisions[0].decision, 'eligible');
  input.events[0].at = '2026-10-08T14:00:00Z';
  assert.equal(evaluateScenario(input).decisions[0].decision, 'eligible');
  input.events[0].at = '2026-10-08T13:59:59Z';
  assert.equal(evaluateScenario(input).decisions[0].decision, 'expired');
});
