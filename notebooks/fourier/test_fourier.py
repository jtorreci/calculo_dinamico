"""Comprobaciones de fourier.py:  python -m pytest -q test_fourier.py"""

import numpy as np

import fourier as fu

M = 4096


def test_seno_solo_armonico_2():
    caso = fu.caso_seno(T=2.0, frecuencia=1.0, M=M, n_max=12)
    assert abs(caso["b"][2] - 1.0) < 1e-9
    assert np.all(np.abs(np.delete(caso["b"], 2)) < 1e-9)
    assert np.all(np.abs(caso["a"]) < 1e-9)


def test_suma_de_senos_amplitudes_y_fases():
    componentes = [
        {"amplitud": 1.00, "frecuencia": 1.0, "fase": 0.0, "tipo": "sen"},
        {"amplitud": 0.50, "frecuencia": 3.0, "fase": np.pi / 4, "tipo": "sen"},
        {"amplitud": 0.25, "frecuencia": 5.0, "fase": 0.0, "tipo": "cos"},
    ]
    caso = fu.caso_suma_senos(2.0, componentes, M, 16)
    np.testing.assert_allclose(caso["A"][[2, 6, 10]], [1.0, 0.5, 0.25], atol=1e-9)
    np.testing.assert_allclose(caso["fase"][[2, 6, 10]], [0.0, np.pi / 4, np.pi / 2], atol=1e-9)


def test_lcg_valores_conocidos():
    # x_1 = (1664525·12345 + 1013904223) mod 2^32
    assert fu.lcg(1)[0] == (1664525 * 12345 + 1013904223) % 2**32
    v = fu.normalizar_lcg(fu.lcg(32))
    assert np.all((v >= -1) & (v < 1))


def test_fft_igual_a_integral():
    caso = fu.caso_pseudoaleatorio(2.0, 32, 12345, M, 64)
    a, b = fu.coeficientes_fft(caso["f"][:-1], 64)
    np.testing.assert_allclose(a, caso["a"], atol=1e-12)
    np.testing.assert_allclose(b, caso["b"], atol=1e-12)


def test_parseval_y_error_decreciente():
    caso = fu.caso_pseudoaleatorio(2.0, 32, 12345, M, 64)
    barrido = fu.barrido_reconstruccion(caso, range(65))
    assert np.all(np.diff(barrido["e_rms"]) <= 1e-12)
    cociente = barrido["potencia_serie"] / barrido["potencia_senal"]
    np.testing.assert_allclose(cociente, 1 - barrido["e_rms"] ** 2, atol=1e-10)
