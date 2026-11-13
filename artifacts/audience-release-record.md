# Audience source decision

Worked example for [Making 200 Million Messages Boring](../work/200m-messages.html). The scenario and values are illustrative.

| Field | Decision record |
| --- | --- |
| Situation | An upcoming send has an approved audience extract. A new customer-data segment is available for comparison, with eligibility differences still open. |
| Recommendation | Use the approved extract for this release if it still covers the intended audience and passes the current QA checks. Reconcile the new segment in parallel. |
| Other options | Switch to the new segment if differences are explained and approved. Move the send if the approved extract also fails a critical check. |
| Decision owner | Client release owner, with the delivery recommendation, QA evidence and confirmation from the data owner. |
| Acceptance evidence | Reconcile the approved counts, test inclusions and exclusions, verify the current consent rule, and record the source and file version under review. |
| After launch | Operations compares the first send results with the approved audience and knows whom to contact for a count or eligibility discrepancy. |
| Revisit when | The data owner can explain who moves in or out under the new segment and QA has repeated the eligibility and consent tests. |

The decision record shows what the review would need to establish. It contains no client records, measured outcome or live delivery data.
