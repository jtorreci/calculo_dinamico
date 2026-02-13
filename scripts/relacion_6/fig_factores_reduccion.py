"""
Figura: Factores de reducción R_mu vs ductilidad
Problema 03 - Relación 6
Compara reglas de igual desplazamiento e igual energía
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

# Rango de ductilidades
mu = np.linspace(1, 8, 100)

# Factores de reducción
R_igual_desp = mu  # R = μ (igual desplazamiento, T > Tc)
R_igual_energia = np.sqrt(2 * mu - 1)  # R = sqrt(2μ-1) (igual energía, T < Tc)

# Crear figura
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

# ============================================
# SUBPLOT 1: Factores R vs μ
# ============================================
ax1.plot(mu, R_igual_desp, 'b-', linewidth=2, label=r'Igual desplazamiento: $R_\mu = \mu$')
ax1.plot(mu, R_igual_energia, 'r--', linewidth=2, label=r'Igual energía: $R_\mu = \sqrt{2\mu-1}$')

# Punto del problema (μ = 4)
mu_prob = 4
R_desp = mu_prob
R_ener = np.sqrt(2*mu_prob - 1)

ax1.plot(mu_prob, R_desp, 'bo', markersize=10, zorder=5)
ax1.plot(mu_prob, R_ener, 'rs', markersize=10, zorder=5)

ax1.annotate(f'$R_\\mu = {R_desp:.1f}$', xy=(mu_prob, R_desp),
             xytext=(mu_prob + 0.5, R_desp + 0.5), fontsize=9)
ax1.annotate(f'$R_\\mu = {R_ener:.2f}$', xy=(mu_prob, R_ener),
             xytext=(mu_prob + 0.5, R_ener - 0.8), fontsize=9)

ax1.axvline(x=mu_prob, color='gray', linestyle=':', linewidth=1)

ax1.set_xlabel('Ductilidad $\\mu$')
ax1.set_ylabel('Factor de reducción $R_\\mu$')
ax1.set_title('Comparación de reglas de ductilidad')
ax1.legend(loc='upper left', fontsize=9)
ax1.grid(True, alpha=0.3)
ax1.set_xlim(1, 8)
ax1.set_ylim(1, 8)

# ============================================
# SUBPLOT 2: Ilustración gráfica de las reglas
# ============================================
# Desplazamiento normalizado
u_norm = np.linspace(0, 2, 100)

# Sistema elástico
F_el = u_norm * 4  # pendiente arbitraria alta

# Sistema elastoplástico (fluencia en u=1)
F_ep = np.where(u_norm <= 1, u_norm, 1.0)

# Áreas
ax2.fill_between(u_norm[u_norm <= 1], 0, u_norm[u_norm <= 1], alpha=0.3, color='blue', label='Energía elástica')
ax2.fill_between(u_norm, 0, np.minimum(F_ep, 1), alpha=0.3, color='red', label='Energía EP')

ax2.plot(u_norm, F_ep, 'r-', linewidth=2.5, label='Elastoplástico')
ax2.plot([0, 1], [0, 1], 'b--', linewidth=2, label='Elástico equiv.')

# Línea de fluencia
ax2.axhline(y=1, color='gray', linestyle=':', linewidth=1)
ax2.text(1.8, 1.05, r'$F_y$', fontsize=10)

# Puntos
ax2.plot(1, 1, 'ko', markersize=8)
ax2.plot(2, 1, 'ro', markersize=8)

# Anotaciones
ax2.annotate(r'$u_y$', xy=(1, 0), xytext=(1, -0.15), fontsize=10, ha='center')
ax2.annotate(r'$u_{max} = \mu \cdot u_y$', xy=(2, 0), xytext=(2, -0.15), fontsize=10, ha='center')

ax2.set_xlabel('Desplazamiento normalizado $u/u_y$')
ax2.set_ylabel('Fuerza normalizada $F/F_y$')
ax2.set_title('Principio de igual energía')
ax2.legend(loc='upper right', fontsize=8)
ax2.grid(True, alpha=0.3)
ax2.set_xlim(0, 2.5)
ax2.set_ylim(0, 1.5)

plt.tight_layout()

# Guardar figura
output_dir = Path(__file__).parent.parent / 'figs'
output_dir.mkdir(exist_ok=True)
plt.savefig(output_dir / 'fig_factores_reduccion.pdf', bbox_inches='tight', dpi=150)
plt.savefig(output_dir / 'fig_factores_reduccion.png', bbox_inches='tight', dpi=150)
plt.close()

print("Figura guardada: fig_factores_reduccion.pdf/png")
