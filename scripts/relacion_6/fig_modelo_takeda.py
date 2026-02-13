"""
Figura: Modelo de degradación Takeda
Problema 06 - Relación 6
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

# Parámetros del problema
k0 = 20  # MN/m (normalizado a 1)
Fy = 200  # kN (normalizado a 1)
uy = Fy / k0 / 1000  # m -> normalizado a 1
alpha = 0.4  # exponente Takeda

# Crear figura
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

# ============================================
# SUBPLOT 1: Modelo Takeda - ciclos con degradación
# ============================================
# Normalizar
uy_n = 1.0
Fy_n = 1.0
k0_n = 1.0

# Diferentes amplitudes de ciclo
amplitudes = [2, 3, 4]  # en términos de uy
colores = ['blue', 'green', 'red']

for amp, color in zip(amplitudes, colores):
    u_max = amp * uy_n
    mu = amp

    # Rigidez de descarga Takeda
    ku = k0_n * mu**(-alpha)

    # Puntos del ciclo Takeda simplificado
    # Carga: rama elástica hasta fluencia, luego plástico
    # Descarga: con rigidez ku

    # Punto de fluencia
    u1, F1 = uy_n, Fy_n
    # Punto máximo
    u2, F2 = u_max, Fy_n
    # Descarga con ku hasta F=0
    u3 = u2 - F2/ku
    F3 = 0
    # Continúa con ku hasta -Fy
    u4 = u3 - Fy_n/ku
    F4 = -Fy_n
    # Rama plástica negativa
    u5 = -u_max
    F5 = -Fy_n
    # Recarga con ku
    u6 = u5 + Fy_n/ku
    F6 = 0
    u7 = u6 + Fy_n/ku
    F7 = Fy_n

    u_ciclo = [0, u1, u2, u3, u4, u5, u6, u7, u2]
    F_ciclo = [0, F1, F2, F3, F4, F5, F6, F7, F2]

    ax1.plot(u_ciclo, F_ciclo, color=color, linewidth=1.5,
             label=f'$\\mu = {mu}$, $k_u/k_0 = {ku:.2f}$')

# Rama elástica inicial
ax1.plot([0, uy_n], [0, Fy_n], 'k-', linewidth=2.5, label='Elástico inicial')
ax1.plot([0, -uy_n], [0, -Fy_n], 'k-', linewidth=2.5)

ax1.axhline(y=0, color='k', linewidth=0.5)
ax1.axvline(x=0, color='k', linewidth=0.5)
ax1.axhline(y=Fy_n, color='gray', linestyle=':', linewidth=0.5)
ax1.axhline(y=-Fy_n, color='gray', linestyle=':', linewidth=0.5)

ax1.set_xlabel('Desplazamiento $u/u_y$')
ax1.set_ylabel('Fuerza $F/F_y$')
ax1.set_title(f'Modelo Takeda ($\\alpha = {alpha}$)')
ax1.legend(loc='lower right', fontsize=8)
ax1.grid(True, alpha=0.3)
ax1.set_xlim(-5, 5)
ax1.set_ylim(-1.5, 1.5)

# ============================================
# SUBPLOT 2: Degradación de rigidez vs ductilidad
# ============================================
mu_range = np.linspace(1, 8, 100)

# Diferentes valores de alpha
alphas = [0.0, 0.3, 0.4, 0.5, 0.6]
estilos = ['-', '--', '-', '-.', ':']
colores2 = ['gray', 'blue', 'red', 'green', 'orange']

for a, estilo, color in zip(alphas, estilos, colores2):
    ku_k0 = mu_range**(-a)
    lw = 2.5 if a == 0.4 else 1.5
    ax2.plot(mu_range, ku_k0, linestyle=estilo, color=color, linewidth=lw,
             label=f'$\\alpha = {a}$')

# Punto del problema (mu=4, alpha=0.4)
mu_prob = 4
ku_prob = mu_prob**(-0.4)
ax2.plot(mu_prob, ku_prob, 'ro', markersize=10, zorder=5)
ax2.annotate(f'$k_u/k_0 = {ku_prob:.2f}$', xy=(mu_prob, ku_prob),
             xytext=(mu_prob + 0.5, ku_prob + 0.1), fontsize=10)

# Degradación
degradacion = (1 - ku_prob) * 100
ax2.text(6, 0.3, f'Degradación = {degradacion:.0f}%', fontsize=10,
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

ax2.set_xlabel('Ductilidad $\\mu$')
ax2.set_ylabel('Rigidez de descarga $k_u/k_0$')
ax2.set_title('Degradación de rigidez Takeda')
ax2.legend(loc='upper right', fontsize=8)
ax2.grid(True, alpha=0.3)
ax2.set_xlim(1, 8)
ax2.set_ylim(0, 1.1)

plt.tight_layout()

# Guardar figura
output_dir = Path(__file__).parent.parent / 'figs'
output_dir.mkdir(exist_ok=True)
plt.savefig(output_dir / 'fig_modelo_takeda.pdf', bbox_inches='tight', dpi=150)
plt.savefig(output_dir / 'fig_modelo_takeda.png', bbox_inches='tight', dpi=150)
plt.close()

print("Figura guardada: fig_modelo_takeda.pdf/png")
