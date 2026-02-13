# -*- coding: utf-8 -*-
"""
Módulo MDOF - Sistemas de Múltiples Grados de Libertad
======================================================

Funciones para análisis modal, matrices de masa y rigidez,
y respuesta de sistemas MDOF.
"""

import numpy as np
from scipy import linalg
from typing import Tuple, Optional, List, Union


class MDOF:
    """
    Clase para sistemas de múltiples grados de libertad.

    Parámetros
    ----------
    M : np.ndarray
        Matriz de masa [kg]
    K : np.ndarray
        Matriz de rigidez [N/m]
    C : np.ndarray, opcional
        Matriz de amortiguamiento [N·s/m]
    """

    def __init__(self, M: np.ndarray, K: np.ndarray, C: Optional[np.ndarray] = None):
        self.M = np.atleast_2d(M).astype(float)
        self.K = np.atleast_2d(K).astype(float)
        self.n_dof = self.M.shape[0]

        if C is not None:
            self.C = np.atleast_2d(C).astype(float)
        else:
            self.C = np.zeros_like(self.M)

        # Calcular propiedades modales
        self._calcular_modos()

    def _calcular_modos(self):
        """Calcula frecuencias naturales y modos de vibración."""
        # Resolver problema de autovalores generalizado: K·φ = ω²·M·φ
        eigenvalues, eigenvectors = linalg.eigh(self.K, self.M)

        # Ordenar por frecuencia
        idx = np.argsort(eigenvalues)
        self.omega2 = eigenvalues[idx]
        self.omega = np.sqrt(np.maximum(self.omega2, 0))  # rad/s
        self.f_n = self.omega / (2 * np.pi)  # Hz
        self.freq = self.f_n  # Alias
        self.T_n = np.where(self.f_n > 0, 1 / self.f_n, np.inf)  # s
        self.T = self.T_n  # Alias

        # Modos (columnas)
        self.phi = eigenvectors[:, idx]

        # Normalizar modos con masa unitaria: φᵀ·M·φ = 1
        for i in range(self.n_dof):
            norm = np.sqrt(self.phi[:, i] @ self.M @ self.phi[:, i])
            self.phi[:, i] /= norm

        # Verificar normalización
        self.M_modal = self.phi.T @ self.M @ self.phi  # Debe ser ≈ I
        self.K_modal = self.phi.T @ self.K @ self.phi  # Debe ser ≈ diag(ω²)

    def factores_participacion(self, r: Optional[np.ndarray] = None) -> np.ndarray:
        """
        Calcula los factores de participación modal.

        Parámetros
        ----------
        r : np.ndarray, opcional
            Vector de influencia (por defecto, vector unitario para excitación de base)

        Retorna
        -------
        Gamma : np.ndarray
            Factores de participación modal
        """
        if r is None:
            r = np.ones(self.n_dof)

        Gamma = np.zeros(self.n_dof)
        for i in range(self.n_dof):
            Gamma[i] = self.phi[:, i] @ self.M @ r

        return Gamma

    def masas_efectivas(self, r: Optional[np.ndarray] = None) -> Tuple[np.ndarray, np.ndarray, float]:
        """
        Calcula las masas modales efectivas.

        Parámetros
        ----------
        r : np.ndarray, opcional
            Vector de influencia

        Retorna
        -------
        M_eff : np.ndarray
            Masas efectivas [kg]
        pct : np.ndarray
            Porcentajes de masa participante [%]
        M_total : float
            Masa total del sistema [kg]
        """
        Gamma = self.factores_participacion(r)
        M_total = np.sum(np.diag(self.M))

        # Para modos masa-unitaria: M_eff = Γ²
        M_eff = Gamma ** 2
        pct = 100 * M_eff / M_total

        return M_eff, pct, M_total

    def respuesta_modal_armonica(self, F0: np.ndarray, Omega: float,
                                  zeta: Optional[np.ndarray] = None) -> np.ndarray:
        """
        Respuesta estacionaria a excitación armónica por superposición modal.

        Parámetros
        ----------
        F0 : np.ndarray
            Amplitud del vector de fuerzas [N]
        Omega : float
            Frecuencia de excitación [rad/s]
        zeta : np.ndarray, opcional
            Amortiguamientos modales (por defecto 0)

        Retorna
        -------
        X : np.ndarray
            Amplitudes complejas de desplazamiento [m]
        """
        if zeta is None:
            zeta = np.zeros(self.n_dof)

        # Fuerzas modales
        f_modal = self.phi.T @ F0

        # Respuesta modal
        q = np.zeros(self.n_dof, dtype=complex)
        for i in range(self.n_dof):
            r = Omega / self.omega[i] if self.omega[i] > 0 else 0
            H = 1 / (1 - r**2 + 2j * zeta[i] * r)
            q[i] = f_modal[i] / self.omega[i]**2 * H if self.omega[i] > 0 else 0

        # Reconstruir respuesta física
        X = self.phi @ q

        return X

    def respuesta_libre(self, x0: np.ndarray, v0: np.ndarray,
                        t: np.ndarray) -> np.ndarray:
        """
        Respuesta libre (vibración libre no amortiguada).

        Parámetros
        ----------
        x0 : np.ndarray
            Desplazamientos iniciales [m]
        v0 : np.ndarray
            Velocidades iniciales [m/s]
        t : np.ndarray
            Vector de tiempos [s]

        Retorna
        -------
        x : np.ndarray
            Historia de desplazamientos [m] (n_dof × len(t))
        """
        # Condiciones iniciales modales
        q0 = self.phi.T @ self.M @ x0
        dq0 = self.phi.T @ self.M @ v0

        # Respuesta modal
        x = np.zeros((self.n_dof, len(t)))
        for i in range(self.n_dof):
            if self.omega[i] > 0:
                q_t = q0[i] * np.cos(self.omega[i] * t) + \
                      dq0[i] / self.omega[i] * np.sin(self.omega[i] * t)
            else:
                q_t = q0[i] + dq0[i] * t

            x += np.outer(self.phi[:, i], q_t)

        return x

    def __repr__(self):
        freqs = ', '.join([f'{f:.2f}' for f in self.f_n])
        return f"MDOF({self.n_dof} DOF, f_n = [{freqs}] Hz)"


