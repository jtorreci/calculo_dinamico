"""
Figura: Análisis pushover y formato ADRS
Problema 07 - Relación 6
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
M_star = 450e3  # kg
Vy = 900e3      # N
dy = 0.050      # m
du = 0.200      # m
Gamma = 1.35

# Conversión a ADRS
Say = Vy / (Gamma * M_star)
Sdy = dy / Gamma
Sdu = du / Gamma

# Crear figura
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

# ============================================
# SUBPLOT 1: Curva de capacidad (V-d)
# ============================================
d = np.array([0, dy, du]) * 1000  # mm
V = np.array([0, Vy, Vy]) / 1000  # kN

ax1.plot(d, V, 'b-', linewidth=2.5, label='Curva de capacidad')
ax1.fill_between(d, 0, V, alpha=0.2, color='blue')

# Puntos clave
ax1.plot(dy*1000, Vy/1000, 'ro', markersize=10, label='Punto de fluencia')
ax1.plot(du*1000, Vy/1000, 'gs', markersize=10, label='Capacidad última')

# Anotaciones
ax1.annotate(f'$(d_y, V_y) = ({dy*1000:.0f}, {Vy/1000:.0f})$',
             xy=(dy*1000, Vy/1000), xytext=(dy*1000 + 30, Vy/1000 - 150),
             fontsize=9, arrowprops=dict(arrowstyle='->', color='gray'))
ax1.annotate(f'$(d_u, V_y) = ({du*1000:.0f}, {Vy/1000:.0f})$',
             xy=(du*1000, Vy/1000), xytext=(du*1000 - 50, Vy/1000 + 100),
             fontsize=9)

# Ductilidad
mu = du / dy
ax1.text(120, 400, f'$\\mu = d_u/d_y = {mu:.1f}$', fontsize=11,
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

ax1.set_xlabel('Desplazamiento en azotea $d$ [mm]')
ax1.set_ylabel('Cortante en base $V$ [kN]')
ax1.set_title('Curva de capacidad (Pushover)')
ax1.legend(loc='lower right', fontsize=9)
ax1.grid(True, alpha=0.3)
ax1.set_xlim(0, 250)
ax1.set_ylim(0, 1200)

# ============================================
# SUBPLOT 2: Formato ADRS (Sa-Sd)
# ============================================
Sd = np.array([0, Sdy, Sdu]) * 1000  # mm
Sa = np.array([0, Say, Say])  # m/s²

ax2.plot(Sd, Sa, 'b-', linewidth=2.5, label='Curva de capacidad ADRS')

# Espectro de demanda (ejemplo)
T_range = np.linspace(0.1, 4, 100)
ag = 0.25 * 9.81  # 0.25g en m/s²
TC = 0.5

# Espectro simplificado
Sa_demand = np.where(T_range < TC, 2.5 * ag, 2.5 * ag * TC / T_range)
Sd_demand = Sa_demand * (T_range / (2*np.pi))**2 * 1000  # en mm

ax2.plot(Sd_demand, Sa_demand, 'r--', linewidth=2, label='Espectro de demanda')

# Punto de fluencia y último
ax2.plot(Sdy*1000, Say, 'ro', markersize=10)
ax2.plot(Sdu*1000, Say, 'gs', markersize=10)

# Punto de desempeño (intersección aproximada)
Sd_perf = 120  # mm (del problema)
ax2.plot(Sd_perf, Say, 'ko', markersize=12, zorder=5, label='Punto de desempeño')
ax2.axvline(x=Sd_perf, color='gray', linestyle=':', linewidth=1)

# Anotaciones
ax2.annotate(f'$S_{{dy}} = {Sdy*1000:.0f}$ mm', xy=(Sdy*1000, Say),
             xytext=(Sdy*1000 - 10, Say + 0.3), fontsize=9)
ax2.annotate(f'$S_{{du}} = {Sdu*1000:.0f}$ mm', xy=(Sdu*1000, Say),
             xytext=(Sdu*1000 - 10, Say + 0.3), fontsize=9)

# Período efectivo
omega = np.sqrt(Say / Sdy)
T_eff = 2*np.pi / omega
ax2.text(100, 0.5, f'$T_{{eff}} = {T_eff:.2f}$ s', fontsize=10,
         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

ax2.set_xlabel('Desplazamiento espectral $S_d$ [mm]')
ax2.set_ylabel('Aceleración espectral $S_a$ [m/s²]')
ax2.set_title('Formato ADRS (Acceleration-Displacement Response Spectrum)')
ax2.legend(loc='upper right', fontsize=8)
ax2.grid(True, alpha=0.3)
ax2.set_xlim(0, 200)
ax2.set_ylim(0, 3)

plt.tight_layout()

# Guardar figura
output_dir = Path(__file__).parent.parent / 'figs'
output_dir.mkdir(exist_ok=True)
plt.savefig(output_dir / 'fig_pushover_ADRS.pdf', bbox_inches='tight', dpi=150)
plt.savefig(output_dir / 'fig_pushover_ADRS.png', bbox_inches='tight', dpi=150)
plt.close()

print("Figura guardada: fig_pushover_ADRS.pdf/png")
