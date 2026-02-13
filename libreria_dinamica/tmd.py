# -*- coding: utf-8 -*-
"""
Módulo TMD - Absorbedores de Masa Sintonizada (Tuned Mass Dampers)
==================================================================

Funciones para diseño óptimo de TMD según criterios clásicos:
- Den Hartog (1956): TMD óptimo para estructura sin amortiguamiento
- Warburton (1982): TMD óptimo para estructura amortiguada
- Aplicaciones: puentes, edificios altos, maquinaria

Referencias
-----------
- Den Hartog, J.P. (1956). "Mechanical Vibrations", 4th ed., McGraw-Hill.
- Warburton, G.B. (1982). "Optimum absorber parameters for various
  combinations of response and excitation parameters."
- Connor, J.J. (2003). "Introduction to Structural Motion Control."
"""

import numpy as np
from typing import Tuple, Optional, Dict
from dataclasses import dataclass


@dataclass
class TMDOptimo:
    """
    Resultado del diseño óptimo de un TMD.

    Atributos
    ---------
    mu : float
        Ratio de masas m_d/m_s [-]
    f_opt : float
        Ratio de frecuencias óptimo ω_d/ω_s [-]
    zeta_opt : float
        Amortiguamiento óptimo del TMD [-]
    m_d : float
        Masa del TMD [kg]
    k_d : float
        Rigidez del TMD [N/m]
    c_d : float
        Amortiguamiento del TMD [N·s/m]
    omega_d : float
        Frecuencia natural del TMD [rad/s]
    reduccion_max : float
        Reducción máxima de la respuesta [-]
    """
    mu: float
    f_opt: float
    zeta_opt: float
    m_d: float
    k_d: float
    c_d: float
    omega_d: float
    reduccion_max: float


def den_hartog(m_s: float, k_s: float, mu: float) -> TMDOptimo:
    """
    Diseño óptimo de TMD según Den Hartog (1956).

    Fórmulas para estructura primaria sin amortiguamiento (ζ_s = 0)
    bajo excitación armónica. Minimiza la máxima amplificación dinámica.

    Parámetros
    ----------
    m_s : float
        Masa de la estructura principal [kg]
    k_s : float
        Rigidez de la estructura principal [N/m]
    mu : float
        Ratio de masas deseado m_d/m_s [-] (típico: 0.01-0.05)

    Retorna
    -------
    tmd : TMDOptimo
        Objeto con todos los parámetros del TMD óptimo

    Ejemplo
    -------
    >>> # Edificio de 1000 toneladas, f = 0.5 Hz, TMD del 2%
    >>> m_s = 1e6  # kg
    >>> k_s = (2*np.pi*0.5)**2 * m_s  # N/m
    >>> tmd = den_hartog(m_s, k_s, mu=0.02)
    >>> print(f"Masa TMD: {tmd.m_d/1000:.1f} t")
    >>> print(f"f_opt: {tmd.f_opt:.3f}")
    >>> print(f"ζ_opt: {tmd.zeta_opt:.3f}")

    Notas
    -----
    Fórmulas de Den Hartog:
    - Ratio de frecuencias óptimo: f_opt = 1/(1+μ)
    - Amortiguamiento óptimo: ζ_opt = √(3μ/(8(1+μ)³))
    - Reducción máxima: 1/√(1+2μ) (aproximada)

    Para μ = 2%: f_opt ≈ 0.98, ζ_opt ≈ 8.5%
    """
    # Frecuencia natural de la estructura
    omega_s = np.sqrt(k_s / m_s)

    # Fórmulas de Den Hartog
    f_opt = 1 / (1 + mu)
    zeta_opt = np.sqrt(3 * mu / (8 * (1 + mu)**3))

    # Parámetros del TMD
    m_d = mu * m_s
    omega_d = f_opt * omega_s
    k_d = m_d * omega_d**2
    c_d = 2 * zeta_opt * m_d * omega_d

    # Reducción máxima (aproximada)
    reduccion = 1 / np.sqrt(1 + 2 * mu)

    return TMDOptimo(
        mu=mu,
        f_opt=f_opt,
        zeta_opt=zeta_opt,
        m_d=m_d,
        k_d=k_d,
        c_d=c_d,
        omega_d=omega_d,
        reduccion_max=reduccion
    )


