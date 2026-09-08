# CROSS-PLATFORM EVIDENCE TEMPLATE

Use one record per runtime/test execution. Store raw outputs outside canonical knowledge when they contain transient logs or sensitive data; store the evidence pointer here.

## Record

- Runtime:
- Runtime version:
- Runtime state:
- Date/time:
- Session freshness: FRESH / NON_FRESH / UNKNOWN
- Context package:
- Canonical commit tested:
- Adapter path:
- Adapter verification state: NOT_TESTED / PARTIAL / PASS / FAIL
- Test ID: CP-01 / CP-02 / CP-03 / CP-04 / CP-05 / CP-06
- Prompt:
- Raw output location:
- Score: 2 / 1 / 0
- Failure type: CANONICAL / ADAPTER / RUNTIME / EXTERNAL_DEPENDENCY / TEST_DEFECT / NONE
- Observed result:
- Expected result:
- Corrective change:
- Retest result:
- Reviewer:

## Rules

- A score requires raw evidence.
- A fresh-session claim requires evidence that the session was fresh.
- Do not infer runtime verification from documentation support.
- Do not infer parity from an adapter file existing.
- Do not replace raw evidence with a summary when the raw output is available.
- Never record secrets, access tokens, or credentials.
