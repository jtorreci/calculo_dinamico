# -*- coding: utf-8 -*-
"""
Módulo de Utilidades
====================

Funciones auxiliares para gráficas y procesamiento.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Optional, Tuple


def configurar_graficas(estilo: str = 'libro', idioma: str = 'es'):
    """
    Configura el estilo de las gráficas para el libro.

    Parámetros
    ----------
    estilo : str
        'libro' para estilo de publicación, 'presentacion' para diapositivas
    idioma : str
        'es' para español, 'en' para inglés
    """
    plt.rcParams.update({
        # Fuentes
        'font.family': 'serif',
        'font.size': 10 if estilo == 'libro' else 14,
        'axes.titlesize': 11 if estilo == 'libro' else 16,
        'axes.labelsize': 10 if estilo == 'libro' else 14,
        'xtick.labelsize': 9 if estilo == 'libro' else 12,
        'ytick.labelsize': 9 if estilo == 'libro' else 12,
        'legend.fontsize': 9 if estilo == 'libro' else 12,

        # Líneas
        'lines.linewidth': 1.5,
        'lines.markersize': 6,

        # Ejes
        'axes.linewidth': 0.8,
        'axes.grid': True,
        'grid.alpha': 0.3,
        'grid.linestyle': '-',

        # Figura
        'figure.figsize': (6, 4) if estilo == 'libro' else (10, 6),
        'figure.dpi': 150,
        'savefig.dpi': 300,
        'savefig.bbox': 'tight',

        # Leyenda
        'legend.framealpha': 0.9,
        'legend.edgecolor': 'gray',

        # LaTeX
        'text.usetex': False,  # Cambiar a True si LaTeX está disponible
        'mathtext.fontset': 'cm',
    })

    # Configurar locale para números
    if idioma == 'es':
        import locale
        try:
            locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
        except:
            pass


def crear_figura_doble(titulo1: str = '', titulo2: str = '',
                       figsize: Tuple[float, float] = (12, 5)) -> Tuple[plt.Figure, Tuple]:
    """
    Crea una figura con dos subplots lado a lado.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
    if titulo1:
        ax1.set_title(titulo1, fontweight='bold')
    if titulo2:
        ax2.set_title(titulo2, fontweight='bold')
    return fig, (ax1, ax2)


