---
doc_id: HTS-REG-001
title: HatchSide regulatory and standards register
project: HatchSide
doc_type: Regulatory register
version: "0.1"
status: Draft
date: '2026-11-05'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-11-05'
  author: Amish Chadha
  change: First draft at the kit 1.9.1 upgrade (stage P3), for option A with option B noted
---

# HatchSide regulatory and standards register

HatchSide is a hand-powered material-handling frame used over confined spaces, so the rules that matter most are the ones it must not be mistaken for: personnel retrieval and fall-protection equipment. Nothing in the kit is certified, nothing here is a compliance claim, and anything marked "to assess" needs a qualified reviewer before any product claim or sale. Not legal advice. Sources were checked on 2026-11-05; standard titles are as published and clauses were not read unless a row says so. Method: STANDARDS section 23.

Table 1. Regulatory and standards register.

| # | Standard or regulation | Jurisdiction | What it covers | Applicability to this design | Owner (role) | Status |
| --- | --- | --- | --- | --- | --- | --- |
| G1 | OSHA 29 CFR 1910.146(k)(3), permit-required confined spaces: retrieval systems | United States | Retrieval systems for entrants, including a mechanical retrieval device for vertical permit spaces more than 5 ft (1.5 m) deep | HatchSide moves tools and material and is never a personnel retrieval system (PR-018); the retrieval head only clips a line to a casualty and the haul is made on certified rescue gear (HTS-DDR-001, D2) | Design lead | Does not apply to the kit as designed; context for every use claim (to assess with a safety professional) |
| G2 | OSHA letter of interpretation, 25 February 2013, "Permit-Required Confined Space Rescue Retrieval Lines" | United States | Interpretation of retrieval line rules in the standard above | Listed on OSHA's page for G1; the letter was not read | Design lead | To assess |
| G3 | ANSI/ASSE Z359.4-2013, assisted-rescue and self-rescue systems, subsystems and components | United States | Personnel rescue equipment | The kit is not designed, rated or labelled for people; the labels say so (BOM line 24) | Design lead | Does not apply (by design); not read |
| G4 | EN 795, personal fall protection equipment: anchor devices (tripods are among the products listed) | Europe | Single-user anchor devices | A crew might clip a person's harness to the head; the label and the guide-only retrieval head are the controls (RSK H1) | Design lead | Does not apply by design; misuse is a hazard (RSK H1); edition not checked, to assess |
| G5 | EN 13157:2004+A1:2009, cranes: safety: hand powered cranes | Europe | Hand-powered cranes, including drum winches; excludes lifting persons | The nearest published standard for a hand-powered tripod hoist; used as guidance for the proof load, brake and labelling | Design lead | To assess (guidance, clauses not read; certification needed later for any EU sale) |
| G6 | Machinery Directive 2006/42/EC (lifting machinery and lifting accessories carry CE marking) | European Union | Placing machinery and lifting accessories on the EU market | The Directive's definition of machinery turns on the drive system, and a hand winch is driven by direct human effort; whether the tripod, winch and rope count as lifting machinery or accessories is a legal question | Design lead | To assess (certification needed later if sold in the EU) |
| G7 | EN 362:2004, personal protective equipment against falls from a height: connectors | Europe | Connectors such as the auto-locking steel connector | The connector on the retrieval head sling (BOM line 20) is bought certified to this standard; HatchSide does not make it | Design lead | Met by purchase specification (the supplier's certificate to confirm) |
| G8 | ISO 12100:2010, safety of machinery: risk assessment and risk reduction | International | Hazard identification and the order of risk reduction | HTS-RSK-001 follows its method as guidance for a non-certified tool | Design lead | Applies (as guidance) |
| G9 | Prohibition of Employment as Manual Scavengers and their Rehabilitation Act, 2013, section 7 | India | Prohibits hazardous cleaning of sewers and septic tanks by people | HatchSide helps crews stay outside; it does not change what the law requires | Co-design partner | Applies (context); legal review to assess |
| G10 | NAMASTE (National Action for Mechanised Sanitation Ecosystem), Ministry of Social Justice and Empowerment with the Ministry of Housing and Urban Affairs | India | Programme to end hazardous entry into sewers and septic tanks; urban local bodies take part | The most likely route for a municipal buyer or partner; whether this kit could be listed or funded under it is not known | Co-design partner | To assess |
| G11 | Local traffic work-zone rules for street manholes | Country and city of use | Cones, barriers and signs at an open manhole | Cones and barrier chain are in the kit (BOM line 22); the rule that applies is the city's | Co-design partner | To assess |
| G12 | Wire rope, chain and shackle standards for lifting use | Country of use | Rating and marking of the rope, chain and shackles | The BOM asks for catalogue ratings and certificates (HTS-DEC-001, items 3 and 4); no standard is named here because none was checked | Design lead | To assess |
| G13 | Safety data sheets and handling rules for digester sealant and for biogas (methane, hydrogen sulfide) | Country of use | Chemical handling and gas exposure | DomeReach applies a generic sealant by type; no product is named (HTS-DDR-001, D8) | Co-design partner | To assess |
| G14 | Equipment for flammable atmospheres (ATEX in the EU, hazardous-location rules elsewhere) | Country of use | Equipment used in explosive atmospheres | The kit makes no claim of intrinsic safety (STM S17); gas testing comes first | Design lead | To assess |
| G15 | Patents around the Bandicoot arm and gripper, and expired US5431248A | Several | Freedom to operate | The preliminary screen in HTS-PRB-001 notes three Bandicoot patents and litigation; DomeReach is a single hinge with no gripper as a design-around (HTS-DDR-001, D9) | Design lead | To assess (not a legal opinion) |

Status: to assess, applies, does not apply, met by design, certification needed later.

## Sources

- J. J. Keller and Associates, "Is there an OSHA or ANSI standard for confined space tripods?" (page dated 2026-08-20), https://jjkellercompliancenetwork.com/regsense/is-there-an-osha-or-ansi-standard-for-confined-space-tripods, checked 2026-11-05. Source for G1 (retrieval systems and the 5 ft depth rule) and for the title of ANSI/ASSE Z359.4-2013 (G3).
- OSHA, interlinking page for 29 CFR 1910.146(k)(3)(i), https://www.osha.gov/laws-regs/interlinking/standards/1910.146(k)(3)(i)/all, checked 2026-11-05. Lists the 25 February 2013 letter of interpretation (G2); the regulation text itself could not be fetched on that date.
- SIR Safety, "EN 795," https://www.sirsafety.com/en-795, checked 2026-11-05 (no edition year given). Source for G4.
- Estonian Centre for Standardisation and Accreditation, "EVS-EN 13157:2004+A1:2009 Cranes: Safety: Hand powered cranes," https://evs.ee/en/evs-en-13157-2004-a1-2009-consolidated, checked 2026-11-05. Valid from 2009-10-08; scope covers drum winches and excludes lifting persons (G5).
- RISE, "CE marking of lifting accessories and lifting machinery," https://ri.se/en/what-we-do/services/ce-marking-lifting-accessories-and-lifting-machinery, checked 2026-11-05 (G6).
- Standards Ireland, "I.S. EN 362:2004," https://shop.standards.ie/en-ie/standards/en-362-2004-345746_saig_cen_cen_790805/, checked 2026-11-05 (G7).
- New Zealand Building Performance, "ISO 12100:2010 Safety of machinery," https://codehub.building.govt.nz/resources/iso-121002010, checked 2026-11-05 (G8).
- Drishti IAS, "NAMASTE Scheme: nationwide survey of sewer and septic tank workers" (dated 17 December 2025), https://www.drishtiias.com/state-pcs-current-affairs/namaste-scheme-nationwide-survey-of-sewer-and-septic-tank-workers/print_manually, checked 2026-11-05 (G9, G10; the 2013 Act's section 7).
- Press Information Bureau, Government of India, release of 17 December 2024, https://pib.gov.in/PressReleasePage.aspx?PRID=2085141, checked 2026-11-05 (G10).
- Directive 2006/42/EC; Regulation (EU) 2023/1230; ISO 12100:2010; EN 13157; EN 362; EN 795: titles and scope as published. Clauses are to be read with a qualified reviewer before any compliance claim.
