"""Superconducting-transition metrics from R(T) and M(T) (validation by Tc).

The protocols in docs/protocols.md require every Tc claim to state *which*
criterion was used. This module makes the criteria explicit and reproducible:

tc_from_resistance     T at 90 % / 50 % / 10 % of the extrapolated normal-state
                       resistance, zero-resistance T, and 10-90 % width
tc_from_magnetization  onset of diamagnetism (baseline + n*sigma) and the
                       T at 10 % / 50 % / 90 % of the low-T shielding signal
demag_factor_prism     effective demagnetising factor of a rectangular prism,
                       field along the thickness (Prozorov & Kogan 2018)
shielding_fraction     -chi (SI, volume) after demagnetisation correction from
                       a ZFC moment; 1.0 = full shielding
bulk_verdict           applies the bulk-superconductivity acceptance rule

Units: moment in emu, field in Oe, volume in cm3 (CGS SQUID convention).
"""

from __future__ import annotations

import math
from typing import Sequence

import numpy as np


def _crossing_from_above(T: np.ndarray, y: np.ndarray, level: float) -> float:
    """Highest temperature at which y falls through `level` on cooling."""
    for i in range(len(T) - 1, 0, -1):
        y_hi, y_lo = y[i], y[i - 1]
        if y_hi >= level > y_lo or y_hi > level >= y_lo:
            if y_hi == y_lo:
                return float(T[i])
            return float(T[i - 1] + (level - y_lo) * (T[i] - T[i - 1]) / (y_hi - y_lo))
    return float("nan")


def tc_from_resistance(
    T: Sequence[float],
    R: Sequence[float],
    normal_window: tuple[float, float] | None = None,
    zero_threshold: float = 1e-3,
) -> dict:
    """Transition metrics from R(T).

    normal_window: (Tmin, Tmax) used for a linear normal-state fit. If None,
    the top 20 % of the temperature range is used.
    zero_threshold: R/R_n below which the sample is counted as zero-resistance
    (set it from your noise floor).
    """
    T = np.asarray(T, float)
    R = np.asarray(R, float)
    order = np.argsort(T)
    T, R = T[order], R[order]
    if normal_window is None:
        lo = T.min() + 0.8 * (T.max() - T.min())
        normal_window = (lo, T.max())
    m = (T >= normal_window[0]) & (T <= normal_window[1])
    if m.sum() < 2:
        raise ValueError("normal-state window needs >= 2 points")
    slope, icpt = np.polyfit(T[m], R[m], 1)
    ratio = R / (slope * T + icpt)
    t90 = _crossing_from_above(T, ratio, 0.9)
    t50 = _crossing_from_above(T, ratio, 0.5)
    t10 = _crossing_from_above(T, ratio, 0.1)
    above = np.where(ratio > zero_threshold)[0]
    t_zero = float(T[above[0] - 1]) if len(above) and above[0] > 0 else float("nan")
    return {
        "Tc_onset90_K": t90,
        "Tc_mid50_K": t50,
        "Tc_10_K": t10,
        "Tc_zero_K": t_zero,
        "width_10_90_K": t90 - t10,
        "normal_slope": float(slope),
        "normal_intercept": float(icpt),
    }


def tc_from_magnetization(
    T: Sequence[float],
    M: Sequence[float],
    baseline_window: tuple[float, float] | None = None,
    n_sigma: float = 5.0,
) -> dict:
    """Diamagnetic onset and fractional-shielding temperatures from ZFC M(T)."""
    T = np.asarray(T, float)
    M = np.asarray(M, float)
    order = np.argsort(T)
    T, M = T[order], M[order]
    if baseline_window is None:
        lo = T.min() + 0.8 * (T.max() - T.min())
        baseline_window = (lo, T.max())
    m = (T >= baseline_window[0]) & (T <= baseline_window[1])
    if m.sum() < 3:
        raise ValueError("baseline window needs >= 3 points")
    p = np.polyfit(T[m], M[m], 1)
    base = np.polyval(p, T)
    sigma = float(np.std(M[m] - base[m], ddof=1)) or 1e-30
    dM = M - base  # negative below Tc
    below = dM < -n_sigma * sigma
    onset = float("nan")
    for i in range(len(T) - 1, -1, -1):  # highest T from which signal stays below threshold on cooling
        if below[: i + 1].all():
            onset = float(T[i])
            break
    full = float(dM[0])
    frac = dM / full if full < 0 else np.zeros_like(dM)
    return {
        "Tc_onset_K": onset,
        "T_10pct_K": _crossing_from_above(T, -frac, -0.10),
        "T_50pct_K": _crossing_from_above(T, -frac, -0.50),
        "T_90pct_K": _crossing_from_above(T, -frac, -0.90),
        "noise_emu": sigma,
    }


def demag_factor_prism(a: float, b: float, c: float) -> float:
    """Effective demagnetising factor for a rectangular prism a x b (in-plane)
    x c (along the field). Prozorov & Kogan, Phys. Rev. Applied 10, 014030 (2018):
    1/N = 1 + (3/4)(c/a)(1 + a/b). Most accurate for thin plates (c << a, b).
    """
    return 1.0 / (1.0 + 0.75 * (c / a) * (1.0 + a / b))


def shielding_fraction(moment_emu: float, field_Oe: float, volume_cm3: float, N: float = 0.0) -> float:
    """Shielding fraction -chi_int (SI volume susceptibility) from a ZFC moment.

    chi_app = 4*pi*M/(V*H) (dimensionless SI);  chi_int = chi_app / (1 - N*chi_app).
    """
    if field_Oe == 0 or volume_cm3 <= 0:
        raise ValueError("field and volume must be non-zero")
    chi_app = 4.0 * math.pi * moment_emu / (volume_cm3 * field_Oe)
    denom = 1.0 - N * chi_app
    if denom <= 0:
        raise ValueError("demagnetisation correction diverges; check N and units")
    return -chi_app / denom


def volume_from_mass(mass_mg: float, density_g_cm3: float) -> float:
    return mass_mg * 1e-3 / density_g_cm3


def bulk_verdict(
    shielding: float | None,
    zero_resistance: bool | None,
    specific_heat_anomaly: bool | None,
    n_samples: int = 1,
) -> str:
    """Acceptance rule from docs/protocols.md section P5.

    BULK      : shielding >= 0.5 AND (zero resistance OR specific-heat anomaly), >= 2 samples
    PROBABLE  : shielding >= 0.5 with one sample, or shielding 0.1-0.5 plus zero resistance
    FILAMENTARY / TRACE : anything weaker
    """
    s = shielding or 0.0
    corroborated = bool(zero_resistance) or bool(specific_heat_anomaly)
    if s >= 0.5 and corroborated and n_samples >= 2:
        return "BULK"
    if s >= 0.5 or (s >= 0.1 and zero_resistance):
        return "PROBABLE"
    if s > 0.0 or zero_resistance:
        return "FILAMENTARY"
    return "NONE"
