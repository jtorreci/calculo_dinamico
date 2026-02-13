"""
Figura: Edificio 4 plantas con verificación de derivas
Problema 23 - Relación 5
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
from pathlib import Path

# Configuración
plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 10,
    'text.usetex': False,
    'mathtext.fontset': 'cm',
})

# Parámetros del edificio
n_plantas = 4
h_piso = 3.2  # m
ancho = 4.5   # m
alturas = np.array([h_piso * i for i in range(n_plantas + 1)])

# Desplazamientos y derivas (del problema)
u = np.array([0, 8, 22, 35, 45])  # mm (incluyendo base)
dr = np.array([16, 28, 26, 20])  # mm (deriva de servicio)
dr_lim = 16  # mm

# Escala para desplazamientos visuales
escala = 0.08  # m/mm

# Crear figura
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 6))

# ============================================
# SUBPLOT 1: Edificio deformado
# ============================================
ax1.set_xlim(-3, 10)
ax1.set_ylim(-2, 16)
ax1.set_aspect('equal')
ax1.axis('off')

# Base
ax1.fill([-1.5, ancho + 3, ancho + 3, -1.5], [-1, -1, 0, 0], color='gray', alpha=0.5)
ax1.plot([-1.5, ancho + 3], [0, 0], 'k-', linewidth=2)

# Estructura deformada
for i in range(n_plantas):
    y_inf = alturas[i]
    y_sup = alturas[i+1]
    dx_inf = u[i] * escala
    dx_sup = u[i+1] * escala

    # Posición original (línea punteada)
    ax1.plot([0, 0], [y_inf, y_sup], 'b--', linewidth=0.5, alpha=0.5)
    ax1.plot([ancho, ancho], [y_inf, y_sup], 'b--', linewidth=0.5, alpha=0.5)

    # Columnas deformadas
    ax1.plot([dx_inf, dx_sup], [y_inf, y_sup], 'r-', linewidth=2)
    ax1.plot([ancho + dx_inf, ancho + dx_sup], [y_inf, y_sup], 'r-', linewidth=2)

    # Viga/forjado
    ax1.add_patch(Rectangle((dx_sup - 0.2, y_sup - 0.2), ancho + 0.4, 0.4,
                            facecolor='lightyellow', edgecolor='red', linewidth=1.5))

    # Deriva de entrepiso
    delta = (u[i+1] - u[i]) * escala
    ax1.annotate('', xy=(ancho + dx_sup + 0.5, y_sup),
                xytext=(ancho + dx_inf + 0.5, y_inf),
                arrowprops=dict(arrowstyle='<->', color='green', lw=1.5))

    # Etiqueta de deriva
    color = 'red' if dr[i] > dr_lim else 'green'
    ax1.text(ancho + max(dx_inf, dx_sup) + 1.2, (y_inf + y_sup)/2,
            f'$\\Delta_{i+1}={dr[i]}$ mm', fontsize=9, va='center', color=color)

# Desplazamientos absolutos
for i, (h, desp) in enumerate(zip(alturas[1:], u[1:]), 1):
    dx = desp * escala
    ax1.text(-1.5, h, f'$u_{i}={desp}$ mm', fontsize=9, va='center', ha='right')

# Título
ax1.set_title('Deformada y derivas de entrepiso', fontsize=12, fontweight='bold')

# Leyenda
ax1.plot([], [], 'r-', linewidth=2, label='Deformada')
ax1.plot([], [], 'b--', linewidth=1, label='Posición original')
ax1.legend(loc='upper left', fontsize=9)

# ============================================
# SUBPLOT 2: Gráfico de barras de derivas
# ============================================
plantas = np.arange(1, n_plantas + 1)
colores = ['green' if d <= dr_lim else 'red' for d in dr]

bars = ax2.barh(plantas, dr, color=colores, alpha=0.7, edgecolor='black', height=0.6)

# Línea de límite
ax2.axvline(x=dr_lim, color='darkred', linestyle='--', linewidth=2, label=f'Límite = {dr_lim} mm')

# Valores en las barras
for i, (bar, d) in enumerate(zip(bars, dr)):
    width = bar.get_width()
    estado = "OK" if d <= dr_lim else "NO CUMPLE"
    ax2.text(width + 1, bar.get_y() + bar.get_height()/2,
            f'{d} mm ({estado})', va='center', fontsize=9,
            color='green' if d <= dr_lim else 'red')

# Drift ratio
ax2_twin = ax2.twiny()
drift_lim = 100 * dr_lim / (h_piso * 1000)
ax2_twin.set_xlim(0, ax2.get_xlim()[1] / (h_piso * 1000) * 100)
ax2_twin.set_xlabel('Drift ratio [%]', fontsize=10)
ax2_twin.axvline(x=drift_lim, color='darkred', linestyle='--', linewidth=1, alpha=0.5)

ax2.set_xlabel('Deriva $d_r$ [mm]', fontsize=11)
ax2.set_ylabel('Planta', fontsize=11)
ax2.set_yticks(plantas)
ax2.set_title('Verificación de derivas (ELS)', fontsize=12, fontweight='bold')
ax2.legend(loc='lower right', fontsize=9)
ax2.grid(True, alpha=0.3, axis='x')
ax2.set_xlim(0, 35)

plt.tight_layout()

# Guardar figura
output_dir = Path(__file__).parent.parent / 'figs'
output_dir.mkdir(exist_ok=True)
plt.savefig(output_dir / 'fig_edificio_4plantas_derivas.pdf', bbox_inches='tight', dpi=150)
plt.savefig(output_dir / 'fig_edificio_4plantas_derivas.png', bbox_inches='tight', dpi=150)
plt.close()

print("Figura guardada: fig_edificio_4plantas_derivas.pdf/png")
