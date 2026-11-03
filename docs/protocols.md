# Shared experimental protocols (P1–P8)

These procedures are used by every idea in [`research_program.md`](research_program.md). The tools in [`../tools/`](../tools) carry out the calculations each protocol calls for. Every sample gets one row in [`../data/sample_log_template.csv`](../data/sample_log_template.csv).

---

## P1. Reactor, materials and phase-behaviour checks

**Hardware (minimum set).**

| Item | Specification | Purpose |
|---|---|---|
| CO₂ syringe pump | ≥ 260 mL, cooled head, ≤ 50 MPa, ±0.1 % flow | pressurisation, isopycnic set-points |
| Cosolvent / reagent pump | HPLC, ≤ 40 MPa | dosing donor/salt/cosolvent solutions |
| CO₂ purification | SFC grade (99.999 %) → in-line O₂/H₂O purifier → inline moisture/O₂ sensor (≤ 1 ppm) | reduced hosts and metallocenes are O₂/H₂O sensitive |
| Variable-volume view cell | sapphire windows, 5–30 mL, 40 MPa / 150 °C | cloud points, single-phase check |
| Reaction cells | 10–50 mL; **316 SS** for organics and metallocenes; **Hastelloy C-276 / Monel** for halogens, O₃, XeF₂, HF-forming chemistry; PEEK sample baskets; glovebox-loadable with isolation valves | intercalation runs |
| Recirculation | magnetic-drive high-pressure gear pump through the crystal bed | removes boundary-layer limits |
| Electrochemical cell (I-02) | 3-electrode, Hastelloy body, PEEK insulation, sapphire window, glass-frit counter compartment, potentiostat with EIS | CO₂-expanded electrolyte work |
| In-situ XRD cell | sapphire-tube or Be-window cell, ≤ 40 MPa / 150 °C, synchrotron transmission (30–60 keV) | kinetics, staging (P4) |
| Gravimetry (I-05) | magnetic-suspension balance, ≤ 35 MPa | uptake with buoyancy correction |
| Safety | rupture discs at ≤ 90 % of rating, polycarbonate shields, CO₂ / H₂ / H₂Se monitors as relevant | P8 |

**State-point design.** Choose T and target density, then read P from [`tools/scco2.py`](../tools/scco2.py):
```bash
python -m tools.scco2 isopycnic --rho 800 --T 40 60 80
```
```bash
python -m tools.scco2 state --T 60 --P 25 --Vb 180
```
Report every run as (T, ρ), not (T, P) alone.

**Cloud-point test** (required for every new reagent mixture):
1. Load the weighed solutes and cosolvent into the view cell under Ar.
2. Pressurise at T until one clear phase forms. Hold 15 min with stirring.
3. Decompress at ≤ 0.05 MPa min⁻¹ until the first persistent turbidity appears. That pressure is P_cloud. Repeat three times.
4. Operate at P ≥ P_cloud + 2 MPa. Log P_cloud with the composition.

**Solubility and Chrastil fit.** Measure saturation solubility by UV-Vis in the view cell or by gravimetric extraction at ≥ 3 temperatures × ≥ 4 densities. Fit with `tools.scco2.chrastil_fit`. The fitted k and a give the guest activity that I-05 uses.

---

## P2. Mandatory blanks and controls

| Control | Conditions | Acceptance |
|---|---|---|
| **CO₂-only blank** | host in neat purified scCO₂ at the most aggressive (T, ρ, time × 2) of the campaign; also with the strongest donor rung *without* cation salt | Δc < 0.01 Å; ΔTc < 0.2 K; Δm < 0.2 %; no new reflections; no carbonate/formate bands in FTIR (1350–1600 cm⁻¹) |
| **Cosolvent-only blank** | same with cosolvent at its maximum fraction | same |
| **Conventional-liquid twin** | sister crystal from the same host piece, same guest/T/time in liquid solvent | comparison only; documents the scCO₂ effect |
| **Electrochemical window** (I-02) | CV of the CO₂-expanded electrolyte on Pt, glassy carbon and an FeSe crystal, 20 mV s⁻¹ | define the CO₂-reduction onset E_red; potential cap = E_red + 0.15 V |
| **Impurity-phase screen** | XRD + magnetisation on every sample | absent: Fe, Fe₇Se₈, Li₂Se, Li₂CO₃/K₂CO₃, KₓFe₂₋ᵧSe₂, (Li,Fe)OHFeSe, crystalline metallocene |
| **Reference superconductors** | Pb (7.2 K) and Nb (9.25 K) monthly; YBa₂Cu₃O₇ (≈ 92 K) for high-T thermometry | Tc within ±0.05 K / ±0.3 K of reference |