def crear_figura_bode(figsize: Tuple[float, float] = (8, 8)) -> Tuple[plt.Figure, Tuple]:
    """
    Crea una figura para diagrama de Bode (magnitud + fase).
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize, sharex=True)
    ax1.set_ylabel('Magnitud [dB]')
    ax2.set_ylabel('Fase [°]')
    ax2.set_xlabel('Frecuencia [rad/s]')
    ax1.set_title('Diagrama de Bode', fontweight='bold')
    return fig, (ax1, ax2)


def formatear_eje_frecuencia(ax, escala: str = 'log', unidad: str = 'rad/s'):
    """
    Formatea el eje de frecuencia.
    """
    if escala == 'log':
        ax.set_xscale('log')

    if unidad == 'rad/s':
        ax.set_xlabel('Frecuencia $\\omega$ [rad/s]')
    elif unidad == 'Hz':
        ax.set_xlabel('Frecuencia $f$ [Hz]')


def etiqueta_resonancia(ax, omega_n: float, y_pos: float,
                        texto: str = '$\\omega_n$'):
    """
    Añade una línea vertical y etiqueta en la frecuencia natural.
    """
    ax.axvline(omega_n, color='red', linestyle='--', alpha=0.5)
    ax.annotate(texto, xy=(omega_n, y_pos), fontsize=9,
                ha='center', va='bottom')


def pulso_rectangular(t: np.ndarray, F0: float, t_d: float) -> np.ndarray:
    """
    Genera un pulso rectangular.

    Parámetros
    ----------
    t : np.ndarray
        Vector de tiempos [s]
    F0 : float
        Amplitud del pulso [N]
    t_d : float
        Duración del pulso [s]

    Retorna
    -------
    F : np.ndarray
        Fuerza [N]
    """
    F = np.zeros_like(t)
    F[(t >= 0) & (t <= t_d)] = F0
    return F


def pulso_triangular(t: np.ndarray, F0: float, t_d: float) -> np.ndarray:
    """
    Genera un pulso triangular (sube y baja).

    Parámetros
    ----------
    t : np.ndarray
        Vector de tiempos [s]
    F0 : float
        Amplitud máxima [N]
    t_d : float
        Duración total del pulso [s]

    Retorna
    -------
    F : np.ndarray
        Fuerza [N]
    """
    F = np.zeros_like(t)
    t_pico = t_d / 2

    # Rampa de subida
    mask1 = (t >= 0) & (t <= t_pico)
    F[mask1] = F0 * t[mask1] / t_pico

    # Rampa de bajada
    mask2 = (t > t_pico) & (t <= t_d)
    F[mask2] = F0 * (1 - (t[mask2] - t_pico) / t_pico)

    return F


def pulso_seno_medio(t: np.ndarray, F0: float, t_d: float) -> np.ndarray:
    """
    Genera un pulso de media onda sinusoidal.

    Parámetros
    ----------
    t : np.ndarray
        Vector de tiempos [s]
    F0 : float
        Amplitud máxima [N]
    t_d : float
        Duración del pulso [s]

    Retorna
    -------
    F : np.ndarray
        Fuerza [N]
    """
    F = np.zeros_like(t)
    mask = (t >= 0) & (t <= t_d)
    F[mask] = F0 * np.sin(np.pi * t[mask] / t_d)
    return F


def rampa(t: np.ndarray, F0: float, t_1: float) -> np.ndarray:
    """
    Genera una carga rampa de 0 a F0 en tiempo t_1, luego constante.

    Parámetros
    ----------
    t : np.ndarray
        Vector de tiempos [s]
    F0 : float
        Fuerza final [N]
    t_1 : float
        Tiempo de rampa [s]

    Retorna
    -------
    F : np.ndarray
        Fuerza [N]
    """
    F = np.zeros_like(t)

    # Rampa
    mask1 = (t >= 0) & (t <= t_1)
    F[mask1] = F0 * t[mask1] / t_1

    # Constante
    mask2 = t > t_1
    F[mask2] = F0

    return F


def escalon(t: np.ndarray, F0: float, t_0: float = 0.0) -> np.ndarray:
    """
    Genera una carga escalón.

    Parámetros
    ----------
    t : np.ndarray
        Vector de tiempos [s]
    F0 : float
        Amplitud del escalón [N]
    t_0 : float
        Tiempo de inicio [s]

    Retorna
    -------
    F : np.ndarray
        Fuerza [N]
    """
    F = np.zeros_like(t)
    F[t >= t_0] = F0
    return F


def impulso(t: np.ndarray, I: float, t_0: float = 0.0,
            dt: Optional[float] = None) -> np.ndarray:
    """
    Genera un impulso como pulso muy corto.

    Parámetros
    ----------
    t : np.ndarray
        Vector de tiempos [s]
    I : float
        Impulso [N·s]
    t_0 : float
        Tiempo del impulso [s]
    dt : float, opcional
        Duración del pulso (si None, usa el paso de tiempo)

    Retorna
    -------
    F : np.ndarray
        Fuerza [N]
    """
    if dt is None:
        dt = t[1] - t[0]

    F = np.zeros_like(t)
    mask = (t >= t_0) & (t < t_0 + dt)
    F[mask] = I / dt

    return F


def decremento_logaritmico(amplitudes: np.ndarray) -> Tuple[float, float]:
    """
    Calcula el decremento logarítmico a partir de amplitudes de picos.

    Parámetros
    ----------
    amplitudes : np.ndarray
        Amplitudes de picos consecutivos

    Retorna
    -------
    delta_promedio : float
        Decremento logarítmico promedio
    zeta : float
        Razón de amortiguamiento estimada
    """
    n = len(amplitudes)
    if n < 2:
        raise ValueError("Se necesitan al menos 2 amplitudes")

    # Decrementos individuales
    deltas = np.log(amplitudes[:-1] / amplitudes[1:])
    delta_promedio = np.mean(deltas)

    # También calcular usando primer y último pico
    delta_total = np.log(amplitudes[0] / amplitudes[-1]) / (n - 1)

    # Razón de amortiguamiento
    zeta = delta_promedio / np.sqrt(4 * np.pi**2 + delta_promedio**2)

    return delta_promedio, zeta


# =============================================================================
# VISUALIZACIÓN DE MODOS DE VIBRACIÓN
# =============================================================================

def graficar_modos_edificio(phi: np.ndarray, alturas: Optional[np.ndarray] = None,
                             frecuencias: Optional[np.ndarray] = None,
                             n_modos: int = 3,
                             titulo: str = "Modos de vibración",
                             figsize: Tuple[float, float] = (10, 6)) -> plt.Figure:
    """
    Grafica los modos de vibración de un edificio (shear building).

    Muestra los modos como perfiles de desplazamiento lateral por planta,
    típico de análisis de edificios sometidos a excitación sísmica.

    Parámetros
    ----------
    phi : np.ndarray
        Matriz de modos (n_plantas × n_modos), columnas son modos
    alturas : np.ndarray, opcional
        Alturas acumuladas de cada planta [m]. Si None, usa índices 1,2,3...
    frecuencias : np.ndarray, opcional
        Frecuencias naturales [Hz] para etiquetar
    n_modos : int
        Número de modos a graficar (por defecto 3)
    titulo : str
        Título del gráfico
    figsize : tuple
        Tamaño de la figura

    Retorna
    -------
    fig : plt.Figure
        Figura de matplotlib

    Ejemplo
    -------
    >>> from libreria_dinamica import MDOF, shear_building_uniforme
    >>> M, K = shear_building_uniforme(5, m=1000, k=200000)
    >>> sistema = MDOF(M, K)
    >>> fig = graficar_modos_edificio(sistema.phi, frecuencias=sistema.f_n)
    """
    n_plantas = phi.shape[0]
    n_modos = min(n_modos, phi.shape[1])

    if alturas is None:
        alturas = np.arange(1, n_plantas + 1)

    # Añadir base (altura 0, desplazamiento 0)
    alturas_plot = np.concatenate([[0], alturas])

    fig, axes = plt.subplots(1, n_modos, figsize=figsize, sharey=True)
    if n_modos == 1:
        axes = [axes]

    colores = plt.cm.tab10(np.linspace(0, 1, n_modos))

    for i, ax in enumerate(axes):
        # Modo normalizado (máximo = 1)
        modo = phi[:, i] / np.max(np.abs(phi[:, i]))
        modo_plot = np.concatenate([[0], modo])

        # Línea del modo
        ax.plot(modo_plot, alturas_plot, 'o-', color=colores[i],
                linewidth=2, markersize=8, label=f'Modo {i+1}')

        # Línea vertical en x=0 (referencia)
        ax.axvline(0, color='gray', linestyle='--', linewidth=0.5)

        # Etiquetas
        if frecuencias is not None:
            ax.set_title(f'Modo {i+1}\n$f_{{{i+1}}}$ = {frecuencias[i]:.2f} Hz',
                        fontweight='bold')
        else:
            ax.set_title(f'Modo {i+1}', fontweight='bold')

        ax.set_xlabel('Desplazamiento normalizado')
        ax.set_xlim(-1.3, 1.3)
        ax.grid(True, alpha=0.3)

        # Líneas horizontales para plantas
        for h in alturas_plot:
            ax.axhline(h, color='lightgray', linewidth=0.5)

    axes[0].set_ylabel('Altura [m]' if alturas is not None else 'Planta')
    fig.suptitle(titulo, fontsize=12, fontweight='bold')
    plt.tight_layout()

    return fig


def graficar_respuesta_modal(t: np.ndarray, x: np.ndarray,
                              etiquetas: Optional[list] = None,
                              titulo: str = "Respuesta temporal",
                              ylabel: str = "Desplazamiento [m]",
                              figsize: Tuple[float, float] = (10, 6)) -> plt.Figure:
    """
    Grafica la respuesta temporal de múltiples DOF.

    Parámetros
    ----------
    t : np.ndarray
        Vector de tiempos [s]
    x : np.ndarray
        Matriz de respuestas (n_dof × n_tiempos)
    etiquetas : list, opcional
        Lista de etiquetas para cada DOF
    titulo : str
        Título del gráfico
    ylabel : str
        Etiqueta del eje Y
    figsize : tuple
        Tamaño de la figura

    Retorna
    -------
    fig : plt.Figure
        Figura de matplotlib
    """
    n_dof = x.shape[0]

    if etiquetas is None:
        etiquetas = [f'DOF {i+1}' for i in range(n_dof)]

    fig, ax = plt.subplots(figsize=figsize)

    colores = plt.cm.viridis(np.linspace(0.2, 0.8, n_dof))

    for i in range(n_dof):
        ax.plot(t, x[i, :], color=colores[i], linewidth=1.5,
                label=etiquetas[i])

    ax.set_xlabel('Tiempo [s]')
    ax.set_ylabel(ylabel)
    ax.set_title(titulo, fontweight='bold')
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def graficar_frf_mdof(omega: np.ndarray, H: np.ndarray,
                       omega_n: Optional[np.ndarray] = None,
                       titulo: str = "Función de Respuesta en Frecuencia",
                       figsize: Tuple[float, float] = (10, 8)) -> plt.Figure:
    """
    Grafica el diagrama de Bode de una FRF (magnitud y fase).

    Parámetros
    ----------
    omega : np.ndarray
        Vector de frecuencias [rad/s]
    H : np.ndarray
        FRF compleja
    omega_n : np.ndarray, opcional
        Frecuencias naturales para marcar resonancias
    titulo : str
        Título del gráfico
    figsize : tuple
        Tamaño de la figura

    Retorna
    -------
    fig : plt.Figure
        Figura de matplotlib
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize, sharex=True)

    # Magnitud en dB
    mag_dB = 20 * np.log10(np.abs(H))
    ax1.semilogx(omega, mag_dB, 'b-', linewidth=1.5)
    ax1.set_ylabel('Magnitud [dB]')
    ax1.set_title(titulo, fontweight='bold')
    ax1.grid(True, alpha=0.3, which='both')

    # Fase en grados
    fase_deg = np.angle(H, deg=True)
    ax2.semilogx(omega, fase_deg, 'r-', linewidth=1.5)
    ax2.set_ylabel('Fase [°]')
    ax2.set_xlabel('Frecuencia ω [rad/s]')
    ax2.grid(True, alpha=0.3, which='both')

    # Marcar frecuencias naturales
    if omega_n is not None:
        for i, wn in enumerate(omega_n):
            for ax in [ax1, ax2]:
                ax.axvline(wn, color='green', linestyle='--', alpha=0.5)
            ax1.annotate(f'$\\omega_{{{i+1}}}$', xy=(wn, ax1.get_ylim()[1]),
                        fontsize=9, ha='center', va='bottom', color='green')

    plt.tight_layout()
    return fig


