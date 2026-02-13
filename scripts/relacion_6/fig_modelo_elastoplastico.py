"""
Figura: Modelo elastoplástico perfecto (EPP)
Problema 01 - Relación 6
"""
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Configuración para LaTeX
plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 10,
    'text.usetex': False,
    'mathtext.fontset': 'cm',
    'axes.labelsize': 11,
    'axes.titlesize': 11,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
})

# Parámetros del problema
k = 200  # kN/m
Fy = 40  # kN
uy = Fy / k  # m = 0.2 m
u_max = 0.4  # m

# Crear figura con dos subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

# ============================================
# SUBPLOT 1: Modelo constitutivo EPP
# ============================================
u_range = np.linspace(-0.5, 0.5, 100)

# Rama de carga monotónica
u_mono = np.array([0, uy, u_max])
F_mono = np.array([0, Fy, Fy])

# Ciclo de histéresis completo
u_ciclo = np.array([0, uy, u_max, u_max - 2*uy, -u_max, -u_max + 2*uy, uy, u_max])
F_ciclo = np.array([0, Fy, Fy, -Fy, -Fy, Fy, Fy, Fy])

# Simplificar: ciclo desde u_max
u_hist = [u_max, u_max - 2*uy, -uy, -u_max, -u_max + 2*uy, uy, u_max]
F_hist = [Fy, -Fy, -Fy, -Fy, Fy, Fy, Fy]

ax1.plot(u_mono * 1000, F_mono, 'b-', linewidth=2, label='Carga monotónica')
ax1.plot(np.array(u_hist) * 1000, F_hist, 'r--', linewidth=1.5, label='Ciclo histerético')

# Anotaciones
ax1.annotate(r'$(u_y, F_y)$', xy=(uy*1000, Fy), xytext=(uy*1000 + 50, Fy + 5),
             fontsize=9, arrowprops=dict(arrowstyle='->', color='gray'))
ax1.annotate(r'$(u_{max}, F_y)$', xy=(u_max*1000, Fy), xytext=(u_max*1000 - 30, Fy + 8),
             fontsize=9)

# Indicar pendiente k
ax1.annotate('', xy=(100, 20), xytext=(50, 0),
             arrowprops=dict(arrowstyle='->', color='green', lw=1.5))
ax1.text(40, 12, r'$k$', fontsize=10, color='green')

ax1.axhline(y=0, color='k', linewidth=0.5)
ax1.axvline(x=0, color='k', linewidth=0.5)
ax1.axhline(y=Fy, color='gray', linewidth=0.5, linestyle=':')
ax1.axhline(y=-Fy, color='gray', linewidth=0.5, linestyle=':')

ax1.set_xlabel('Desplazamiento $u$ [mm]')
ax1.set_ylabel('Fuerza $F$ [kN]')
ax1.set_title('Modelo Elastoplástico Perfecto (EPP)')
ax1.legend(loc='lower right', fontsize=8)
ax1.grid(True, alpha=0.3)
ax1.set_xlim(-500, 500)
ax1.set_ylim(-60, 60)

# ============================================
# SUBPLOT 2: Energía disipada (área del lazo)
# ============================================
# Lazo de histéresis simplificado para mostrar área
u_lazo = np.array([uy, u_max, u_max, uy, -uy, -u_max, -u_max, -uy, uy]) * 1000
F_lazo = np.array([Fy, Fy, -Fy, -Fy, -Fy, -Fy, Fy, Fy, Fy])

# Dibujar y rellenar
ax2.fill(u_lazo, F_lazo, alpha=0.3, color='red', label=r'$E_d$ = Área del lazo')
ax2.plot(u_lazo, F_lazo, 'r-', linewidth=2)

# Rama elástica
ax2.plot([0, uy*1000], [0, Fy], 'b-', linewidth=2, label='Rama elástica')
ax2.plot([0, -uy*1000], [0, -Fy], 'b-', linewidth=2)

# Anotaciones de energía
Ed = 4 * Fy * (u_max - uy)  # kJ
ax2.text(0, 0, f'$E_d = {Ed:.0f}$ kJ', fontsize=10, ha='center', va='center',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

ax2.axhline(y=0, color='k', linewidth=0.5)
ax2.axvline(x=0, color='k', linewidth=0.5)

ax2.set_xlabel('Desplazamiento $u$ [mm]')
ax2.set_ylabel('Fuerza $F$ [kN]')
ax2.set_title('Energía disipada por histéresis')
ax2.legend(loc='lower right', fontsize=8)
ax2.grid(True, alpha=0.3)
ax2.set_xlim(-500, 500)
ax2.set_ylim(-60, 60)

plt.tight_layout()

# Guardar figura
output_dir = Path(__file__).parent.parent / 'figs'
output_dir.mkdir(exist_ok=True)
plt.savefig(output_dir / 'fig_modelo_elastoplastico.pdf', bbox_inches='tight', dpi=150)
plt.savefig(output_dir / 'fig_modelo_elastoplastico.png', bbox_inches='tight', dpi=150)
plt.close()

print("Figura guardada: fig_modelo_elastoplastico.pdf/png")
