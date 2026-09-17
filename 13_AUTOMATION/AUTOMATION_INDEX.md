# AUTOMATION INDEX

Status: CURRENT V1+ AUTOMATION INDEX
Canonical protocol: `03_PROTOCOLS/AIOS_AUTOMATION_PROTOCOL_V1.md`

Automation is allowed only inside the effective authority scope:

`Owner Policy → Root Bot → Delegated Bot → Tool/Action`

## Current classes

| Action class | Automation status |
|---|---|
| Read-only / reversible work | Autonomous when within delegated scope |
| Bounded internal mutation | Autonomous when explicitly authorized and auditable |
| External communication | Autonomous only when owner policy explicitly delegates the capability and scope |
| Irreversible / high-impact action | Requires explicit policy-level authorization and remains subject to safety/platform constraints |

Every automation must be bounded, logged, evidence-backed, tied to acceptance criteria, and recoverable/reversible where feasible.

## Historical note

The former universal `R0/R1/R2/R3` approval matrix is historical/superseded for V1+. Do not use it as the current automation policy.