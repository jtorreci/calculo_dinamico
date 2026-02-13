# -*- coding: utf-8 -*-
"""
Módulo SDOF - Sistemas de Un Grado de Libertad
==============================================

Clase principal para análisis de sistemas SDOF con métodos para:
- Propiedades dinámicas (frecuencia natural, período, amortiguamiento)
- Vibración libre amortiguada
- Respuesta a excitación armónica
- Respuesta a cargas arbitrarias (integral de Duhamel)
"""

import numpy as np
from typing import Tuple, Optional, Union, Callable


class SDOF:
    """
    Sistema de un grado de libertad (SDOF).

    Parámetros
    ----------
    m : float
        Masa [kg]
    k : float
        Rigidez [N/m]
    c : float, opcional
        Amortiguamiento viscoso [N·s/m]. Si no se proporciona, se calcula desde zeta.
    zeta : float, opcional
        Razón de amortiguamiento [-]. Por defecto 0.05 (5%).

    Atributos
    ---------
    omega_n : float
        Frecuencia natural circular [rad/s]
    f_n : float
        Frecuencia natural [Hz]
    T_n : float
        Período natural [s]
    omega_d : float
        Frecuencia amortiguada [rad/s]
    c_cr : float
        Amortiguamiento crítico [N·s/m]
    """

    def __init__(self, m: float, k: float, c: Optional[float] = None,
                 zeta: Optional[float] = None):
        self.m = m
        self.k = k

        # Propiedades naturales
        self.omega_n = np.sqrt(k / m)
        self.f_n = self.omega_n / (2 * np.pi)
        self.T_n = 1 / self.f_n

        # Amortiguamiento crítico
        self.c_cr = 2 * np.sqrt(k * m)

        # Determinar c y zeta
        if c is not None:
            self.c = c
            self.zeta = c / self.c_cr
        elif zeta is not None:
            self.zeta = zeta
            self.c = zeta * self.c_cr
        else:
            self.zeta = 0.05  # 5% por defecto
            self.c = self.zeta * self.c_cr

        # Frecuencia amortiguada
        if self.zeta < 1:
            self.omega_d = self.omega_n * np.sqrt(1 - self.zeta**2)
        else:
            self.omega_d = 0  # Sistema sobreamortiguado

    def __repr__(self) -> str:
        return (f"SDOF(m={self.m:.2f} kg, k={self.k:.2f} N/m, "
                f"zeta={self.zeta:.3f}, f_n={self.f_n:.2f} Hz)")

    def vibracion_libre(self, t: np.ndarray, u0: float = 1.0,
                        v0: float = 0.0) -> np.ndarray:
        """
        Respuesta en vibración libre con condiciones iniciales.

        Parámetros
        ----------
        t : np.ndarray
            Vector de tiempos [s]
        u0 : float
            Desplazamiento inicial [m]
        v0 : float
            Velocidad inicial [m/s]

        Retorna
        -------
        u : np.ndarray
            Desplazamiento en función del tiempo [m]
        """
        if self.zeta >= 1:
            raise NotImplementedError("Solo sistemas subamortiguados implementados")

        # Amplitud y fase
        A = np.sqrt(u0**2 + ((v0 + self.zeta * self.omega_n * u0) / self.omega_d)**2)
        phi = np.arctan2(u0 * self.omega_d, v0 + self.zeta * self.omega_n * u0)

        # Respuesta
        u = A * np.exp(-self.zeta * self.omega_n * t) * np.sin(self.omega_d * t + phi)
        return u

    def respuesta_armonica(self, t: np.ndarray, F0: float,
                           omega: float) -> Tuple[np.ndarray, float, float]:
        """
        Respuesta estacionaria a excitación armónica F(t) = F0*sin(omega*t).

        Parámetros
        ----------
        t : np.ndarray
            Vector de tiempos [s]
        F0 : float
            Amplitud de la fuerza [N]
        omega : float
            Frecuencia de excitación [rad/s]

        Retorna
        -------
        u : np.ndarray
            Desplazamiento [m]
        X : float
            Amplitud de respuesta [m]
        phi : float
            Desfase [rad]
        """
        r = omega / self.omega_n

        # Factor de amplificación dinámica
        DAF = 1 / np.sqrt((1 - r**2)**2 + (2 * self.zeta * r)**2)

        # Amplitud y fase
        X = (F0 / self.k) * DAF
        phi = np.arctan2(2 * self.zeta * r, 1 - r**2)

        # Respuesta estacionaria
        u = X * np.sin(omega * t - phi)

        return u, X, phi

    def factor_amplificacion(self, r: Union[float, np.ndarray]) -> np.ndarray:
        """
        Factor de amplificación dinámica (DAF).

        Parámetros
        ----------
        r : float o np.ndarray
            Ratio de frecuencias omega/omega_n

        Retorna
        -------
        DAF : np.ndarray
            Factor de amplificación dinámica
        """
        r = np.asarray(r)
        return 1 / np.sqrt((1 - r**2)**2 + (2 * self.zeta * r)**2)

    def transmisibilidad(self, r: Union[float, np.ndarray]) -> np.ndarray:
        """
        Transmisibilidad de fuerza/desplazamiento.

        Parámetros
        ----------
        r : float o np.ndarray
            Ratio de frecuencias omega/omega_n

        Retorna
        -------
        TR : np.ndarray
            Transmisibilidad
        """
        r = np.asarray(r)
        return np.sqrt((1 + (2 * self.zeta * r)**2) /
                       ((1 - r**2)**2 + (2 * self.zeta * r)**2))

    def respuesta_impulsiva(self, t: np.ndarray) -> np.ndarray:
        """
        Respuesta impulsiva h(t) del sistema.

        Parámetros
        ----------
        t : np.ndarray
            Vector de tiempos [s]

        Retorna
        -------
        h : np.ndarray
            Respuesta impulsiva [m/(N·s)]
        """
        h = np.zeros_like(t)
        mask = t >= 0
        h[mask] = (1 / (self.m * self.omega_d)) * \
                  np.exp(-self.zeta * self.omega_n * t[mask]) * \
                  np.sin(self.omega_d * t[mask])
        return h

    def decremento_logaritmico(self, n_ciclos: int = 1) -> float:
        """
        Decremento logarítmico para n ciclos.

        Parámetros
        ----------
        n_ciclos : int
            Número de ciclos

        Retorna
        -------
        delta : float
            Decremento logarítmico
        """
        return n_ciclos * 2 * np.pi * self.zeta / np.sqrt(1 - self.zeta**2)

    def ciclos_para_reduccion(self, fraccion: float) -> float:
        """
        Número de ciclos para reducir la amplitud a una fracción dada.

        Parámetros
        ----------
        fraccion : float
            Fracción de la amplitud original (ej: 0.1 para 10%)

        Retorna
        -------
        n : float
            Número de ciclos necesarios
        """
        delta = self.decremento_logaritmico(1)
        return np.log(1 / fraccion) / delta