def shear_building(m: np.ndarray, k: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Genera matrices M y K para un edificio de corte (shear building).

    Parámetros
    ----------
    m : np.ndarray
        Masas de cada planta [kg]
    k : np.ndarray
        Rigideces de entreplanta [N/m]

    Retorna
    -------
    M : np.ndarray
        Matriz de masa diagonal
    K : np.ndarray
        Matriz de rigidez tridiagonal
    """
    n = len(m)
    M = np.diag(m)

    K = np.zeros((n, n))
    for i in range(n):
        if i == 0:
            K[i, i] = k[0] + (k[1] if n > 1 else 0)
            if n > 1:
                K[i, i + 1] = -k[1]
        elif i == n - 1:
            K[i, i] = k[i]
            K[i, i - 1] = -k[i]
        else:
            K[i, i] = k[i] + k[i + 1]
            K[i, i - 1] = -k[i]
            K[i, i + 1] = -k[i + 1]

    return M, K


def shear_building_uniforme(n: int, m: float, k: float) -> Tuple[np.ndarray, np.ndarray]:
    """
    Genera matrices M y K para un edificio de corte uniforme.

    Parámetros
    ----------
    n : int
        Número de plantas
    m : float
        Masa por planta [kg]
    k : float
        Rigidez por entreplanta [N/m]

    Retorna
    -------
    M : np.ndarray
        Matriz de masa diagonal
    K : np.ndarray
        Matriz de rigidez tridiagonal
    """
    masses = np.full(n, m)
    stiffs = np.full(n, k)
    return shear_building(masses, stiffs)


def frecuencias_shear_uniforme(n: int, m: float, k: float) -> np.ndarray:
    """
    Frecuencias naturales exactas de edificio de corte uniforme.

    Fórmula cerrada: ωⱼ² = (2k/m)(1 - cos(jπ/(n+1)))

    Parámetros
    ----------
    n : int
        Número de plantas
    m : float
        Masa por planta [kg]
    k : float
        Rigidez por entreplanta [N/m]

    Retorna
    -------
    omega : np.ndarray
        Frecuencias naturales [rad/s]
    """
    j = np.arange(1, n + 1)
    omega2 = (2 * k / m) * (1 - np.cos(j * np.pi / (n + 1)))
    return np.sqrt(omega2)


def modos_shear_uniforme(n: int) -> np.ndarray:
    """
    Modos de vibración exactos de edificio de corte uniforme.

    Fórmula: φⱼₖ = sin(jkπ/(n+1))

    Parámetros
    ----------
    n : int
        Número de plantas

    Retorna
    -------
    phi : np.ndarray
        Matriz de modos (n × n), columnas son modos
    """
    phi = np.zeros((n, n))
    for j in range(1, n + 1):
        for i in range(1, n + 1):
            phi[i - 1, j - 1] = np.sin(j * i * np.pi / (n + 1))

    # Normalizar cada columna
    for j in range(n):
        phi[:, j] /= np.linalg.norm(phi[:, j])

    return phi


def condensacion_guyan(M: np.ndarray, K: np.ndarray,
                       dof_maestros: List[int]) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Condensación estática de Guyan.

    Parámetros
    ----------
    M : np.ndarray
        Matriz de masa original
    K : np.ndarray
        Matriz de rigidez original
    dof_maestros : List[int]
        Índices de los DOF maestros (retenidos)

    Retorna
    -------
    M_red : np.ndarray
        Matriz de masa reducida
    K_red : np.ndarray
        Matriz de rigidez reducida
    T : np.ndarray
        Matriz de transformación
    """
    n = M.shape[0]
    dof_esclavos = [i for i in range(n) if i not in dof_maestros]

    n_m = len(dof_maestros)
    n_s = len(dof_esclavos)

    # Reordenar: primero maestros, luego esclavos
    orden = dof_maestros + dof_esclavos
    K_reord = K[np.ix_(orden, orden)]
    M_reord = M[np.ix_(orden, orden)]

    # Particionar
    K_mm = K_reord[:n_m, :n_m]
    K_ms = K_reord[:n_m, n_m:]
    K_sm = K_reord[n_m:, :n_m]
    K_ss = K_reord[n_m:, n_m:]

    M_mm = M_reord[:n_m, :n_m]
    M_ms = M_reord[:n_m, n_m:]
    M_sm = M_reord[n_m:, :n_m]
    M_ss = M_reord[n_m:, n_m:]

    # Matriz de transformación de Guyan
    T_sm = -np.linalg.solve(K_ss, K_sm)
    T = np.vstack([np.eye(n_m), T_sm])

    # Matrices reducidas
    K_red = T.T @ K_reord @ T
    M_red = T.T @ M_reord @ T

    return M_red, K_red, T


def amortiguamiento_rayleigh(M: np.ndarray, K: np.ndarray,
                              omega1: float, omega2: float,
                              zeta1: float, zeta2: float) -> np.ndarray:
    """
    Matriz de amortiguamiento de Rayleigh: C = α·M + β·K

    Los coeficientes α y β se calculan para dar amortiguamientos
    ζ₁ y ζ₂ en las frecuencias ω₁ y ω₂.

    Parámetros
    ----------
    M : np.ndarray
        Matriz de masa
    K : np.ndarray
        Matriz de rigidez
    omega1, omega2 : float
        Frecuencias de referencia [rad/s]
    zeta1, zeta2 : float
        Amortiguamientos en ω₁ y ω₂

    Retorna
    -------
    C : np.ndarray
        Matriz de amortiguamiento
    """
    # Sistema: [1/(2ω₁)  ω₁/2] [α]   [ζ₁]
    #          [1/(2ω₂)  ω₂/2] [β] = [ζ₂]
    A = np.array([[1 / (2 * omega1), omega1 / 2],
                  [1 / (2 * omega2), omega2 / 2]])
    b = np.array([zeta1, zeta2])

    coefs = np.linalg.solve(A, b)
    alpha, beta = coefs

    C = alpha * M + beta * K

    return C


# =============================================================================
# COMBINACIÓN MODAL (SRSS, CQC)
# =============================================================================

def combinacion_srss(respuestas_modales: np.ndarray) -> float:
    """
    Combinación modal SRSS (Square Root of Sum of Squares).

    Método de combinación modal que asume modos estadísticamente
    independientes. Válido cuando las frecuencias están bien separadas
    (ωⱼ/ωᵢ < 0.8 o > 1.25 aproximadamente).

    Parámetros
    ----------
    respuestas_modales : np.ndarray
        Vector de respuestas máximas modales (una por modo)

    Retorna
    -------
    R_total : float
        Respuesta total combinada

    Ejemplo
    -------
    >>> R_modal = np.array([100, 30, 10])  # Cortantes modales [kN]
    >>> R_total = combinacion_srss(R_modal)
    >>> print(f"Cortante total: {R_total:.1f} kN")
    Cortante total: 104.9 kN
    """
    return np.sqrt(np.sum(np.array(respuestas_modales)**2))


def coeficiente_cqc(omega_i: float, omega_j: float,
                    zeta_i: float, zeta_j: float) -> float:
    """
    Coeficiente de correlación modal para CQC (Der Kiureghian, 1981).

    Mide la correlación estadística entre dos modos. Vale 1.0 cuando
    las frecuencias son iguales y tiende a 0 cuando están muy separadas.

    Parámetros
    ----------
    omega_i : float
        Frecuencia del modo i [rad/s]
    omega_j : float
        Frecuencia del modo j [rad/s]
    zeta_i : float
        Amortiguamiento del modo i [-]
    zeta_j : float
        Amortiguamiento del modo j [-]

    Retorna
    -------
    rho_ij : float
        Coeficiente de correlación (0 ≤ ρ ≤ 1)

    Notas
    -----
    Fórmula de Der Kiureghian (1981):

    ρᵢⱼ = 8·√(ζᵢ·ζⱼ)·(ζᵢ+r·ζⱼ)·r^(3/2) / [(1-r²)² + 4·ζᵢ·ζⱼ·r·(1+r²) + 4·(ζᵢ²+ζⱼ²)·r²]

    donde r = ωⱼ/ωᵢ
    """
    if omega_i == 0:
        return 0.0

    r = omega_j / omega_i

    numerador = 8 * np.sqrt(zeta_i * zeta_j) * (zeta_i + r * zeta_j) * r**(3/2)

    denominador = ((1 - r**2)**2 +
                   4 * zeta_i * zeta_j * r * (1 + r**2) +
                   4 * (zeta_i**2 + zeta_j**2) * r**2)

    if denominador == 0:
        return 1.0

    return numerador / denominador


def matriz_correlacion_cqc(omega: np.ndarray, zeta: Union[float, np.ndarray]) -> np.ndarray:
    """
    Calcula la matriz completa de coeficientes de correlación CQC.

    Parámetros
    ----------
    omega : np.ndarray
        Vector de frecuencias naturales [rad/s]
    zeta : float o np.ndarray
        Amortiguamiento modal (escalar si es igual para todos, o vector)

    Retorna
    -------
    rho : np.ndarray
        Matriz de correlación (n × n)

    Ejemplo
    -------
    >>> omega = np.array([10, 15, 25])  # rad/s
    >>> zeta = 0.05
    >>> rho = matriz_correlacion_cqc(omega, zeta)
    >>> print(rho)
    """
    n = len(omega)

    # Convertir zeta a vector si es escalar
    if np.isscalar(zeta):
        zeta = np.full(n, zeta)

    rho = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            rho[i, j] = coeficiente_cqc(omega[i], omega[j], zeta[i], zeta[j])

    return rho


def combinacion_cqc(respuestas_modales: np.ndarray,
                    omega: np.ndarray,
                    zeta: Union[float, np.ndarray] = 0.05) -> float:
    """
    Combinación modal CQC (Complete Quadratic Combination).

    Método de combinación modal que considera la correlación entre modos
    con frecuencias cercanas. Más preciso que SRSS para estructuras con
    modos acoplados o frecuencias próximas.

    Parámetros
    ----------
    respuestas_modales : np.ndarray
        Vector de respuestas máximas modales (una por modo)
    omega : np.ndarray
        Vector de frecuencias naturales [rad/s]
    zeta : float o np.ndarray
        Amortiguamiento modal [-] (por defecto 5%)

    Retorna
    -------
    R_total : float
        Respuesta total combinada

    Ejemplo
    -------
    >>> R_modal = np.array([100, 80, 30])  # Cortantes modales [kN]
    >>> omega = np.array([10, 12, 25])     # Frecuencias cercanas
    >>> R_total = combinacion_cqc(R_modal, omega, zeta=0.05)
    >>> print(f"Cortante CQC: {R_total:.1f} kN")

    Notas
    -----
    Fórmula CQC:
    R = √(Σᵢ Σⱼ ρᵢⱼ · Rᵢ · Rⱼ)

    donde ρᵢⱼ es el coeficiente de correlación de Der Kiureghian.

    Referencias
    -----------
    - Der Kiureghian, A. (1981). "A response spectrum method for random vibration
      analysis of MDOF systems." Earthquake Engineering & Structural Dynamics.
    - EC8 (Eurocódigo 8): Recomienda CQC para combinación modal sísmica.
    """
    R = np.array(respuestas_modales)
    n = len(R)

    # Calcular matriz de correlación
    rho = matriz_correlacion_cqc(omega, zeta)

    # Combinación cuadrática completa: R = sqrt(Σᵢ Σⱼ ρᵢⱼ·Rᵢ·Rⱼ)
    suma = 0.0
    for i in range(n):
        for j in range(n):
            suma += rho[i, j] * R[i] * R[j]

    return np.sqrt(suma)


def comparar_srss_cqc(respuestas_modales: np.ndarray,
                      omega: np.ndarray,
                      zeta: Union[float, np.ndarray] = 0.05) -> dict:
    """
    Compara los resultados de combinación SRSS y CQC.

    Parámetros
    ----------
    respuestas_modales : np.ndarray
        Vector de respuestas máximas modales
    omega : np.ndarray
        Vector de frecuencias naturales [rad/s]
    zeta : float o np.ndarray
        Amortiguamiento modal [-]

    Retorna
    -------
    resultados : dict
        Diccionario con:
        - 'SRSS': resultado SRSS
        - 'CQC': resultado CQC
        - 'diferencia_pct': diferencia porcentual (CQC-SRSS)/SRSS * 100
        - 'rho_max': máximo coeficiente de correlación fuera de diagonal
        - 'recomendacion': 'SRSS' o 'CQC' según separación de frecuencias
    """
    R_srss = combinacion_srss(respuestas_modales)
    R_cqc = combinacion_cqc(respuestas_modales, omega, zeta)

    # Matriz de correlación
    rho = matriz_correlacion_cqc(omega, zeta)
    n = len(omega)

    # Máximo coeficiente fuera de diagonal
    rho_off_diag = np.abs(rho - np.eye(n))
    rho_max = np.max(rho_off_diag)

    # Ratios de frecuencia mínimo
    ratios = []
    for i in range(n):
        for j in range(i+1, n):
            if omega[i] > 0:
                ratios.append(omega[j] / omega[i])

    ratio_min = min(ratios) if ratios else 1.0

    # Recomendación basada en separación de frecuencias
    if ratio_min < 1.25 or rho_max > 0.1:
        recomendacion = "CQC (frecuencias cercanas, ρ_max={:.2f})".format(rho_max)
    else:
        recomendacion = "SRSS (frecuencias bien separadas)"

    return {
        'SRSS': R_srss,
        'CQC': R_cqc,
        'diferencia_pct': (R_cqc - R_srss) / R_srss * 100 if R_srss > 0 else 0,
        'rho_max': rho_max,
        'ratio_freq_min': ratio_min,
        'recomendacion': recomendacion
    }


def newmark_mdof(M: np.ndarray, C: np.ndarray, K: np.ndarray,
                  F: np.ndarray, dt: float,
                  u0: Optional[np.ndarray] = None,
                  v0: Optional[np.ndarray] = None,
                  gamma: float = 0.5, beta: float = 0.25) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Integración temporal por método de Newmark para sistemas MDOF.

    Parámetros
    ----------
    M : np.ndarray
        Matriz de masa (n × n)
    C : np.ndarray
        Matriz de amortiguamiento (n × n)
    K : np.ndarray
        Matriz de rigidez (n × n)
    F : np.ndarray
        Historia de fuerzas (n × nt)
    dt : float
        Paso de tiempo [s]
    u0 : np.ndarray, opcional
        Desplazamientos iniciales
    v0 : np.ndarray, opcional
        Velocidades iniciales
    gamma, beta : float
        Parámetros de Newmark

    Retorna
    -------
    u : np.ndarray
        Desplazamientos (n × nt)
    v : np.ndarray
        Velocidades (n × nt)
    a : np.ndarray
        Aceleraciones (n × nt)
    """
    n = M.shape[0]
    nt = F.shape[1]

    # Inicializar
    u = np.zeros((n, nt))
    v = np.zeros((n, nt))
    a = np.zeros((n, nt))

    if u0 is not None:
        u[:, 0] = u0
    if v0 is not None:
        v[:, 0] = v0

    # Aceleración inicial
    a[:, 0] = np.linalg.solve(M, F[:, 0] - C @ v[:, 0] - K @ u[:, 0])

    # Constantes de Newmark
    a0 = 1 / (beta * dt**2)
    a1 = gamma / (beta * dt)
    a2 = 1 / (beta * dt)
    a3 = 1 / (2 * beta) - 1
    a4 = gamma / beta - 1
    a5 = dt * (gamma / (2 * beta) - 1)

    # Matriz efectiva
    K_eff = K + a0 * M + a1 * C

    # Factorización LU para eficiencia
    lu, piv = linalg.lu_factor(K_eff)

    # Integración paso a paso
    for i in range(nt - 1):
        # Fuerza efectiva
        F_eff = F[:, i + 1] + \
                M @ (a0 * u[:, i] + a2 * v[:, i] + a3 * a[:, i]) + \
                C @ (a1 * u[:, i] + a4 * v[:, i] + a5 * a[:, i])

        # Resolver
        u[:, i + 1] = linalg.lu_solve((lu, piv), F_eff)

        # Actualizar velocidad y aceleración
        a[:, i + 1] = a0 * (u[:, i + 1] - u[:, i]) - a2 * v[:, i] - a3 * a[:, i]
        v[:, i + 1] = v[:, i] + dt * ((1 - gamma) * a[:, i] + gamma * a[:, i + 1])

    return u, v, a