---

## P3. Standard scCO2 run sequence

1. **Host preparation.** Cleave or cut crystals. Record mass, dimensions, baseline c, Tc (SQUID) and RRR. Pair sister crystals from the same piece for twin comparisons. Store under Ar.
2. **Loading** in a glovebox (Ar, < 0.5 ppm O₂/H₂O): crystals into a PEEK basket; solid reagents into the cell or a reservoir. Close the isolation valves.
3. **Purge.** Three cycles of CO₂ to 2 MPa and vent, at room temperature. Solid reagents do not dissolve appreciably at this density.
4. **Heat, then pressurise** to the target density, isothermally, at ≤ 1 MPa min⁻¹. Start recirculation. Dose cosolvent/reagent solutions through the HPLC pump.
5. **Hold.** Follow progress by in-situ XRD (P4) or by sacrificial crystals pulled through a sampling lock.
6. **Wash** at constant T and P:
   - ≥ 10 cell volumes of CO₂ + cosolvent, to dissolve reagents and by-products;
   - then ≥ 10 volumes of neat CO₂;
   - for electrolytes (I-02), a salt-free solvent rinse first, to avoid antisolvent precipitation.

   Collect the effluent in a cold trap for mass balance.
7. **Vent** isothermally at T ≥ 35 °C: ≤ 0.2 MPa min⁻¹ down to 1 MPa, then ≤ 0.5 MPa min⁻¹. The fluid goes from supercritical to gas without a liquid meniscus, which preserves the galleries. A *rapid* vent (> 5 MPa min⁻¹) exfoliates crystals; use it only when nanosheets are wanted.
8. **Unload** into the glovebox. Store metastable intercalates at −30 °C in the glovebox freezer.
9. **Log** every parameter (template row).

---

## P4. XRD protocols

**Ex situ, single crystals and oriented plates.**
- θ–2θ scans along c\* with Cu Kα₁, using an air-tight dome (Kapton or Be) loaded in the glovebox. Collect ≥ 4 orders of (00l).
- Fit c, the zero shift and CV(l·d):
  ```bash
  python -m tools.xrd fit --peaks 5.70 11.42 17.17 22.97 --l 1 2 3 4 --refine-zero --host FeSe
  ```
- Report c, d, Δd, CV(l·d) and the rationality flag (CV < 0.75 %; Bailey criterion, R53).
- Report the 00l FWHM (coherence length via `scherrer_length`, after removing instrumental width) and the rocking-curve FWHM (mosaicity).
- **Homogeneity:** measure both faces, and a face cleaved at mid-thickness, for crystals > 0.2 mm.
- **Staging:** for a repeat I_c, n = 1 + (I_c − d_filled)/d_empty (`tools.xrd.stage_index`).
- **Phase purity:** no impurity reflection > 1 % of the strongest 00l.

**Structure.** Single-crystal XRD at 100 K gives h(Se) and the Se–Fe–Se angle. Synchrotron PDF covers galleries too disordered for Bragg analysis.

**In situ, under scCO₂.**
- Sapphire-tube or Be-window cell, synchrotron 30–60 keV, area detector, 10–60 s frames.
- Subtract CO₂ scattering using fluid-only frames at the same (T, ρ); fluid scattering scales with density.
- Use the 00l positions in each frame for kinetics: fraction transformed α(t) from integrated intensities of the host and intercalate 00l peaks.

---

## P5. Tc metrology and acceptance rule

**Magnetisation (SQUID).**
- ZFC and FC at 1–2 mT, field ∥ c, and ⊥ c on a subset. Before each ZFC, quench the magnet so the residual field is < 0.1 mT.
- Volume comes from crystal dimensions, or from mass divided by X-ray density computed from the refined cell and composition.
- Demagnetisation correction: `tc.demag_factor_prism(a, b, c)` (R52), then `tc.shielding_fraction`.
- Report the onset (5σ above baseline) and T at 10 / 50 / 90 % of full shielding (`tc.tc_from_magnetization`).

**Transport.**
- Four-probe or van der Pauw; Au wires and silver epoxy cured in the glovebox; current reversal at 0.1–1 mA.
- Report the 90 % / 50 % / 10 % points of the extrapolated normal state, T(zero) at the noise floor, and the 10–90 % width (`tc.tc_from_resistance`).
- Hc₂(T) up to 9 T for ∥ and ⊥ c.

**Specific heat.** Relaxation calorimetry on ≥ 5 mg; report ΔC/γTc. This is the strongest bulk evidence.

**Acceptance rule** (`tc.bulk_verdict`):

