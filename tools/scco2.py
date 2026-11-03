"""Supercritical-CO2 process-window calculator.

Planning aid for scCO2-assisted intercalation experiments (focus area 1).
It answers the questions an experimentalist needs before loading a cell:

* What pressure gives a target CO2 density at a given temperature
  (isopycnic sweeps decouple solvent power from thermal activation)?
* What are the density, viscosity, Giddings solubility parameter and an
  order-of-magnitude solute diffusivity at a state point?
* How do measured solubilities fit the Chrastil density model?

Thermodynamic backend
---------------------
If CoolProp is installed, the Span-Wagner reference equation of state and
the reference transport correlations are used (recommended). Without
CoolProp, density falls back to the plain Peng-Robinson EOS. Against
Span-Wagner over 35-150 C and 12-40 MPa its density error is within about
-9 % / +4 % (largest under-prediction along the near-critical ridge at
40-60 C); see tests/test_tools.py. Treat it as a planning estimate only,
and never use it within ~+-10 K / +-2 MPa of the critical point.
Viscosity and diffusivity estimates require CoolProp.

Usage
-----
    python -m tools.scco2 state --T 60 --P 20
    python -m tools.scco2 isopycnic --rho 800 --T 40 60 80 100
    python -m tools.scco2 table --out data/process_windows.csv
"""

from __future__ import annotations

import argparse
import csv
import math
import sys
from dataclasses import asdict, dataclass
from typing import Iterable, Sequence

try:  # optional, preferred backend
    import CoolProp.CoolProp as _CP  # type: ignore

    HAVE_COOLPROP = True
except ImportError:  # pragma: no cover - exercised only without CoolProp
    _CP = None
    HAVE_COOLPROP = False

# Critical constants of CO2 (Span & Wagner 1996)
TC_K = 304.1282
PC_MPA = 7.3773
RHOC_KG_M3 = 467.6
M_CO2_G_MOL = 44.0095
OMEGA = 0.22394
R_J_MOLK = 8.314462618


# --------------------------------------------------------------------------
# Equation of state
# --------------------------------------------------------------------------
def _pr_params(T_K: float) -> tuple[float, float]:
    Pc = PC_MPA * 1e6
    a = 0.45724 * R_J_MOLK**2 * TC_K**2 / Pc
    b = 0.07780 * R_J_MOLK * TC_K / Pc
    kappa = 0.37464 + 1.54226 * OMEGA - 0.26992 * OMEGA**2
    alpha = (1.0 + kappa * (1.0 - math.sqrt(T_K / TC_K))) ** 2
    return a * alpha, b


def _real_cubic_roots(c2: float, c1: float, c0: float) -> list[float]:
    """Real roots of z^3 + c2 z^2 + c1 z + c0 = 0."""
    q = (3 * c1 - c2**2) / 9.0
    r = (9 * c2 * c1 - 27 * c0 - 2 * c2**3) / 54.0
    disc = q**3 + r**2
    shift = -c2 / 3.0
    if disc > 0:
        s = math.copysign(abs(r + math.sqrt(disc)) ** (1 / 3), r + math.sqrt(disc))
        t = math.copysign(abs(r - math.sqrt(disc)) ** (1 / 3), r - math.sqrt(disc))
        return [s + t + shift]
    theta = math.acos(max(-1.0, min(1.0, r / math.sqrt(-(q**3))))) if q < 0 else 0.0
    m = 2 * math.sqrt(-q) if q < 0 else 0.0
    return [
        m * math.cos(theta / 3) + shift,
        m * math.cos((theta + 2 * math.pi) / 3) + shift,
        m * math.cos((theta + 4 * math.pi) / 3) + shift,
    ]


def _pr_density(T_K: float, P_MPa: float) -> float:
    aa, b = _pr_params(T_K)
    P = P_MPa * 1e6
    A = aa * P / (R_J_MOLK * T_K) ** 2
    B = b * P / (R_J_MOLK * T_K)
    roots = [z for z in _real_cubic_roots(-(1 - B), A - 3 * B**2 - 2 * B, -(A * B - B**2 - B**3)) if z > B]
    if not roots:
        raise ValueError("Peng-Robinson: no physical root")

    def g_res(z: float) -> float:  # residual Gibbs energy / RT
        s2 = math.sqrt(2.0)
        return z - 1 - math.log(z - B) - A / (2 * s2 * B) * math.log((z + (1 + s2) * B) / (z + (1 - s2) * B))

    z = min(roots, key=g_res)
    v = z * R_J_MOLK * T_K / P  # m3/mol
    return M_CO2_G_MOL * 1e-3 / v


