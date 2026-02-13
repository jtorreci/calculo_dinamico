"""
Figura: Edificio 6 plantas con fuerzas laterales equivalentes
Problema 19 - Relación 5
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle
from pathlib import Path

# Configuración
plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 10,
    'text.usetex': False,
    'mathtext.fontset': 'cm',
})

# Parámetros del edificio
n_plantas = 6
h_piso = 3.5  # m
ancho = 5.0   # m
alturas = np.array([h_piso * i for i in range(n_plantas + 1)])

# Fuerzas laterales (del problema)
F = np.array([54.4, 108.8, 163.2, 217.6, 272.0, 326.4])  # kN
Q = np.array([1142.4, 1088.0, 979.2, 816.0, 598.4, 326.4])  # kN (cortantes)

# Escala para flechas
F_max = np.max(F)
escala = 3.0 / F_max

# Crear figura con 2 subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 7))

def dibujar_edificio_base(ax):
    """Dibuja la estructura del edificio"""
    # Base
    ax.fill([-1.5, ancho + 1.5, ancho + 1.5, -1.5], [-1, -1, 0, 0], color='gray', alpha=0.5)
    ax.plot([-1.5, ancho + 1.5], [0, 0], 'k-', linewidth=2)

    # Estructura
    for i in range(n_plantas):
        y_inf = alturas[i]
        y_sup = alturas[i+1]
        # Columnas
        ax.plot([0, 0], [y_inf, y_sup], 'b-', linewidth=2)
        ax.plot([ancho, ancho], [y_inf, y_sup], 'b-', linewidth=2)
        # Viga/forjado
        ax.add_patch(Rectangle((-0.3, y_sup - 0.25), ancho + 0.6, 0.5,
                               facecolor='lightblue', edgecolor='blue', linewidth=1.5))

# ============================================
# SUBPLOT 1: Fuerzas laterales
# ============================================
ax1.set_xlim(-4, 12)
ax1.set_ylim(-2, 25)
ax1.set_aspect('equal')
ax1.axis('off')

dibujar_edificio_base(ax1)

# Flechas de fuerzas
for i, (h, f) in enumerate(zip(alturas[1:], F)):
    # Flecha
    arrow_length = f * escala
    ax1.annotate('', xy=(0, h), xytext=(-arrow_length, h),
                arrowprops=dict(arrowstyle='->', color='red', lw=2))
    # Etiqueta
    ax1.text(-arrow_length - 0.5, h, f'$F_{i+1}={f:.0f}$ kN',
            fontsize=9, ha='right', va='center', color='red')

# Etiquetas de altura
for i, h in enumerate(alturas[1:], 1):
    ax1.text(ancho + 1.0, h, f'{h:.1f} m', fontsize=9, va='center')

# Título
ax1.set_title('Fuerzas laterales equivalentes', fontsize=12, fontweight='bold')

# Cortante basal
ax1.annotate('', xy=(ancho/2, 0), xytext=(ancho/2, -1.5),
            arrowprops=dict(arrowstyle='->', color='darkred', lw=2.5))
ax1.text(ancho/2, -1.8, f'$V_b = {Q[0]:.0f}$ kN', fontsize=10, ha='center', color='darkred')

# ============================================
# SUBPLOT 2: Diagrama de cortantes
# ============================================
ax2.set_xlim(-2, 14)
ax2.set_ylim(-2, 25)
ax2.set_aspect('equal')
ax2.axis('off')

dibujar_edificio_base(ax2)

# Escala para cortantes
Q_max = np.max(Q)
escala_Q = 6.0 / Q_max

# Diagrama de cortantes (trapecio por planta)
x_base = ancho + 1.5
for i in range(n_plantas):
    y_inf = alturas[i]
    y_sup = alturas[i+1]
    q_inf = Q[i] * escala_Q if i < n_plantas else 0
    q_sup = Q[i] * escala_Q

    # Área del diagrama
    xs = [x_base, x_base + q_sup, x_base + q_inf, x_base]
    ys = [y_sup, y_sup, y_inf, y_inf]
    ax2.fill(xs, ys, color='lightgreen', alpha=0.5, edgecolor='green', linewidth=1.5)

    # Valor del cortante
    ax2.text(x_base + q_sup + 0.3, y_sup, f'$Q_{i+1}={Q[i]:.0f}$',
            fontsize=8, va='center', color='darkgreen')

# Línea del eje
ax2.plot([x_base, x_base], [0, alturas[-1]], 'k-', linewidth=1)

# Título
ax2.set_title('Diagrama de cortantes', fontsize=12, fontweight='bold')

# Leyenda adicional
ax2.text(x_base + 3, -1, 'Cortante [kN]', fontsize=10, ha='center', color='darkgreen')

plt.tight_layout()

# Guardar figura
output_dir = Path(__file__).parent.parent / 'figs'
output_dir.mkdir(exist_ok=True)
plt.savefig(output_dir / 'fig_edificio_6plantas_fuerzas.pdf', bbox_inches='tight', dpi=150)
plt.savefig(output_dir / 'fig_edificio_6plantas_fuerzas.png', bbox_inches='tight', dpi=150)
plt.close()

print("Figura guardada: fig_edificio_6plantas_fuerzas.pdf/png")
