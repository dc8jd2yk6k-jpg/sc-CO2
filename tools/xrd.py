"""XRD helpers for intercalation studies (validation by c-axis / gallery metrics).

Functions
---------
fit_c_axis        least-squares c (or basal repeat) from a (00l) series, with
                  optional zero-shift refinement, and the coefficient of
                  variation (CV) of l*d(00l) used to test rationality
                  (CV < 0.75 % -> rational series; larger -> interstratified /
                  mixed-stage material, Bailey 1982 / AIPEA criterion)
gallery_expansion Delta d relative to the pristine host layer repeat
stage_index       stage number n from the repeat I_c = d_filled + (n-1) d_empty
scherrer_length   coherence length along c from a (00l) FWHM

Usage
-----
    python -m tools.xrd fit --peaks 11.40 22.92 34.62 46.66 --l 1 2 3 4 --refine-zero
    python -m tools.xrd fit --peaks ... --l ... --host FeSe --layers 1
"""

from __future__ import annotations

import argparse
import math
from typing import Sequence

import numpy as np

WAVELENGTHS_A = {
    "CuKa1": 1.540562,
    "CuKa": 1.541838,  # weighted Ka1/Ka2
    "CoKa1": 1.788965,
    "MoKa1": 0.709300,
    "AgKa1": 0.559421,
}

# Pristine layer repeat d0 (Angstrom) per single host layer (c / layers-per-cell).
# Room-temperature literature values, rounded; refine against your own baseline.
HOST_LAYER_REPEAT_A = {
    "FeSe": 5.52,  # beta-FeSe, P4/nmm, c = 5.52
    "FeS": 5.03,  # mackinawite
    "FeSe0.5Te0.5": 6.0,
    "2H-NbSe2": 6.27,  # c = 12.55, 2 layers
    "2H-NbS2": 5.98,  # c = 11.96
    "2H-TaS2": 6.05,  # c = 12.10
    "2H-MoS2": 6.15,  # c = 12.30
    "2H-WS2": 6.16,
    "1T-SnSe2": 6.14,
    "1T-TiSe2": 6.01,
    "Bi2Se3": 9.55,  # c = 28.64, 3 QL
    "beta-ZrNCl": 9.2,  # c = 27.6, 3 layers
    "beta-HfNCl": 9.3,
    "Bi2212": 15.4,  # half of c ~ 30.8 (body-centred, 2 formula layers)
    "Bi2223": 18.55,  # half of c ~ 37.1
}

RATIONAL_CV_PERCENT = 0.75


def d_from_two_theta(two_theta_deg: float | np.ndarray, wavelength_A: float) -> np.ndarray:
    th = np.radians(np.asarray(two_theta_deg, float) / 2.0)
    return wavelength_A / (2.0 * np.sin(th))


def two_theta_from_d(d_A: float | np.ndarray, wavelength_A: float) -> np.ndarray:
    return 2.0 * np.degrees(np.arcsin(wavelength_A / (2.0 * np.asarray(d_A, float))))


def _fit_fixed_zero(two_theta: np.ndarray, l: np.ndarray, wl: float, zero: float) -> tuple[float, float, np.ndarray]:
    """sin(theta_l) = (wl / 2c) * l, linear through origin. Returns c, sigma_c, residual(2theta)."""
    s = np.sin(np.radians((two_theta - zero) / 2.0))
    slope = float(np.sum(s * l) / np.sum(l * l))
    c = wl / (2.0 * slope)
    pred = two_theta_from_d(c / l, wl) + zero
    resid = two_theta - pred
    n = len(l)
    if n > 1:
        sig_s = math.sqrt(float(np.sum((s - slope * l) ** 2)) / max(n - 1, 1) / float(np.sum(l * l)))
        sigma_c = c * sig_s / slope
    else:
        sigma_c = float("nan")
    return c, sigma_c, resid