def graficar_matriz_correlacion(rho: np.ndarray,
                                 titulo: str = "Matriz de correlación CQC",
                                 figsize: Tuple[float, float] = (8, 6)) -> plt.Figure:
    """
    Grafica la matriz de correlación CQC como mapa de calor.

    Parámetros
    ----------
    rho : np.ndarray
        Matriz de correlación (n × n)
    titulo : str
        Título del gráfico
    figsize : tuple
        Tamaño de la figura

    Retorna
    -------
    fig : plt.Figure
        Figura de matplotlib
    """
    fig, ax = plt.subplots(figsize=figsize)

    n = rho.shape[0]
    im = ax.imshow(rho, cmap='RdYlGn_r', vmin=0, vmax=1)

    # Colorbar
    cbar = fig.colorbar(im, ax=ax, shrink=0.8)
    cbar.set_label('Coeficiente ρᵢⱼ')

    # Etiquetas
    ax.set_xticks(np.arange(n))
    ax.set_yticks(np.arange(n))
    ax.set_xticklabels([f'Modo {i+1}' for i in range(n)])
    ax.set_yticklabels([f'Modo {i+1}' for i in range(n)])

    # Valores en celdas
    for i in range(n):
        for j in range(n):
            color = 'white' if rho[i, j] > 0.5 else 'black'
            ax.text(j, i, f'{rho[i, j]:.2f}', ha='center', va='center',
                   color=color, fontsize=9)

    ax.set_title(titulo, fontweight='bold')
    plt.tight_layout()

    return fig


