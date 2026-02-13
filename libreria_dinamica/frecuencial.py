# -*- coding: utf-8 -*-
"""
Módulo de Análisis Frecuencial
==============================

Funciones para análisis en el dominio de la frecuencia:
- Funciones de respuesta en frecuencia (FRF): receptancia, movilidad, acelerancia
- Espectros de respuesta
- Diagramas de Bode
- Análisis de transmisibilidad
"""

import numpy as np
from typing import Tuple, Union, Optional


def frf_receptancia(omega: np.ndarray, m: float, c: float, k: float,
                    normalizar: bool = False) -> np.ndarray:
    """
    Función de respuesta en frecuencia - Receptancia H(omega) = X/F.

    Parámetros
    ----------
    omega : np.ndarray
        Frecuencias angulares [rad/s]
    m : float
        Masa [kg]
    c : float
        Amortiguamiento [N·s/m]
    k : float
        Rigidez [N/m]
    normalizar : bool
        Si True, normaliza por rigidez estática (1/k)

    Retorna
    -------
    H : np.ndarray (complex)
        Receptancia [m/N] o [-] si normalizada
    """
    H = 1 / (k - m * omega**2 + 1j * c * omega)

    if normalizar:
        H = H * k

    return H


def frf_movilidad(omega: np.ndarray, m: float, c: float, k: float) -> np.ndarray:
    """
    Función de respuesta en frecuencia - Movilidad Y(omega) = V/F.

    Parámetros
    ----------
    omega : np.ndarray
        Frecuencias angulares [rad/s]
    m, c, k : float
        Parámetros del sistema

    Retorna
    -------
    Y : np.ndarray (complex)
        Movilidad [m/s/N]
    """
    H = frf_receptancia(omega, m, c, k)
    return 1j * omega * H


def frf_acelerancia(omega: np.ndarray, m: float, c: float, k: float) -> np.ndarray:
    """
    Función de respuesta en frecuencia - Acelerancia A(omega) = a/F.

    Parámetros
    ----------
    omega : np.ndarray
        Frecuencias angulares [rad/s]
    m, c, k : float
        Parámetros del sistema

    Retorna
    -------
    A : np.ndarray (complex)
        Acelerancia [m/s²/N]
    """
    H = frf_receptancia(omega, m, c, k)
    return -omega**2 * H


def diagrama_bode(omega: np.ndarray, H: np.ndarray,
                  ref_dB: float = 1.0) -> Tuple[np.ndarray, np.ndarray]:
    """
    Convierte FRF a formato de diagrama de Bode.

    Parámetros
    ----------
    omega : np.ndarray
        Frecuencias angulares [rad/s]
    H : np.ndarray (complex)
        Función de respuesta en frecuencia
    ref_dB : float
        Referencia para escala dB

    Retorna
    -------
    magnitud_dB : np.ndarray
        Magnitud en dB
    fase_deg : np.ndarray
        Fase en grados
    """
    magnitud_dB = 20 * np.log10(np.abs(H) / ref_dB)
    fase_deg = np.angle(H, deg=True)

    # Desenvolver fase para continuidad
    fase_deg = np.unwrap(np.angle(H)) * 180 / np.pi

    return magnitud_dB, fase_deg


def espectro_respuesta(aceleracion: np.ndarray, dt: float,
                       T_range: np.ndarray, zeta: float = 0.05,
                       tipo: str = 'Sa') -> np.ndarray:
    """
    Calcula el espectro de respuesta a partir de un acelerograma.

    Parámetros
    ----------
    aceleracion : np.ndarray
        Aceleración del suelo [m/s²]
    dt : float
        Paso de tiempo [s]
    T_range : np.ndarray
        Períodos naturales para el espectro [s]
    zeta : float
        Razón de amortiguamiento (por defecto 5%)
    tipo : str
        Tipo de espectro:
        - 'Sd': Espectro de desplazamiento
        - 'Sv': Espectro de velocidad (pseudo)
        - 'Sa': Espectro de aceleración (pseudo)

    Retorna
    -------
    S : np.ndarray
        Valores espectrales
    """
    from .integracion import newmark

    n_periodos = len(T_range)
    S = np.zeros(n_periodos)

    # Fuerza efectiva = -m * aceleracion_suelo (para m=1)
    m = 1.0
    F = -m * aceleracion

    for i, T_n in enumerate(T_range):
        if T_n <= 0:
            continue

        omega_n = 2 * np.pi / T_n
        k = m * omega_n**2
        c = 2 * zeta * omega_n * m

        # Integrar ecuación de movimiento
        u, v, a = newmark(m, c, k, F, dt)

        # Desplazamiento máximo relativo
        Sd = np.max(np.abs(u))

        if tipo == 'Sd':
            S[i] = Sd
        elif tipo == 'Sv':
            S[i] = omega_n * Sd  # Pseudo-velocidad
        elif tipo == 'Sa':
            S[i] = omega_n**2 * Sd  # Pseudo-aceleración

    return S


