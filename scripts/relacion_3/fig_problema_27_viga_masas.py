"""
Figura para Problema 27 - Relacion 3
Viga con masas puntuales (3DOF): formas modales
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, Polygon
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

def dibujar_apoyo_simple(ax, x, y, size=0.15):
    """Dibuja apoyo simple (triangulo)"""
    triangle = Polygon([(x, y), (x-size, y-size*1.2), (x+size, y-size*1.2)],
                       facecolor='gray', edgecolor='black', lw=1)
    ax.add_patch(triangle)
    # Linea base
    ax.plot([x-size*1.2, x+size*1.2], [y-size*1.2, y-size*1.2], 'k-', lw=2)

def dibujar_masa(ax, x, y, label='m', size=0.4, color='steelblue'):
    """Dibuja masa puntual como circulo"""
    circle = Circle((x, y), size/2, facecolor=color, edgecolor='navy', lw=1.5)
    ax.add_patch(circle)
    ax.text(x, y, label, ha='center', va='center', fontsize=9, fontweight='bold', color='white')

# --- Datos del problema ---
L = 12.0  # Longitud total
x_masas = np.array([L/4, L/2, 3*L/4])  # Posiciones de masas

# Formas modales (normalizadas al maximo)
phi1 = np.array([0.707, 1.0, 0.707])  # Modo 1: simetrico
phi2 = np.array([1.0, 0.0, -1.0])     # Modo 2: antisimetrico
phi3 = np.array([0.707, -1.0, 0.707]) # Modo 3: simetrico con 2 nodos

# Frecuencias
f = [2.45, 5.30, 8.22]  # Hz

# --- Crear figura ---
fig, axes = plt.subplots(2, 2, figsize=(10, 6))

# ======================
# Panel (a): Sistema fisico
# ======================
ax = axes[0, 0]
ax.set_xlim(-1, 14)
ax.set_ylim(-2, 3)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title('(a) Sistema: viga biapoyada con 3 masas puntuales', fontweight='bold', fontsize=10)

# Apoyos
dibujar_apoyo_simple(ax, 0, 0)
dibujar_apoyo_simple(ax, L, 0)

# Viga
ax.plot([0, L], [0, 0], 'b-', lw=4)

# Masas
for i, x in enumerate(x_masas):
    dibujar_masa(ax, x, 0.5, f'$m_{i+1}$', 0.6)
    # Linea vertical a la viga
    ax.plot([x, x], [0, 0.2], 'k-', lw=1.5)

# Cotas
ax.annotate('', xy=(0, -1.2), xytext=(L, -1.2),
            arrowprops=dict(arrowstyle='<->', color='green', lw=1.5))
ax.text(L/2, -1.5, f'$L = {L:.0f}$ m', ha='center', fontsize=10, color='green')

# Posiciones de masas
for i, x in enumerate(x_masas):
    ax.text(x, -0.6, f'$x_{i+1}$', ha='center', fontsize=9, color='darkblue')

# Propiedades
ax.text(6, 2.2, '$EI = 200$ MN$\\cdot$m$^2$', ha='center', fontsize=9,
        bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8, pad=0.3))

# ======================
# Panel (b): Modo 1
# ======================
ax = axes[0, 1]
ax.set_xlim(-1, 14)
ax.set_ylim(-2.5, 2.5)
ax.axis('off')
ax.set_title(f'(b) Modo 1: $f_1 = {f[0]:.2f}$ Hz (simetrico)', fontweight='bold', fontsize=10)

# Eje de referencia
ax.plot([0, L], [0, 0], 'k--', lw=1, alpha=0.3)

# Apoyos
dibujar_apoyo_simple(ax, 0, 0, 0.12)
dibujar_apoyo_simple(ax, L, 0, 0.12)

# Forma modal como curva suave
x_plot = np.linspace(0, L, 100)
# Interpolacion sinusoidal
y_modo = np.sin(np.pi * x_plot / L) * 1.5

ax.fill_between(x_plot, 0, y_modo, alpha=0.3, color='green')
ax.plot(x_plot, y_modo, 'g-', lw=2)

# Desplazamientos en puntos de masa
escala = 1.5
for i, x in enumerate(x_masas):
    y = phi1[i] * escala
    ax.plot([x, x], [0, y], 'r-', lw=2)
    ax.plot(x, y, 'ro', markersize=10)
    ax.text(x+0.3, y, f'{phi1[i]:.2f}', fontsize=8, va='center')

# Formula
ax.text(L/2, -2, r'$\phi^{(1)} = [0.71, 1.00, 0.71]^T$', ha='center', fontsize=9,
        bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7, pad=0.3))

# ======================
# Panel (c): Modo 2
# ======================
ax = axes[1, 0]
ax.set_xlim(-1, 14)
ax.set_ylim(-2.5, 2.5)
ax.axis('off')
ax.set_title(f'(c) Modo 2: $f_2 = {f[1]:.2f}$ Hz (antisimetrico)', fontweight='bold', fontsize=10)

# Eje de referencia
ax.plot([0, L], [0, 0], 'k--', lw=1, alpha=0.3)

# Apoyos
dibujar_apoyo_simple(ax, 0, 0, 0.12)
dibujar_apoyo_simple(ax, L, 0, 0.12)

# Forma modal
x_plot = np.linspace(0, L, 100)
y_modo = np.sin(2 * np.pi * x_plot / L) * 1.5

ax.fill_between(x_plot, 0, y_modo, where=y_modo>=0, alpha=0.3, color='orange')
ax.fill_between(x_plot, 0, y_modo, where=y_modo<0, alpha=0.3, color='orange')
ax.plot(x_plot, y_modo, color='darkorange', lw=2)

# Desplazamientos en puntos de masa
escala = 1.5
for i, x in enumerate(x_masas):
    y = phi2[i] * escala
    ax.plot([x, x], [0, y], 'r-', lw=2)
    ax.plot(x, y, 'ro', markersize=10)
    ax.text(x+0.3, y if abs(y) > 0.1 else 0.3, f'{phi2[i]:.2f}', fontsize=8, va='center')

# Nodo en el centro
ax.plot(L/2, 0, 'ko', markersize=8, zorder=5)
ax.text(L/2, -0.5, 'nodo', fontsize=8, ha='center', style='italic')

# Formula
ax.text(L/2, -2, r'$\phi^{(2)} = [1.00, 0.00, -1.00]^T$', ha='center', fontsize=9,
        bbox=dict(boxstyle='round', facecolor='navajowhite', alpha=0.7, pad=0.3))

# ======================
# Panel (d): Modo 3
# ======================
ax = axes[1, 1]
ax.set_xlim(-1, 14)
ax.set_ylim(-2.5, 2.5)
ax.axis('off')
ax.set_title(f'(d) Modo 3: $f_3 = {f[2]:.2f}$ Hz (simetrico, 2 nodos)', fontweight='bold', fontsize=10)

# Eje de referencia
ax.plot([0, L], [0, 0], 'k--', lw=1, alpha=0.3)

# Apoyos
dibujar_apoyo_simple(ax, 0, 0, 0.12)
dibujar_apoyo_simple(ax, L, 0, 0.12)

# Forma modal
x_plot = np.linspace(0, L, 100)
y_modo = np.sin(3 * np.pi * x_plot / L) * 1.2

ax.fill_between(x_plot, 0, y_modo, where=y_modo>=0, alpha=0.3, color='purple')
ax.fill_between(x_plot, 0, y_modo, where=y_modo<0, alpha=0.3, color='purple')
ax.plot(x_plot, y_modo, color='purple', lw=2)

# Desplazamientos en puntos de masa
escala = 1.2
for i, x in enumerate(x_masas):
    y = phi3[i] * escala
    ax.plot([x, x], [0, y], 'r-', lw=2)
    ax.plot(x, y, 'ro', markersize=10)
    ax.text(x+0.3, y, f'{phi3[i]:.2f}', fontsize=8, va='center')

# Nodos
for x_nodo in [L/3, 2*L/3]:
    ax.plot(x_nodo, 0, 'ko', markersize=6, zorder=5)

# Formula
ax.text(L/2, -2, r'$\phi^{(3)} = [0.71, -1.00, 0.71]^T$', ha='center', fontsize=9,
        bbox=dict(boxstyle='round', facecolor='thistle', alpha=0.7, pad=0.3))

plt.tight_layout()
plt.savefig(output_dir / "fig_problema_27_viga_masas.pdf")
plt.savefig(output_dir / "fig_problema_27_viga_masas.png")
plt.close()

print(f"Figura guardada en: {output_dir / 'fig_problema_27_viga_masas.pdf'}")
