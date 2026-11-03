import math

import numpy as np
import pytest

from tools import scco2, tc, xrd

needs_coolprop = pytest.mark.skipif(not scco2.HAVE_COOLPROP, reason="CoolProp not installed")


# ----------------------------------------------------------------- scco2
@needs_coolprop
@pytest.mark.parametrize(
    "T_C,P,rho_ref",
    [(40.0, 10.0, 628.6), (40.0, 20.0, 839.8), (35.0, 8.0, 419.1), (100.0, 30.0, 661.9)],
)
def test_coolprop_density_reference(T_C, P, rho_ref):
    assert scco2.density(T_C + 273.15, P, "coolprop") == pytest.approx(rho_ref, rel=2e-3)


@needs_coolprop
def test_pr_fallback_within_stated_band():
    errs = []
    for T_C in range(35, 151, 5):
        for P in np.arange(12.0, 40.1, 1.0):
            T = T_C + 273.15
            ref = scco2.density(T, P, "coolprop")
            errs.append((scco2.density(T, P, "pr") - ref) / ref)
    errs = np.array(errs)
    assert errs.min() > -0.09 and errs.max() < 0.045


@pytest.mark.parametrize("backend", ["pr"] + (["coolprop"] if scco2.HAVE_COOLPROP else []))
def test_isopycnic_roundtrip(backend):
    for T in (313.15, 353.15, 393.15):
        for rho in (400.0, 700.0, 900.0):
            P = scco2.pressure_for_density(T, rho, backend)
            assert scco2.density(T, P, backend) == pytest.approx(rho, rel=1e-4)


def test_giddings_delta_dense_co2_is_hexane_like():
    assert scco2.giddings_delta(900.0) == pytest.approx(15.8, abs=0.2)
    assert scco2.giddings_delta(300.0) < 7.0


def test_wilke_chang_order_of_magnitude():
    D = scco2.wilke_chang_diffusivity(313.15, 47.65e-6, 150.0)
    assert 1e-8 < D < 3e-8


def test_chrastil_recovers_parameters():
    rng = np.random.default_rng(1)
    rho = rng.uniform(500, 950, 40)
    T = rng.choice([313.15, 333.15, 353.15], 40)
    S = np.exp(4.5 * np.log(rho) - 5200.0 / T - 14.0)
    fit = scco2.chrastil_fit(rho, T, S)
    assert fit["k"] == pytest.approx(4.5, rel=1e-6)
    assert fit["a"] == pytest.approx(-5200.0, rel=1e-6)
    assert scco2.chrastil_predict(800.0, 333.15, fit["k"], fit["a"], fit["b"]) == pytest.approx(
        math.exp(4.5 * math.log(800.0) - 5200.0 / 333.15 - 14.0), rel=1e-6
    )


def test_phase_labels():
    assert scco2.phase_label(313.15, 10.0) == "supercritical"
    assert scco2.phase_label(298.15, 10.0) == "compressed liquid"


# ------------------------------------------------------------------- xrd
def _synthetic_peaks(c, ls, wl, zero=0.0):
    return xrd.two_theta_from_d(c / np.asarray(ls, float), wl) + zero


def test_fit_c_axis_with_zero_shift():
    wl = xrd.WAVELENGTHS_A["CuKa1"]
    ls = [1, 2, 3, 4, 5, 6]
    tt = _synthetic_peaks(15.50, ls, wl, zero=0.07)
    r = xrd.fit_c_axis(tt, ls, wl, refine_zero=True)
    assert r["c_A"] == pytest.approx(15.50, abs=2e-3)
    assert r["zero_deg"] == pytest.approx(0.07, abs=2e-3)
    assert r["rational"]


def test_irrational_series_flagged():
    wl = xrd.WAVELENGTHS_A["CuKa1"]
    # 50:50 random interstratification of 5.52 and 9.3 A layers gives peaks
    # that are not orders of one repeat; mimic with an irregular l*d set.
    d = np.array([7.6, 3.65, 2.38, 1.86])
    tt = xrd.two_theta_from_d(d, wl)
    r = xrd.fit_c_axis(tt, [1, 2, 3, 4], wl)
    assert not r["rational"]


def test_gallery_expansion_and_stage():
    g = xrd.gallery_expansion(18.64, 2, "FeSe")  # (Li,Fe)OH-like spacing ~9.32 A
    assert g["delta_d_A"] == pytest.approx(9.32 - 5.52, abs=1e-6)
    s = xrd.stage_index(9.32 + 5.52, d_filled_A=9.32, d_empty_A=5.52)
    assert s["n"] == 2 and abs(s["misfit_A"]) < 1e-9


def test_scherrer():
    L = xrd.scherrer_length(0.1, 30.0, xrd.WAVELENGTHS_A["CuKa1"], instrumental_fwhm_deg=0.05)
    assert 900 < L < 1000


# -------------------------------------------------------------------- tc
def test_tc_from_resistance_tanh():
    T = np.linspace(2, 80, 800)
    Rn = 1.0 + 0.01 * T
    R = Rn * 0.5 * (1 + np.tanh((T - 45.0) / 0.8))
    R[T < 41] = 0.0
    r = tc.tc_from_resistance(T, R, normal_window=(55, 80))
    assert r["Tc_mid50_K"] == pytest.approx(45.0, abs=0.1)
    assert r["Tc_onset90_K"] > r["Tc_mid50_K"] > r["Tc_10_K"]
    # R/Rn = 0.5(1 + tanh((T-45)/0.8)) drops below the 1e-3 threshold at T = 45 - 0.8*atanh(0.998)
    assert r["Tc_zero_K"] == pytest.approx(45.0 - 0.8 * math.atanh(0.998), abs=0.15)


def test_tc_from_magnetization_onset():
    rng = np.random.default_rng(0)
    T = np.linspace(2, 70, 300)
    M = -1e-3 * 0.5 * (1 - np.tanh((T - 48.0) / 1.0)) + rng.normal(0, 1e-7, T.size)
    r = tc.tc_from_magnetization(T, M, baseline_window=(56, 70))
    assert 49.0 < r["Tc_onset_K"] < 52.5
    assert r["T_50pct_K"] == pytest.approx(48.0, abs=0.3)


def test_demag_and_shielding_roundtrip():
    N = tc.demag_factor_prism(2.0, 2.0, 0.1)
    assert 0.85 < N < 0.95
    V = 2.0 * 2.0 * 0.1 / 1000.0  # cm3 from mm3
    H = 10.0
    chi_app = -1.0 / (1.0 - N)  # perfect diamagnet seen through demag
    M = chi_app * V * H / (4 * math.pi)
    assert tc.shielding_fraction(M, H, V, N) == pytest.approx(1.0, rel=1e-9)


def test_bulk_verdict():
    assert tc.bulk_verdict(0.8, True, None, n_samples=2) == "BULK"
    assert tc.bulk_verdict(0.8, None, None) == "PROBABLE"
    assert tc.bulk_verdict(0.02, None, None) == "FILAMENTARY"