def transmisibilidad_fuerza(r: np.ndarray, zeta: float) -> np.ndarray:
    """
    Transmisibilidad de fuerza para excitación de base.

    Parámetros
    ----------
    r : np.ndarray
        Ratio de frecuencias omega/omega_n
    zeta : float
        Razón de amortiguamiento

    Retorna
    -------
    TR : np.ndarray
        Transmisibilidad
    """
    return np.sqrt((1 + (2 * zeta * r)**2) /
                   ((1 - r**2)**2 + (2 * zeta * r)**2))


def transmisibilidad_desplazamiento_relativo(r: np.ndarray, zeta: float) -> np.ndarray:
    """
    Razón de desplazamiento relativo Z/Y para excitación de base.

    Parámetros
    ----------
    r : np.ndarray
        Ratio de frecuencias omega/omega_n
    zeta : float
        Razón de amortiguamiento

    Retorna
    -------
    Z_Y : np.ndarray
        Razón de desplazamiento relativo
    """
    return r**2 / np.sqrt((1 - r**2)**2 + (2 * zeta * r)**2)


def ancho_banda_3dB(omega_n: float, zeta: float) -> Tuple[float, float, float]:
    """
    Calcula las frecuencias a -3dB (media potencia) y el ancho de banda.

    Parámetros
    ----------
    omega_n : float
        Frecuencia natural [rad/s]
    zeta : float
        Razón de amortiguamiento

    Retorna
    -------
    omega_1 : float
        Frecuencia inferior a -3dB [rad/s]
    omega_2 : float
        Frecuencia superior a -3dB [rad/s]
    delta_omega : float
        Ancho de banda [rad/s]
    """
    # Aproximación para zeta pequeño
    omega_1 = omega_n * (1 - zeta)
    omega_2 = omega_n * (1 + zeta)
    delta_omega = 2 * zeta * omega_n

    return omega_1, omega_2, delta_omega


def frf_modal_sdof(omega: np.ndarray, omega_n: float, zeta: float,
                   A: complex = 1.0) -> np.ndarray:
    """
    FRF de un modo SDOF con residuo A.

    Parámetros
    ----------
    omega : np.ndarray
        Frecuencias [rad/s]
    omega_n : float
        Frecuencia natural del modo [rad/s]
    zeta : float
        Amortiguamiento del modo
    A : complex
        Residuo modal (constante modal)

    Retorna
    -------
    H : np.ndarray (complex)
        Contribución modal a la FRF
    """
    r = omega / omega_n
    return A / (omega_n**2 * (1 - r**2 + 2j * zeta * r))


def frf_modal_suma(omega: np.ndarray, modos: list) -> np.ndarray:
    """
    FRF como suma de contribuciones modales.

    Parámetros
    ----------
    omega : np.ndarray
        Frecuencias [rad/s]
    modos : list of dict
        Lista de diccionarios con 'omega_n', 'zeta', 'A' para cada modo

    Retorna
    -------
    H : np.ndarray (complex)
        FRF total
    """
    H = np.zeros(len(omega), dtype=complex)

    for modo in modos:
        H += frf_modal_sdof(omega, modo['omega_n'], modo['zeta'], modo['A'])

    return H


def psd_respuesta(S_input: np.ndarray, H: np.ndarray) -> np.ndarray:
    """
    PSD de respuesta dado PSD de entrada y FRF.

    S_output(f) = |H(f)|^2 * S_input(f)

    Parámetros
    ----------
    S_input : np.ndarray
        PSD de la excitación
    H : np.ndarray (complex)
        Función de transferencia

    Retorna
    -------
    S_output : np.ndarray
        PSD de la respuesta
    """
    return np.abs(H)**2 * S_input


def varianza_desde_psd(S: np.ndarray, df: float) -> float:
    """
    Calcula la varianza integrando la PSD.

    sigma^2 = integral S(f) df

    Parámetros
    ----------
    S : np.ndarray
        Densidad espectral de potencia
    df : float
        Resolución en frecuencia [Hz]

    Retorna
    -------
    varianza : float
        Varianza de la señal
    """
    return np.trapz(S, dx=df)


def kanai_tajimi(f: np.ndarray, omega_g: float, zeta_g: float,
                 S0: float) -> np.ndarray:
    """
    Modelo de PSD de Kanai-Tajimi para aceleración del suelo.

    Parámetros
    ----------
    f : np.ndarray
        Frecuencias [Hz]
    omega_g : float
        Frecuencia dominante del suelo [rad/s]
    zeta_g : float
        Amortiguamiento del suelo
    S0 : float
        Nivel de ruido blanco [m²/s³/rad]

    Retorna
    -------
    S : np.ndarray
        PSD de Kanai-Tajimi [m²/s³/rad]
    """
    omega = 2 * np.pi * f
    r = omega / omega_g

    numerador = 1 + (2 * zeta_g * r)**2
    denominador = (1 - r**2)**2 + (2 * zeta_g * r)**2

    return S0 * numerador / denominador
