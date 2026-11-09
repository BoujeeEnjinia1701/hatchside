---
doc_id: HTS-PRB-001
title: HatchSide problem statement
project: HatchSide
doc_type: Problem statement
version: "0.4"
status: Draft
date: '2026-11-05'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-30'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-10-03'
  author: Amish Chadha
  change: Populated to TRL 2; budget worded as a value-engineering target; open questions answered (HTS-DDR-001)
- version: "0.3"
  date: '2026-10-03'
  author: Amish Chadha
  change: TRL 3; safety section added; first candidate partners recorded
- version: "0.4"
  date: '2026-11-05'
  author: Amish Chadha
  change: Kit 1.9.1 upgrade (stage P3); users-and-needs and stakeholder tables added (feed HTS-URS-001)
---

# HatchSide problem statement

Cleaning, sampling and retrieval jobs in sewers, tanks and digesters are still done by sending a person inside. The air in these spaces can kill in seconds, and it kills the rescuers too.

## The problem

Deaths follow a pattern: one worker enters to clean or free something, collapses, and others follow. In a 1989 Michigan case, five family members died one after another in a manure pit ([NIOSH FACE 89-46](https://stacks.cdc.gov/view/cdc/164363)). In India, most sewer and septic tank victims audited had no safety equipment ([The Wire, 2025](https://m.thewire.in/article/rights/more-than-90-workers-who-died-while-cleaning-sewers-didnt-have-safety-gears-govt)), and in the US repeated tank cleaning deaths followed a failure to test the atmosphere before entry ([OSHA, 2024](https://www.osha.gov/news/newsreleases/region6/07082024)).

Existing tools cover parts of the job. The Bandicoot robot cleans manholes with a pneumatic arm, but beta units cost about INR 10 to 12 lakh to make ([Forbes India](https://www.forbesindia.com/article/startups-special-2018/bandicoot-genrobotics-robot-that-scoops-out-filth-from-sewers/50401/1)). Commercial confined-space tripods with winches cost about USD 5,850 to 6,120 and are built to lower and retrieve people ([PK Safety](https://pksafety.com/products/3m-dbi-sala-confined-space-aluminum-tripod-w-winch-83010)). Sludge samplers exist but work alone ([Hach](https://www.hach.com/p-sampler-water-core-sludge-judge-standard-capacity-34-diameter/2194300)). What is missing is a low-cost, open frame that carries many non-entry tools, so that the default for routine jobs becomes staying outside.

## Users and context

Table 1. Users and needs (desk research, to confirm with co-design partners; the needs feed HTS-URS-001).

| User type | Goals and needs | Typical use scenario | Pain points and challenges |
| --- | --- | --- | --- |
| Sanitation and septic tank workers | Clear a blockage, take a sample or recover a dropped item without going down; kit they can carry on foot or by handcart | A crew of two or three at a street manhole or household septic tank, often informal work with little or no safety gear | No gas detection or rescue gear; cost of any kit; heavy loads on narrow lanes; tools that need training |
| Municipal and utility crews | Fast set-up on routine desilting and inspection; one kit for several jobs; kit that survives daily use | Sewer network, pump station and drain rounds from a truck, several sites a day | Traffic at the opening; short job windows; maintenance by their own workshop |
| Farm families and biogas technicians | Service and reseal a household fixed-dome digester from the opening, without entering a dome that holds methane and hydrogen sulfide | A technician with one helper at a 0.5 to 0.6 m dome opening, on foot or by motorbike | Small opening; digester up to about 2.5 m deep; no workshop; very low budget |
| Oil, gas and industrial tank contractors | Sample and loosen residues from the hatch before any entry decision | A crew at a storage tank roof hatch or frac tank, with permits and gas monitors already in place | Flammable atmospheres; hatch height above ground; rules on equipment used at the hatch |
| Safety and rescue teams (secondary) | A way to clip a line to a casualty from the rim without entering, with the haul made on certified rescue gear | A standby team at a permit-required space with its own rescue equipment | Time; kit that must not be mistaken for certified rescue equipment |

## Stakeholders

Table 2. Stakeholders.

| Stakeholder group | Role or interest | Engagement needed |
| --- | --- | --- |
| Sanitation workers and their organisations | Users and the people most at risk; they decide whether the kit is used | Co-design partner (none agreed; HTS-DDR-001, D11); walk through each head at a mock opening |
| Municipal sewer and sanitation departments | Buyers and operators of routine crews; responsible under the 2013 Indian act and the mechanised sanitation programme | Candidate partner (none agreed); confirm opening sizes, depths and routines |
| Household biogas programmes and technicians | Users of DomeReach; programme funders | Candidate partner (none agreed); confirm digester openings and sealant practice |
| Industrial tank operators and contractors | Users under permit-required confined space rules | Review of the retrieval head and equipment rules before any use claim |
| Regulators and standards bodies (labour, machinery, traffic) | Set the rules the kit must not be mistaken for breaking (lifting equipment, personnel rescue, confined space entry) | Read HTS-REG-001; ask a regulator or notified body before any sale or claim |
| Local fabricators and galvanizers | Make and mend the kit; they decide whether it can be built locally | Review the drawings and the build plan (BLD-001) for buildability |
| Traffic and public at the opening | Bystanders and passing vehicles at street manholes | Rim guard, cones and barrier chain; local work-zone rules to assess |
| Amish Chadha (Design Molecule) | Owner; decides scope, budget and release | Decisions listed in HTS-DEC-001 and docs/REVIEW.md |
| Funders and open hardware community | Fund trials; reuse and improve the design | Open licence (CERN-OHL-S-2.0); public repository after Amish's release decision |

## Operating environment

- Street manholes about 0.6 m (24 in) across and tank hatches on roofs or sides; depths to about 10 m (33 ft) assumed for a first version (estimate).
- Toxic, flammable or oxygen-deficient atmospheres inside the space, including hydrogen sulfide, methane and carbon monoxide.
- Traffic on streets, uneven ground, mud and sewage splash at the rim.
- Outdoor use in heat and monsoon rain; corrosive sewage and sludge on every wetted part.
- Crews of two to four people, with a handcart or small vehicle for transport.

## Constraints

- Value-engineering target of USD 5,000 for the tripod, winch and the five tool heads including DomeReach (a hypothetical control target, not a spending limit).
- Hand winch only; no engine at the hatch.
- Kit carried in loads of 25 kg (55 lb) or less each (target).
- Every tool head worked from outside the space; no design step may require entry.
- Open design: hardware under CERN-OHL-S-2.0, any software under MIT.

## Out of scope

- Planned human entry and the equipment that supports it (breathing apparatus, entry permits).
- Powered robots and articulated robotic arms.
- Gas detection electronics, which crews should buy as certified instruments.
- Sewer jetting and vacuum trucks.
- Building or repairing digester structures beyond sealing from the opening.

## Prior work

| Prior work | What it does | Gap for these users | Source |
| --- | --- | --- | --- |
| Genrobotics Bandicoot | Pneumatic, remote-controlled manhole cleaning robot with a sweeping arm | High cost and a powered robot; the preliminary screen notes three patents and ongoing litigation around its arm and gripper | [link](https://www.forbesindia.com/article/startups-special-2018/bandicoot-genrobotics-robot-that-scoops-out-filth-from-sewers/50401/1) |
| 3M DBI-SALA confined space tripod and winch | Aluminium tripod of 2.13 or 2.74 m with a retrieval winch for entry and rescue | Built for lowering people in; costs about USD 5,850 or more and carries no work tools | [link](https://pksafety.com/products/3m-dbi-sala-confined-space-aluminum-tripod-w-winch-83010) |
| US5431248A confined space lowering and retrieving apparatus | Tripod or quadruped frame for lowering and retrieving personnel through manways | Expired patent for a personnel system; free prior art for a frame | [link](https://patents.google.com/patent/US5431248) |
| Sludge Judge sampler | Core sampler for settled solids depth in tanks | Single task and hand-held; limited depth and no frame | [link](https://www.hach.com/p-sampler-water-core-sludge-judge-standard-capacity-34-diameter/2194300) |
| Biogas plant maintenance guidance | Guidance that digester maintenance should be done from above ground where possible | Guidance only; no tools for small household digesters | [link](https://energypedia.info/wiki/Maintenance_of_a_Biogas_Plant) |

## Co-design

A sanitation workers' organisation or municipal sanitation department that already runs mechanised cleaning programmes, plus a biogas programme with field technicians for DomeReach, so heads are shaped by the real jobs and real openings.

First candidates to approach (none agreed): a municipal sewer department in India running mechanised cleaning under the national mechanised sanitation programme, and a household biogas programme with field technicians in India or Nepal (HTS-DDR-001, D11).

Co-design checklist:

- [ ] Confirm the five tasks with crews who do them today.
- [ ] Measure common manhole, tank hatch and digester openings in the first region.
- [ ] Walk through each head at a mock opening with the crew.
- [ ] Confirm that crews will carry a certified gas detector.

## Safety

> **Safety:** HatchSide lifts loads over an open confined space whose air can kill in seconds. It is an open engineering reference for a material-handling frame, never certified rescue, lifting or fall-protection equipment. Nobody enters the space, and the winch never lifts or lowers a person. Test the air at the opening with a certified gas detector before and during work, keep sparks and flames away from sewers and digesters, guard the opening from traffic and falls, and never stand under a raised load.

## Answered questions

The scaffold's open questions were answered at the TRL 2 review (HTS-DDR-001) and are tracked in the design decisions register (HTS-DEC-001):

- Tasks that still force entry: none of the five routine tasks needs entry with the five heads; any task found in co-design that does gets a new head, not an entry.
- The retrieval head stays, as a clip-on guide only; the haul is made with certified rescue equipment.
- The frame carries 150 kg; WellSling's 400 to 600 kg loads need their own frame.
- DomeReach uses a generic roller-applied digester sealant, named by type.
- First trial hosts are recorded as candidates to approach, above.
