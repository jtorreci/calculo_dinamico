"""
Figura: Modelo bilineal con endurecimiento
Problema 02 - Relación 6
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
k = 500  # kN/m
alpha = 0.05  # ratio post-fluencia
Fy = 100  # kN
uy = Fy / k  # m = 0.2 m
u_max = 0.5  # m

k2 = alpha * k  # rigidez post-fluencia

# Fuerza máxima
F_max = Fy + k2 * (u_max - uy)

# Crear figura con dos subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

# ============================================
# SUBPLOT 1: Comparación EPP vs Bilineal
# ============================================
u = np.linspace(0, 0.6, 100)

# EPP
F_epp = np.where(u <= uy, k * u, Fy)

# Bilineal
F_bil = np.where(u <= uy, k * u, Fy + k2 * (u - uy))

ax1.plot(u * 1000, F_epp, 'b--', linewidth=2, label='EPP ($\\alpha = 0$)')
ax1.plot(u * 1000, F_bil, 'r-', linewidth=2, label=f'Bilineal ($\\alpha = {alpha}$)')

# Puntos clave
ax1.plot(uy * 1000, Fy, 'ko', markersize=8)
ax1.plot(u_max * 1000, F_max, 'ro', markersize=8)
ax1.plot(u_max * 1000, Fy, 'bo', markersize=6)

# Anotaciones
ax1.annotate(r'$(u_y, F_y)$', xy=(uy*1000, Fy), xytext=(uy*1000 + 80, Fy - 15),
             fontsize=9, arrowprops=dict(arrowstyle='->', color='gray'))
ax1.annotate(f'$F_{{max}} = {F_max:.0f}$ kN', xy=(u_max*1000, F_max),
             xytext=(u_max*1000 - 150, F_max + 10), fontsize=9)

# Indicar pendientes
ax1.annotate('', xy=(150, 75), xytext=(80, 40),
             arrowprops=dict(arrowstyle='->', color='green', lw=1.5))
ax1.text(70, 60, r'$k$', fontsize=10, color='green')

ax1.annotate('', xy=(450, 115), xytext=(350, 105),
             arrowprops=dict(arrowstyle='->', color='orange', lw=1.5))
ax1.text(380, 115, r'$\alpha k$', fontsize=10, color='orange')

ax1.axhline(y=0, color='k', linewidth=0.5)
ax1.axvline(x=0, color='k', linewidth=0.5)

ax1.set_xlabel('Desplazamiento $u$ [mm]')
ax1.set_ylabel('Fuerza $F$ [kN]')
ax1.set_title('Modelo Bilineal con Endurecimiento')
ax1.legend(loc='lower right', fontsize=9)
ax1.grid(True, alpha=0.3)
ax1.set_xlim(0, 600)
ax1.set_ylim(0, 140)

# ============================================
# SUBPLOT 2: Ciclo histerético bilineal
# ============================================
# Puntos del ciclo
u_ciclo = np.array([0, uy, u_max, u_max - 2*uy, -(u_max - 2*uy) - 2*uy, -u_max,
                    -u_max + 2*uy, u_max - 2*uy + 2*uy, u_max]) * 1000

# Simplificar ciclo
u1 = [0, uy*1000, u_max*1000]
F1 = [0, Fy, F_max]

# Descarga desde u_max
u2 = [u_max*1000, (u_max - 2*uy)*1000]
F2 = [F_max, F_max - k*2*uy]

# Rama negativa
u_neg = u_max - 2*uy
F_neg = F_max - k*2*uy
u3 = [(u_max - 2*uy)*1000, -uy*1000, -u_max*1000]
F3 = [F_neg, -Fy, -F_max]

# Recarga
u4 = [-u_max*1000, (-u_max + 2*uy)*1000, uy*1000, u_max*1000]
F4 = [-F_max, -F_max + k*2*uy, Fy, F_max]

ax2.plot(u1, F1, 'b-', linewidth=2, label='Carga inicial')
ax2.plot(u2, F2, 'r-', linewidth=2)
ax2.plot(u3, F3, 'r-', linewidth=2, label='Ciclo histerético')
ax2.plot(u4, F4, 'r-', linewidth=2)

# Rellenar área (aproximado)
u_fill = np.array([uy, u_max, u_max - 2*uy, -uy, -u_max, -u_max + 2*uy, uy]) * 1000
F_fill = np.array([Fy, F_max, F_max - k*2*uy, -Fy, -F_max, -F_max + k*2*uy, Fy])
ax2.fill(u_fill, F_fill, alpha=0.2, color='red')

ax2.axhline(y=0, color='k', linewidth=0.5)
ax2.axvline(x=0, color='k', linewidth=0.5)

ax2.set_xlabel('Desplazamiento $u$ [mm]')
ax2.set_ylabel('Fuerza $F$ [kN]')
ax2.set_title('Ciclo histerético bilineal')
ax2.legend(loc='lower right', fontsize=9)
ax2.grid(True, alpha=0.3)
ax2.set_xlim(-600, 600)
ax2.set_ylim(-140, 140)

plt.tight_layout()

# Guardar figura
output_dir = Path(__file__).parent.parent / 'figs'
output_dir.mkdir(exist_ok=True)
plt.savefig(output_dir / 'fig_modelo_bilineal.pdf', bbox_inches='tight', dpi=150)
plt.savefig(output_dir / 'fig_modelo_bilineal.png', bbox_inches='tight', dpi=150)
plt.close()

print("Figura guardada: fig_modelo_bilineal.pdf/png")
