# End-to-End Validation Matrix

| Layer | Question | Proof | Owner if it fails |
|---|---|---|---|
| Source | Did the business event become true? | Source record / event evidence | Source-system owner |
| Transport / ingestion | Was the payload or file accepted? | Request, file or ingestion evidence | Integration / platform owner |
| Identity | Did it attach to the intended customer? | Canonical ID / profile evidence | Identity owner |
| Profile / data state | Are required fields/events present and current? | Profile / dataset validation | Data owner |
| Eligibility | Does the customer qualify under business rules? | Segment / decision evidence | Journey / business-rule owner |
| Orchestration | Did the workflow enter, branch and exit correctly? | Journey / automation evidence | Platform owner |
| Customer outcome | Did the intended experience actually happen? | Rendered message / action / conversion | Delivery owner |
| Exception path | If anything failed, did the right team know? | Alert / log / escalation evidence | Operations / support |
