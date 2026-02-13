"""
Problema 06 - Relación 4: Viga continua de dos vanos
Diagrama mostrando modos simétricos y antisimétricos

Autor: Generado para el libro "Cálculo Dinámico de Estructuras"
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, FancyArrowPatch
import matplotlib.patches as mpatches

# Configuración general
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 10
plt.rcParams['text.usetex'] = False

def draw_pinned_support(ax, x, y, size=0.15, color='black'):
    """Dibuja apoyo articulado (triángulo)"""
    triangle = Polygon([
        [x, y],
        [x - size, y - size*1.2],
        [x + size, y - size*1.2]
    ], closed=True, fill=False, edgecolor=color, linewidth=1.5)
    ax.add_patch(triangle)
    # Línea de suelo
    ax.plot([x - size*1.2, x + size*1.2], [y - size*1.2, y - size*1.2], 'k-', linewidth=1.5)
    # Sombreado
    for i in range(5):
        xi = x - size*1.1 + i * size*0.55
        ax.plot([xi, xi - size*0.3], [y - size*1.2, y - size*1.5], 'k-', linewidth=0.8)

def draw_beam(ax, x1, x2, y, linewidth=3, color='steelblue'):
    """Dibuja la viga"""
    ax.plot([x1, x2], [y, y], color=color, linewidth=linewidth, solid_capstyle='round')

def draw_mode_shape(ax, x, y, amplitude, mode_type='symmetric', color='red', label=None):
    """Dibuja forma modal"""
    if mode_type == 'symmetric':
        # Modo simétrico: mismo sentido en ambos vanos
        # Primer vano
        y1 = amplitude * np.sin(np.pi * x[x <= 0.5] / 0.5) * 0.7
        # Segundo vano
        y2 = amplitude * np.sin(np.pi * (x[x > 0.5] - 0.5) / 0.5) * 0.7
        y_mode = np.concatenate([y1, y2])
    else:
        # Modo antisimétrico: sentidos opuestos
        # Primer vano
        y1 = amplitude * np.sin(np.pi * x[x <= 0.5] / 0.5)
        # Segundo vano
        y2 = -amplitude * np.sin(np.pi * (x[x > 0.5] - 0.5) / 0.5)
        y_mode = np.concatenate([y1, y2])

    ax.plot(x * 10, y + y_mode, color=color, linewidth=2.5, label=label)
    ax.fill_between(x * 10, y, y + y_mode, alpha=0.2, color=color)

# Crear figura con 3 subplots
fig, axes = plt.subplots(3, 1, figsize=(10, 8))
fig.suptitle('Viga continua de dos vanos: análisis modal por simetría', fontsize=14, fontweight='bold')

L = 5  # Longitud de cada vano

# ============================================
# Subplot 1: Estructura original
# ============================================
ax1 = axes[0]
ax1.set_xlim(-1, 11)
ax1.set_ylim(-1.2, 1.5)
ax1.set_aspect('equal')
ax1.axis('off')
ax1.set_title('Estructura: viga continua de dos vanos iguales', fontsize=11, pad=10)

# Viga
draw_beam(ax1, 0, 10, 0, linewidth=4, color='steelblue')

# Apoyos
draw_pinned_support(ax1, 0, 0)
draw_pinned_support(ax1, 5, 0)
draw_pinned_support(ax1, 10, 0)

# Etiquetas
ax1.annotate('', xy=(5, 0.8), xytext=(0, 0.8),
            arrowprops=dict(arrowstyle='<->', color='black', lw=1.5))
ax1.text(2.5, 1.0, r'$L = 5$ m', ha='center', fontsize=11)

ax1.annotate('', xy=(10, 0.8), xytext=(5, 0.8),
            arrowprops=dict(arrowstyle='<->', color='black', lw=1.5))
ax1.text(7.5, 1.0, r'$L = 5$ m', ha='center', fontsize=11)

ax1.text(0, -0.9, 'A', ha='center', fontsize=11, fontweight='bold')
ax1.text(5, -0.9, 'B', ha='center', fontsize=11, fontweight='bold')
ax1.text(10, -0.9, 'C', ha='center', fontsize=11, fontweight='bold')

# ============================================
# Subplot 2: Primer modo antisimétrico (fundamental)
# ============================================
ax2 = axes[1]
ax2.set_xlim(-1, 11)
ax2.set_ylim(-1.5, 1.8)
ax2.set_aspect('equal')
ax2.axis('off')
ax2.set_title(r'1er Modo Antisimétrico (fundamental): $f_1 = 4.9$ Hz', fontsize=11, pad=10, color='#d62728')

# Viga deformada - modo antisimétrico
x = np.linspace(0, 1, 100)
amplitude = 0.8

# Primer vano: medio seno hacia arriba
x1 = np.linspace(0, 5, 50)
y1 = amplitude * np.sin(np.pi * x1 / 5)

# Segundo vano: medio seno hacia abajo
x2 = np.linspace(5, 10, 50)
y2 = -amplitude * np.sin(np.pi * (x2 - 5) / 5)

# Viga original (referencia)
ax2.plot([0, 10], [0, 0], 'k--', linewidth=1, alpha=0.5, label='Posición original')

# Modo deformado
ax2.plot(x1, y1, color='#d62728', linewidth=3)
ax2.plot(x2, y2, color='#d62728', linewidth=3)
ax2.fill_between(x1, 0, y1, alpha=0.15, color='#d62728')
ax2.fill_between(x2, 0, y2, alpha=0.15, color='#d62728')

# Apoyos
draw_pinned_support(ax2, 0, 0)
draw_pinned_support(ax2, 5, 0)
draw_pinned_support(ax2, 10, 0)

# Flechas indicando movimiento
ax2.annotate('', xy=(2.5, 1.1), xytext=(2.5, 0.5),
            arrowprops=dict(arrowstyle='->', color='#d62728', lw=2))
ax2.annotate('', xy=(7.5, -1.1), xytext=(7.5, -0.5),
            arrowprops=dict(arrowstyle='->', color='#d62728', lw=2))

# Texto explicativo
ax2.text(2.5, 1.35, r'$+w$', ha='center', fontsize=10, color='#d62728')
ax2.text(7.5, -1.35, r'$-w$', ha='center', fontsize=10, color='#d62728')

# Nota sobre equivalencia
ax2.text(11.5, 0, 'Cada vano equivale a\nviga biapoyada', fontsize=9,
         ha='left', va='center', style='italic',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# ============================================
# Subplot 3: Primer modo simétrico
# ============================================
ax3 = axes[2]
ax3.set_xlim(-1, 11)
ax3.set_ylim(-1.5, 1.8)
ax3.set_aspect('equal')
ax3.axis('off')
ax3.set_title(r'1er Modo Simétrico: $f_1 = 7.6$ Hz', fontsize=11, pad=10, color='#2ca02c')

# Modo simétrico - empotrado-apoyado en cada vano
# Forma modal para viga empotrada-apoyada (aproximación)
x1 = np.linspace(0, 5, 50)
# Forma más realista: pendiente nula en el centro
beta_L = 3.9266
y1_sym = amplitude * 0.8 * (np.cosh(beta_L * x1/5) - np.cos(beta_L * x1/5)
         - 0.9825 * (np.sinh(beta_L * x1/5) - np.sin(beta_L * x1/5)))
y1_sym = y1_sym / np.max(np.abs(y1_sym)) * amplitude * 0.7

x2 = np.linspace(5, 10, 50)
y2_sym = amplitude * 0.8 * (np.cosh(beta_L * (10-x2)/5) - np.cos(beta_L * (10-x2)/5)
         - 0.9825 * (np.sinh(beta_L * (10-x2)/5) - np.sin(beta_L * (10-x2)/5)))
y2_sym = y2_sym / np.max(np.abs(y2_sym)) * amplitude * 0.7

# Viga original (referencia)
ax3.plot([0, 10], [0, 0], 'k--', linewidth=1, alpha=0.5)

# Modo deformado
ax3.plot(x1, y1_sym, color='#2ca02c', linewidth=3)
ax3.plot(x2, y2_sym, color='#2ca02c', linewidth=3)
ax3.fill_between(x1, 0, y1_sym, alpha=0.15, color='#2ca02c')
ax3.fill_between(x2, 0, y2_sym, alpha=0.15, color='#2ca02c')

# Apoyos
draw_pinned_support(ax3, 0, 0)
draw_pinned_support(ax3, 5, 0)
draw_pinned_support(ax3, 10, 0)

# Flechas indicando movimiento (mismo sentido)
ax3.annotate('', xy=(2.0, 0.9), xytext=(2.0, 0.4),
            arrowprops=dict(arrowstyle='->', color='#2ca02c', lw=2))
ax3.annotate('', xy=(8.0, 0.9), xytext=(8.0, 0.4),
            arrowprops=dict(arrowstyle='->', color='#2ca02c', lw=2))

# Indicar pendiente nula en B
ax3.plot([4.7, 5.3], [y1_sym[-1], y2_sym[0]], 'ko', markersize=4)
ax3.annotate(r"$\theta_B = 0$", xy=(5, y1_sym[-1]), xytext=(5.3, 1.2),
            fontsize=10, color='#2ca02c',
            arrowprops=dict(arrowstyle='->', color='#2ca02c', lw=1))

# Texto explicativo
ax3.text(11.5, 0.3, 'Cada vano equivale a\nviga empotrada-apoyada\n(pendiente nula en B)',
         fontsize=9, ha='left', va='center', style='italic',
         bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.3))

# Comparación final
fig.text(0.5, 0.02,
         r'El modo antisimétrico es el fundamental ($f = 4.9$ Hz) porque tiene menos restricciones que el simétrico ($f = 7.6$ Hz)',
         ha='center', fontsize=10, style='italic',
         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

plt.tight_layout(rect=[0, 0.05, 1, 0.95])

# Guardar figura
output_path = '../figs/fig_viga_continua_modos'
plt.savefig(output_path + '.pdf', dpi=300, bbox_inches='tight')
plt.savefig(output_path + '.png', dpi=150, bbox_inches='tight')
print(f"Figura guardada en {output_path}.pdf y {output_path}.png")

plt.close()
