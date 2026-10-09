# Decision record: Waypoint abandoned-search eligibility

**Status:** accepted for a fictional local exercise, not a production release\
**Date:** 2026-10-09\
**Decision / delivery owner:** Danoishan Sinnathamby, portfolio exercise\
**Data classification:** synthetic identifiers only

## Objective and constraints

Evaluate whether an abandoned search should qualify for a reminder after two hours. Protect consent, avoid a reminder for a matched booking, reject malformed inputs and preserve an explanation for the decision. This exercise has no vendor calls or message delivery.

## Options and decision

| Option | Benefit | Cost / failure risk | Decision |
| --- | --- | --- | --- |
| Delay, then qualify every search | Simple | Ignores purchase, identity and current consent | Reject |
| Match booking on customer only | Easy exit | An unrelated booking may suppress the wrong search | Reject |
| Evaluate customer + search ID, current consent and freshness | Explicit business context and inspectable exits | Requires source IDs and consent timestamps | Use in the local model |

## Acceptance criteria

- A matching booking suppresses the reminder, including when delivery order is reversed.
- A booking for another search does not exit this search.
- An opt-out after entry prevents eligibility. Stale opt-in cannot reverse it.
- Anonymous identity cannot grant consent to an identified profile; a newer opt-out survives resolution.
- Duplicate event ID and payload is ignored; a conflicting payload is reported.
- Malformed records are reported independently from valid records.
- At two hours the delay has elapsed. At 24 hours the search is still fresh; after 24 hours it expires.

## Validation evidence

`lab/waypoint-demo/test.mjs` validates the independent expectations in 18 input scenarios plus consent, boundary, input and mock transport tests. `results.json` records deterministic policy decisions and traces. The browser imports the same engine.

See [the filled validation matrix](waypoint-validation-matrix.md) and [the runnable exercise](../lab/waypoint-demo.html).

## Residual risks and revisit conditions

The event ledger is in memory within one evaluation. Eligibility does not deliver a message. A real integration requires persistent idempotency, scheduling, verified identity semantics, a consent authority, cooldowns, recovery and monitoring. Revisit this decision if search IDs are not stable, booking exits cannot be correlated, consent timestamps are ambiguous or the freshness requirement changes.

## Launch decision

**Local demonstration:** ready after the automated suite and recorded-result check pass.\
**Production go/no-go:** not assessed. Platform, engineering, data and QA owners must produce end-to-end evidence before any customer release.
