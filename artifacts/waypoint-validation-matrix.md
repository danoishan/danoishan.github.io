# Waypoint validation matrix

**Date:** 2026-10-09\
**Environment:** deterministic local model with synthetic fixtures\
**Owner:** Danoishan Sinnathamby, portfolio exercise\
**Evidence:** [source and tests](../lab/waypoint-demo/), [inputs](../lab/waypoint-demo/fixtures.json), [recorded outputs](../lab/waypoint-demo/results.json)

| Scenario ID | Expected result | Evidence / owner if a production equivalent fails |
| --- | --- | --- |
| eligible | Eligible after delay | Identity, consent and timing / platform + data |
| booked | Suppressed: matched booking | Booking correlation / source + platform |
| duplicate | One decision, one duplicate ignored | Event identity / integration engineering |
| opt-out | Suppressed: no email consent | Current channel eligibility / consent owner |
| identity-merge | Journey resolves to known customer | Canonical ID contract / identity owner |
| stale | Expired: older than 24 hours | Freshness rule / lifecycle owner |
| late-search | Suppressed despite reversed arrival order | Delayed event handling / integration engineering |
| partial-records | Valid record evaluated, invalid record reported | Record reconciliation / integration + operations |
| future | Future-dated event rejected | Source clock and schema / source owner |
| waiting | Waiting: delay not elapsed | Scheduling policy / platform owner |
| unidentified | Suppressed: unresolved identity | Identity resolution / identity owner |
| different-search | Unrelated booking does not suppress | Business correlation / source + platform |
| id-conflict | Changed payload under existing ID rejected | Event contract / source engineering |
| stale-consent | Old opt-in cannot reverse new opt-out | Consent freshness / consent owner |
| merge-consent | Anonymous opt-in does not grant consent | Merge policy / identity + consent owners |
| merge-optout | Newer anonymous opt-out survives merge | Merge policy / identity + consent owners |
| identified-conflict | Two known customers cannot merge | Identity integrity / identity owner |
| null-record | Malformed record reported without batch crash | Ingestion validation / engineering |

Additional tests cover input immutability, invalid initial state, equal-time opt-out, two-hour / 24-hour boundaries, short rate-limit waits, long-wait deferral, transport recovery, retry exhaustion, non-retryable errors and partial HTTP 200 responses.

**Result:** all expectations must pass in `node --test lab/waypoint-demo/test.mjs`. `node lab/waypoint-demo/run.mjs --check` must reproduce the published outputs. A pass is evidence of this local model only. No live profile, journey entry, message delivery, business conversion or load-test result is asserted.

**Production release gate:** source counts, accepted and rejected records, identity, consent, journey entry and exits, customer-visible delivery, alert routing and recovery must be reconciled with named owners. None of those live release gates is marked complete by this exercise.
