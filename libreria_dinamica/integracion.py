# -*- coding: utf-8 -*-
"""
Módulo de Integración Numérica
==============================

Métodos de integración temporal para ecuaciones de movimiento:
- Método de Newmark (aceleración promedio y lineal)
- Método de diferencias centrales
- Integral de Duhamel (convolución numérica)
"""

import numpy as np
from typing import Tuple, Union, Callable, Optional


def newmark(m: float, c: float, k: float,
            F: np.ndarray, dt: float,
            u0: float = 0.0, v0: float = 0.0,
            gamma: float = 0.5, beta: float = 0.25) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Integración por método de Newmark para sistema SDOF.

    Parámetros
    ----------
    m : float
        Masa [kg]
    c : float
        Amortiguamiento [N·s/m]
    k : float
        Rigidez [N/m]
    F : np.ndarray
        Vector de fuerzas en cada paso de tiempo [N]
    dt : float
        Paso de tiempo [s]
    u0 : float
        Desplazamiento inicial [m]
    v0 : float
        Velocidad inicial [m/s]
    gamma : float
        Parámetro gamma de Newmark (0.5 para precisión 2do orden)
    beta : float
        Parámetro beta de Newmark:
        - 0.25: aceleración promedio (incondicionalmente estable)
        - 1/6: aceleración lineal
        - 0: diferencias centrales (explícito, condicionalmente estable)

    Retorna
    -------
    u : np.ndarray
        Desplazamiento [m]
    v : np.ndarray
        Velocidad [m/s]
    a : np.ndarray
        Aceleración [m/s²]

    Notas
    -----
    El método con gamma=0.5 y beta=0.25 (aceleración promedio) es:
    - Incondicionalmente estable
    - Sin amortiguamiento numérico
    - Precisión de segundo orden

    Para beta=0 (diferencias centrales), el criterio de estabilidad es:
    dt < T_n / pi
    """
    n = len(F)

    # Arrays de salida
    u = np.zeros(n)
    v = np.zeros(n)
    a = np.zeros(n)

    # Condiciones iniciales
    u[0] = u0
    v[0] = v0
    a[0] = (F[0] - c * v0 - k * u0) / m

    # Constantes de integración
    a1 = 1 / (beta * dt**2)
    a2 = 1 / (beta * dt)
    a3 = 1 / (2 * beta) - 1
    a4 = gamma / (beta * dt)
    a5 = gamma / beta - 1
    a6 = dt * (gamma / (2 * beta) - 1)

    # Rigidez efectiva
    k_eff = k + a4 * c + a1 * m

    # Bucle de integración
    for i in range(n - 1):
        # Fuerza efectiva
        F_eff = F[i + 1] + m * (a1 * u[i] + a2 * v[i] + a3 * a[i]) + \
                c * (a4 * u[i] + a5 * v[i] + a6 * a[i])

        # Resolver desplazamiento
        u[i + 1] = F_eff / k_eff

        # Actualizar aceleración y velocidad
        a[i + 1] = a1 * (u[i + 1] - u[i]) - a2 * v[i] - a3 * a[i]
        v[i + 1] = v[i] + dt * ((1 - gamma) * a[i] + gamma * a[i + 1])

    return u, v, a


def diferencias_centrales(m: float, c: float, k: float,
                          F: np.ndarray, dt: float,
                          u0: float = 0.0, v0: float = 0.0) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Integración por método de diferencias centrales (explícito).

    Parámetros
    ----------
    m : float
        Masa [kg]
    c : float
        Amortiguamiento [N·s/m]
    k : float
        Rigidez [N/m]
    F : np.ndarray
        Vector de fuerzas en cada paso de tiempo [N]
    dt : float
        Paso de tiempo [s]
    u0 : float
        Desplazamiento inicial [m]
    v0 : float
        Velocidad inicial [m/s]

    Retorna
    -------
    u : np.ndarray
        Desplazamiento [m]
    v : np.ndarray
        Velocidad [m/s]
    a : np.ndarray
        Aceleración [m/s²]

    Notas
    -----
    Este método es condicionalmente estable. El criterio de estabilidad es:
    dt < T_n / pi  o equivalentemente  dt < 2 / omega_n

    Ventajas:
    - Método explícito (no requiere resolver ecuaciones)
    - Muy eficiente para problemas de propagación de ondas

    Desventajas:
    - Requiere paso de tiempo pequeño
    - Puede tener oscilaciones numéricas
    """
    n = len(F)

    # Verificar estabilidad
    omega_n = np.sqrt(k / m)
    dt_critico = 2 / omega_n
    if dt >= dt_critico:
        import warnings
        warnings.warn(f"dt={dt:.4f}s >= dt_critico={dt_critico:.4f}s. "
                      f"El método puede ser inestable.")

    # Arrays de salida
    u = np.zeros(n)
    v = np.zeros(n)
    a = np.zeros(n)

    # Condiciones iniciales
    u[0] = u0
    v[0] = v0
    a[0] = (F[0] - c * v0 - k * u0) / m

    # Calcular u_{-1} usando expansión de Taylor
    u_minus1 = u0 - dt * v0 + 0.5 * dt**2 * a[0]

    # Constantes
    c1 = m / dt**2 + c / (2 * dt)
    c2 = k - 2 * m / dt**2
    c3 = m / dt**2 - c / (2 * dt)

    # Primer paso especial
    u[1] = (F[0] - c2 * u[0] - c3 * u_minus1) / c1

    # Bucle de integración
    u_prev = u_minus1
    for i in range(1, n - 1):
        u[i + 1] = (F[i] - c2 * u[i] - c3 * u_prev) / c1
        u_prev = u[i]

    # Calcular velocidades y aceleraciones
    for i in range(1, n - 1):
        v[i] = (u[i + 1] - u[i - 1]) / (2 * dt)
        a[i] = (u[i + 1] - 2 * u[i] + u[i - 1]) / dt**2

    # Bordes
    v[0] = v0
    v[-1] = (u[-1] - u[-2]) / dt
    a[-1] = (F[-1] - c * v[-1] - k * u[-1]) / m

    return u, v, a