| Verdict | Requirement |
|---|---|
| **BULK** | shielding ≥ 0.5 **and** (zero resistance **or** Cp anomaly) in ≥ 2 independent samples |
| PROBABLE | shielding ≥ 0.5 in one sample, or 0.1–0.5 with zero resistance |
| FILAMENTARY | weaker signals |

A claim that a result is **beyond benchmark** requires all three:
- verdict BULK;
- magnetisation onset above the benchmark Tc (benchmarks are mostly quoted as onsets);
- resistive midpoint within 2 K of that onset.

Report every Tc with the criterion used; never quote an unlabelled "Tc".

---

## P6. Composition, charge transfer and air-sensitive handling

| Quantity | Method | Notes |
|---|---|---|
| Metal content (Li, Na, K, Co, Cr, Fe, Se, Nb, Ta, Mo, Sn) | ICP-OES after HNO₃/HCl digestion | Co:M ratio distinguishes co-intercalation from exchange (I-04) |
| C, H, N | combustion analysis, capsules sealed in glovebox | organic guest and ligand content |
| Volatile guests | TGA-MS under Ar to 400 °C | NH₃ / amine / CO₂ / solvent release (I-07) |
| Degree of ionisation | XPS (vacuum-transfer vessel): Co 2p (Co(III) cobaltocenium vs Co(II)), Fe 2p, Se 3d, Mo 3d (1T/2H) | |
| Carrier density | Hall (PPMS), ARPES pocket area (Luttinger count) on cleaved crystals at < 20 K | |
| Side products | FTIR-ATR in glovebox: carbonate 1400–1500 cm⁻¹, formate ≈ 1600/1350 cm⁻¹, carbamate ≈ 1550–1600 cm⁻¹ | |
| Vibrational fingerprint | Raman (sealed cell): FeSe A₁g, MoS₂ J₁/J₂/J₃, guest modes for I-03 | |

**Electron count:** n = Σᵢ zᵢ xᵢ θᵢ. Here xᵢ is the amount of guest i per formula unit, zᵢ its charge, and θᵢ its degree of ionisation (from XPS for metallocenes; 1 for alkali cations). Cross-check against ARPES or Hall on a subset.

---

## P7. Pressure-quench (PQP) amplifier module

Purpose: keep, at ambient pressure, high-Tc states that appear only under compression. Candidates are Hg-1223 after F/O loading (I-08) and the best FeSe intercalates, whose SC-II phase exceeds 50 K near 12 GPa (R8).

1. **Screen first.** Measure Tc(P) in a DAC up to 30 GPa to locate the pressure of maximum Tc. Organic galleries may become amorphous; check by XRD under pressure.
2. **Quench.** Compress at room temperature to the target pressure. Cool to 4.2 K. Release the pressure at 4.2 K. Then measure Tc on warming by AC susceptibility or resistance in the DAC, following the published Hg-1223 procedure (R24). Do **not** use CO₂ as the pressure medium.
3. **Retention.** Warm in steps (77, 150, 200, 250, 300 K), re-cooling after each to measure Tc. Report the highest temperature at which Tc is retained, and recover the sample for XRD (peak broadening = strain).

---

## P8. Safety

- **Pressure.** Hydrotest cells at 1.5× working pressure. Rupture discs ≤ 90 % of rating. Shields in place. Never exceed the rated (P, T) envelope; check [`data/process_windows.csv`](../data/process_windows.csv), where `within_60MPa_rating` flags state points above typical equipment limits. Vent to an extracted line. Fit CO₂ asphyxiation monitors.
- **Oxidants vs organics.** Keep **dedicated, oxygen-cleaned Hastelloy/Monel cells** for O₃, XeF₂, F₂, NO⁺ and halogens, and never use them with organics or metallocenes. Compressing an oxidant–organic mixture adiabatically is an explosion hazard.
- **Toxic species.**
  - H₂Se (I-10): fixed monitor and lead-acetate indicator.
  - Hg compounds (I-08): Hg vapour monitoring; cold traps.
  - XeF₂ / HF: calcium gluconate on hand; soda-lime / alumina scrubber on the vent.
  - NH₃ (I-07): cold handling in a fume hood.
- **Air-sensitive and pyrophoric reagents.** Decamethylcobaltocene and cobaltocene are highly air-sensitive; handle only in the glovebox and quench residues with isopropanol under Ar. H₂ (I-10): LEL monitor, no ignition sources, H₂ partial pressure ≤ 5 MPa.
- **Exfoliation risk.** Unplanned rapid venting turns crystals into airborne nanosheets; enclose vent outlets with HEPA filters.
