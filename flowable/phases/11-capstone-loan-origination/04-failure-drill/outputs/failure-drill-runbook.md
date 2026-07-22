---
name: failure-drill-runbook
description: Capstone failure drill — bureau down, offer expired, manual override, stuck jobs
kind: runbook
phase: 11
lesson: 04
---

# Loan origination — failure drill runbook

Run each drill against a local engine with the capstone deployed
(lesson 03's driver deploys both artifacts). Every diagnostic here was built in an
earlier phase; the page numbers are the point.

## Drill 1 — bureau unreachable at pull time

**Inject:** start an application with `bureauBaseUrl=http://bureau.invalid`
(the driver's default).

**Expected:** the HTTP task's failure statuses raise a BPMN error; the boundary
routes to *Pull bureau report manually* (Phase 4, lessons 02/04). The instance never
freezes.

**Verify:** `open_tasks` shows `manualBureauPull` in the credit-ops pool;
history shows `bureauDown` fired. **If instead** the job dead-lettered: the
boundary/`handleStatusCodes` wiring is wrong — triage with Phase 4's
`incident_client.py`.

## Drill 2 — bureau flaky (retries, then recovery)

**Inject:** point `bureauBaseUrl` at a server returning 502 twice then 200
(20 lines of Python http.server).

**Expected:** `flowable:async="true"` means the caller's transaction committed; the
job executor retries per its cycle (Phase 2 lesson 04, Phase 4 lesson 05). No human
sees anything unless retries exhaust.

**Verify:** `ACT_RU_JOB` retries decrement; on success the token advances. Tune with
`flowable:failedJobRetryTimeCycle="R5/PT10M"` sized to the bureau's real outage
profile.

## Drill 3 — offer expires

**Inject:** start with `offerValidity=PT15S`, complete KYC + review, then *don't*
accept the offer.

**Expected:** the interrupting timer boundary (Phase 7, lesson 01) cancels
`acceptOffer` ~15 s later; the instance ends at `expired`.

**Verify:** the open task disappears without anyone completing it; history ends
`acceptOffer -> offerExpiry -> expired`. **Policy note:** validity comes in as a
variable so the *value* can move to the DMN table without a model change.

## Drill 4 — manual override of an auto-decline

**Situation:** table says decline; business insists on review.

**Right fix:** change the *policy*, not the instance — new `loanDecision` version
widening the manual-review band (Phase 5 governance ritual: diff, golden cases,
impact replay). New applications pick it up immediately.

**Wrong fix flagged for completeness:** mutating the live instance's `decision`
variable and triggering the gateway by hand — it bypasses the audit chain the DMN
version history provides. If a one-off override is genuinely required, do it as a
*documented* variable update + comment on the instance, and count each one as a
policy-gap signal.

## Drill 5 — the silent stuck state (the one that pages you at month-end)

**Inject:** drill 2's flaky server, but returning 502 forever.

**Expected:** retries exhaust → dead-letter job. Nothing visible in any inbox: the
instance is frozen invisibly (Phase 4, lesson 05's 22:40 scenario).

**Verify & recover:** `incident_client.py` triage groups the cause; fix the URL/
service; `retry-all` revives with a fresh budget. **Standing defence:** alert on
`deadletter-jobs count > 0` (Phase 9).

## The five-line health check

```bash
# open instances, oldest first          — anything ancient?
curl -su rest-admin:test "$B/runtime/process-instances?sort=startTime&order=asc&size=5"
# dead letters                          — must be 0
curl -su rest-admin:test "$B/management/deadletter-jobs" | jq .total
# timer jobs due in the past            — executor keeping up?
curl -su rest-admin:test "$B/management/timer-jobs?dueBefore=$(date -u +%FT%T)" | jq .total
# deepest pools                         — staffing vs inflow
curl -su rest-admin:test -X POST "$B/query/tasks" -H 'Content-Type: application/json' \
  -d '{"candidateGroup":"credit-ops","unassigned":true}' | jq .total
```