def duhamel(m: float, c: float, k: float,
            F: np.ndarray, t: np.ndarray,
            u0: float = 0.0, v0: float = 0.0) -> np.ndarray:
    """
    Integral de Duhamel (convolución numérica).

    Calcula la respuesta de un sistema SDOF a una carga arbitraria
    mediante convolución con la respuesta impulsiva.

    Parámetros
    ----------
    m : float
        Masa [kg]
    c : float
        Amortiguamiento [N·s/m]
    k : float
        Rigidez [N/m]
    F : np.ndarray
        Vector de fuerzas [N]
    t : np.ndarray
        Vector de tiempos [s]
    u0 : float
        Desplazamiento inicial [m]
    v0 : float
        Velocidad inicial [m/s]

    Retorna
    -------
    u : np.ndarray
        Desplazamiento [m]

    Notas
    -----
    La integral de Duhamel es:
    u(t) = (1/m*omega_d) * integral_0^t F(tau) * exp(-zeta*omega_n*(t-tau))
                                               * sin(omega_d*(t-tau)) dtau
           + u_libre(t)

    Este método usa convolución discreta, que puede ser menos preciso que
    Newmark para pasos de tiempo grandes.
    """
    # Propiedades del sistema
    omega_n = np.sqrt(k / m)
    c_cr = 2 * np.sqrt(k * m)
    zeta = c / c_cr
    omega_d = omega_n * np.sqrt(1 - zeta**2)

    n = len(t)
    dt = t[1] - t[0]  # Asume paso constante

    # Respuesta impulsiva
    def h(tau):
        return (1 / (m * omega_d)) * np.exp(-zeta * omega_n * tau) * np.sin(omega_d * tau)

    # Convolución numérica (método del trapecio)
    u = np.zeros(n)

    for i in range(n):
        # Integral de convolución
        integral = 0.0
        for j in range(i + 1):
            tau = t[i] - t[j]
            if j == 0 or j == i:
                weight = 0.5
            else:
                weight = 1.0
            integral += weight * F[j] * h(tau) * dt

        # Respuesta libre
        if zeta < 1:
            A = np.sqrt(u0**2 + ((v0 + zeta * omega_n * u0) / omega_d)**2)
            phi = np.arctan2(u0 * omega_d, v0 + zeta * omega_n * u0)
            u_libre = A * np.exp(-zeta * omega_n * t[i]) * np.sin(omega_d * t[i] + phi)
        else:
            u_libre = 0

        u[i] = integral + u_libre

    return u


