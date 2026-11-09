---
doc_id: HTS-URS-001
title: HatchSide user requirements
project: HatchSide
doc_type: User requirements
version: "0.1"
status: Draft
date: '2026-11-05'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-11-05'
  author: Amish Chadha
  change: First user requirements, written at the kit 1.9.1 upgrade from the users and stakeholders in HTS-PRB-001 Tables 1 and 2; desk draft, not yet reviewed with a co-design partner
---

# HatchSide user requirements

What the people who use and live around the kit need, written from their side. They come from the users and stakeholders in HTS-PRB-001 (Tables 1 and 2) and from the five tasks the kit exists for. They are a desk draft: no crew, utility or biogas programme has reviewed them yet, and the co-design partners in HTS-PRB-001 are candidates, none agreed. Each need traces to one or more product requirements in HTS-PRS-001 (matrix: HTS-RTM-001). Method: STANDARDS section 22.

Table 1. User requirements.

| ID | Category | Title | Need | Priority | Source |
| --- | --- | --- | --- | --- | --- |
| UR-001 | Safety | Nobody goes in | Routine clearing, sampling, raking and recovery are done from outside the space, so no job needs a person to enter | High | Sanitation workers, municipal crews (PRB Table 1) |
| UR-002 | Performance | Fits the openings we meet | The kit sets up over, and every tool passes through, the common street manhole, tank hatch and digester opening | High | Sanitation workers, biogas technicians (PRB Table 1) |
| UR-003 | Performance | Works at our depths | Tools reach the working depth of sewers, tanks and household digesters, and the crew knows how deep the tool is | High | Municipal crews, biogas technicians |
| UR-004 | Performance | Does the five jobs | One kit clears silt, takes samples, rakes, clips a line to a casualty and reseals a digester dome | High | All user types (PRB Table 1) |
| UR-005 | Usability | Up in minutes | A crew of two or three sets the kit up before the job in a few minutes, without special tools | Medium | Municipal crews |
| UR-006 | Logistics | Carried by the crew | The kit travels in loads one person can carry, on foot, by handcart or on a motorbike | High | Sanitation workers, biogas technicians |
| UR-007 | Cost | Affordable | A municipality or a farmer cooperative can afford one, well under the price of a commercial tripod and winch | High | All user types, funders |
| UR-008 | Safety | Never a lifeline, never tips | The kit cannot be mistaken for equipment that lifts people, holds its load without failing, and does not tip if the rope pulls sideways | High | Sanitation workers, regulators, safety teams |
| UR-009 | Durability | Lasts in sewage and sun | Parts survive sewage splash, hydrogen sulfide air, heat and monsoon rain | Medium | Municipal crews, industrial contractors |
| UR-010 | Usability | Changes heads fast | A crew changes from one tool head to another in about a minute without tools | Medium | Municipal crews |
| UR-011 | Maintenance | Made and mended locally | A local workshop with a welder and drill can make and mend every part from stock sizes | Medium | Local fabricators, municipal workshops |
| UR-012 | Safety | Guards the opening | The open manhole is guarded against falls in and against traffic while the kit is set up | Medium | Municipal crews, public at the opening |
| UR-013 | Usability | Easy for one person to work | One person can raise and lower a full tool from the winch without strain | Medium | Sanitation workers |
| UR-014 | Performance | Samples tell us where | A sample can be tied to the depth it came from, to within about the length of the sampler | Low | Municipal crews, industrial contractors |

Priority: High (weight 3 in concept scoring), Medium (2), Low (1).

## Notes

- UR-008 is a safety need first: the winch lifts material and tool heads only. Nobody is lowered or raised on it, and the retrieval head only clips a line to a casualty, with the haul made on certified rescue equipment (HTS-DDR-001, D2).
- UR-007 is read against the USD 5,000 value-engineering target in `project.yaml`, a hypothetical control target and not a spending limit (STANDARDS section 18).
- UR-009 cannot be closed on paper: corrosion life is a TRL 4 test.
