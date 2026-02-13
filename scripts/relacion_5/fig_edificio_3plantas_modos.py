"""
Figura: Edificio 3 plantas con modos de vibración
Problema 13 - Relación 5
Usa StructDraw para el esquema estructural
"""
import sys
from pathlib import Path

# Añadir la ruta de StructDraw
structdraw_path = Path(__file__).parent.parent.parent.parent / "Libreria_dibujo" / "structdraw_studio_v0_4_3c"
sys.path.insert(0, str(structdraw_path))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

# Configuración
plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 10,
    'text.usetex': False,
    'mathtext.fontset': 'cm',
})

# Crear figura con 4 subplots
fig, axes = plt.subplots(1, 4, figsize=(12, 5))

# Parámetros del edificio
n_plantas = 3
h_piso = 3.5  # m
ancho = 4.0   # m
alturas = np.array([h_piso * i for i in range(n_plantas + 1)])

# Modos de vibración (normalizados)
modos = {
    1: np.array([0, 0.45, 0.80, 1.00]),
    2: np.array([0, 0.80, 0.45, -0.80]),
    3: np.array([0, 1.00, -1.00, 0.45])
}
periodos = [0.60, 0.22, 0.12]
masas_eff = [82, 13, 5]

def dibujar_edificio(ax, modo=None, amplitud=1.5, titulo=""):
    """Dibuja el edificio con o sin deformación modal"""
    ax.set_xlim(-3, 8)
    ax.set_ylim(-1.5, 13)
    ax.set_aspect('equal')
    ax.axis('off')

    # Base
    ax.fill([-2, 6, 6, -2], [-0.5, -0.5, 0, 0], color='gray', alpha=0.5)
    ax.plot([-2, 6], [0, 0], 'k-', linewidth=2)

    # Posiciones originales
    x_izq, x_der = 0, ancho

    if modo is None:
        # Edificio sin deformar
        for i in range(n_plantas):
            y_inf = alturas[i]
            y_sup = alturas[i+1]
            # Columnas
            ax.plot([x_izq, x_izq], [y_inf, y_sup], 'b-', linewidth=2)
            ax.plot([x_der, x_der], [y_inf, y_sup], 'b-', linewidth=2)
            # Viga
            ax.plot([x_izq, x_der], [y_sup, y_sup], 'b-', linewidth=2)
            # Masa
            ax.add_patch(plt.Rectangle((x_izq-0.3, y_sup-0.2), ancho+0.6, 0.4,
                                       facecolor='lightblue', edgecolor='blue', linewidth=1.5))
            ax.text(x_izq + ancho/2, y_sup, f'$m_{i+1}$', ha='center', va='center', fontsize=10)
        # Etiquetas de altura
        for i, h in enumerate(alturas[1:], 1):
            ax.text(x_der + 0.8, h, f'{h:.1f} m', fontsize=9, va='center')
    else:
        # Edificio deformado
        phi = modos[modo]
        for i in range(n_plantas):
            y_inf = alturas[i]
            y_sup = alturas[i+1]
            dx_inf = amplitud * phi[i]
            dx_sup = amplitud * phi[i+1]
            # Columnas deformadas
            ax.plot([x_izq + dx_inf, x_izq + dx_sup], [y_inf, y_sup], 'r-', linewidth=2)
            ax.plot([x_der + dx_inf, x_der + dx_sup], [y_inf, y_sup], 'r-', linewidth=2)
            # Viga
            ax.plot([x_izq + dx_sup, x_der + dx_sup], [y_sup, y_sup], 'r-', linewidth=2)
            # Masa
            ax.add_patch(plt.Rectangle((x_izq + dx_sup - 0.3, y_sup - 0.2), ancho + 0.6, 0.4,
                                       facecolor='lightyellow', edgecolor='red', linewidth=1.5))

        # Línea de referencia (original)
        for i in range(n_plantas):
            y_inf = alturas[i]
            y_sup = alturas[i+1]
            ax.plot([x_izq, x_izq], [y_inf, y_sup], 'b--', linewidth=0.5, alpha=0.5)
            ax.plot([x_der, x_der], [y_inf, y_sup], 'b--', linewidth=0.5, alpha=0.5)

        # Valores del modo
        for i, (h, phi_val) in enumerate(zip(alturas[1:], phi[1:])):
            ax.text(x_der + amplitud * phi_val + 1.0, h, f'$\\phi_{i+1}={phi_val:.2f}$',
                   fontsize=9, va='center')

    ax.set_title(titulo, fontsize=11, fontweight='bold')

# Dibujar cada configuración
dibujar_edificio(axes[0], modo=None, titulo="Estructura")
dibujar_edificio(axes[1], modo=1, amplitud=1.5, titulo=f"Modo 1\n$T_1={periodos[0]}$ s, $M^*={masas_eff[0]}$%")
dibujar_edificio(axes[2], modo=2, amplitud=1.5, titulo=f"Modo 2\n$T_2={periodos[1]}$ s, $M^*={masas_eff[1]}$%")
dibujar_edificio(axes[3], modo=3, amplitud=1.5, titulo=f"Modo 3\n$T_3={periodos[2]}$ s, $M^*={masas_eff[2]}$%")

plt.tight_layout()

# Guardar figura
output_dir = Path(__file__).parent.parent / 'figs'
output_dir.mkdir(exist_ok=True)
plt.savefig(output_dir / 'fig_edificio_3plantas_modos.pdf', bbox_inches='tight', dpi=150)
plt.savefig(output_dir / 'fig_edificio_3plantas_modos.png', bbox_inches='tight', dpi=150)
plt.close()

print("Figura guardada: fig_edificio_3plantas_modos.pdf/png")
