# Waypoint: abandoned-search policy exercise

A fictional, AI-assisted portfolio exercise by Danoishan Sinnathamby. It turns an architecture recommendation into an inspectable policy model. No client data, credentials, Braze SDK or live messaging service is used.

## Run it

From the repository root, with Node.js 20 or newer:

```sh
node --test lab/waypoint-demo/test.mjs
node lab/waypoint-demo/run.mjs --check
```

For the browser evaluator, serve the repository over HTTP:

```sh
python3 -m http.server 8000
```

Open `http://localhost:8000/lab/waypoint-demo.html`. The browser and test runner import the same `engine.mjs`. No package installation or build step is required. `run.mjs --write` refreshes the committed `results.json` after an intentional policy change; review the independent expectations in `fixtures.json` before changing them.

## Policy and contract

- Evaluate at `input.now`, an explicit timestamp. Profiles and events are arrays.
- A profile has `id`, `identified`, `emailConsent` and `consentAt`.
- Each event has a stable `id`, `type`, `userId` and timestamp `at`.
- Supported events: `search_completed`, `booking_completed`, `consent_changed`, `identify`.
- Search and booking events require `searchId`. Consent events require a boolean `emailConsent`. Identity events require an existing identified `customerId`.
- The journey key is customer ID plus search ID. A matching booking suppresses that search even if it arrives first.
- An identified, opted-in customer becomes eligible after two hours, up to and including 24 hours after the search. Older searches expire.
- Consent is checked at evaluation. The latest timestamp wins; an equal-time opt-out wins a conflict.
- Identity resolution moves journey state. It never grants consent from an anonymous profile and preserves an equally recent or newer opt-out. Two identified customers cannot be merged.
- An identical event ID and payload is ignored. A changed payload under the same event ID is rejected. The event ledger is in memory for one evaluation only.
- Invalid records are reported separately. Invalid initial profile state fails explicitly.

`evaluateScenario()` returns decisions, duplicate counts, rejected records and a processing trace. Eligibility is a policy result, not a sent-message result. The fixtures contain explicit expected decisions written separately from the engine.

## Mock transport tests

`ingestWithRetry()` accepts an injected local adapter, not a vendor client. Tests cover a short rate-limit wait, retry exhaustion, a transport error, a non-retryable response and HTTP 200 with record errors. Partial responses do not trigger a retry of the entire accepted batch. A server wait over the one-second exercise budget is deferred, never shortened. The test clock and sleep are injected so the tests do not wait on real services.

The illustrative `body.accepted` and `body.errors` schema is **not asserted to match Braze's actual response contract**. A real adapter must map the documented endpoint response before deciding what to retry. A timeout has an ambiguous outcome, so production retries require durable event identity and downstream idempotency.

## Production gaps and ownership

This model does not implement durable queues, cross-run deduplication, a transactional outbox, scheduling, delivery, live identity semantics, warehouse sync, multi-search cooldowns, throughput tests, production retention or observability infrastructure. Separate searches are evaluated independently; selecting only the most recent search and limiting fatigue are broader design requirements.

For a live implementation, source owners establish business truth and consent authority; platform specialists validate identity and channel semantics; engineering owns persistence and adapter behavior; QA supplies source-to-outcome evidence; delivery coordinates the decision and rollout. Store minimal identifiers, protect credentials outside browser code, bound retention, reconcile counts and name an alert and recovery owner.

## References

Consult the live primary documentation before implementing a vendor adapter:

- [Braze `/users/track`](https://www.braze.com/docs/api/endpoints/user_data/post_user_track/)
- [Braze API rate limits](https://www.braze.com/docs/api/api_limits/)
- [Braze API errors](https://www.braze.com/docs/api/errors/)

The local outputs establish only that the stated model behaves as tested. They do not establish production integration, customer impact or performance under load.
