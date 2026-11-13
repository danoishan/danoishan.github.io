# Audience source decision

Worked example for [Making 200 Million Messages Boring](../work/200m-messages.html). The scenario and values are illustrative.

| Field | Decision record |
| --- | --- |
| Situation | The approved extract has 48,000 eligible records. The new segment has 47,400: 900 are missing from the new segment and 300 are new additions. The counts are fictional. |
| Recommendation | Use the approved extract for this release if it still covers the intended audience and passes the current QA checks. Reconcile the new segment in parallel. |
| Other options | Switch to the new segment if differences are explained and approved. Move the send if the approved extract also fails a critical check. |
| Decision owner | Client release owner, with the delivery recommendation, QA evidence and confirmation from the data owner. |
| Acceptance evidence | Reconcile the two groups separately by customer ID. Check opt-outs, suppressions and eligibility in each group, and record the source and file version under review. |
| After launch | I review the first send counts with operations and escalate any unexplained count or eligibility difference to the data and release owners. |
| Revisit when | The data owner can explain who moves in or out under the new segment and QA has repeated the eligibility and consent tests. |

The decision record shows what the review would need to establish. It contains no client records, measured outcome or live delivery data.
