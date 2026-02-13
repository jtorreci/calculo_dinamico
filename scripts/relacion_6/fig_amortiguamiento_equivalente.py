"""
Figura: Amortiguamiento viscoso equivalente desde histéresis
Problema 04 - Relación 6
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

# Parámetros
mu = 3.0
Fy = 1.0  # normalizado
uy = 1.0  # normalizado
u_max = mu * uy

# Crear figura
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

# ============================================
# SUBPLOT 1: Lazo histerético y energías
# ============================================
# Lazo elastoplástico
u_lazo = np.array([0, uy, u_max, u_max, u_max - 2*uy, -uy, -u_max, -u_max, -u_max + 2*uy, uy, u_max])
F_lazo = np.array([0, Fy, Fy, Fy, -Fy, -Fy, -Fy, -Fy, Fy, Fy, Fy])

# Simplificar para visualización
u_hist = np.array([uy, u_max, u_max - 2*uy, -uy, -u_max, -u_max + 2*uy, uy])
F_hist = np.array([Fy, Fy, -Fy, -Fy, -Fy, Fy, Fy])

ax1.fill(u_hist, F_hist, alpha=0.3, color='red', label=r'$E_d$ (disipada)')
ax1.plot(u_hist, F_hist, 'r-', linewidth=2)

# Triángulo de energía elástica secante
k_sec = Fy / u_max
u_tri = np.array([0, u_max, 0])
F_tri = np.array([0, Fy, 0])
ax1.fill(u_tri, F_tri, alpha=0.3, color='blue', label=r'$E_s$ (almacenada)')
ax1.plot([0, u_max], [0, k_sec * u_max], 'b--', linewidth=2, label=r'Rigidez secante $k_{sec}$')

ax1.axhline(y=0, color='k', linewidth=0.5)
ax1.axvline(x=0, color='k', linewidth=0.5)

# Fórmula de zeta_eq
Ed = 4 * Fy * (u_max - uy)
Es = 0.5 * k_sec * u_max**2
zeta_eq = Ed / (4 * np.pi * Es)

ax1.text(0, -0.3, f'$\\zeta_{{eq}} = \\frac{{E_d}}{{4\\pi E_s}} = {zeta_eq*100:.1f}$%',
         fontsize=11, ha='center', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

ax1.set_xlabel('Desplazamiento $u/u_y$')
ax1.set_ylabel('Fuerza $F/F_y$')
ax1.set_title(f'Energías en ciclo histerético ($\\mu = {mu:.0f}$)')
ax1.legend(loc='upper left', fontsize=9)
ax1.grid(True, alpha=0.3)
ax1.set_xlim(-4, 4)
ax1.set_ylim(-1.5, 1.5)

# ============================================
# SUBPLOT 2: zeta_eq vs ductilidad
# ============================================
mu_range = np.linspace(1.01, 8, 100)

# Para EPP: Ed = 4*Fy*(u_max - uy), Es = 0.5*k_sec*u_max^2
# k_sec = Fy/u_max = Fy/(mu*uy) = k/mu (si k=Fy/uy)
# zeta_eq = 4*Fy*(mu-1)*uy / (4*pi * 0.5 * (Fy/mu/uy) * (mu*uy)^2)
#         = 4*(mu-1) / (4*pi * 0.5 * mu) = 2*(mu-1)/(pi*mu)

zeta_eq_epp = 2 * (mu_range - 1) / (np.pi * mu_range)

# Fórmula de Jacobsen
zeta_jacobsen = (2/np.pi) * (mu_range - 1) / mu_range

ax2.plot(mu_range, zeta_eq_epp * 100, 'r-', linewidth=2, label='EPP')
ax2.plot(mu_range, zeta_jacobsen * 100, 'b--', linewidth=2, label='Jacobsen')

# Punto del problema
ax2.plot(mu, zeta_eq * 100, 'ko', markersize=10, zorder=5)
ax2.annotate(f'$\\zeta_{{eq}} = {zeta_eq*100:.1f}\\%$', xy=(mu, zeta_eq*100),
             xytext=(mu + 0.5, zeta_eq*100 + 3), fontsize=10)

# Límite asintótico
ax2.axhline(y=2/np.pi * 100, color='gray', linestyle=':', linewidth=1)
ax2.text(7.5, 2/np.pi * 100 + 1, r'$\frac{2}{\pi} \approx 63.7\%$', fontsize=9)

ax2.set_xlabel('Ductilidad $\\mu$')
ax2.set_ylabel('Amortiguamiento equivalente $\\zeta_{eq}$ [%]')
ax2.set_title('Amortiguamiento equivalente vs ductilidad')
ax2.legend(loc='lower right', fontsize=9)
ax2.grid(True, alpha=0.3)
ax2.set_xlim(1, 8)
ax2.set_ylim(0, 50)

plt.tight_layout()

# Guardar figura
output_dir = Path(__file__).parent.parent / 'figs'
output_dir.mkdir(exist_ok=True)
plt.savefig(output_dir / 'fig_amortiguamiento_equivalente.pdf', bbox_inches='tight', dpi=150)
plt.savefig(output_dir / 'fig_amortiguamiento_equivalente.png', bbox_inches='tight', dpi=150)
plt.close()

print("Figura guardada: fig_amortiguamiento_equivalente.pdf/png")