def _pr_pressure(T_K: float, rho: float) -> float:
    aa, b = _pr_params(T_K)
    v = M_CO2_G_MOL * 1e-3 / rho
    P = R_J_MOLK * T_K / (v - b) - aa / (v * v + 2 * b * v - b * b)
    return P / 1e6


def _use_coolprop(backend: str) -> bool:
    if backend == "coolprop":
        if not HAVE_COOLPROP:
            raise RuntimeError("CoolProp backend requested but CoolProp is not installed")
        return True
    if backend == "pr":
        return False
    return HAVE_COOLPROP


def density(T_K: float, P_MPa: float, backend: str = "auto") -> float:
    """CO2 density in kg/m3."""
    if _use_coolprop(backend):
        return float(_CP.PropsSI("D", "T", T_K, "P", P_MPa * 1e6, "CO2"))
    return _pr_density(T_K, P_MPa)


def pressure_for_density(T_K: float, rho_kg_m3: float, backend: str = "auto") -> float:
    """Pressure (MPa) giving density rho at temperature T (isopycnic design)."""
    if _use_coolprop(backend):
        return float(_CP.PropsSI("P", "T", T_K, "D", rho_kg_m3, "CO2")) / 1e6
    return _pr_pressure(T_K, rho_kg_m3)


def viscosity(T_K: float, P_MPa: float) -> float:
    """Dynamic viscosity in Pa s (requires CoolProp)."""
    if not HAVE_COOLPROP:
        raise RuntimeError("viscosity requires CoolProp (pip install CoolProp)")
    return float(_CP.PropsSI("V", "T", T_K, "P", P_MPa * 1e6, "CO2"))


# --------------------------------------------------------------------------
# Solvent-power and transport descriptors
# --------------------------------------------------------------------------
_CAL_TO_MPA_HALF = 2.0455  # (cal/cm3)^0.5 -> MPa^0.5


def giddings_delta(rho_kg_m3: float) -> float:
    """Giddings solubility parameter of CO2 (MPa^0.5).

    delta = 1.25 Pc^0.5 (rho_r / rho_r,liq), Pc in atm, rho_r,liq = 2.66.
    A coarse but standard yardstick for 'liquid-like' solvent power:
    ~15 MPa^0.5 at 900 kg/m3 (similar to hexane/pentane) versus <7 at 300 kg/m3.
    """
    pc_atm = PC_MPA * 1e6 / 101325.0
    rho_r = rho_kg_m3 / RHOC_KG_M3
    return 1.25 * math.sqrt(pc_atm) * rho_r / 2.66 * _CAL_TO_MPA_HALF


def wilke_chang_diffusivity(T_K: float, eta_Pa_s: float, solute_molar_volume_cm3: float, phi: float = 1.0) -> float:
    """Wilke-Chang estimate of solute diffusivity in CO2 (m2/s).

    solute_molar_volume_cm3: molar volume at normal boiling point (Le Bas or
    group-contribution estimate). Typical accuracy in SCFs is +-20-30 %; use it
    for ranking state points, not as a measured value.
    """
    eta_cP = eta_Pa_s * 1e3
    d_cm2_s = 7.4e-8 * math.sqrt(phi * M_CO2_G_MOL) * T_K / (eta_cP * solute_molar_volume_cm3**0.6)
    return d_cm2_s * 1e-4


@dataclass
class StatePoint:
    T_C: float
    P_MPa: float
    rho_kg_m3: float
    rho_reduced: float
    delta_MPa05: float
    eta_uPa_s: float | None
    D_solute_m2_s: float | None
    phase: str


def phase_label(T_K: float, P_MPa: float) -> str:
    if T_K >= TC_K and P_MPa >= PC_MPA:
        return "supercritical"
    if T_K >= TC_K:
        return "gas (T>Tc, P<Pc)"
    if P_MPa >= PC_MPA:
        return "compressed liquid"
    return "subcritical (check saturation)"


def state(T_C: float, P_MPa: float, solute_molar_volume_cm3: float = 150.0, backend: str = "auto") -> StatePoint:
    T_K = T_C + 273.15
    rho = density(T_K, P_MPa, backend)
    eta = D = None
    if HAVE_COOLPROP and backend != "pr":
        eta = viscosity(T_K, P_MPa)
        D = wilke_chang_diffusivity(T_K, eta, solute_molar_volume_cm3)
    return StatePoint(
        T_C=T_C,
        P_MPa=P_MPa,
        rho_kg_m3=rho,
        rho_reduced=rho / RHOC_KG_M3,
        delta_MPa05=giddings_delta(rho),
        eta_uPa_s=None if eta is None else eta * 1e6,
        D_solute_m2_s=D,
        phase=phase_label(T_K, P_MPa),
    )