def fit_c_axis(
    two_theta_deg: Sequence[float],
    l_indices: Sequence[int],
    wavelength_A: float = WAVELENGTHS_A["CuKa1"],
    refine_zero: bool = False,
    zero_bounds_deg: tuple[float, float] = (-0.5, 0.5),
) -> dict:
    """Fit the basal repeat c from (00l) peak positions.

    Returns dict with c_A, sigma_c_A, zero_deg, rms_resid_deg, cv_percent,
    rational (bool), and per-peak d and l*d.
    """
    tt = np.asarray(two_theta_deg, float)
    l = np.asarray(l_indices, float)
    if tt.shape != l.shape or len(tt) < 1:
        raise ValueError("two_theta and l must be equal-length, non-empty")
    if refine_zero and len(tt) < 3:
        raise ValueError("zero-shift refinement needs >= 3 reflections")

    def sse(z: float) -> float:
        return float(np.sum(_fit_fixed_zero(tt, l, wavelength_A, z)[2] ** 2))

    zero = 0.0
    if refine_zero:  # golden-section search on the zero offset
        a, b = zero_bounds_deg
        g = (math.sqrt(5) - 1) / 2
        x1, x2 = b - g * (b - a), a + g * (b - a)
        f1, f2 = sse(x1), sse(x2)
        for _ in range(200):
            if f1 < f2:
                b, x2, f2 = x2, x1, f1
                x1 = b - g * (b - a)
                f1 = sse(x1)
            else:
                a, x1, f1 = x1, x2, f2
                x2 = a + g * (b - a)
                f2 = sse(x2)
            if b - a < 1e-7:
                break
        zero = (a + b) / 2

    c, sigma_c, resid = _fit_fixed_zero(tt, l, wavelength_A, zero)
    d = d_from_two_theta(tt - zero, wavelength_A)
    ld = l * d
    cv = float(np.std(ld, ddof=1) / np.mean(ld) * 100) if len(ld) > 1 else 0.0
    return {
        "c_A": c,
        "sigma_c_A": sigma_c,
        "zero_deg": zero,
        "rms_resid_deg": float(np.sqrt(np.mean(resid**2))),
        "cv_percent": cv,
        "rational": cv < RATIONAL_CV_PERCENT,
        "d_A": d.tolist(),
        "l_times_d_A": ld.tolist(),
    }


def gallery_expansion(c_A: float, layers_per_cell: int, host: str | float) -> dict:
    """Interlayer repeat d = c / layers and its expansion relative to the host."""
    d0 = HOST_LAYER_REPEAT_A[host] if isinstance(host, str) else float(host)
    d = c_A / layers_per_cell
    return {"d_A": d, "d0_A": d0, "delta_d_A": d - d0, "expansion_percent": (d - d0) / d0 * 100}


def stage_index(repeat_A: float, d_filled_A: float, d_empty_A: float) -> dict:
    """Stage n from I_c = d_filled + (n - 1) * d_empty."""
    n = 1.0 + (repeat_A - d_filled_A) / d_empty_A
    return {"n_float": n, "n": int(round(n)), "misfit_A": repeat_A - (d_filled_A + (round(n) - 1) * d_empty_A)}


def scherrer_length(
    fwhm_deg: float,
    two_theta_deg: float,
    wavelength_A: float = WAVELENGTHS_A["CuKa1"],
    K: float = 0.9,
    instrumental_fwhm_deg: float = 0.0,
) -> float:
    """Coherence length (Angstrom); instrumental width removed in quadrature."""
    beta2 = fwhm_deg**2 - instrumental_fwhm_deg**2
    if beta2 <= 0:
        return float("inf")
    beta = math.radians(math.sqrt(beta2))
    return K * wavelength_A / (beta * math.cos(math.radians(two_theta_deg / 2)))


def _cli(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Fit a (00l) series")
    sub = p.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("fit")
    f.add_argument("--peaks", type=float, nargs="+", required=True, help="2theta positions, deg")
    f.add_argument("--l", type=int, nargs="+", required=True, help="l indices")
    f.add_argument("--wavelength", default="CuKa1", help="name or value in Angstrom")
    f.add_argument("--refine-zero", action="store_true")
    f.add_argument("--host", default=None, help="host key for Delta d, e.g. FeSe")
    f.add_argument("--layers", type=int, default=1, help="host layers per fitted repeat")
    args = p.parse_args(argv)

    wl = WAVELENGTHS_A.get(args.wavelength)
    wl = float(args.wavelength) if wl is None else wl
    r = fit_c_axis(args.peaks, args.l, wl, args.refine_zero)
    print(f"c = {r['c_A']:.4f} +- {r['sigma_c_A']:.4f} A   zero = {r['zero_deg']:+.4f} deg   rms = {r['rms_resid_deg']:.4f} deg")
    print(f"CV(l*d) = {r['cv_percent']:.3f} %  -> {'rational' if r['rational'] else 'NON-rational (mixed stage / interstratified?)'}")
    if args.host:
        g = gallery_expansion(r["c_A"], args.layers, args.host)
        print(f"d = {g['d_A']:.3f} A, host d0 = {g['d0_A']:.3f} A, Delta d = {g['delta_d_A']:+.3f} A ({g['expansion_percent']:+.1f} %)")
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())
