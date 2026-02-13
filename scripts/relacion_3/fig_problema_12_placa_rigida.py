"""
Figura para Problema 12 - Relacion 3
Placa rigida con dos apoyos elasticos: acoplamiento u-theta
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Polygon
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

def dibujar_resorte(ax, x0, y0, x1, y1, n_coils=6, width=0.15, color='blue'):
    """Dibuja un resorte vertical entre (x0,y0) y (x1,y1)"""
    length = y1 - y0
    # Puntos del resorte en zigzag
    coil_height = length / (n_coils + 1)
    y_points = [y0]
    x_points = [x0]

    for i in range(n_coils):
        y_mid = y0 + (i + 0.5) * coil_height + coil_height/2
        if i % 2 == 0:
            x_points.append(x0 - width)
        else:
            x_points.append(x0 + width)
        y_points.append(y_mid)

    y_points.append(y1)
    x_points.append(x1)

    ax.plot(x_points, y_points, color=color, linewidth=1.5)

def dibujar_resorte_simple(ax, x, y_base, y_top, label=None, color='steelblue'):
    """Dibuja un resorte simple con zigzag"""
    n_coils = 5
    height = y_top - y_base
    coil_h = height / (n_coils + 2)

    # Linea base
    ax.plot([x, x], [y_base, y_base + coil_h], color=color, lw=1.5)

    # Zigzag
    points_x = [x]
    points_y = [y_base + coil_h]
    w = 0.12
    for i in range(n_coils):
        y = y_base + coil_h + (i + 0.5) * coil_h
        if i % 2 == 0:
            points_x.append(x - w)
        else:
            points_x.append(x + w)
        points_y.append(y)

    points_x.append(x)
    points_y.append(y_top - coil_h)
    ax.plot(points_x, points_y, color=color, lw=1.5)

    # Linea superior
    ax.plot([x, x], [y_top - coil_h, y_top], color=color, lw=1.5)

    if label:
        ax.text(x, y_base - 0.2, label, ha='center', va='top', fontsize=9)

# --- Crear figura ---
fig, axes = plt.subplots(1, 3, figsize=(10, 4))

# ======================
# Panel (a): Sistema original
# ======================
ax = axes[0]
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-0.8, 2.5)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title('(a) Sistema fisico', fontweight='bold', fontsize=10)

# Base (suelo)
ax.fill_between([-1.3, 1.3], [-0.6, -0.6], [-0.5, -0.5], color='brown', alpha=0.5)
ax.plot([-1.3, 1.3], [-0.5, -0.5], 'k-', lw=2)

# Bloques de neopreno (base de resortes)
for x in [-0.6, 0.6]:
    rect = Rectangle((x-0.15, -0.5), 0.3, 0.15, facecolor='gray', edgecolor='black', lw=1)
    ax.add_patch(rect)

# Resortes
dibujar_resorte_simple(ax, -0.6, -0.35, 0.5, '$k$', 'steelblue')
dibujar_resorte_simple(ax, 0.6, -0.35, 0.5, '$k$', 'steelblue')

# Placa rigida (losa)
losa = FancyBboxPatch((-1.0, 0.5), 2.0, 0.4, boxstyle="round,pad=0.02",
                       facecolor='lightsteelblue', edgecolor='navy', linewidth=2)
ax.add_patch(losa)
ax.text(0, 0.7, '$m$, $I$', ha='center', va='center', fontsize=10, fontweight='bold')

# Centro de masa
ax.plot(0, 0.7, 'ko', markersize=6)

# Distancias
ax.annotate('', xy=(-0.6, 1.1), xytext=(0, 1.1),
            arrowprops=dict(arrowstyle='<->', color='darkgreen', lw=1.5))
ax.text(-0.3, 1.25, '$b$', ha='center', va='bottom', fontsize=10, color='darkgreen')

ax.annotate('', xy=(0.6, 1.1), xytext=(0, 1.1),
            arrowprops=dict(arrowstyle='<->', color='darkgreen', lw=1.5))
ax.text(0.3, 1.25, '$b$', ha='center', va='bottom', fontsize=10, color='darkgreen')

# Coordenadas u y theta
ax.annotate('', xy=(0, 1.7), xytext=(0, 2.2),
            arrowprops=dict(arrowstyle='->', color='red', lw=2))
ax.text(0.15, 2.0, '$u$', fontsize=11, color='red', fontweight='bold')

# Arco para theta
theta_arc = np.linspace(-30, 30, 20) * np.pi / 180
r_arc = 0.5
x_arc = r_arc * np.sin(theta_arc) + 0
y_arc = r_arc * np.cos(theta_arc) + 0.7
ax.plot(x_arc, y_arc, 'r-', lw=1.5)
ax.annotate('', xy=(x_arc[-1], y_arc[-1]), xytext=(x_arc[-2], y_arc[-2]),
            arrowprops=dict(arrowstyle='->', color='red', lw=1.5))
ax.text(0.6, 1.0, r'$\theta$', fontsize=11, color='red', fontweight='bold')

# ======================
# Panel (b): Modo de traslacion pura
# ======================
ax = axes[1]
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-0.8, 2.5)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title(r'(b) Modo $u$ (traslacion)', fontweight='bold', fontsize=10)

# Base
ax.fill_between([-1.3, 1.3], [-0.6, -0.6], [-0.5, -0.5], color='brown', alpha=0.5)
ax.plot([-1.3, 1.3], [-0.5, -0.5], 'k-', lw=2)

# Bloques de neopreno
for x in [-0.6, 0.6]:
    rect = Rectangle((x-0.15, -0.5), 0.3, 0.15, facecolor='gray', edgecolor='black', lw=1)
    ax.add_patch(rect)

# Resortes comprimidos uniformemente
dibujar_resorte_simple(ax, -0.6, -0.35, 0.7, None, 'steelblue')
dibujar_resorte_simple(ax, 0.6, -0.35, 0.7, None, 'steelblue')

# Placa desplazada hacia arriba
losa = FancyBboxPatch((-1.0, 0.7), 2.0, 0.4, boxstyle="round,pad=0.02",
                       facecolor='lightsteelblue', edgecolor='navy', linewidth=2)
ax.add_patch(losa)

# Posicion original (linea discontinua)
ax.plot([-1.0, 1.0], [0.5, 0.5], 'k--', lw=1, alpha=0.5)
ax.plot([-1.0, 1.0], [0.9, 0.9], 'k--', lw=1, alpha=0.5)

# Flecha de desplazamiento
ax.annotate('', xy=(0, 1.3), xytext=(0, 1.6),
            arrowprops=dict(arrowstyle='->', color='green', lw=2))
ax.text(0.2, 1.45, '$u$', fontsize=11, color='green', fontweight='bold')

# Formula
ax.text(0, 2.1, r'$\omega_u = \sqrt{\frac{2k}{m}}$', fontsize=10, ha='center',
        bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8, pad=0.3))

# ======================
# Panel (c): Modo de rotacion pura
# ======================
ax = axes[2]
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-0.8, 2.5)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title(r'(c) Modo $\theta$ (rotacion)', fontweight='bold', fontsize=10)

# Base
ax.fill_between([-1.3, 1.3], [-0.6, -0.6], [-0.5, -0.5], color='brown', alpha=0.5)
ax.plot([-1.3, 1.3], [-0.5, -0.5], 'k-', lw=2)

# Bloques de neopreno
for x in [-0.6, 0.6]:
    rect = Rectangle((x-0.15, -0.5), 0.3, 0.15, facecolor='gray', edgecolor='black', lw=1)
    ax.add_patch(rect)

# Resortes: uno comprimido, otro extendido
dibujar_resorte_simple(ax, -0.6, -0.35, 0.35, None, 'steelblue')  # comprimido
dibujar_resorte_simple(ax, 0.6, -0.35, 0.65, None, 'steelblue')   # extendido

# Placa rotada
theta_rot = 8 * np.pi / 180  # 8 grados
corners = np.array([[-1.0, 0.5], [1.0, 0.5], [1.0, 0.9], [-1.0, 0.9]])
# Rotar alrededor del centro
centro = np.array([0, 0.7])
rot_matrix = np.array([[np.cos(theta_rot), -np.sin(theta_rot)],
                       [np.sin(theta_rot), np.cos(theta_rot)]])
corners_rot = np.array([rot_matrix @ (c - centro) + centro for c in corners])

losa_rot = Polygon(corners_rot, facecolor='lightsteelblue', edgecolor='navy', linewidth=2)
ax.add_patch(losa_rot)

# Posicion original (linea discontinua)
ax.plot([-1.0, 1.0], [0.5, 0.5], 'k--', lw=1, alpha=0.5)
ax.plot([-1.0, 1.0], [0.9, 0.9], 'k--', lw=1, alpha=0.5)

# Arco de rotacion
theta_arc = np.linspace(-10, 10, 20) * np.pi / 180
r_arc = 0.6
x_arc = r_arc * np.sin(theta_arc)
y_arc = r_arc * np.cos(theta_arc) + 0.7
ax.plot(x_arc, y_arc, 'purple', lw=1.5)
ax.annotate('', xy=(x_arc[-1], y_arc[-1]), xytext=(x_arc[-3], y_arc[-3]),
            arrowprops=dict(arrowstyle='->', color='purple', lw=1.5))
ax.text(0.7, 1.15, r'$\theta$', fontsize=11, color='purple', fontweight='bold')

# Formula
ax.text(0, 2.1, r'$\omega_\theta = \sqrt{\frac{2kb^2}{I}}$', fontsize=10, ha='center',
        bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8, pad=0.3))

plt.tight_layout()
plt.savefig(output_dir / "fig_problema_12_placa_rigida.pdf")
plt.savefig(output_dir / "fig_problema_12_placa_rigida.png")
plt.close()

print(f"Figura guardada en: {output_dir / 'fig_problema_12_placa_rigida.pdf'}")
