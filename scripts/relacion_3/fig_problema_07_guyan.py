"""
Figura para Problema 07 - Relacion 3
Condensacion estatica de Guyan en sistema 3DOF
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle, FancyArrowPatch
from pathlib import Path

plt.rcParams.update({
    'font.size': 9,
    'axes.labelsize': 10,
    'axes.titlesize': 11,
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'font.family': 'sans-serif'
})

output_dir = Path(__file__).parent.parent / "figuras"
output_dir.mkdir(exist_ok=True)

def dibujar_edificio_3dof(ax, titulo, desplaz=None, modo_num=None, destacar_gdl=None):
    """Dibuja edificio 3DOF tipo shear building"""
    ax.set_xlim(-0.5, 4)
    ax.set_ylim(-0.8, 10)
    ax.axis('off')
    ax.set_title(titulo, fontweight='bold', fontsize=10)

    h_planta = 2.5

    # Base
    ax.fill_between([-0.2, 2.2], [-0.4, -0.4], [0, 0], color='brown', alpha=0.5, hatch='///')
    ax.plot([-0.2, 2.2], [0, 0], 'k-', lw=2)

    # Colores para GDL
    colores = ['steelblue', 'steelblue', 'steelblue']
    if destacar_gdl is not None:
        for i in destacar_gdl:
            colores[i] = 'coral'

    for i in range(3):
        y = (i + 1) * h_planta

        # Desplazamiento
        dx = 0
        if desplaz is not None:
            escala = 0.8 / max(abs(desplaz)) if max(abs(desplaz)) > 0 else 1
            dx = desplaz[i] * escala

        # Pilares
        if i == 0:
            ax.plot([1 + 0, 1 + dx], [0, y], 'b-', lw=2)
        else:
            dx_prev = desplaz[i-1] * escala if desplaz is not None else 0
            ax.plot([1 + dx_prev, 1 + dx], [(i) * h_planta, y], 'b-', lw=2)

        # Forjado
        color = colores[i]
        ax.fill_between([1 + dx - 0.4, 1 + dx + 0.4], [y - 0.1, y - 0.1],
                        [y + 0.1, y + 0.1], color=color, alpha=0.8)

        # Etiqueta masa
        ax.text(1 + dx + 0.7, y, f'$m_{i+1}$', fontsize=9, va='center')

        # GDL
        if destacar_gdl is not None and i in destacar_gdl:
            ax.annotate('', xy=(1 + dx + 1.3, y), xytext=(1 + dx + 0.9, y),
                       arrowprops=dict(arrowstyle='->', color='red', lw=2))
            ax.text(1 + dx + 1.5, y, f'$u_{i+1}$', fontsize=10, va='center', color='red')
        else:
            ax.annotate('', xy=(1 + dx + 1.3, y), xytext=(1 + dx + 0.9, y),
                       arrowprops=dict(arrowstyle='->', color='gray', lw=1.5))
            ax.text(1 + dx + 1.5, y, f'$u_{i+1}$', fontsize=9, va='center', color='gray')

    return ax

# --- Crear figura ---
fig, axes = plt.subplots(1, 3, figsize=(10, 5))

# ======================
# Panel (a): Sistema original 3DOF
# ======================
ax = axes[0]
dibujar_edificio_3dof(ax, '(a) Sistema original 3DOF', destacar_gdl=[0, 1, 2])
ax.text(2.0, 9, '$\\mathbf{M} = m \\cdot I_3$\n$\\mathbf{K} = k \\cdot K_{shear}$',
        fontsize=9, ha='center', va='top',
        bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9, pad=0.3))

# ======================
# Panel (b): Condensacion - GDL eliminado
# ======================
ax = axes[1]
ax.set_xlim(-0.5, 4)
ax.set_ylim(-0.8, 10)
ax.axis('off')
ax.set_title('(b) Condensacion de Guyan', fontweight='bold', fontsize=10)

h_planta = 2.5

# Base
ax.fill_between([-0.2, 2.2], [-0.4, -0.4], [0, 0], color='brown', alpha=0.5, hatch='///')
ax.plot([-0.2, 2.2], [0, 0], 'k-', lw=2)

# Edificio con GDL 2 marcado como eliminado
for i in range(3):
    y = (i + 1) * h_planta

    # Pilares
    ax.plot([1, 1], [(i) * h_planta if i > 0 else 0, y], 'b-', lw=2)

    # Forjado - GDL 2 (central) en gris
    if i == 1:
        color = 'lightgray'
        ax.fill_between([0.6, 1.4], [y - 0.1, y - 0.1], [y + 0.1, y + 0.1],
                        color=color, alpha=0.8, linestyle='--', edgecolor='gray')
        ax.text(1.9, y, '$u_2$', fontsize=9, va='center', color='gray')
        ax.text(2.2, y-0.4, '(eliminado)', fontsize=8, va='top', color='gray', style='italic')
    else:
        color = 'coral'
        ax.fill_between([0.6, 1.4], [y - 0.1, y - 0.1], [y + 0.1, y + 0.1],
                        color=color, alpha=0.8)
        ax.text(1.9, y, f'$u_{i+1}$', fontsize=10, va='center', color='red')
        ax.text(2.3, y-0.4, '(retenido)', fontsize=8, va='top', color='red', style='italic')

# Flecha de transformacion
ax.annotate('', xy=(1, 7.2), xytext=(1, 9),
            arrowprops=dict(arrowstyle='->', color='green', lw=2,
                          connectionstyle='arc3,rad=0'))
ax.text(1, 9.3, 'Relacion de\ncondensacion', fontsize=8, ha='center', va='bottom',
        color='green')

# Matriz T (simplificada para matplotlib)
ax.text(1, 8.2, '$\\mathbf{T}_{3\\times 2}$:\n$u_2 = \\frac{1}{2}(u_1 + u_3)$',
        fontsize=9, ha='center', va='center')

# ======================
# Panel (c): Sistema reducido 2DOF
# ======================
ax = axes[2]
ax.set_xlim(-0.5, 4)
ax.set_ylim(-0.8, 10)
ax.axis('off')
ax.set_title('(c) Sistema reducido 2DOF', fontweight='bold', fontsize=10)

h_planta = 3.5

# Base
ax.fill_between([-0.2, 2.2], [-0.4, -0.4], [0, 0], color='brown', alpha=0.5, hatch='///')
ax.plot([-0.2, 2.2], [0, 0], 'k-', lw=2)

# Solo 2 plantas (GDL 1 y 3)
for i, label in enumerate([1, 3]):
    y = (i + 1) * h_planta

    # Pilares
    ax.plot([1, 1], [(i) * h_planta if i > 0 else 0, y], 'b-', lw=2)

    # Forjado
    ax.fill_between([0.6, 1.4], [y - 0.12, y - 0.12], [y + 0.12, y + 0.12],
                    color='coral', alpha=0.8)

    # Etiqueta
    ax.text(1.8, y, f'$u_{label}$', fontsize=10, va='center', color='red')

# Matrices reducidas (simplificadas)
ax.text(1, 8.5, '$\\mathbf{M}_{red}$, $\\mathbf{K}_{red}$\n(2x2)',
        fontsize=10, ha='center', va='center',
        bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8, pad=0.3))

# Error
ax.text(1, 1.5, 'Error: $\\omega_1^{red} = 4.5$ rad/s\n'
                'vs $\\omega_1^{exact} = 7.7$ rad/s\n'
                '($\\approx 40\\%$ error)',
        fontsize=8, ha='center', va='top',
        bbox=dict(boxstyle='round', facecolor='mistyrose', alpha=0.9, pad=0.3))

plt.tight_layout()
plt.savefig(output_dir / "fig_problema_07_guyan.pdf")
plt.savefig(output_dir / "fig_problema_07_guyan.png")
plt.close()

print(f"Figura guardada en: {output_dir / 'fig_problema_07_guyan.pdf'}")
