---
doc_id: HTS-PLN-001
title: HatchSide project plan
project: HatchSide
doc_type: Project plan
version: "0.1"
status: Draft
date: '2026-11-05'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-11-05'
  author: Amish Chadha
  change: First draft at the kit 1.9.1 upgrade (stage P3), for option A
---

# HatchSide project plan

HatchSide is at stage P3 (TRL 3, proof of concept on paper). The next gate is Amish's decision on the concept choice and on the open calls in HTS-DEC-001; nothing from P4 on starts under the TRL 3 cap (`.kit/PHASE.yaml`). The decision requested: confirm option A, the tripod and hand winch, as the concept (HTS-OPT-001, HTS-DDR-003, proposed, awaiting Amish), and say whether to approach the candidate partners. Method: STANDARDS sections 19 and 23.

## Workstreams

Table 1. Workstreams.

| Workstream | Owner (role) | Deliverable | Status |
| --- | --- | --- | --- |
| Problem and requirements | Design lead | PRB, URS, PRS, RTM | Done for P3; URS is a desk draft pending a co-design partner |
| STEM check and calculations | Design lead | STM, CAL-001, `sizing.py`, `stem_check.py` | Done for P3; two reviewer follow-ups in HTS-STM-001 |
| Concept options | Design lead | OPT, DDR-003 | Done; proposed, awaiting Amish |
| Detailed CAD of every option | Design lead | `cad/src/model.py` at D3, `cad/fidelity.json`, drawings, STEP, STL | Done for options A and B |
| Build plan (paper) | Design lead | BLD-001, sheets 101 to 112 | Done; a plan, never a build record |
| Regulatory, feasibility, risk, market | Design lead | REG, FEA, RSK, MKT | First pass done; several rows "to assess" |
| Partner outreach | Amish | Co-design partner (municipal sewer department, biogas programme) | Not started; none agreed |
| Prototype build, proof load, corrosion test | Local fabricator, test house | TRL 4 work | Planned only; on hold under the P3 cap |

## Resources needed

Table 2. Resources.

| Resource | Deliverable | Effort | Estimated cost (USD) |
| --- | --- | --- | --- |
| Design lead time for partner review and revisions | Updated URS, PRS and BOM | 5 to 10 working days (estimate) | Not costed (own time) |
| Parts for one prototype | Built kit at TRL 4 | One build | 2,838 (BOM estimate; supplier quotes to get) |
| Fabrication, galvanizing and welding | Made parts | Quote needed | To assess |
| Proof-load test with a competent person | Proof load to 1.5 times SWL (PR-004) | One day (estimate) | To assess |
| Coupon test for corrosion | PR-011 | Weeks (estimate) | To assess |
| Legal and standards review | G2, G5, G6, G12 in HTS-REG-001 | To assess | To assess |

## Stage gates

Table 3. Stages (P4 to P6 on hold while the stage cap is P3).

| Stage | Gate criteria | Status |
| --- | --- | --- |
| P0 Scaffold | Problem, pitch and first concept | Done (2026-09-30) |
| P1 Concept | Concept document, first requirements | Done (2026-10-03) |
| P2 Concept review | TRL 2 decisions recorded | Done (2026-10-03) |
| P3 Proof of concept on paper | STEM check, concept options, URS and PRS, calculations, D3 CAD of every option, build plan, regulatory, feasibility, risk, market and plan | Done (2026-11-05); concept choice proposed, awaiting Amish |
| P4 Prototype | Build, proof load, tests | On hold (TRL cap) |
| P5 Pilot | Field trial with a partner | On hold (TRL cap) |
| P6 Release | Release gate, public repository | On hold; Amish's decision |

## Next steps and decision requested

1. Amish: confirm option A or ask for option B to be developed (HTS-DDR-003); decide on HTS-DDR-004's modelling corrections (HTS-DEC-001).
2. Amish: approve approaching the two candidate partners in HTS-PRB-001.
3. When the TRL cap is lifted: buy the winch, rope, chain and shackles with certificates (HTS-DEC-001, items 1 to 5) and write the proof-load test plan; neither is started here.

## References

- Sources for the regulatory register: HTS-REG-001, Sources.
- Sources for the market benchmarks: HTS-MKT-001, Sources.
- Sources for the problem: HTS-PRB-001 (NIOSH FACE 89-46; The Wire, 2025; OSHA news release, 2024; Forbes India, 2018; PK Safety; Hach; energypedia; Google Patents US5431248).
