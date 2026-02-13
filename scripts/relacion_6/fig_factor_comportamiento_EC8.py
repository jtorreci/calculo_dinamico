"""
Figura: Factor de comportamiento según EC8
Problema 05 - Relación 6
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
})

# Crear figura
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

# ============================================
# SUBPLOT 1: Espectros reducidos por q
# ============================================
T = np.linspace(0.01, 4, 200)
ag = 0.3  # g
S = 1.0
TB, TC, TD = 0.15, 0.5, 2.0

# Espectro elástico EC8 (simplificado)
Se = np.zeros_like(T)
for i, Ti in enumerate(T):
    if Ti < TB:
        Se[i] = ag * S * (1 + Ti/TB * (2.5 - 1))
    elif Ti < TC:
        Se[i] = ag * S * 2.5
    elif Ti < TD:
        Se[i] = ag * S * 2.5 * TC / Ti
    else:
        Se[i] = ag * S * 2.5 * TC * TD / Ti**2

# Factores q
q_DCH = 5.85
q_DCM = 3.9
q_DCL = 1.5

ax1.plot(T, Se, 'k-', linewidth=2.5, label='Elástico')
ax1.plot(T, Se/q_DCL, 'g--', linewidth=2, label=f'DCL ($q = {q_DCL}$)')
ax1.plot(T, Se/q_DCM, 'b-.', linewidth=2, label=f'DCM ($q = {q_DCM}$)')
ax1.plot(T, Se/q_DCH, 'r:', linewidth=2, label=f'DCH ($q = {q_DCH}$)')

# Período del problema
T1 = 0.9
ax1.axvline(x=T1, color='gray', linestyle=':', linewidth=1)
ax1.text(T1 + 0.05, 0.7, f'$T_1 = {T1}$ s', fontsize=9)

ax1.set_xlabel('Período $T$ [s]')
ax1.set_ylabel('Aceleración espectral $S_a$ [g]')
ax1.set_title('Espectros de diseño EC8')
ax1.legend(loc='upper right', fontsize=8)
ax1.grid(True, alpha=0.3)
ax1.set_xlim(0, 4)
ax1.set_ylim(0, 0.8)

# ============================================
# SUBPLOT 2: Comparación de clases
# ============================================
clases = ['DCL', 'DCM', 'DCH']
q_vals = [q_DCL, q_DCM, q_DCH]
colores = ['green', 'blue', 'red']

# Barras de factor q
x = np.arange(len(clases))
width = 0.35

bars = ax2.bar(x, q_vals, width, color=colores, alpha=0.7, edgecolor='black')

# Añadir valores
for bar, q in zip(bars, q_vals):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
             f'$q = {q}$', ha='center', fontsize=10, fontweight='bold')

# Reducción de fuerzas
ax2_twin = ax2.twinx()
reducciones = [(1 - 1/q) * 100 for q in q_vals]
ax2_twin.plot(x, reducciones, 'ko-', markersize=10, linewidth=2, label='Reducción')

for i, red in enumerate(reducciones):
    ax2_twin.text(i, red + 2, f'{red:.0f}%', ha='center', fontsize=9)

ax2.set_xticks(x)
ax2.set_xticklabels(clases)
ax2.set_ylabel('Factor de comportamiento $q$')
ax2_twin.set_ylabel('Reducción de fuerzas [%]')
ax2.set_title('Clases de ductilidad EC8')
ax2.set_ylim(0, 8)
ax2_twin.set_ylim(0, 100)
ax2.grid(True, alpha=0.3, axis='y')

plt.tight_layout()

# Guardar figura
output_dir = Path(__file__).parent.parent / 'figs'
output_dir.mkdir(exist_ok=True)
plt.savefig(output_dir / 'fig_factor_comportamiento_EC8.pdf', bbox_inches='tight', dpi=150)
plt.savefig(output_dir / 'fig_factor_comportamiento_EC8.png', bbox_inches='tight', dpi=150)
plt.close()

print("Figura guardada: fig_factor_comportamiento_EC8.pdf/png")