def warburton(m_s: float, k_s: float, mu: float,
              zeta_s: float = 0.02) -> TMDOptimo:
    """
    Diseño óptimo de TMD según Warburton (1982).

    Extensión del criterio de Den Hartog para estructuras con
    amortiguamiento (ζ_s ≠ 0). Las fórmulas son aproximaciones
    válidas para ζ_s < 0.1.

    Parámetros
    ----------
    m_s : float
        Masa de la estructura principal [kg]
    k_s : float
        Rigidez de la estructura principal [N/m]
    mu : float
        Ratio de masas deseado m_d/m_s [-]
    zeta_s : float
        Amortiguamiento de la estructura principal [-]

    Retorna
    -------
    tmd : TMDOptimo
        Objeto con todos los parámetros del TMD óptimo

    Notas
    -----
    Modificaciones respecto a Den Hartog:
    - f_opt se reduce ligeramente con ζ_s
    - ζ_opt aumenta con ζ_s
    """
    omega_s = np.sqrt(k_s / m_s)

    # Fórmulas de Warburton (aproximaciones para ζ_s pequeño)
    f_opt = (1 / (1 + mu)) * (1 - zeta_s * np.sqrt(mu / (1 + mu)))
    zeta_opt = np.sqrt(3 * mu / (8 * (1 + mu)**3)) + zeta_s * np.sqrt(mu)

    # Parámetros del TMD
    m_d = mu * m_s
    omega_d = f_opt * omega_s
    k_d = m_d * omega_d**2
    c_d = 2 * zeta_opt * m_d * omega_d

    # Reducción (aproximada)
    reduccion = 1 / np.sqrt(1 + 2 * mu) * (1 - 2 * zeta_s)

    return TMDOptimo(
        mu=mu,
        f_opt=f_opt,
        zeta_opt=zeta_opt,
        m_d=m_d,
        k_d=k_d,
        c_d=c_d,
        omega_d=omega_d,
        reduccion_max=reduccion
    )


def frf_con_tmd(omega: np.ndarray, m_s: float, k_s: float,
                c_s: float, tmd: TMDOptimo) -> np.ndarray:
    """
    Función de respuesta en frecuencia del sistema estructura+TMD.

    Parámetros
    ----------
    omega : np.ndarray
        Vector de frecuencias [rad/s]
    m_s : float
        Masa de la estructura [kg]
    k_s : float
        Rigidez de la estructura [N/m]
    c_s : float
        Amortiguamiento de la estructura [N·s/m]
    tmd : TMDOptimo
        Parámetros del TMD

    Retorna
    -------
    H : np.ndarray
        FRF compleja (desplazamiento/fuerza) [m/N]
    """
    m_d, k_d, c_d = tmd.m_d, tmd.k_d, tmd.c_d

    # Matrices del sistema 2DOF
    # [m_s  0 ][ẍ_s]   [c_s+c_d  -c_d][ẋ_s]   [k_s+k_d  -k_d][x_s]   [F]
    # [0  m_d][ẍ_d] + [-c_d     c_d][ẋ_d] + [-k_d     k_d][x_d] = [0]

    H = np.zeros(len(omega), dtype=complex)

    for i, w in enumerate(omega):
        # Matriz dinámica: -ω²M + iωC + K
        D = np.array([
            [-w**2 * m_s + 1j * w * (c_s + c_d) + (k_s + k_d), -1j * w * c_d - k_d],
            [-1j * w * c_d - k_d, -w**2 * m_d + 1j * w * c_d + k_d]
        ])

        # Resolver para fuerza unitaria en estructura
        F = np.array([1, 0])
        X = np.linalg.solve(D, F)
        H[i] = X[0]  # Desplazamiento de la estructura

    return H


def comparar_con_sin_tmd(m_s: float, k_s: float, zeta_s: float,
                          tmd: TMDOptimo,
                          omega_range: Optional[np.ndarray] = None) -> Dict:
    """
    Compara la respuesta de la estructura con y sin TMD.

    Parámetros
    ----------
    m_s : float
        Masa de la estructura [kg]
    k_s : float
        Rigidez de la estructura [N/m]
    zeta_s : float
        Amortiguamiento de la estructura [-]
    tmd : TMDOptimo
        Parámetros del TMD
    omega_range : np.ndarray, opcional
        Rango de frecuencias [rad/s]

    Retorna
    -------
    resultados : dict
        - 'omega': vector de frecuencias
        - 'H_sin_tmd': FRF sin TMD
        - 'H_con_tmd': FRF con TMD
        - 'max_sin_tmd': máximo sin TMD
        - 'max_con_tmd': máximo con TMD
        - 'reduccion_pct': reducción porcentual del pico
    """
    omega_s = np.sqrt(k_s / m_s)
    c_s = 2 * zeta_s * m_s * omega_s

    if omega_range is None:
        omega_range = np.linspace(0.5 * omega_s, 1.5 * omega_s, 500)

    # FRF sin TMD (SDOF)
    H_sin = np.zeros(len(omega_range), dtype=complex)
    for i, w in enumerate(omega_range):
        H_sin[i] = 1 / (-w**2 * m_s + 1j * w * c_s + k_s)

    # FRF con TMD
    H_con = frf_con_tmd(omega_range, m_s, k_s, c_s, tmd)

    # Magnitudes
    mag_sin = np.abs(H_sin)
    mag_con = np.abs(H_con)

    max_sin = np.max(mag_sin)
    max_con = np.max(mag_con)

    return {
        'omega': omega_range,
        'H_sin_tmd': H_sin,
        'H_con_tmd': H_con,
        'mag_sin_tmd': mag_sin,
        'mag_con_tmd': mag_con,
        'max_sin_tmd': max_sin,
        'max_con_tmd': max_con,
        'reduccion_pct': (1 - max_con / max_sin) * 100
    }