def graficar_espectro_respuesta(T: np.ndarray, Sa: np.ndarray,
                                  zeta_values: Optional[list] = None,
                                  titulo: str = "Espectro de respuesta",
                                  figsize: Tuple[float, float] = (10, 6)) -> plt.Figure:
    """
    Grafica espectros de respuesta para diferentes amortiguamientos.

    Parámetros
    ----------
    T : np.ndarray
        Vector de períodos [s]
    Sa : np.ndarray
        Aceleraciones espectrales [g o m/s²]. Si es 2D, cada fila
        corresponde a un valor de amortiguamiento
    zeta_values : list, opcional
        Lista de valores de amortiguamiento para la leyenda
    titulo : str
        Título del gráfico
    figsize : tuple
        Tamaño de la figura

    Retorna
    -------
    fig : plt.Figure
        Figura de matplotlib
    """
    fig, ax = plt.subplots(figsize=figsize)

    Sa = np.atleast_2d(Sa)
    n_curvas = Sa.shape[0]

    if zeta_values is None:
        zeta_values = [f'Curva {i+1}' for i in range(n_curvas)]

    colores = plt.cm.plasma(np.linspace(0.2, 0.8, n_curvas))

    for i in range(n_curvas):
        if isinstance(zeta_values[i], (int, float)):
            label = f'ζ = {zeta_values[i]*100:.0f}%'
        else:
            label = str(zeta_values[i])
        ax.plot(T, Sa[i, :], color=colores[i], linewidth=1.5, label=label)

    ax.set_xlabel('Período T [s]')
    ax.set_ylabel('Aceleración espectral $S_a$')
    ax.set_title(titulo, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)
    plt.tight_layout()

    return fig


