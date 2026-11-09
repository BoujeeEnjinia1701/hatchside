---
doc_id: HTS-DDR-003
title: HatchSide concept selection
project: HatchSide
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-11-05'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-11-05'
  author: Amish Chadha
  change: First record, at the kit 1.9.1 upgrade; the choice is proposed, awaiting Amish
---

# 0003: Concept selection, tripod (A) or straddle-frame davit (B)

- **Date:** 2026-11-05
- **Status:** proposed, awaiting Amish. Nothing here is decided.

## Context

Kit 1.8 asks for at least two concept options with different working principles, scored against the user requirements, with the choice recorded as proposed (STANDARDS section 21). HatchSide was designed before kit 1.8, so the current design is option A and is not changed. Option B was added at this upgrade and modelled to detail level D3 beside it (HTS-OPT-001, `cad/src/model.py`).

## Options considered

- **A, tripod and hand winch.** Three telescoping legs in compression, a head sheave and a winch on one leg. USD 2,838 in parts, 9.0 min setup (estimate), heaviest load 23.7 kg, tips at 25.0 degrees.
- **B, straddle-frame davit.** A base frame, a bolted mast and a cantilever boom in bending. About USD 3,910 (estimate), a heaviest piece of 26.2 kg, tips at 46 degrees, a clear 1.8 by 2.3 m area needed.
- **A hitch-mounted or wall-mounted jib** was considered and not modelled: it needs a vehicle or wall at the opening.

Weighted scores over 15 criteria taken from the user requirements: A 160 of 180, B 138 of 180 (HTS-OPT-001, Table 2). A leads by 13.8 % of its score, outside the 10 % band.

## Decision

**Proposed, awaiting Amish:** option A stays the concept. B stays in the repository as a modelled alternative. If Amish prefers B, or wants the two kept open, say so and the requirements and BOM follow it.

The runner-up's best idea, the winch at waist height, is a suggestion for option A in HTS-DEC-001, not applied.

## Consequences

- If A is confirmed: nothing changes in the model, BOM or calculations; the requirements in HTS-PRS-001 already describe A.
- If B is chosen: a BOM, a build plan, drawings and a FMEA for B are needed, and PR-005 and PR-006 are not met without a lighter frame (80 x 80 x 4 rails, about 22 kg) and a faster joint.
- `concept_chosen` in `project.yaml` reads "proposed: A, awaiting Amish" until Amish decides.
