# scCO₂-assisted intercalation of layered superconductors

A research program for using **supercritical CO₂ (scCO₂)** to intercalate layered superconductors (iron chalcogenides, cuprates, transition-metal dichalcogenides, and related hosts). The goal is to **raise Tc above established benchmarks**, with every claim validated by **Tc measurements and XRD**.

The repository has three parts:
- the ranked idea set, with experimental protocols;
- the benchmark and chemical-compatibility data the ideas rely on;
- small, tested tools for planning scCO₂ state points and turning raw XRD and Tc data into the numbers the protocols ask for.

## Where to start

| File | What it is |
|---|---|
| [`docs/research_program.md`](docs/research_program.md) | **Main document.** Design rules, benchmarks and targets, ranking method, and **11 ranked ideas**. Each has a hypothesis, process window, step-by-step protocol, go/no-go criteria and risks |
| [`docs/protocols.md`](docs/protocols.md) | Shared procedures P1–P8: reactor and phase behaviour, blanks/controls, run sequence, XRD, Tc metrology and acceptance rule, composition and charge transfer, pressure-quench module, safety |
| [`docs/references.md`](docs/references.md) | Reference list (`R#` keys) |
| [`data/benchmarks.csv`](data/benchmarks.csv) | Host baselines and best modified-phase Tc values, with routes and confidence |
| [`data/co2_compatibility.csv`](data/co2_compatibility.csv) | Which intercalant classes survive CO₂ and which react (carbamate, carbonate, carboxylation) |
| [`data/redox_ladder.csv`](data/redox_ladder.csv) | CO₂-compatible molecular donors and acceptors on one potential scale |
| [`data/process_windows.csv`](data/process_windows.csv) | Generated T × ρ grid: pressure, solvent power, viscosity, solute diffusivity |
| [`data/sample_log_template.csv`](data/sample_log_template.csv) | One row per sample; same descriptors across all ideas |

## Ranked ideas (summary)

| Rank | ID | Idea | Score |
|---|---|---|---|
| 1 | I-01 | Redox-buffered equilibrium electron doping with CO₂-stable molecular donors (metallocene ladder + crown-solvated alkali ions) | 4.45 |
| 2 | I-02 | Electrochemical organic-cation intercalation in CO₂-expanded electrolytes, then supercritical washing and drying (TBA⁺-family FeSe) | 4.25 |
| 3 | I-03 | Polar-phonon / high-ε co-intercalants that mimic the FeSe/SrTiO₃ interface in bulk, with a guest-isotope test | 4.20 |
| 4 | I-04 | Pillar-then-dope sequential co-intercalation to tune spacing d and doping n independently | 4.15 |
| 5 | I-05 | Density-programmed guest activity: staging, kinetics, pressure-swing pumping (platform) | 4.00 |
| 6 | I-06 | Layer separation plus doping in bulk TaS₂ and MoS₂; scCO₂/I₂ deintercalation route to 2M-WS₂ | 3.90 |
| 7 | I-07 | In-gallery CO₂ fixation of labile NH₃ / amine co-intercalants | 3.70 |
| 8 | I-08 | scCO₂-carried F/O loading of Hg-1223 plus pressure-quench | 3.65 |
| 9 | I-09 | Acceptor (hole) intercalation of NbSe₂ in a medium that cannot be oxidised | 3.60 |
| 10 | I-10 | H₂-fugacity-controlled spillover protonation | 3.45 |
| 11 | I-11 | CO₂-philic fluorous cation superlattices: the low-ε end of the dielectric range | 3.30 |

Three findings drive the program (details in §0 and §2 of the main document):
1. **CO₂ is a reagent.** Li/NH₃, amines, hydroxides and organolithiums react with it. The program therefore uses CO₂-stable donors, separate sources for electrons and charge-balancing ions, electrochemistry in CO₂-expanded electrolytes, and oxidants in a medium that cannot be oxidised.
2. **MPa process pressures do not compress lattices.** The levers are density-controlled guest activity, fast transport, CO₂ pre-swelling of galleries, and solvent removal without collapse.
3. **FeSe saturates near 45–50 K once spacing exceeds about 9 Å.** Going higher needs doping control independent of spacing, an extra ingredient in the gallery that helps pairing, or a pressure-quench.

## Tools

Pure Python with numpy. CoolProp is optional but recommended: it supplies the Span–Wagner EOS and transport properties. Without it, density falls back to Peng–Robinson, which is accurate to about −9 % / +4 % above 12 MPa.

```bash
pip install -r requirements.txt
```
```bash
python -m pytest
```

**scCO₂ state points and isopycnic design**
```bash
python -m tools.scco2 state --T 60 --P 25
```
```bash
python -m tools.scco2 isopycnic --rho 800 --T 40 60 80 100
```
```bash
python -m tools.scco2 table --out data/process_windows.csv
```

**XRD (00l) series: c, zero shift, Δd vs host, rationality (CV of l·d)**
```bash
python -m tools.xrd fit --peaks 5.70 11.42 17.17 22.97 --l 1 2 3 4 --refine-zero --host FeSe
```

**Tc metrics** (Python API):
```python
from tools import tc
tc.tc_from_resistance(T, R)            # 90/50/10 % and zero-resistance Tc
tc.tc_from_magnetization(T, M)         # onset + 10/50/90 % shielding temperatures
N = tc.demag_factor_prism(a, b, c)     # field along c
tc.shielding_fraction(m_emu, H_Oe, V_cm3, N)
tc.bulk_verdict(shielding, zero_res, cp_anomaly, n_samples)
```

## Status and limitations

This is a **proposal-stage** repository: no experimental data exist yet. Benchmarks were checked against the literature available in November 2026, and values from preprints are flagged. Approximate redox potentials marked "verify" in `redox_ladder.csv` should be measured in the actual fluid before relying on them. The tools support planning and data reduction; they make no claims about Tc.