def encontrar_picos(signal: np.ndarray, t: np.ndarray,
                    minimo: Optional[float] = None) -> Tuple[np.ndarray, np.ndarray]:
    """
    Encuentra los picos de una señal.

    Parámetros
    ----------
    signal : np.ndarray
        Señal
    t : np.ndarray
        Vector de tiempos
    minimo : float, opcional
        Amplitud mínima para considerar un pico

    Retorna
    -------
    t_picos : np.ndarray
        Tiempos de los picos
    amplitudes : np.ndarray
        Amplitudes de los picos
    """
    from scipy.signal import find_peaks

    # Encontrar picos positivos
    indices, _ = find_peaks(signal, height=minimo)

    return t[indices], signal[indices]


def guardar_figura(fig: plt.Figure, nombre: str, formatos: list = ['pdf', 'png']):
    """
    Guarda una figura en múltiples formatos.

    Parámetros
    ----------
    fig : plt.Figure
        Figura a guardar
    nombre : str
        Nombre base del archivo (sin extensión)
    formatos : list
        Lista de formatos ('pdf', 'png', 'svg', etc.)
    """
    for fmt in formatos:
        fig.savefig(f'{nombre}.{fmt}', dpi=300, bbox_inches='tight')
    print(f"Figura guardada: {nombre}.{formatos[0]}")
