"""
Generador de figuras para Relación 3 - Sistemas MDOF
Problemas 02, 03, 11, 17
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch, FancyBboxPatch
from matplotlib.lines import Line2D
import matplotlib.patches as mpatches
from pathlib import Path

# Configuración general
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['figure.dpi'] = 150

# Directorio de salida
OUTPUT_DIR = Path(__file__).parent.parent / 'figs'
OUTPUT_DIR.mkdir(exist_ok=True)


def fig_problema_02():
    """
    Problema 02: Edificio uniforme de 3 plantas - esquema y modos
    """
    fig, axes = plt.subplots(1, 4, figsize=(14, 5))

    # Datos del problema
    m = 1000  # kg
    k = 200e3  # N/m
    n = 3

    # Frecuencias y modos (fórmula cerrada)
    omega = np.array([np.sqrt(2*k/m * (1 - np.cos(j*np.pi/(n+1)))) for j in range(1, n+1)])
    freq = omega / (2*np.pi)

    # Modos (sin normalizar para visualización)
    modes = np.array([[np.sin(j*i*np.pi/(n+1)) for i in range(1, n+1)] for j in range(1, n+1)]).T

    # Colores
    colors = ['#2E86AB', '#A23B72', '#F18F01']

    # --- Panel 1: Esquema del edificio ---
    ax = axes[0]
    ax.set_xlim(-1, 3)
    ax.set_ylim(-0.5, 4)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Modelo shear building', fontweight='bold')

    # Dibujar edificio
    floor_width = 1.5
    floor_height = 0.15
    story_height = 1.0
    col_width = 0.08

    # Base (tierra)
    ax.fill_between([-0.5, 2.5], [-0.3, -0.3], [-0.5, -0.5],
                    color='brown', alpha=0.5, hatch='///')
    ax.plot([-0.5, 2.5], [0, 0], 'k-', linewidth=2)

    for i in range(n):
        y = i * story_height
        # Columnas
        ax.add_patch(Rectangle((0.2, y), col_width, story_height,
                               facecolor='gray', edgecolor='black'))
        ax.add_patch(Rectangle((1.5-col_width, y), col_width, story_height,
                               facecolor='gray', edgecolor='black'))
        # Forjado
        ax.add_patch(Rectangle((0, y + story_height - floor_height/2),
                               floor_width + 0.2, floor_height,
                               facecolor='lightblue', edgecolor='black'))
        # Masa
        ax.text(2.2, y + story_height, f'$m_{i+1}$', fontsize=11, va='center')
        # Rigidez
        ax.text(-0.3, y + story_height/2, f'$k_{i+1}$', fontsize=11, va='center', ha='right')

    # --- Paneles 2-4: Modos de vibración ---
    for j in range(3):
        ax = axes[j+1]
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-0.5, 4)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title(f'Modo {j+1}: $f_{j+1}$ = {freq[j]:.2f} Hz', fontweight='bold')

        # Escala del modo para visualización
        mode = modes[:, j]
        scale = 0.8 / np.max(np.abs(mode))

        # Línea de referencia (posición estática)
        for i in range(n):
            y = (i + 1) * story_height
            ax.plot([0, 0], [y-story_height, y], 'k--', alpha=0.3, linewidth=1)

        # Forma modal deformada
        x_def = [0] + list(mode * scale)
        y_def = [0] + [i * story_height for i in range(1, n+1)]
        ax.plot(x_def, y_def, 'o-', color=colors[j], linewidth=2.5, markersize=10)

        # Base fija
        ax.plot([-0.3, 0.3], [0, 0], 'k-', linewidth=3)
        ax.fill_between([-0.3, 0.3], [-0.15, -0.15], [0, 0],
                       color='gray', hatch='///')

        # Etiquetas de amplitud
        for i, (x, y) in enumerate(zip(x_def[1:], y_def[1:])):
            ax.annotate(f'{mode[i]:.2f}', (x + 0.15*np.sign(x+0.01), y),
                       fontsize=9, ha='left' if x >= 0 else 'right')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'fig_problema_02_edificio_3plantas.pdf',
                bbox_inches='tight', dpi=300)
    plt.close()
    print("[OK] Generada: fig_problema_02_edificio_3plantas.pdf")


def fig_problema_03():
    """
    Problema 03: Sistema 2DOF no uniforme - esquema y modos
    """
    fig, axes = plt.subplots(1, 3, figsize=(12, 5))

    # Datos del problema
    m1, m2 = 800, 1200  # kg
    # Modos (con primera componente unitaria)
    phi1 = np.array([1, 2])
    phi2 = np.array([1, -1/3])
    omega = np.array([11.180, 20.412])
    freq = omega / (2*np.pi)

    colors = ['#2E86AB', '#A23B72']

    # --- Panel 1: Esquema ---
    ax = axes[0]
    ax.set_xlim(-1, 3)
    ax.set_ylim(-0.5, 3)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Sistema 2DOF no uniforme', fontweight='bold')

    story_height = 1.0

    # Base
    ax.fill_between([-0.5, 2.5], [-0.3, -0.3], [-0.5, -0.5],
                    color='brown', alpha=0.5, hatch='///')
    ax.plot([-0.5, 2.5], [0, 0], 'k-', linewidth=2)

    # Planta 1 (m1 = 800 kg)
    ax.add_patch(Rectangle((0.2, 0), 0.08, story_height,
                           facecolor='gray', edgecolor='black'))
    ax.add_patch(Rectangle((1.42, 0), 0.08, story_height,
                           facecolor='gray', edgecolor='black'))
    ax.add_patch(FancyBboxPatch((0, 0.9), 1.7, 0.2,
                                boxstyle="round,pad=0.02",
                                facecolor='lightblue', edgecolor='black'))
    ax.text(2.2, 1.0, f'$m_1$ = {m1} kg', fontsize=10, va='center')

    # Planta 2 (m2 = 1200 kg) - más grande
    ax.add_patch(Rectangle((0.2, 1.0), 0.08, story_height,
                           facecolor='gray', edgecolor='black'))
    ax.add_patch(Rectangle((1.42, 1.0), 0.08, story_height,
                           facecolor='gray', edgecolor='black'))
    ax.add_patch(FancyBboxPatch((-0.1, 1.9), 1.9, 0.25,
                                boxstyle="round,pad=0.02",
                                facecolor='#87CEEB', edgecolor='black', linewidth=1.5))
    ax.text(2.2, 2.0, f'$m_2$ = {m2} kg', fontsize=10, va='center')

    # --- Paneles 2-3: Modos ---
    modes = [phi1, phi2]
    for j in range(2):
        ax = axes[j+1]
        ax.set_xlim(-1.5, 2)
        ax.set_ylim(-0.5, 3)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title(f'Modo {j+1}: $f_{j+1}$ = {freq[j]:.2f} Hz', fontweight='bold')

        mode = modes[j]
        scale = 0.6 / np.max(np.abs(mode))

        # Referencia
        ax.plot([0, 0], [0, 2], 'k--', alpha=0.3)

        # Deformada
        x_def = [0] + list(mode * scale)
        y_def = [0, 1, 2]
        ax.plot(x_def, y_def, 'o-', color=colors[j], linewidth=2.5, markersize=12)

        # Base
        ax.plot([-0.3, 0.3], [0, 0], 'k-', linewidth=3)
        ax.fill_between([-0.3, 0.3], [-0.15, -0.15], [0, 0],
                       color='gray', hatch='///')

        # Etiquetas
        for i, (x, y) in enumerate(zip(x_def[1:], y_def[1:])):
            label = f'{mode[i]:.2f}' if mode[i] != 1 else '1.00'
            ax.annotate(label, (x + 0.2*np.sign(x+0.01), y),
                       fontsize=10, ha='left' if x >= 0 else 'right')

        # Tipo de modo
        tipo = "En fase" if j == 0 else "Contrafase"
        ax.text(0, -0.3, tipo, fontsize=10, ha='center', style='italic')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'fig_problema_03_2dof_no_uniforme.pdf',
                bbox_inches='tight', dpi=300)
    plt.close()
    print("[OK] Generada: fig_problema_03_2dof_no_uniforme.pdf")


def fig_problema_11():
    """
    Problema 11: Péndulos acoplados con muelle
    """
    fig, axes = plt.subplots(1, 3, figsize=(13, 5))

    # Datos
    L = 1.0  # m
    omega = np.array([3.132, 5.459])
    freq = omega / (2*np.pi)

    colors = ['#2E86AB', '#A23B72']

    # --- Panel 1: Esquema del sistema ---
    ax = axes[0]
    ax.set_xlim(-2, 2)
    ax.set_ylim(-1.5, 0.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Péndulos acoplados', fontweight='bold')

    # Soporte superior
    ax.plot([-1.5, 1.5], [0, 0], 'k-', linewidth=4)
    ax.fill_between([-1.5, 1.5], [0.1, 0.1], [0, 0], color='gray', hatch='///')

    # Péndulos
    theta = 0.2  # ángulo para visualización
    for sign, label in [(-1, '1'), (1, '2')]:
        x0 = sign * 0.8
        x1 = x0 + L * np.sin(theta * sign * 0.5)
        y1 = -L * np.cos(theta)

        # Varilla
        ax.plot([x0, x1], [0, y1], 'k-', linewidth=2)

        # Masa
        circle = Circle((x1, y1), 0.12, facecolor='steelblue', edgecolor='black', linewidth=1.5)
        ax.add_patch(circle)
        ax.text(x1, y1 - 0.3, f'$m$', fontsize=11, ha='center')

        # Pivote
        ax.plot(x0, 0, 'ko', markersize=6)

        # Ángulo
        ax.annotate(f'$\\theta_{label}$', (x0 + 0.15*sign, -0.25),
                   fontsize=11, ha='center')

    # Muelle entre masas
    n_coils = 8
    x_spring = np.linspace(-0.8 + L*np.sin(-theta*0.5), 0.8 + L*np.sin(theta*0.5), 100)
    y_spring = -L*np.cos(theta) + 0.05*np.sin(n_coils * np.pi *
               (x_spring - x_spring[0]) / (x_spring[-1] - x_spring[0]))
    ax.plot(x_spring, y_spring, 'k-', linewidth=1.5)
    ax.text(0, -L*np.cos(theta) + 0.2, '$k_s$', fontsize=11, ha='center')

    # Etiquetas
    ax.text(-0.8, 0.2, '$\\ell$', fontsize=11, ha='center')

    # --- Paneles 2-3: Modos ---
    for j in range(2):
        ax = axes[j+1]
        ax.set_xlim(-2, 2)
        ax.set_ylim(-1.5, 0.5)
        ax.set_aspect('equal')
        ax.axis('off')

        modo_nombre = "En fase" if j == 0 else "Contrafase"
        ax.set_title(f'Modo {j+1}: {modo_nombre}\n$f_{j+1}$ = {freq[j]:.2f} Hz', fontweight='bold')

        # Soporte
        ax.plot([-1.5, 1.5], [0, 0], 'k-', linewidth=4)
        ax.fill_between([-1.5, 1.5], [0.1, 0.1], [0, 0], color='gray', hatch='///')

        # Ángulos para cada modo
        if j == 0:  # En fase
            theta1, theta2 = 0.4, 0.4
        else:  # Contrafase
            theta1, theta2 = 0.4, -0.4

        for sign, theta_i in [(-1, theta1), (1, theta2)]:
            x0 = sign * 0.8
            x1 = x0 + L * np.sin(theta_i)
            y1 = -L * np.cos(theta_i)

            # Posición de equilibrio (punteada)
            ax.plot([x0, x0], [0, -L], 'k--', alpha=0.3, linewidth=1)

            # Varilla deformada
            ax.plot([x0, x1], [0, y1], '-', color=colors[j], linewidth=2.5)

            # Masa
            circle = Circle((x1, y1), 0.12, facecolor=colors[j],
                           edgecolor='black', linewidth=1.5, alpha=0.8)
            ax.add_patch(circle)

            # Pivote
            ax.plot(x0, 0, 'ko', markersize=6)

            # Flecha de movimiento
            dx = 0.25 * np.sign(theta_i) if abs(theta_i) > 0.01 else 0
            ax.annotate('', xy=(x1 + dx, y1), xytext=(x1, y1),
                       arrowprops=dict(arrowstyle='->', color=colors[j], lw=2))

        # Muelle
        x1_left = -0.8 + L * np.sin(theta1)
        x1_right = 0.8 + L * np.sin(theta2)
        x_spring = np.linspace(x1_left, x1_right, 100)
        y_base = -L * np.cos(max(abs(theta1), abs(theta2)))

        if j == 0:  # En fase - muelle no se deforma
            ax.plot([x1_left + 0.12, x1_right - 0.12], [y_base, y_base],
                   'k-', linewidth=1.5)
            ax.text(0, y_base + 0.15, 'No deforma', fontsize=9, ha='center', style='italic')
        else:  # Contrafase - muelle se comprime
            n_coils = 12
            y_spring = y_base + 0.06*np.sin(n_coils * np.pi *
                       (x_spring - x_spring[0]) / (x_spring[-1] - x_spring[0]))
            ax.plot(x_spring, y_spring, 'k-', linewidth=1.5)
            ax.text(0, y_base + 0.2, 'Trabaja', fontsize=9, ha='center', style='italic')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'fig_problema_11_pendulos_acoplados.pdf',
                bbox_inches='tight', dpi=300)
    plt.close()
    print("[OK] Generada: fig_problema_11_pendulos_acoplados.pdf")


def fig_problema_17():
    """
    Problema 17: Péndulo doble
    """
    fig, axes = plt.subplots(1, 3, figsize=(13, 5))

    # Datos
    L1, L2 = 1.0, 1.0
    m1, m2 = 2.0, 1.0
    omega = np.array([2.47, 5.42])
    freq = omega / (2*np.pi)

    # Modos (primera componente unitaria)
    phi1 = np.array([1, 1.35])
    phi2 = np.array([1, -0.74])

    colors = ['#2E86AB', '#A23B72']

    # --- Panel 1: Esquema ---
    ax = axes[0]
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-2.5, 0.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Péndulo doble', fontweight='bold')

    # Soporte
    ax.plot([-0.5, 0.5], [0, 0], 'k-', linewidth=4)
    ax.fill_between([-0.5, 0.5], [0.1, 0.1], [0, 0], color='gray', hatch='///')
    ax.plot(0, 0, 'ko', markersize=8)

    # Péndulo 1
    theta1 = 0.25
    x1 = L1 * np.sin(theta1)
    y1 = -L1 * np.cos(theta1)
    ax.plot([0, x1], [0, y1], 'k-', linewidth=3)
    circle1 = Circle((x1, y1), 0.15, facecolor='steelblue', edgecolor='black', linewidth=2)
    ax.add_patch(circle1)
    ax.text(x1 + 0.3, y1, f'$m_1$ = {m1} kg', fontsize=10, va='center')
    ax.text(-0.3, -0.5, f'$L_1$', fontsize=11)

    # Ángulo theta1
    arc1 = mpatches.Arc((0, 0), 0.4, 0.4, angle=0, theta1=270, theta2=270+np.degrees(theta1))
    ax.add_patch(arc1)
    ax.text(0.15, -0.25, r'$\theta_1$', fontsize=11)

    # Péndulo 2
    theta2 = 0.15
    x2 = x1 + L2 * np.sin(theta1 + theta2)
    y2 = y1 - L2 * np.cos(theta1 + theta2)
    ax.plot([x1, x2], [y1, y2], 'k-', linewidth=3)
    circle2 = Circle((x2, y2), 0.12, facecolor='coral', edgecolor='black', linewidth=2)
    ax.add_patch(circle2)
    ax.text(x2 + 0.25, y2, f'$m_2$ = {m2} kg', fontsize=10, va='center')
    ax.text(x1 + 0.15, y1 - 0.5, f'$L_2$', fontsize=11)

    # Ángulo theta2
    arc2 = mpatches.Arc((x1, y1), 0.35, 0.35, angle=0,
                        theta1=270-np.degrees(theta1),
                        theta2=270-np.degrees(theta1)+np.degrees(theta2))
    ax.add_patch(arc2)
    ax.text(x1 + 0.25, y1 - 0.2, r'$\theta_2$', fontsize=11)

    # --- Paneles 2-3: Modos ---
    modes = [phi1, phi2]
    for j in range(2):
        ax = axes[j+1]
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-2.5, 0.5)
        ax.set_aspect('equal')
        ax.axis('off')

        modo_nombre = "En fase" if j == 0 else "Contrafase"
        ax.set_title(f'Modo {j+1}: {modo_nombre}\n$f_{j+1}$ = {freq[j]:.2f} Hz', fontweight='bold')

        # Soporte
        ax.plot([-0.5, 0.5], [0, 0], 'k-', linewidth=4)
        ax.fill_between([-0.5, 0.5], [0.1, 0.1], [0, 0], color='gray', hatch='///')
        ax.plot(0, 0, 'ko', markersize=8)

        # Posición de equilibrio
        ax.plot([0, 0], [0, -L1], 'k--', alpha=0.3)
        ax.plot([0, 0], [-L1, -L1-L2], 'k--', alpha=0.3)

        # Ángulos del modo (escalados para visualización)
        mode = modes[j]
        scale = 0.4 / np.max(np.abs(mode))
        t1 = mode[0] * scale
        t2 = mode[1] * scale

        # Péndulo 1 deformado
        x1 = L1 * np.sin(t1)
        y1 = -L1 * np.cos(t1)
        ax.plot([0, x1], [0, y1], '-', color=colors[j], linewidth=3)
        circle1 = Circle((x1, y1), 0.15, facecolor=colors[j],
                         edgecolor='black', linewidth=2, alpha=0.8)
        ax.add_patch(circle1)

        # Péndulo 2 deformado
        x2 = x1 + L2 * np.sin(t1 + t2)
        y2 = y1 - L2 * np.cos(t1 + t2)
        ax.plot([x1, x2], [y1, y2], '-', color=colors[j], linewidth=3)
        circle2 = Circle((x2, y2), 0.12, facecolor=colors[j],
                         edgecolor='black', linewidth=2, alpha=0.6)
        ax.add_patch(circle2)

        # Flechas de movimiento
        dx1 = 0.2 * np.sign(t1)
        ax.annotate('', xy=(x1 + dx1, y1), xytext=(x1, y1),
                   arrowprops=dict(arrowstyle='->', color=colors[j], lw=2))

        dx2 = 0.15 * np.sign(t2)
        ax.annotate('', xy=(x2 + dx2, y2), xytext=(x2, y2),
                   arrowprops=dict(arrowstyle='->', color=colors[j], lw=2))

        # Etiquetas de amplitud relativa
        ax.text(0.8, -0.5, f'$\\phi_1$ = {mode[0]:.2f}', fontsize=10)
        ax.text(0.8, -1.5, f'$\\phi_2$ = {mode[1]:.2f}', fontsize=10)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'fig_problema_17_pendulo_doble.pdf',
                bbox_inches='tight', dpi=300)
    plt.close()
    print("[OK] Generada: fig_problema_17_pendulo_doble.pdf")


if __name__ == '__main__':
    print("Generando figuras para Relación 3...")
    print(f"Directorio de salida: {OUTPUT_DIR}")
    print()

    fig_problema_02()
    fig_problema_03()
    fig_problema_11()
    fig_problema_17()

    print()
    print("¡Todas las figuras generadas correctamente!")
