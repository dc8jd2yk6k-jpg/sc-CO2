# Supercritical-CO₂-Assisted Intercalation of Layered Superconductors
## Research program and ranked ideas

*Version 1.0, 2026-11-03. Shared protocols: [`protocols.md`](protocols.md). References: [`references.md`](references.md) (keys such as `R1` are used throughout). Data tables: [`../data/`](../data). Planning and analysis tools: [`../tools/`](../tools).*

---

## 0. Executive summary

The challenge asks which hosts, intercalants and scCO₂ processing regimes give **measurable Tc increases** in layered superconductors, compared against bulk-host baselines and the best intercalated phases. Our literature search (Nov 2026) found **no report of scCO₂ intercalation into any superconducting host**. scCO₂ has been used to intercalate clays (R44, R45), to exfoliate graphite and MoS₂ (R46, R47), to deposit metals (R43) and as an electrochemical medium (R41, R42). So the area is open. Three findings shape every idea below.

1. **CO₂ is a reagent, not an inert solvent.** The chemistries behind the current FeSe records cannot be run in CO₂. Alkali/NH₃ forms carbamate and reduces CO₂. Alkali/ethylenediamine forms carbamate. LiOH hydrothermal routes carbonate. n-BuLi carboxylates. This rules them out, but it also opens a new design space: **CO₂-stable molecular reductants**, **separate sources for electrons and charge-balancing ions**, **electrochemistry in CO₂-expanded electrolytes**, and **strong oxidants in a medium that cannot be oxidised** ([§2.2](#22-chemical-compatibility-co2-as-a-reagent), [`data/co2_compatibility.csv`](../data/co2_compatibility.csv)).
2. **Process pressure does not compress the lattice.** Practical scCO₂ pressures (8–60 MPa) are about 10³ times smaller than the GPa pressures that change Tc in FeSe or cuprates. The useful levers are elsewhere:
   - CO₂ density sets the solvation and chemical potential of the guest.
   - Transport is fast: solute diffusivity is about 10⁻⁸ m² s⁻¹ and viscosity 20–80 µPa s, roughly 10 times faster than liquid electrolytes, and there is no surface tension.
   - CO₂ itself pre-swells the galleries.
   - The solvent can be removed without collapsing the galleries, because there is no capillary stress.
3. **In FeSe, Tc stops rising with spacing at about 45–50 K once d ≳ 9 Å** (R9; (TBA)₀.₃FeSe ≈ 50 K is the bulk record, R1). Beating that benchmark needs something beyond more spacing. Options: (i) control doping *n* independently of spacing *d*; (ii) put something in the gallery that helps pairing, such as polar phonons or high dielectric screening, which is how monolayer FeSe/SrTiO₃ reaches about 65 K (R11, R12); or (iii) lock in a compressed state metastably (pressure-quench, R24). The idea set is built to test these three routes separately.

**Top four ideas** (full ranking in [§3](#3-ranking)):

| Rank | ID | Idea | Primary host → target |
|---|---|---|---|
| 1 | **I-01** | Redox-buffered equilibrium electron doping with CO₂-stable molecular donors | FeSe → bulk Tc > 50 K; first Tc(n) map at fixed gallery chemistry |
| 2 | **I-02** | Electrochemical organic-cation intercalation in CO₂-expanded electrolytes, followed by supercritical washing and drying | FeSe (TBA⁺ family) → ≥ 50 K onset with ≥ 90 % shielding in ≥ 10 mg crystals |
| 3 | **I-03** | Polar-phonon / high-ε co-intercalants that mimic the substrate interface in bulk, with a guest-isotope test | FeSe → > 50 K (stretch 55–60 K) |
| 4 | **I-04** | Pillar-then-dope sequential co-intercalation to tune spacing d and doping n independently | FeSe, SnSe₂, TaS₂ → beyond 50 K / 7.6 K / 4.6 K |

---

## 1. Baselines, benchmarks and success targets

Full table with references: [`data/benchmarks.csv`](../data/benchmarks.csv). "Beyond benchmark" means bulk superconductivity under the acceptance rule in [`protocols.md` §P5](protocols.md#p5-tc-metrology-and-acceptance-rule): shielding ≥ 50 % after demagnetisation correction, plus zero resistance or a specific-heat anomaly, in ≥ 2 independent samples.

| Host (bulk Tc) | Best modified phase (route) | Benchmark to beat | Program target (stretch) |
|---|---|---|---|
| β-FeSe (8.5–9 K) | (TBA)₀.₃FeSe ≈ 50 K onset (electrochem., R1); Li/NH₃, Li/en, Li/pyridine 43–45 K; (Li,Fe)OHFeSe 40–43 K | 50 K bulk | **> 50 K** (55 K; aspirational 60–65 K, the FeSe/SrTiO₃ monolayer level) |
| 1T-SnSe₂ (non-SC) | Li/THF ≈ 7.6 K (R35); {CoCp₂}₀.₃ ≈ 6.1 K (R34) | 7.6 K | **> 7.6 K** (9 K) |
| 2H-TaS₂ (0.8 K) | hydrate/organic ≈ 4.6 K (R28); CTA⁺ ≈ 3.7 K (R27); pyridine ≈ 3.5 K (R26) | 4.6 K | **> 4.6 K** (≥ 6 K, about 7× the host) |
| 2H-MoS₂ (non-SC) | AₓMoS₂ ≈ 6.9 K bulk (R31); gated ≈ 10.8 K (surface, R32) | 6.9 K bulk | **> 6.9 K bulk** (> 10.8 K) |
| 2M-WS₂ (8.8 K) | made by oxidative deintercalation (R33) | 8.8 K | **≥ 8.8 K** with narrower transition; any doping-driven rise |
| 2H-NbSe₂ (7.2 K) | organic cations only *lower* Tc (R61) | 7.2 K | **any reproducible increase** |
| β-HfNCl (insulator) | Li₀.₄₈(THF)ᵧHfNCl ≈ 25.5 K (R38) | 25.5 K | > 25.5 K |
| Hg-1223 (133–135 K) | fluorinated 138 K (R22); PQP-retained 151 K (R24, preprint) | 138 K chemical / 151 K PQP | **> 138 K** chemical; **> 151 K** after PQP |
| Bi-2212 (85–95 K) | I₂/HgI₂/organic intercalates keep Tc roughly unchanged at Δd 3.6 Å to several nm (R17, R18) | Tc retention | Bring underdoped crystals to optimum (≥ +5 K) by staging control |

---

## 2. Design rules for scCO₂-assisted intercalation

### 2.1 Fluid physics: what the knobs actually do

Values from [`tools/scco2.py`](../tools/scco2.py) (Span–Wagner EOS via CoolProp). Diffusivity is a Wilke–Chang estimate for a 150 cm³ mol⁻¹ solute, about the size of a metallocene. Full grid: [`data/process_windows.csv`](../data/process_windows.csv).

| T (°C) | P (MPa) | ρ (kg m⁻³) | Giddings δ (MPa^½) | η (µPa s) | D_solute (10⁻⁸ m² s⁻¹) |
|---|---|---|---|---|---|
| 40 | 10 | 629 | 11.0 | 48 | 1.6 |
| 40 | 20 | 840 | 14.7 | 79 | 1.0 |
| 60 | 15 | 604 | 10.6 | 46 | 1.8 |
| 60 | 25 | 787 | 13.8 | 70 | 1.2 |
| 80 | 30 | 746 | 13.1 | 64 | 1.3 |
| 120 | 40 | 693 | 12.2 | 59 | 1.6 |

For comparison, DMF at 25 °C has η ≈ 800 µPa s, and solute D ≈ 10⁻⁹ m² s⁻¹.

Consequences used throughout:

- **Density sets solvent power and guest activity.** Solubility follows Chrastil, ln S = k ln ρ + a/T + b (R48), with k typically 3–10 for organometallics. So a 20 % density change moves solubility, and therefore the guest's chemical potential in a closed cell, by a factor of about 2–6. Basis of **I-05**.
- **Isopycnic design.** Each temperature is run at the pressure that gives the same density: `python -m tools.scco2 isopycnic --rho 800 --T 40 60 80 100` gives 16.4, 26.4, 36.5 and 46.6 MPa. This separates thermal activation (Arrhenius) from solvation; the two are confounded in ordinary isobaric runs.
- **Pressure is not compression.** The highest pressure here, 60 MPa, is 0.06 GPa. FeSe needs about 9 GPa to reach about 37 K (R10). CO₂ also solidifies at about 0.5 GPa near room temperature. Any compressive Tc gain has to come from a separate DAC step (the PQP module, [`protocols.md` §P7](protocols.md#p7-pressure-quench-pqp-amplifier-module)).
- **Venting is a processing step.** Fast depressurisation exfoliates layered crystals; it is the basis of scCO₂ exfoliation (R46). For bulk single crystals, vent isothermally above 31 °C at ≤ 0.2 MPa min⁻¹, so the fluid goes from supercritical to gas without a liquid meniscus. This is how the supercritical-drying advantage is realised ([`protocols.md` §P3](protocols.md#p3-standard-scco2-run-sequence)).

### 2.2 Chemical compatibility: CO2 as a reagent

Full table: [`data/co2_compatibility.csv`](../data/co2_compatibility.csv). Rules:

- **Excluded:** alkali and alkaline-earth metals, solvated electrons, organolithiums, Grignard reagents, arene radical anions, hydrides, N-heterocyclic carbenes, hydroxide/alkoxide guests (they carbonate), and NH₃ or primary/secondary amines (carbamates, except deliberately in I-07).
- **Allowed:** tertiary amines and pyridines (dry), ethers, glymes, crown ethers, nitriles, ketones, amides, sulfoxides, sulfones, cyclic carbonates, metallocenes, metal β-diketonates, quaternary ammonium/phosphonium salts (with cosolvent or fluorinated anions), halogens, O₃/XeF₂ (hardware permitting), and H₂ (≤ 80 °C, no base).
- **Conditional:** amidines and guanidines (DBU, TMG) turn ionic with CO₂ plus alcohol or water (R58); use them only dry.
- **Water** turns CO₂ into carbonic acid (pH ≈ 3 at process pressure). Dry everything to < 1 ppm H₂O / O₂ (in-line purifier), except where water activity is deliberately controlled (I-06a).

### 2.3 The redox window

The one-electron reduction of CO₂ sits at about −2.7 V vs Fc⁺/Fc (−2.21 V vs SCE in DMF, R55), roughly 0.5 V vs Li⁺/Li. On catalytically active surfaces it is less negative, so the practical cathodic limit is set by a blank CV ([`protocols.md` §P2](protocols.md#p2-mandatory-blanks-and-controls)). Every reductant and every applied potential must stay positive of that limit. [`data/redox_ladder.csv`](../data/redox_ladder.csv) lists the usable ladder:

| Rung | E vs Fc⁺/Fc (V) | ≈ V vs Li⁺/Li |
|---|---|---|
| CoCp\*₂ | −1.94 | 1.3 |
| CoCp₂ | −1.33 | 1.9 |
| Cr(C₆H₆)₂ | ≈ −1.2 | 2.0 |
| CrCp\*₂ | ≈ −1.0 | 2.2 |
| FeCp\*₂ | ≈ −0.5 | 2.7 |

This gives about 1.5 V of tunable reducing power with at least 0.7 V of margin to CO₂ reduction.

**Key hypothesis built on this:** Li/NH₃ (≈ 0 V vs Li) **overshoots**. It can drive FeSe toward conversion (Fe extrusion, Fe vacancies, Li₂Se). A ladder that stops at 1.3–2.7 V vs Li may allow electron doping without that damage. This is a falsifiable advantage of the CO₂-compatible chemistry, tested in I-01.

On the oxidising side, CO₂ cannot be oxidised further. So I₂ < magic blue (+0.70 V) < NO⁺ (+0.87–1.00 V) < XeF₂/O₃ can be used without the solvent being attacked. That medium is rarely available for acceptor intercalation (I-08, I-09).

### 2.4 Mandatory controls (every idea)

1. **CO₂-only blank:** host in neat scCO₂ at the most aggressive run condition. Must show no change in c, Tc or mass. CO₂ itself enters some galleries (R45).
2. **Cosolvent-only blank.**
3. **Conventional-liquid twin:** same guest, same T and time, liquid solvent, on a sister crystal cut from the same host piece.
4. **Host baseline** measured on the same instruments (FeSe: Tc 8.5–9 K, c = 5.52 Å).
5. **Impurity-phase screen** for known parasitic superconductors and magnets: K–Fe–Se (about 30 K), (Li,Fe)OHFeSe (about 42 K), Fe₇Se₈ (ferrimagnetic), Li₂CO₃ / alkali carbonates (from CO₂), and metallocene decomposition products.

---

## 3. Ranking

Scoring (1–5) follows the stated preferences. Weights: **Tc upside vs benchmark 0.30**, **experimental tractability and protocol clarity 0.25**, **validation by Tc + XRD 0.15**, **scCO₂-specific advantage 0.15**, **novelty 0.15**. Computational screening carries no weight; every idea is defined by synthesis and characterization protocols.

| Rank | ID | Title | Focus | Tc | Tract. | Valid. | scCO₂ | Novel | **Score** |
|---|---|---|---|---|---|---|---|---|---|
| 1 | I-01 | Redox-buffered equilibrium doping with CO₂-stable donors | FA2 · FA1 | 4 | 4 | 5 | 5 | 5 | **4.45** |
| 2 | I-02 | CO₂-expanded-electrolyte electrochemical intercalation + supercritical finishing | FA1 · FA3 | 4 | 5 | 5 | 4 | 3 | **4.25** |
| 3 | I-03 | Polar-phonon / high-ε co-intercalants + guest-isotope test | FA3 · FA2 | 5 | 3 | 4 | 4 | 5 | **4.20** |
| 4 | I-04 | Pillar-then-dope sequential co-intercalation (tunes d and n separately) | FA3 · FA2 | 4 | 4 | 5 | 4 | 4 | **4.15** |
| 5 | I-05 | Density-programmed guest activity: staging, kinetics, pressure-swing pumping | FA1 | 3 | 4 | 5 | 5 | 4 | **4.00** |
| 6 | I-06 | Monolayer-like layer separation + doping in bulk TMDs; scCO₂ deintercalation route to 2M-WS₂ | FA2 · FA3 | 4 | 3 | 5 | 4 | 4 | **3.90** |
| 7 | I-07 | In-gallery CO₂ fixation of labile amine/NH₃ co-intercalants | FA3 | 2 | 4 | 4 | 5 | 5 | **3.70** |
| 8 | I-08 | scCO₂-carried F/O anion loading of Hg-1223 + pressure-quench | FA2 | 5 | 2 | 4 | 3 | 4 | **3.65** |
| 9 | I-09 | Acceptor (hole) intercalation of NbSe₂ in a medium that cannot be oxidised | FA2 | 3 | 3 | 5 | 3 | 5 | **3.60** |
| 10 | I-10 | H₂-fugacity-controlled spillover protonation | FA2 · FA1 | 3 | 3 | 4 | 4 | 4 | **3.45** |
| 11 | I-11 | CO₂-philic fluorous cation superlattices: the low-ε end of the dielectric range | FA3 | 2 | 3 | 4 | 5 | 4 | **3.30** |

*Sensitivity:* raising the Tc-upside weight to 0.45 moves I-03 to rank 1 and I-08 to rank 4. **Recommended portfolio:** I-01 and I-02 as the core, I-03 as the high-reward bet, I-05 as the enabling platform, and I-08 as the long shot.

---

## 4. Ideas

Each idea lists: hypothesis, why scCO₂, hosts and targets, reagents, process window, protocol, characterization with go/no-go, risks and mitigations, and what is learned even if Tc does not rise. Shared procedures (P1–P8) are in [`protocols.md`](protocols.md).

---

### I-01 · Redox-buffered equilibrium electron doping with CO₂-stable molecular donors
**Focus:** electronic-structure engineering (FA2); processing parameters (FA1). **Score 4.45.**

**Hypothesis.** The scCO₂ solution contains three things:
- a buffered donor couple, D/D⁺ (e.g. CoCp\*₂ / [CoCp\*₂][BArF]);
- an alkali cation solubilised by a crown ether or glyme, M⁺(L) (Li⁺·12-crown-4, Na⁺·15-crown-5, K⁺·18-crown-6);
- a few mol % ether cosolvent.

Together these fix the electrochemical potential of both electrons, E = E°(D⁺/D) + (RT/F) ln([D⁺]/[D]), and ions, via ln a(M⁺). At equilibrium the host takes up Mₓ(L)ᵧ with an electron count n set by that potential, not by reaction time. This gives:
- **uniform bulk doping**, with no gradient from a surface-limited reaction;
- **no overshoot into conversion**, because the ladder stops at 1.3–2.7 V vs Li;
- **a full Tc(n) dome at fixed gallery chemistry**, which has not been measured for bulk intercalated FeSe.

Prediction: Tc(n) peaks at n\* ≈ 0.1–0.15 e/Fe (by analogy with K-dosed and gated FeSe, R13, R14). At n\*, low-disorder phases with d ≈ 9–12 Å reach or exceed 50 K.

**Why scCO₂.**
- Metallocenes and fluorinated (BArF) salts dissolve.
- High diffusivity and near-zero surface tension speed equilibration in mm-scale crystals.
- CO₂ is inert toward the whole donor ladder, with ≥ 0.7 V margin, and automatically excludes over-reducing reagents.
- A supercritical wash removes excess reagent without capillary collapse.

**Hosts and targets.**

| Host | Target |
|---|---|
| β-FeSe | Tc > 50 K bulk |
| FeSe₀.₉S₀.₁ (nematicity suppressed) | Tc > 50 K bulk; tests whether nematicity matters after doping |
| 1T-SnSe₂ | > 7.6 K |
| 2H-TaS₂ | > 4.6 K |

**Reagents.**
- Donors: CoCp\*₂, CoCp₂, CrCp\*₂, FeCp\*₂ and their [D⁺][BArF⁻] or [D⁺][PF₆⁻] salts.
- Alkali salts: M[BArF] or MTFSI.
- Ligands: 12-crown-4 / 15-crown-5 / 18-crown-6, or diglyme / TMEDA.
- Cosolvent: THF or 2-MeTHF, 2–10 mol %.

**Process window.** 40–80 °C; ρ = 700–900 kg m⁻³ (about 12–36 MPa); 6–72 h; a recirculating loop through a crystal basket.

**Buffer-capacity design rule.** 10 mg FeSe is 74 µmol Fe. Doping to n = 0.15 consumes 11 µmol of D. To keep the potential drift below 25 mV at 60 °C (66 mV per decade), start with ≥ 30 µmol each of D and D⁺, which is about 1.2 mM in a 25 mL cell. Check solubility by cloud point (P1).

**Protocol.**
1. Phase behaviour (P1). Confirm a single phase for donor + salt + crown + cosolvent at each (T, ρ). Record cloud-point pressure.
2. Ladder design. Use 4 donors × buffer ratios [D⁺]/[D] of 0.01, 0.1, 1, 10 and 100. This spans about −0.4 to −2.1 V vs Fc in steps of ≈ 70 mV.
3. Load pre-characterised FeSe crystals (1–20 mg; Tc, c and RRR recorded) into a PEEK mesh basket in a glovebox. Seal, transfer, purge, then pressurise with purified CO₂ (P3).
4. Dose the reagent solution through an HPLC pump. Recirculate. Determine the time to equilibrium either by in-situ XRD (P4) or by sacrificial crystals pulled at 2, 6, 24 and 72 h. The criterion is c and composition constant within error.
5. Wash isobarically with ≥ 10 cell volumes of CO₂ + 5 % THF, then ≥ 10 volumes of neat CO₂. Vent isothermally at ≤ 0.2 MPa min⁻¹ (P3).
6. Characterise:
   - XRD (00l) series: c, Δd, CV(l·d), impurities.
   - ICP-OES for M and Co. Co tells whether D⁺ co-intercalated.
   - CHN; TGA-MS for ligand content.
   - XPS Co 2p to distinguish Co(III) cobaltocenium from Co(II).
   - Hall coefficient.
   - SQUID ZFC/FC and R(T) (P5).
   - ARPES electron-pocket area on a subset, for n via Luttinger count.

**Go/no-go.**
- G1 (month 3): a clear c-axis change and a bulk Tc ≥ 30 K at some rung.
- G2 (month 6): a Tc(n) curve with ≥ 5 points at fixed L, and samples rational by CV(l·d) < 0.75 %.
- G3 (month 12): Tc,onset > 50 K under the bulk rule.

**Controls.** No donor (M⁺ only; no intercalation expected). Donor only (D⁺ pillaring; links to I-04). Liquid-THF twin. CO₂ blank.

**Risks and mitigations.**

| Risk | Mitigation |
|---|---|
| Slow ion transfer in a low-ε fluid | Raise cosolvent to the CO₂-expanded-liquid regime (10–30 mol %) |
| D⁺ intercalates instead of M⁺ | Use the bulkiest donor (CoCp\*₂) and crown-solvated M⁺; if D⁺ still enters, analyse the result as I-04 |
| Conversion at the strongest rung | Watch in-situ XRD for Fe(110) and Li₂Se reflections; stop at the previous rung |
| Trace O₂ / H₂O | In-line purifier; check ≤ 1 ppm with an inline sensor |

**What we learn regardless.** The first equilibrium (open-circuit-like) Tc(n) isotherm of a bulk FeSe intercalate. A potential scale for FeSe electron doping, which goes into [`data/redox_ladder.csv`](../data/redox_ladder.csv). A tested reagent set that I-03, I-04 and I-06 reuse.

---

### I-02 · CO₂-expanded electrolytes for electrochemical organic-cation intercalation, with supercritical finishing
**Focus:** processing parameters (FA1); exotic molecular guests (FA3). **Score 4.25.**

**Hypothesis.** The bulk FeSe benchmark, (TBA)₀.₃FeSe ≈ 50 K (R1), is made electrochemically in liquid DMF. Two things limit it:
- moving a bulky cation through mm-scale crystals in a viscous electrolyte, which risks gradients and mixed-phase cores;
- taking the solvent out afterwards, which can degrade the crystals.

Expanding the electrolyte with CO₂ (CO₂ mole fraction 0.3–0.6) lowers viscosity several-fold and raises diffusivity while keeping enough polarity to dissolve salts; electrochemistry in scCO₂/MeCN is demonstrated (R41, R42). Ending with a salt-free rinse, then a supercritical wash and an isothermal vent, removes solvent without capillary collapse. Predictions:
- intercalation reaches 90 % of completion (t₉₀) **≥ 3× faster**;
- **phase-pure, homogeneous** crystals (rational 00l series, narrow rocking curves);
- holding the potential lets doping be tuned along the organic-cation series, giving **Tc,onset ≥ 50 K with ≥ 90 % shielding** (stretch ≥ 52 K).

**Why scCO₂.** Gas-expanded liquids (R59) are the only medium whose viscosity and dielectric constant can be tuned continuously at constant composition of the dissolved salt. The supercritical end-state gives drying without collapse, which ordinary electrolytes cannot.

**Guests.**
- Cations: TBA⁺, tetrapropyl-, tetrapentyl- and tetrahexylammonium, CTA⁺, [P₄₄₄₄]⁺, [PYR₁₄]⁺, cobaltocenium.
- Anions: BF₄⁻, PF₆⁻, TFSI⁻.
- Solvents: DMF, MeCN, PC.

**Cell.** A three-electrode high-pressure cell (Hastelloy body, PEEK insulators, sapphire window). Working electrode: FeSe crystal held by a Au clip. Counter: Pt behind a glass frit. Reference: Ag/Ag⁺ calibrated in situ against decamethylferrocene, which is known to behave well in scCO₂/MeCN (R42).

**Process window.** 35–45 °C; 3–8 MPa (expanded-liquid regime) for the intercalation step; then 40 °C at 12–15 MPa (single phase) for washing. Salt 0.05–0.2 M, kept below the salt cloud point during expansion, which is measured by EIS conductivity and the view cell.

**Protocol.**
1. Blank CVs in the CO₂-expanded electrolyte on Pt, glassy carbon and an FeSe crystal. Define the CO₂-reduction onset, then set the potential cap 150 mV positive of it.
2. Intercalate potentiostatically in steps from OCV toward the cap. Record charge Q(t). End when current falls to the blank background. A galvanostatic variant runs at C/50 with the same cap.
3. Rinse in situ: switch the feed to salt-free solvent (5 volumes), then to CO₂-rich expanded solvent, then to neat scCO₂ (≥ 20 volumes) at 40 °C / 15 MPa. Vent at ≤ 0.2 MPa min⁻¹.
4. Characterise:
   - XRD on both faces and after cleaving at mid-thickness (homogeneity); rocking curves.
   - Raman map of the cleaved face.
   - CHN/ICP and coulometric efficiency.
   - SQUID / R(T) / specific heat on ≥ 10 mg pieces.

**Controls.** A sister crystal from the same boule run in liquid DMF with the same potential programme. CO₂ blank on FeSe. Gas analysis of the headspace (GC) for CO, and IR for formate/oxalate, to quantify parasitic CO₂ reduction.

**Metrics and go/no-go.**
- G1: the CO₂-expanded run reaches the same phase as the DMF run (Δc ≤ 0.05 Å) with faradaic efficiency ≥ 70 %.
- G2: t₉₀ ≥ 3× shorter, and 10–90 % transition width ≤ 2 K.
- G3: Tc,onset ≥ 50 K, shielding ≥ 0.9, Cp anomaly present.

**Risks and mitigations.**

| Risk | Mitigation |
|---|---|
| CO₂ reduction overlaps the intercalation potential | Run transport-limited "soak" steps at open circuit in CO₂, and potentiostatic steps after partial depressurisation. Fallback: supercritical CHF₃- or CH₂F₂-expanded electrolytes, as in the Southampton work on supercritical hydrofluorocarbons (R64) |
| Salt precipitates as an antisolvent effect during the wash | Rinse salt-free first (step 3) |
| Over-intercalation or decomposition | Q-capped steps |

**What we learn regardless.** Whether bulky-cation intercalation is transport-limited or thermodynamics-limited, and transferable rules for organic-cation intercalation of thick crystals.

---

### I-03 · Polar-phonon / high-dielectric co-intercalants: the FeSe/SrTiO₃ interface reproduced in bulk
**Focus:** co-intercalation and exotic guests (FA3); electronic-structure engineering (FA2). **Score 4.20 (highest Tc upside).**

**Hypothesis.** Above d ≈ 9 Å, FeSe layers are electronically 2D and more spacing adds nothing (R9). The remaining gap between bulk intercalates (≤ 50 K) and monolayer FeSe/SrTiO₃ (gap closes at about 60–65 K) is attributed to two features of the substrate (R11, R12):
- coupling to polar, high-frequency (≈ 80–100 meV), mostly forward-scattering interface phonons;
- strong dielectric screening.

A gallery filled with **strongly polar, high-ε molecules whose IR-active modes lie at 60–120 meV**, sitting 3–4 Å from the Se plane, could supply an analogous boost. Supporting evidence: polar organic co-intercalants raise Tc in electron-doped 1T-SnSe₂ across the board (R60).

**Decisive experiment: a guest-isotope effect.** Make pairs of samples with the same n and d, using deuterated or ¹³C/¹⁸O-labelled co-intercalants (DMSO-d₆, EC-d₄, PC-¹³C=O). A reproducible ΔTc between pairs would prove that guest modes take part in pairing. Threshold: ≥ 0.3 K, beyond the 2σ spread of ≥ 5 pairs. This test is not possible in FeSe/SrTiO₃.

**Why scCO₂.** Polar co-intercalants are delivered as cosolvents in the CO₂-expanded regime at controlled activity, and the same activity can be held across the series. Excess solvent is removed by a supercritical wash, so the sample is not left in a solvated state of unknown composition.

**Co-intercalant matrix** (dielectric constant ε; relevant modes):

| Co-intercalant | ε | Role / relevant modes |
|---|---|---|
| 1,4-dioxane | 2.2 | non-polar control |
| THF | 7.5 | |
| pyridine | 12.4 | |
| acetone | 21 | |
| MeCN | 37 | C–C ≈ 114 meV |
| sulfolane | 43 | |
| DMSO | 47 | C–S ≈ 87 meV; S=O ≈ 130 meV |
| propylene carbonate | 64 | ring ≈ 88 meV |
| ethylene carbonate | 90 | ring ≈ 89 meV |
| N-methylformamide | 182 | |

Doping is held fixed by I-01 buffering, or by the I-04 pillar-then-dope route. Each sample is still measured for n.

**Process window.** 40–70 °C (ethylene carbonate melts at 36 °C); co-intercalant 5–20 mol % in CO₂; ρ 700–850 kg m⁻³; 24–72 h.

**Protocol.**
1. Validate the method first on 1T-SnSe₂, where a polar-guest effect is known (R60). Expect Tc ordering that follows ε.
2. Transfer to FeSe.
3. For each sample: XRD (d, CV), composition (n), Raman/IR of the intercalate to locate guest modes, SQUID/R(T).
4. Cleave the best phases for ARPES. Look for replica bands displaced by the guest-mode energy.
5. Run the isotope pairs.

**Analysis.** Regress Tc on n, d, ε, dipole moment μ, and the integrated IR oscillator strength in 60–120 meV. Hypothesis passes if ε or IR strength carries significant weight after controlling for n and d.

**Go/no-go.**
- G1 (SnSe₂): Tc rises monotonically with ε at fixed n (Spearman ρ ≥ 0.7).
- G2 (FeSe): ≥ 2 K spread in Tc that n and d cannot explain.
- G3: Tc > 50 K bulk, or a guest-isotope effect.

**Risks and mitigations.**

| Risk | Mitigation |
|---|---|
| Polar molecules solvate M⁺ differently and change n | Measure n every time and regress on it |
| Ethylene carbonate is reduced (≈ 0.8 V vs Li) by the CoCp\*₂ rung | Use CoCp₂ and weaker rungs with EC/PC |
| N-methylformamide has an N–H; amides are not nucleophilic enough to form carbamates, but this is unverified | Check by CO₂ + NMF blank with IR |

**What we learn regardless.** A dielectric-environment descriptor for Tc in layered superconductors. Even a null result (no ε dependence at fixed n and d) narrows explanations of the interface enhancement to effects that need the substrate itself.

---

### I-04 · Pillar-then-dope sequential co-intercalation: tuning d and n independently
**Focus:** co-intercalation (FA3); charge transfer and strain (FA2). **Score 4.15.**

**Hypothesis.** With a single guest, d and n are coupled:
- a bulky cation sets d, but its footprint caps loading at about 0.25–0.35 per formula unit;
- a small cation dopes but leaves d small.

A two-step route separates them:
- **Step A** (scCO₂ soak). Neutral, CO₂-soluble CoCp₂ ionises itself on entry and leaves CoCp₂⁺ pillars in open galleries, with partial doping.
- **Step B** (same sealed cell, no air exposure). Top up with Li⁺/Na⁺ + e⁻ through the I-01 redox buffer or I-02 electrochemistry, into galleries that are already open.

This gives a 2D map Tc(n, d) on one host. Reversing the order (dope first, then pillar) tests whether the result depends on path. Mixing pillars (CoCp₂⁺ with CoCp\*₂⁺) tunes d in about 1 Å steps.

**Why scCO₂.** Neutral metallocenes are soluble and move quickly. Both steps run in one cell by sequential dosing, with nothing between them. Excess CoCp₂ is washed out supercritically, leaving only intercalated species.

**Hosts and targets.**

| Host | Benchmark | Target |
|---|---|---|
| FeSe | 50 K | > 50 K |
| 1T-SnSe₂ | CoCp₂ 6.1 K, Li/THF 7.6 K | > 7.6 K |
| 2H-TaS₂ | 4.6 K | > 4.6 K |
| β-HfNCl, pre-lithiated outside CO₂ with n-BuLi | 25.5 K | > 25.5 K |

HfNCl is a cautionary branch: LiₓHfNCl may reduce CO₂, so it needs a CO₂ blank before any run.

**Process window.**
- Step A: 60–120 °C, 20–35 MPa, CoCp₂ 2–5× stoichiometric, 24–96 h. Conventional solution routes need days at reflux.
- Step B: as in I-01.

**Characterization.**
- XRD CV(l·d) is the key output. Two-guest galleries can stay mixed (rational series), separate into stages, or interstratify randomly (CV > 0.75 %).
- Co:M ratio by ICP, tracked to detect exchange (M⁺ displacing CoCp₂⁺) versus co-occupation.
- ²H/⁷Li solid-state NMR for local environments, where available.

**Go/no-go.**
- G1: a rational co-intercalated phase with Co:M ratio stable over ≥ 3 runs.
- G2: Tc(n) at two different fixed d values.
- G3: beyond-benchmark Tc on at least one host.

**Risks and mitigations.**

| Risk | Mitigation |
|---|---|
| Exchange instead of co-intercalation | Lower M⁺ activity; use a bulkier pillar (CoCp\*₂⁺) |
| Segregated domains | Anneal in fluid at 60–80 °C; segregation is itself informative |
| HfNCl–CO₂ reactivity | If the blank fails, run Step B under Ar pressure and use scCO₂ only for Step A |

**What we learn regardless.** The separate ∂Tc/∂n and ∂Tc/∂d on one host, which is the core of a predictive Tc(n, d) relation (§5).

---

### I-05 · Density-programmed guest activity: staging, kinetics and pressure-swing pumping (platform)
**Focus:** processing-parameter optimisation (FA1). **Score 4.00.**

**Hypothesis.** In a closed cell holding a fixed amount of guest, CO₂ density sets the guest's fugacity through solvation (Chrastil k ≈ 3–10). So **pressure is a continuous, reversible, in-situ control of guest activity at constant temperature**. It replaces the two-zone temperature gradient used in classic vapour-phase staging. Two sweeps separate the contributions:
- isothermal ρ sweeps give thermodynamics (activity → stage thresholds);
- isopycnic T sweeps give kinetics (activation energy at constant solvation).

The result is a transferable processing map, plus stage-pure phases with distinct Tc. A second hypothesis: **pressure-swing pumping**, cycling ρ between two supercritical states (e.g. 850 ↔ 500 kg m⁻³ at 50 °C, i.e. 27.0 ↔ 11.0 MPa), speeds up the advancing intercalation front. Each cycle swells edge galleries with CO₂ and lets guest in, then partly drives CO₂ out while the guest stays.

**Model systems** (chosen because staging or slow kinetics is already documented):

| System | Why chosen | Target |
|---|---|---|
| I₂ → Bi-2212 / Bi-2223 | Stage-1 / stage-2 IBi2212 are known; I₂ is highly CO₂-soluble; doping effect on Tc of a few K (R17) | Bring underdoped crystals to optimum (≥ +5 K) |
| CoCp₂ → 1T-SnSe₂ | Tc depends on loading and polytype (R34) | Stage/polytype-pure phase, Tc > 6.1 K |
| Pyridine / 4-picoline → 2H-TaS₂ | Classic intercalation that takes weeks (R26) | Same ≈ 3.5 K phase in ≤ 1/5 of the conventional time |

**Measurements.**
- Time-resolved in-situ synchrotron XRD of the 00l series in a high-pressure cell (P4).
- Gravimetric uptake on a magnetic-suspension balance, corrected for buoyancy using the EOS density.
- UV-Vis of the fluid through a sapphire window, giving guest concentration (I₂ ≈ 500 nm).

**Analysis.**
- Fit JMAK/Avrami exponents and shrinking-core diffusion; extract k(T, ρ).
- Get Eₐ from isopycnic runs and ∂ln k/∂ln ρ from isothermal runs.
- Plot uptake against fugacity (from the Chrastil fit, [`tools/scco2.py`](../tools/scco2.py)) to locate stage transitions.

**Process window.** 35–120 °C; 8–45 MPa; ρ 300–900 kg m⁻³ (see [`data/process_windows.csv`](../data/process_windows.csv)).

**Go/no-go.**
- G1: stage selected by pressure alone at fixed T and loading, reversible over ≥ 2 cycles.
- G2: pressure-swing t₉₀ ≤ 0.5× static at the same time-averaged ρ.

**Risks and mitigations.**

| Risk | Mitigation |
|---|---|
| Guest adsorbs on cell walls | Passivate the cell; measure fluid concentration directly |
| Pressure-swing cracks crystals | Limit amplitude; monitor rocking curves |

**What we learn regardless.** Quantitative processing maps that every other idea uses to choose T, ρ and time.

---

### I-06 · Monolayer-like layer separation plus doping in bulk TMDs; scCO₂ deintercalation route to 2M-WS₂
**Focus:** charge transfer and strain (FA2); co-intercalation (FA3). **Score 3.90.**

**(a) 2H-TaS₂ (0.8 K → target > 4.6 K, stretch ≥ 6 K).** Isolated (monolayer) TaS₂ superconducts at higher Tc than bulk, because its CDW is weaker. The best intercalates combine layer separation with doping and water or organic co-guests (4.6 K, R28). Approach:
- CoCp₂⁺ pillars from scCO₂, which separate the layers and dope them;
- polar co-guests from the I-03 set;
- water activity controlled precisely through scCO₂'s known water solubility, to reach hydrate phases reproducibly.

Note that wet CO₂ is acidic, so protonation is a second, possibly useful, doping channel; it is quantified by TGA-MS.

Diagnostics: suppression of the CDW, seen as the disappearance of superlattice reflections and the R(T) kink, alongside the Tc rise.

**(b) 2H-MoS₂ (non-SC → target > 6.9 K bulk, stretch > 10.8 K).**
- Electrons come from CoCp\*₂, with K⁺(18-crown-6) as the cation top-up (I-01 chemistry).
- **Watch the phase.** CO₂ is reported to promote 2H → 1T conversion in MoS₂ (R47). Track 2H/1T fraction by Raman (J₁/J₂/J₃ at ≈ 150/220/330 cm⁻¹) and XPS (Mo 3d shift ≈ 0.9 eV).
- The useful control is the 2H/1T ratio as a function of T and ρ (R47). The target is electron-doped 2H at about 0.1 e/Mo, the doping where gating gives the 10.8 K maximum (R32), with layers separated by pillars.

**(c) 2M-WS₂ (8.8 K).** The 8.8 K phase is made by oxidatively deintercalating KₓWS₂ in acidic aqueous oxidant (R33). The proposed alternative uses anhydrous I₂ in scCO₂, at constant I₂ activity under I-05 control:
- KₓWS₂ + x/2 I₂ → 2M-WS₂ + x KI;
- KI is removed by a CO₂-expanded MeCN wash.

Expected: fewer protons and water taken up, narrower transitions. Partial electron doping can then be re-introduced in situ.
Target: ≥ 8.8 K with ΔT(10–90) ≤ 0.3 K; any rise driven by doping is beyond benchmark.

**Go/no-go.**
- (a) Tc ≥ 4 K bulk within 6 months.
- (b) 2H fraction ≥ 80 % at n ≥ 0.05 e/Mo.
- (c) Phase-pure 2M by XRD with Tc ≥ 8.5 K.

**Risks and mitigations.**

| Risk | Mitigation |
|---|---|
| 2H → 1T conversion in MoS₂ | Treat it as a mapped variable |
| Acid attack on TaS₂ under wet CO₂ | Cap water at sub-saturation |
| I₂ over-oxidation of WS₂ layers | Use I-05 activity control with in-situ XRD |

---

### I-07 · In-gallery CO₂ fixation: locking labile amine/NH₃ co-intercalants as carbamate networks
**Focus:** co-intercalation and exotic guests (FA3). **Score 3.70.**

**Hypothesis.** FeSe phases co-intercalated with NH₃ or amines (Tc 43–45 K, R3–R6) are metastable: they lose the co-intercalant at room temperature or in air (R62). CO₂'s reactivity toward N–H, normally the reason those routes are excluded, can be used on purpose. Controlled exposure to liquid or supercritical CO₂ (−20 to 40 °C) converts gallery NH₃, NH₂⁻ and amines into carbamate / ammonium-carbamate networks. No redox step is involved, so the electron count on FeSe is unchanged. Three effects are predicted:
1. the co-intercalant is immobilised as a non-volatile, H-bonded ionic network;
2. d increases modestly, e.g. 8.3 → ≥ 9.5 Å for Li/NH₃, onto the ≈ 45 K plateau of Tc(d);
3. the Se environment shifts through N–H···Se and N–H···O hydrogen bonds.

**Targets.** Tc retained at ≥ 43–45 K after storage at room temperature and cycling to 100 °C (baseline: the unfixed phase degrades). Secondary: +1 to 3 K for phases with d < 9 Å.

**Protocol.**
1. Prepare Liₓ(NH₃)ᵧFe₂Se₂ by the standard liquid-NH₃ route at −78 °C, plus Li/en and Li/HMDA analogues.
2. Transfer cold under Ar into a pre-cooled high-pressure cell. Admit CO₂ at a controlled rate, with the dose in mol CO₂ per mol N.
3. Follow by in-situ IR/Raman (carbamate ν_as(CO₂⁻) ≈ 1550–1600 cm⁻¹) and XRD.
4. Characterise: TGA-MS (release of NH₃ and CO₂), ¹³C/¹⁵N solid-state NMR, SQUID/R(T); repeat after ageing.

**Go/no-go.** Carbamate formed inside the gallery (IR + d change) with Tc ≥ 40 K retained after 7 days at 295 K.

**Risks.** CO₂ may oxidise or deintercalate the doped host (Li₂CO₃ / formate). Detect by XRD and Tc loss; mitigate with a lower temperature and limited CO₂ dose.

---

### I-08 · scCO₂-carried F/O anion loading of Hg-1223, plus pressure-quench
**Focus:** charge transfer and strain (FA2). **Score 3.65 (long shot, highest absolute Tc).**

**Hypothesis.** In Hg-1223 the dopant anions sit in the HgOδ layer.
- Fluorination raised ambient Tc to about 138 K (R22) and to about 166 K at 23 GPa (R23).
- A pressure-quench protocol retained 139–151 K at ambient pressure in oxygenated Hg-1223, but retention degrades above about 200 K (R24, preprint).

Proposed: load anions at low temperature (60–200 °C) in a carrier fluid that cannot be oxidised, scCO₂ with dissolved XeF₂ (fluorine) or O₃ (oxygen). Fluorination is exothermic, and the dense fluid absorbs the heat. The aim is uniform, near-optimal δ without Hg loss. The resulting material is better pressure-quench feedstock.

**Targets.**
1. Ambient Tc > 138 K, chemical route only.
2. PQP-retained Tc > 151 K.
3. Retention to higher temperature (> 200 K) if F-loaded Hg layers really are more ordered.

Secondary host: La₂CuO₄ + O₃/scCO₂ at 40–80 °C for staged La₂CuO₄₊δ, target > 45 K.

**Protocol.**
1. Reset Hg-1223 (Tc 133–135 K) to low δ by an Ar anneal.
2. scCO₂ + XeF₂, at 0.05–0.5 F per Cu, 80–150 °C, 15–25 MPa, 2–24 h. Use a Monel or Hastelloy cell with PTFE seals. Vent through an alumina / soda-lime scrubber.
3. XRD (a, c; Rietveld occupancy of the Hg-layer anion site), iodometric/TGA δ, SQUID Tc.
4. On the best composition, run PQP following the published protocol: quench from 10–30 GPa at 4.2 K, then measure Tc on warming and its retention limit ([`protocols.md` §P7](protocols.md#p7-pressure-quench-pqp-amplifier-module)).

**Go/no-go.** G1: ≥ 136 K chemical with no Hg loss (ICP). G2: PQP retention ≥ 145 K.

**Risks.** scCO₂ adds little over vapour-phase XeF₂, hence its low scCO₂ score; first test whether XeF₂ dissolves at useful levels. Hg-1223 crystals are small and hard to obtain. Toxicity (Hg, HF): [`protocols.md` §P8](protocols.md#p8-safety).

---

### I-09 · Acceptor (hole) intercalation of 2H-NbSe₂ in a medium that cannot be oxidised
**Focus:** charge transfer and strain (FA2). **Score 3.60.**

**Hypothesis.** Electron-donating organic cations lower NbSe₂'s Tc, which drops as the hole concentration falls (R61). The other direction, bulk hole doping, is essentially unexplored, because strong oxidants destroy ordinary solvents. scCO₂ allows a controlled oxidant ladder, I₂ < IBr < ICl < Br₂ < magic blue [BArF] < NO⁺[BArF], at fixed activity. The aim is to find a window where the host is oxidised (anion intercalation or charge-transfer surface complexes) before Se is attacked. Target: any reproducible Tc > 7.2 K; CDW (33 K) changes are the diagnostic.

**Calibration sub-aim (low risk).** Self-intercalated Nb₁₊ₓSe₂ has reduced Tc. Mild I₂/scCO₂ oxidation may remove gallery Nb as soluble Nb iodides, bringing Tc back toward 7.2 K. This validates the oxidant-ladder method.

**Protocol.** Step up the ladder at 40–80 °C, with a fixed-activity oxidant at each rung. In-situ XRD distinguishes intercalation (new 00l / Δc) from etching (loss of intensity). ICP of the fluid tracks Nb and Se loss. Stop at the first rung that etches.

**Go/no-go.** Δc > 0.1 Å, or a Hall-sign change, without Se loss > 1 %.

**Risks.** NbSe₂'s high work function makes oxidative intercalation hard; success probability is low and was scored accordingly. Any positive result would be novel.

---

### I-10 · H₂-fugacity-controlled spillover protonation
**Focus:** charge transfer (FA2); processing parameters (FA1). **Score 3.45.**

**Hypothesis.** H₂ mixes completely with scCO₂, so its fugacity can be set precisely (0.1–10 MPa partial pressure) in a single fluid phase. Steps:
- Pd seeds are deposited on crystal edges by scCO₂ chemical fluid deposition (Pd(hfac)₂ + H₂, R43).
- The seeds split H₂; H spills over into the galleries as H⁺ + e⁻, electron-doping the host.
- Protonated FeSe made by ionic-liquid gating reaches about 41–44 K (R15).

Because doping at equilibrium is set by H₂ fugacity and T, this gives contact-free, bulk doping that can be trimmed. The same final trim step applies to pillared hosts from I-04 (target > 50 K), and to TaS₂ and SnSe₂.

**Process window.**
- Pd deposition: 60–80 °C, 15 MPa, 0.5–1 MPa H₂.
- Protonation: 25–80 °C, 0.1–5 MPa H₂ in 15–25 MPa total, 1–7 days.

**Side reactions to monitor.** CO₂ hydrogenation to HCOOH or CO; keep T ≤ 80 °C, no base, and analyse by GC. FeSe + H₂ → H₂Se; detect with lead-acetate paper and GC-SCD, and track Se loss by ICP.

**Go/no-go.** Hydrogen uptake by TGA-MS / NMR, with a Tc shift monotonic in H₂ fugacity.

---

### I-11 · CO₂-philic fluorous / siloxane cation superlattices: the low-ε end of the dielectric range
**Focus:** exotic molecular guests (FA3). **Score 3.30.**

**Hypothesis.** Quaternary ammonium cations with perfluoroalkyl or siloxane tails dissolve in scCO₂, unlike their hydrocarbon analogues. They self-assemble in galleries as bilayers with d = 20–40 Å, turning bulk crystals into stacks of effectively isolated monolayers. The fluorous spacer has very low ε (≈ 2) and low polarisability. Combined with I-03 (ε up to 180), this lets the dielectric dependence of Tc be mapped across nearly two orders of magnitude of gallery ε at matched n.

**Targets.**

| Host | Target |
|---|---|
| 2H-TaS₂ | Monolayer-like Tc ≥ 3.5–4 K |
| NbSe₂ | Ising-type in-plane Hc₂ in bulk crystals |
| FeSe | Test whether Tc falls for d > 12 Å (R9) using a guest that does not dope |

Water-in-CO₂ microemulsions stabilised by perfluoropolyether surfactants are a further delivery route for ionic reagents.

**Risks.** Fluorous cations may be too large to enter without electrochemical drive; fallback is I-02 cells with fluorous electrolytes. Synthesis effort is high.

---

## 5. Cross-cutting analysis: a predictive Tc(n, d, h, ε) map

Focus area 2 asks for predictive relations between structure and superconductivity. Every sample in every idea is logged with the same descriptors ([`data/sample_log_template.csv`](../data/sample_log_template.csv)):

| Descriptor | Primary measurement | Secondary |
|---|---|---|
| d, Δd, stage, CV(l·d) | XRD 00l ([`tools/xrd.py`](../tools/xrd.py)) | in-situ XRD, PDF |
| n (e per formula unit) | composition (ICP/CHN) × degree of ionisation (XPS) | Hall; ARPES pocket area |
| anion height h(Se) / bond angle | single-crystal XRD / PDF | Raman A₁g shift |
| ε, μ, IR strength 60–120 meV of the guest | literature + IR of the intercalate | isotope pairs |
| Tc onset / 50 % / zero / width; shielding | SQUID + R(T) ([`tools/tc.py`](../tools/tc.py)) | specific heat, µSR |

**Analysis plan.**
1. Fit Tc = f(n) at fixed d (I-01).
2. Fit Tc = f(d) at fixed n (I-04).
3. Fit the residual against h(Se) and the Se–Fe–Se bond angle (optimum ≈ 1.38 Å and ≈ 109.5°, R56, R57) and against ε/IR (I-03).
4. A relation counts as **predictive** if, after fitting on ≥ 70 % of samples, it predicts the held-out samples' Tc within ±2 K (FeSe) or ±0.5 K (TMDs).
5. Falsification: if ε has no significant coefficient in the FeSe data, the bulk interface-mimicry route (I-03) is dropped.

---

## 6. Plan and stage gates

| Phase (months) | Work | Gate |
|---|---|---|
| 0–3 | Build the reactor and in-situ XRD cell ([`protocols.md`](protocols.md) P1–P4); host baselines; CO₂ / cosolvent blanks; first I-05 maps with I₂/Bi-2212 and CoCp₂/SnSe₂; I-02 blank CVs | Blanks clean; Tc and c of hosts reproduced |
| 3–9 | I-01 FeSe ladder; I-02 CO₂-expanded vs DMF on sister crystals; I-03 validated on SnSe₂ | I-01 G2 (Tc(n) ≥ 5 points); I-02 G2 |
| 9–18 | I-03 on FeSe with isotope pairs; I-04 2D maps; I-06 TMDs; I-07 | Any bulk FeSe Tc > 50 K, or TMD beyond benchmark |
| 12–24 | Long shots: I-08 (Hg-1223 + PQP), I-09, I-10, I-11; PQP applied to the best FeSe intercalates (SC-II > 50 K at about 12 GPa, R8) | > 151 K PQP or > 138 K chemical (I-08) |

## 7. Program-level risks

| Risk | Impact | Mitigation |
|---|---|---|
| CO₂ reacts with reduced hosts (carbonate / formate) | False negatives; impurity phases | Mandatory CO₂ blank at the most reducing rung; FTIR and XRD screens for Li₂CO₃ and formate |
| Metallocene or salt solubility too low in neat CO₂ | No intercalation | Move to CO₂-expanded liquids (10–30 mol % cosolvent), keeping the transport benefit |
| Filamentary or impurity "superconductivity" misread as a new phase | False positives | Acceptance rule P5; impurity screen §2.4 (5); ≥ 2 samples |
| Intercalates are air-sensitive | Data loss | Glovebox mounting; sealed capillaries / domes for XRD; airtight PPMS pucks (P6) |
| Results depend on the host batch | Irreproducibility | One sister-crystal protocol per comparison; host lot recorded in every log |
