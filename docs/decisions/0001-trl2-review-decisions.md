---
doc_id: HTS-DDR-001
title: HatchSide TRL 2 review decisions
project: HatchSide
doc_type: Design decision record
version: "1.0"
status: Released
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "1.0"
  date: '2026-10-03'
  author: Amish Chadha
  change: TRL 2 review decisions D1 to D12, decided under Amish's 2026-10-03 pre-approval
---

# 0001: TRL 2 review decisions

- **Date:** 2026-10-03
- **Status:** accepted. Decided by Amish Chadha under his pre-approval of 2026-10-03: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost."

## Context

The scaffold (HTS-PRB-001, HTS-PRC-001 and HTS-REQ-001 at v0.1) left five open questions and twelve proposed requirements. Populating the concept to TRL 2 needed answers on the working load, the role of the retrieval head, the materials, the winch, the rope and the depth DomeReach must reach. Every answer below was the recommendation of the populate pass, and each is decided under the pre-approval. Choices that touch safety take the conservative option, and each says what evidence would relax it.

## Options considered and decisions

*Table 1. Decisions D1 to D12.*

| # | Question | Options | Decision | Why |
| --- | --- | --- | --- | --- |
| D1 | Safe working load of the frame | 150 kg for tool heads; 400 to 600 kg to share the frame with WellSling | **150 kg**, proof-loaded to 1.5 times | Tool heads and a full grab weigh well under 100 kg; a 600 kg frame would push every pack past 25 kg. WellSling needs its own heavier frame or a later heavy variant (shared tripod block not adopted at this rating) |
| D2 | Retrieval head in the kit | Keep it; drop it | **Keep it, as a clip-on guide only.** It steers an auto-locking connector onto a line already on a casualty; the haul is made with certified rescue equipment, never with the HatchSide winch | Conservative safety option. Relaxing it would need the frame, winch and rope certified to a personnel standard (for example EN 795 class B and EN 1496) by a notified body |
| D3 | Winch | Hand winch with automatic load brake; ratchet winch; powered winch | **Two-speed hand winch with an automatic (Weston-type) load brake, rated 450 kg on the first layer** | No engine at the hatch (constraint); the brake holds the load when the crank is released |
| D4 | Rope | 6 mm stainless wire rope; synthetic rope | **15 m of 6 mm 7x19 grade 316 wire rope** with a swaged thimble eye | Sewage and grit wear synthetic rope; stainless resists corrosion; 15 m covers R3 with turns left on the drum |
| D5 | Leg material | Aluminium tube; galvanized steel tube | **6082-T6 (or 6061-T6) aluminium square tube**, upper 60 x 60 x 4, lower 50 x 50 x 3, telescoping | Keeps packs under 25 kg; square tube takes bolted joints and a ball-lock pin without crushing |
| D6 | Steel parts | Galvanized S275; stainless | **Hot-dip galvanized S275** for the head, feet, bracket and heads; A4 stainless fasteners, pins and rope | Low cost and widely available in the first region; stainless where parts slide or thread |
| D7 | DomeReach depth for R10 | Set with a partner; assume a typical depth | **2.5 m below the rim** as the design depth until a partner digester is measured | Covers common household fixed-dome digesters; a deeper digester needs a third pole section |
| D8 | DomeReach sealant | Named product; generic | **Generic brush or roller-applied digester sealant**, named by type, never by brand | Patent and trademark screen of 2026-09-30 |
| D9 | DomeReach mechanism | Articulated arm with gripper; single hinge | **Single hinged arm worked by a pull line**, no gripper | Bandicoot patent design-around; simpler to make |
| D10 | Opening and stability requirements | Leave R2 only; add explicit checks | **Add R13** (every head passes a 560 mm opening) **and R14** (stable with the rope 10 degrees off vertical) | Makes the opening and tipping checks measurable |
| D11 | First region and co-design partner | India; United States; Nepal | **India first.** First candidate to approach: a municipal sewer department running mechanised cleaning under India's national mechanised sanitation programme. For DomeReach, first candidate to approach: a household biogas programme with field technicians in India or Nepal. Neither is agreed | Highest documented toll; existing programmes aim to end manual entry |
| D12 | Prototype cost | Hold to the USD 5,000 target; accept overruns | **Value-engineering target stays USD 5,000.** Overruns are accepted under the pre-approval; `budget_usd` is unchanged | Amish's pre-approval |

## Consequences

- HTS-REQ-001 gains R13 and R14, and R4 and R10 lose their "estimate" and "to be set" wording.
- The retrieval head is drawn and costed as a guide with a certified EN 362 connector; every document says the haul is made with certified rescue equipment.
- WellSling does not share this frame at 150 kg; its own repo decides its frame.
- The design is made constructable in HTS-DDR-002.