# --------------------------------------------------------------------------
# Chrastil solubility model: ln S = k ln rho + a / T + b
# --------------------------------------------------------------------------
def chrastil_fit(rho_kg_m3: Sequence[float], T_K: Sequence[float], S: Sequence[float]) -> dict:
    """Least-squares Chrastil fit. S in any consistent units (e.g. kg/m3).

    k ~ association number (CO2 molecules per solvated solute complex);
    a = -dH_total/R (heat of vaporization + solvation).
    Returns k, a, b and the RMS deviation in ln S.
    """
    import numpy as np

    rho = np.asarray(rho_kg_m3, float)
    T = np.asarray(T_K, float)
    y = np.log(np.asarray(S, float))
    X = np.column_stack([np.log(rho), 1.0 / T, np.ones_like(rho)])
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    rms = float(np.sqrt(np.mean((X @ coef - y) ** 2)))
    return {"k": float(coef[0]), "a": float(coef[1]), "b": float(coef[2]), "rms_lnS": rms}


def chrastil_predict(rho_kg_m3: float, T_K: float, k: float, a: float, b: float) -> float:
    return math.exp(k * math.log(rho_kg_m3) + a / T_K + b)


# --------------------------------------------------------------------------
# Design tables
# --------------------------------------------------------------------------
DEFAULT_T_C = (35, 40, 50, 60, 80, 100, 120, 150)
DEFAULT_RHO = (300, 400, 500, 600, 700, 800, 900)
EQUIPMENT_LIMIT_MPA = 60.0  # typical rating of lab autoclaves / view cells


def process_window_rows(
    T_list_C: Iterable[float] = DEFAULT_T_C,
    rho_list: Iterable[float] = DEFAULT_RHO,
    solute_molar_volume_cm3: float = 150.0,
    backend: str = "auto",
) -> list[dict]:
    rows = []
    for T_C in T_list_C:
        T_K = T_C + 273.15
        for rho in rho_list:
            P = pressure_for_density(T_K, rho, backend)
            row = {
                "T_C": T_C,
                "rho_kg_m3": rho,
                "P_MPa": round(P, 2),
                "delta_MPa05": round(giddings_delta(rho), 2),
                "eta_uPa_s": "",
                "D_solute_1e-8_m2_s": "",
                "within_60MPa_rating": P <= EQUIPMENT_LIMIT_MPA,
            }
            if HAVE_COOLPROP and backend != "pr" and P > 0:
                eta = viscosity(T_K, P)
                row["eta_uPa_s"] = round(eta * 1e6, 1)
                row["D_solute_1e-8_m2_s"] = round(wilke_chang_diffusivity(T_K, eta, solute_molar_volume_cm3) / 1e-8, 2)
            rows.append(row)
    return rows


def _cli(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--backend", choices=["auto", "coolprop", "pr"], default="auto")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("state", help="properties at one state point")
    s.add_argument("--T", type=float, required=True, help="temperature, C")
    s.add_argument("--P", type=float, required=True, help="pressure, MPa")
    s.add_argument("--Vb", type=float, default=150.0, help="solute molar volume at Tb, cm3/mol")

    i = sub.add_parser("isopycnic", help="pressures for constant density at several T")
    i.add_argument("--rho", type=float, required=True, help="target density, kg/m3")
    i.add_argument("--T", type=float, nargs="+", required=True, help="temperatures, C")

    t = sub.add_parser("table", help="write a T x rho process-window table (CSV)")
    t.add_argument("--out", default="-", help="output CSV path or - for stdout")
    t.add_argument("--Vb", type=float, default=150.0)

    args = p.parse_args(argv)
    if args.cmd == "state":
        sp = state(args.T, args.P, args.Vb, args.backend)
        for k, v in asdict(sp).items():
            print(f"{k:>16}: {v:.4g}" if isinstance(v, float) else f"{k:>16}: {v}")
    elif args.cmd == "isopycnic":
        print(f"rho = {args.rho:g} kg/m3 (delta = {giddings_delta(args.rho):.2f} MPa^0.5)")
        for T_C in args.T:
            print(f"  T = {T_C:6.1f} C  ->  P = {pressure_for_density(T_C + 273.15, args.rho, args.backend):7.2f} MPa")
    elif args.cmd == "table":
        rows = process_window_rows(solute_molar_volume_cm3=args.Vb, backend=args.backend)
        fh = sys.stdout if args.out == "-" else open(args.out, "w", newline="")
        try:
            w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        finally:
            if fh is not sys.stdout:
                fh.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())