def respuesta_rampa(sistema, F0: float, t1: float, t: np.ndarray) -> np.ndarray:
    """
    Respuesta analítica a carga rampa que crece de 0 a F0 en tiempo t1.

    Parámetros
    ----------
    sistema : SDOF
        Sistema SDOF
    F0 : float
        Fuerza final [N]
    t1 : float
        Tiempo de rampa [s]
    t : np.ndarray
        Vector de tiempos [s]

    Retorna
    -------
    u : np.ndarray
        Desplazamiento [m]
    """
    k = sistema.k
    omega_n = sistema.omega_n
    omega_d = sistema.omega_d
    zeta = sistema.zeta

    u = np.zeros_like(t)

    # Fase de rampa (0 <= t <= t1)
    mask1 = (t >= 0) & (t <= t1)
    t_ramp = t[mask1]

    u[mask1] = (F0 / k) * (t_ramp / t1 - (1 / (omega_n * t1)) *
                          (2 * zeta + (1 / omega_d) *
                           (omega_n**2 / omega_d - omega_d) *
                           np.exp(-zeta * omega_n * t_ramp) *
                           np.sin(omega_d * t_ramp)) -
                          (2 * zeta / (omega_n * t1)) *
                          (1 - np.exp(-zeta * omega_n * t_ramp) *
                           np.cos(omega_d * t_ramp)))

    # Fase constante (t > t1) - requiere superposición
    mask2 = t > t1
    # Simplificación: usar respuesta estática + transitorio
    u[mask2] = F0 / k  # Aproximación (el transitorio se amortiguaría)

    return u


def espectro_choque(m: float, k: float, zeta: float,
                    F_func: Callable[[np.ndarray], np.ndarray],
                    t_d: float, T_range: np.ndarray) -> np.ndarray:
    """
    Calcula el espectro de choque (shock response spectrum).

    Parámetros
    ----------
    m : float
        Masa [kg]
    k : float
        Rigidez [N/m]
    zeta : float
        Razón de amortiguamiento
    F_func : callable
        Función F(t) que devuelve la fuerza
    t_d : float
        Duración del pulso [s]
    T_range : np.ndarray
        Rango de períodos naturales [s]

    Retorna
    -------
    SRS : np.ndarray
        Espectro de choque (desplazamiento máximo normalizado)
    """
    SRS = np.zeros_like(T_range)

    for i, T_n in enumerate(T_range):
        # Sistema con este período natural
        omega_n = 2 * np.pi / T_n
        k_i = m * omega_n**2
        c_i = 2 * zeta * np.sqrt(k_i * m)

        # Tiempo de análisis (suficiente para capturar máximo)
        t_max = max(5 * T_n, 2 * t_d)
        dt = min(T_n / 20, t_d / 50)
        t = np.arange(0, t_max, dt)
        F = F_func(t)

        # Integrar con Newmark
        u, _, _ = newmark(m, c_i, k_i, F, dt)

        # Desplazamiento estático de referencia
        F_max = np.max(np.abs(F))
        u_st = F_max / k_i

        # Factor de amplificación (SRS normalizado)
        SRS[i] = np.max(np.abs(u)) / u_st if u_st > 0 else 0

    return SRS
