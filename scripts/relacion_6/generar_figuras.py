# -*- coding: utf-8 -*-
"""
Generador de figuras para Relacion 6 - No Lineal y Control
Problemas: 10 (HDRB), 12 (amortiguadores viscosos), 13 (ADAS)
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, Polygon, Circle, FancyArrowPatch
from matplotlib.patches import ConnectionPatch
import os

# Configuracion para figuras de calidad
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['font.family'] = 'serif'
plt.rcParams['text.usetex'] = False
plt.rcParams['mathtext.fontset'] = 'cm'

# Directorio de salida
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'figs')
os.makedirs(OUTPUT_DIR, exist_ok=True)


def fig_problema_10():
    """
    Problema 10: Aislador HDRB - Lazo histeretico
    Muestra el lazo fuerza-desplazamiento del elastomero de alto amortiguamiento
    """
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle('Problema 10: Aislador elastomerico HDRB', fontsize=14, fontweight='bold')

    # Izquierda: Esquema del aislador
    ax1 = axes[0]
    ax1.set_xlim(-1, 5)
    ax1.set_ylim(-1, 6)
    ax1.set_aspect('equal')

    # Placa superior
    rect_sup = Rectangle((0.5, 4.5), 3, 0.3, facecolor='steelblue', edgecolor='black', linewidth=1.5)
    ax1.add_patch(rect_sup)
    ax1.text(2, 5.1, 'Placa superior (acero)', ha='center', fontsize=9)

    # Capas de goma y acero alternadas
    n_capas = 8
    h_goma = 0.3
    h_acero = 0.1
    y_base = 1.0

    for i in range(n_capas):
        y = y_base + i * (h_goma + h_acero)
        # Capa de goma
        rect_goma = Rectangle((0.7, y), 2.6, h_goma,
                               facecolor='darkred', edgecolor='black', linewidth=0.5, alpha=0.8)
        ax1.add_patch(rect_goma)
        # Capa de acero (shim)
        if i < n_capas - 1:
            rect_acero = Rectangle((0.7, y + h_goma), 2.6, h_acero,
                                   facecolor='silver', edgecolor='black', linewidth=0.5)
            ax1.add_patch(rect_acero)

    # Placa inferior
    rect_inf = Rectangle((0.5, 0.5), 3, 0.3, facecolor='steelblue', edgecolor='black', linewidth=1.5)
    ax1.add_patch(rect_inf)
    ax1.text(2, 0.1, 'Placa inferior (acero)', ha='center', fontsize=9)

    # Leyenda
    ax1.plot([], [], 's', color='darkred', markersize=10, label='Elastomero (HDRB)')
    ax1.plot([], [], 's', color='silver', markersize=10, label='Chapas de acero')
    ax1.legend(loc='upper right', fontsize=8)

    # Dimensiones
    ax1.annotate('', xy=(4, 0.8), xytext=(4, 4.5),
                arrowprops=dict(arrowstyle='<->', color='black', lw=1.5))
    ax1.text(4.3, 2.5, '$t_r = 400$ mm', fontsize=9, rotation=90, va='center')

    ax1.annotate('', xy=(0.5, -0.3), xytext=(3.5, -0.3),
                arrowprops=dict(arrowstyle='<->', color='black', lw=1.5))
    ax1.text(2, -0.6, '$D = 700$ mm', fontsize=9, ha='center')

    ax1.set_title('Seccion del aislador HDRB', fontsize=11)
    ax1.axis('off')

    # Derecha: Lazo histeretico
    ax2 = axes[1]

    # Parametros del lazo (HDRB con amortiguamiento 15%)
    kH = 790  # kN/m
    Dd = 250  # mm
    zeta = 0.15

    # Lazo histeretico simplificado (eliptico para HDRB)
    t = np.linspace(0, 2*np.pi, 200)
    u = Dd * np.sin(t)  # Desplazamiento
    F_elastico = kH * u / 1000  # Fuerza elastica (kN)

    # Componente amortiguada (desfase de 90 grados)
    F_amort = 2 * zeta * kH * Dd / 1000 * np.cos(t)
    F_total = F_elastico + F_amort

    ax2.fill(u, F_total, alpha=0.3, color='blue', label='Area = energia disipada')
    ax2.plot(u, F_total, 'b-', linewidth=2)

    # Rigidez efectiva
    ax2.plot([-Dd, Dd], [-kH*Dd/1000, kH*Dd/1000], 'r--', linewidth=1.5,
             label=f'$k_{{eff}} = {kH}$ kN/m')

    ax2.axhline(y=0, color='gray', linestyle='-', linewidth=0.5)
    ax2.axvline(x=0, color='gray', linestyle='-', linewidth=0.5)

    ax2.set_xlabel('Desplazamiento (mm)')
    ax2.set_ylabel('Fuerza (kN)')
    ax2.set_title('Lazo histeretico del HDRB', fontsize=11)
    ax2.grid(True, alpha=0.3)
    ax2.legend(loc='upper left', fontsize=9)

    # Anotaciones
    ax2.annotate(f'$D_d = {Dd}$ mm', xy=(Dd, 0), xytext=(Dd+30, 50),
                arrowprops=dict(arrowstyle='->', color='black'),
                fontsize=9)
    ax2.annotate(r'$\zeta_{eff} = 15\%$', xy=(0, 150), fontsize=10,
                ha='center', fontweight='bold')

    plt.tight_layout()

    filepath = os.path.join(OUTPUT_DIR, 'fig_problema_10_HDRB.pdf')
    plt.savefig(filepath, bbox_inches='tight')
    plt.close()
    print(f"[OK] Generada: fig_problema_10_HDRB.pdf")


def fig_problema_12():
    """
    Problema 12: Amortiguadores viscosos en configuracion diagonal
    """
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle('Problema 12: Amortiguadores viscosos en configuracion diagonal',
                 fontsize=14, fontweight='bold')

    # Izquierda: Esquema estructural
    ax1 = axes[0]
    ax1.set_xlim(-0.5, 8)
    ax1.set_ylim(-0.5, 5)
    ax1.set_aspect('equal')

    # Portico de 2 vanos y 2 plantas
    # Columnas
    for x in [0, 3.5, 7]:
        ax1.plot([x, x], [0, 4], 'b-', linewidth=4)

    # Vigas
    for y in [2, 4]:
        ax1.plot([0, 7], [y, y], 'b-', linewidth=4)

    # Base
    ax1.fill_between([-0.3, 7.3], [-0.3, -0.3], [0, 0], color='gray', alpha=0.5, hatch='///')
    ax1.plot([-0.3, 7.3], [0, 0], 'k-', linewidth=2)

    # Amortiguadores diagonales (configuracion chevron/K)
    def dibujar_amortiguador(ax, x1, y1, x2, y2, color='red'):
        # Linea diagonal
        ax.plot([x1, x2], [y1, y2], color=color, linewidth=3, solid_capstyle='round')
        # Simbolo de amortiguador en el centro
        xc, yc = (x1+x2)/2, (y1+y2)/2
        ax.plot(xc, yc, 's', color=color, markersize=12)

    # Planta 1 - vano izquierdo
    dibujar_amortiguador(ax1, 0.2, 0.1, 1.5, 2)
    dibujar_amortiguador(ax1, 3.3, 0.1, 2.0, 2)

    # Planta 2 - vano derecho
    dibujar_amortiguador(ax1, 3.7, 2.1, 5.0, 4)
    dibujar_amortiguador(ax1, 6.8, 2.1, 5.5, 4)

    # Angulo
    ax1.annotate(r'$\theta = 45°$', xy=(1.0, 0.8), fontsize=10,
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    # Leyenda
    ax1.plot([], [], 's-', color='red', markersize=10, linewidth=3, label='Amortiguador viscoso')
    ax1.plot([], [], '-', color='blue', linewidth=4, label='Estructura')
    ax1.legend(loc='upper right', fontsize=9)

    ax1.set_title('Configuracion en K (chevron bracing)', fontsize=11)
    ax1.axis('off')

    # Derecha: Respuesta fuerza-velocidad
    ax2 = axes[1]

    # Parametros
    c = 378  # kN.s/m
    v_max = 0.585  # m/s

    v = np.linspace(-v_max, v_max, 200)
    F = c * v  # Amortiguador lineal

    ax2.plot(v*1000, F, 'b-', linewidth=2.5, label=f'Lineal: $F = c \\cdot v$')

    # Amortiguador no lineal (alpha = 0.5)
    alpha = 0.5
    F_nl = c * np.sign(v) * np.abs(v)**alpha
    ax2.plot(v*1000, F_nl, 'r--', linewidth=2, label=r'No lineal: $F = c \cdot v^{0.5}$')

    ax2.axhline(y=0, color='gray', linestyle='-', linewidth=0.5)
    ax2.axvline(x=0, color='gray', linestyle='-', linewidth=0.5)

    ax2.set_xlabel('Velocidad (mm/s)')
    ax2.set_ylabel('Fuerza (kN)')
    ax2.set_title('Ley constitutiva del amortiguador', fontsize=11)
    ax2.grid(True, alpha=0.3)
    ax2.legend(loc='upper left', fontsize=9)

    # Anotaciones
    ax2.annotate(f'$c = {c}$ kN$\\cdot$s/m', xy=(200, 150), fontsize=10,
                bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
    ax2.annotate(f'$F_{{max}} = {c*v_max:.0f}$ kN', xy=(v_max*1000, c*v_max),
                xytext=(v_max*1000-150, c*v_max+30),
                arrowprops=dict(arrowstyle='->', color='black'),
                fontsize=9)

    plt.tight_layout()

    filepath = os.path.join(OUTPUT_DIR, 'fig_problema_12_amortiguadores_viscosos.pdf')
    plt.savefig(filepath, bbox_inches='tight')
    plt.close()
    print(f"[OK] Generada: fig_problema_12_amortiguadores_viscosos.pdf")


def fig_problema_13():
    """
    Problema 13: Disipador ADAS - Geometria y lazo histeretico
    """
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle('Problema 13: Disipador histeretico ADAS (Added Damping And Stiffness)',
                 fontsize=14, fontweight='bold')

    # Izquierda: Geometria de las placas en X
    ax1 = axes[0]
    ax1.set_xlim(-1, 7)
    ax1.set_ylim(-1, 5)
    ax1.set_aspect('equal')

    # Dibujar 4 placas ADAS en forma de X
    def dibujar_placa_X(ax, x_center, y_base, h=2.0, b_max=0.5, b_min=0.15, color='steelblue'):
        """Placa con forma de X (ancho variable)"""
        # Puntos del perfil
        y = np.array([y_base, y_base + h/4, y_base + h/2, y_base + 3*h/4, y_base + h])
        b_half = np.array([b_max/2, b_min/2, b_max/2, b_min/2, b_max/2])

        # Crear poligono
        x_left = x_center - b_half
        x_right = x_center + b_half
        vertices = np.vstack([
            np.column_stack([x_left, y]),
            np.column_stack([x_right[::-1], y[::-1]])
        ])
        placa = Polygon(vertices, closed=True, facecolor=color, edgecolor='black', linewidth=1)
        ax.add_patch(placa)

    # Placas superiores e inferiores (conexion)
    rect_sup = Rectangle((0.5, 3.5), 5, 0.4, facecolor='gray', edgecolor='black', linewidth=1.5)
    rect_inf = Rectangle((0.5, 0), 5, 0.4, facecolor='gray', edgecolor='black', linewidth=1.5)
    ax1.add_patch(rect_sup)
    ax1.add_patch(rect_inf)

    # 6 placas ADAS
    for i in range(6):
        x_c = 1.0 + i * 0.8
        dibujar_placa_X(ax1, x_c, 0.4, h=3.1, b_max=0.35, b_min=0.12)

    # Dimensiones
    ax1.annotate('', xy=(6, 0.4), xytext=(6, 3.5),
                arrowprops=dict(arrowstyle='<->', color='black', lw=1.5))
    ax1.text(6.3, 2.0, '$h = 200$ mm', fontsize=9, rotation=90, va='center')

    ax1.annotate('', xy=(1.0, -0.5), xytext=(1.35, -0.5),
                arrowprops=dict(arrowstyle='<->', color='black', lw=1.5))
    ax1.text(1.17, -0.8, '$b$', fontsize=9, ha='center')

    # Flechas de movimiento
    ax1.annotate('', xy=(5.8, 4.2), xytext=(4.5, 4.2),
                arrowprops=dict(arrowstyle='->', color='red', lw=2))
    ax1.text(5.2, 4.5, 'Desplazamiento\nrelativo', fontsize=9, ha='center', color='red')

    ax1.set_title('Geometria del disipador ADAS\n(6 placas en X)', fontsize=11)
    ax1.axis('off')

    # Derecha: Lazo histeretico elastoplastico
    ax2 = axes[1]

    # Parametros del problema
    Fy = 282  # kN
    K = 1008  # MN/m = 1008000 kN/m
    delta_y = 0.28  # mm
    delta_max = 30  # mm

    # Lazo elastoplastico idealizado
    # Carga
    d1 = np.array([0, delta_y, delta_max])
    F1 = np.array([0, Fy, Fy])

    # Descarga
    d2 = np.array([delta_max, delta_max - 2*delta_y, -delta_max + 2*delta_y, -delta_max])
    F2 = np.array([Fy, -Fy, -Fy, -Fy])

    # Recarga
    d3 = np.array([-delta_max, -delta_y, 0])
    F3 = np.array([-Fy, -Fy, 0])

    # Ciclo completo
    delta_ciclo = np.concatenate([d1, [delta_max, delta_max-2*delta_y], [-delta_max+2*delta_y, -delta_max],
                                  [-delta_max, -delta_y], [delta_y, delta_max]])
    F_ciclo = np.concatenate([F1, [Fy, -Fy], [-Fy, -Fy],
                             [-Fy, -Fy], [Fy, Fy]])

    # Lazo simplificado
    delta_loop = np.array([0, delta_y, delta_max, delta_max, -delta_max+2*delta_y,
                          -delta_max, -delta_max, delta_max-2*delta_y, delta_max, delta_y, 0])
    F_loop = np.array([0, Fy, Fy, Fy, -Fy,
                      -Fy, -Fy, Fy, Fy, Fy, 0])

    # Lazo mas suave para visualizacion
    delta_vis = np.array([0, delta_y, delta_max, delta_max-2*delta_y, -delta_max,
                         -delta_max+2*delta_y, delta_y])
    F_vis = np.array([0, Fy, Fy, -Fy, -Fy, Fy, Fy])

    ax2.fill([-delta_max, -delta_max, delta_max, delta_max],
             [-Fy, Fy, Fy, -Fy], alpha=0.2, color='blue')
    ax2.plot([-delta_max, delta_max], [-Fy, -Fy], 'b-', linewidth=2)
    ax2.plot([-delta_max, delta_max], [Fy, Fy], 'b-', linewidth=2)
    ax2.plot([-delta_max, -delta_max], [-Fy, Fy], 'b-', linewidth=2)
    ax2.plot([delta_max, delta_max], [-Fy, Fy], 'b-', linewidth=2)

    # Rama elastica
    ax2.plot([0, delta_y], [0, Fy], 'r-', linewidth=2.5, label='Rama elastica')
    ax2.plot([0, -delta_y], [0, -Fy], 'r-', linewidth=2.5)

    # Pendiente elastica
    ax2.plot([0, 5], [0, Fy*5/delta_y/1000], 'r--', linewidth=1,
             label=f'$K = {K}$ MN/m')

    ax2.axhline(y=0, color='gray', linestyle='-', linewidth=0.5)
    ax2.axvline(x=0, color='gray', linestyle='-', linewidth=0.5)

    ax2.set_xlabel('Desplazamiento (mm)')
    ax2.set_ylabel('Fuerza (kN)')
    ax2.set_xlim(-40, 40)
    ax2.set_ylim(-350, 350)
    ax2.set_title('Lazo histeretico elastoplastico', fontsize=11)
    ax2.grid(True, alpha=0.3)
    ax2.legend(loc='upper left', fontsize=9)

    # Anotaciones
    ax2.annotate(f'$F_y = {Fy}$ kN', xy=(delta_max+2, Fy), fontsize=10, va='center')
    ax2.annotate(f'$\\delta_y = {delta_y}$ mm', xy=(delta_y, -50), fontsize=9, ha='center')
    ax2.annotate(f'$\\delta_{{max}} = {delta_max}$ mm', xy=(delta_max, -Fy-30), fontsize=9, ha='center')
    ax2.annotate(f'$\\mu = {delta_max/delta_y:.0f}$', xy=(0, 280), fontsize=11,
                ha='center', fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

    plt.tight_layout()

    filepath = os.path.join(OUTPUT_DIR, 'fig_problema_13_ADAS.pdf')
    plt.savefig(filepath, bbox_inches='tight')
    plt.close()
    print(f"[OK] Generada: fig_problema_13_ADAS.pdf")


if __name__ == '__main__':
    print("Generando figuras para Relacion 6 - No Lineal y Control...")
    print("-" * 50)

    fig_problema_10()
    fig_problema_12()
    fig_problema_13()

    print("-" * 50)
    print("Figuras generadas en:", OUTPUT_DIR)