def tabla_diseno_tmd(m_s: float, k_s: float,
                     mu_values: np.ndarray = None) -> None:
    """
    Imprime una tabla de diseño para diferentes ratios de masa.

    Parámetros
    ----------
    m_s : float
        Masa de la estructura [kg]
    k_s : float
        Rigidez de la estructura [N/m]
    mu_values : np.ndarray, opcional
        Ratios de masa a evaluar (por defecto: 0.5% a 5%)
    """
    if mu_values is None:
        mu_values = np.array([0.005, 0.01, 0.015, 0.02, 0.03, 0.05])

    omega_s = np.sqrt(k_s / m_s)
    f_s = omega_s / (2 * np.pi)

    print("=" * 70)
    print(f"DISEÑO DE TMD - Den Hartog")
    print(f"Estructura: m = {m_s:.0f} kg, f = {f_s:.3f} Hz")
    print("=" * 70)
    print(f"{'μ [%]':>8} {'m_d [kg]':>12} {'f_opt':>8} {'ζ_opt [%]':>10} {'Reducción':>12}")
    print("-" * 70)

    for mu in mu_values:
        tmd = den_hartog(m_s, k_s, mu)
        print(f"{mu*100:>8.1f} {tmd.m_d:>12.1f} {tmd.f_opt:>8.3f} "
              f"{tmd.zeta_opt*100:>10.1f} {(1-tmd.reduccion_max)*100:>11.1f}%")

    print("=" * 70)


def diseno_tmd_edificio(m_modal: float, k_modal: float,
                         mu: float = 0.02,
                         zeta_s: float = 0.02,
                         verbose: bool = True) -> TMDOptimo:
    """
    Diseño de TMD para edificio usando propiedades modales del modo dominante.

    Parámetros
    ----------
    m_modal : float
        Masa modal efectiva del modo a controlar [kg]
    k_modal : float
        Rigidez modal [N/m]
    mu : float
        Ratio de masas deseado [-]
    zeta_s : float
        Amortiguamiento modal de la estructura [-]
    verbose : bool
        Si True, imprime resumen del diseño

    Retorna
    -------
    tmd : TMDOptimo
        Parámetros del TMD óptimo

    Ejemplo
    -------
    >>> # Edificio de 10 plantas, modo 1: M_eff = 800t, f = 0.5 Hz, ζ = 2%
    >>> m_modal = 800e3  # kg
    >>> omega_1 = 2*np.pi*0.5  # rad/s
    >>> k_modal = omega_1**2 * m_modal
    >>> tmd = diseno_tmd_edificio(m_modal, k_modal, mu=0.02, zeta_s=0.02)
    """
    # Usar Warburton si hay amortiguamiento
    if zeta_s > 0.001:
        tmd = warburton(m_modal, k_modal, mu, zeta_s)
    else:
        tmd = den_hartog(m_modal, k_modal, mu)

    if verbose:
        omega_s = np.sqrt(k_modal / m_modal)
        f_s = omega_s / (2 * np.pi)

        print("\n" + "=" * 50)
        print("DISEÑO DE TMD PARA EDIFICIO")
        print("=" * 50)
        print(f"\nEstructura principal:")
        print(f"  Masa modal efectiva: {m_modal/1000:.1f} t")
        print(f"  Frecuencia: {f_s:.3f} Hz ({omega_s:.2f} rad/s)")
        print(f"  Amortiguamiento: {zeta_s*100:.1f}%")
        print(f"\nTMD óptimo (μ = {mu*100:.1f}%):")
        print(f"  Masa: {tmd.m_d/1000:.2f} t")
        print(f"  Rigidez: {tmd.k_d/1000:.1f} kN/m")
        print(f"  Amortiguamiento: {tmd.c_d/1000:.2f} kN·s/m")
        print(f"  f_TMD/f_estructura: {tmd.f_opt:.3f}")
        print(f"  ζ_TMD: {tmd.zeta_opt*100:.1f}%")
        print(f"\nReducción esperada del pico: {(1-tmd.reduccion_max)*100:.0f}%")
        print("=" * 50)

    return tmd
