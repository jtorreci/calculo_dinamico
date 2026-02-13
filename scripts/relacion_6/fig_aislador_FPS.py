"""
Figura: Aislador de péndulo friccional (FPS)
Problema 11 - Relación 6
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
W = 1500  # kN
R = 2.5   # m
mu_f = 0.06
D = 0.300  # m

# Propiedades derivadas
kp = W / R  # rigidez post-deslizamiento
Qd = mu_f * W  # fuerza característica
F_max = Qd + kp * D

# Crear figura
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

# ============================================
# SUBPLOT 1: Diagrama fuerza-desplazamiento
# ============================================
# Ciclo bilineal del FPS
u = np.linspace(-D, D, 100) * 1000  # mm

# Rama de carga (positiva)
u_carga = np.array([0, 0, D]) * 1000
F_carga = np.array([0, Qd, Qd + kp*D])

# Ciclo completo
u_ciclo = np.array([0, D, D, 0, -D, -D, 0]) * 1000
F_ciclo = np.array([Qd, F_max, -Qd - kp*D + 2*Qd, -Qd, -F_max, Qd + kp*D - 2*Qd, Qd])

# Simplificar ciclo
u_hist = np.array([0, D, D, -D, -D, 0]) * 1000
F_hist = np.array([Qd, F_max, -F_max + 2*Qd, -F_max, F_max - 2*Qd, Qd])

ax1.fill(u_hist, F_hist, alpha=0.3, color='red', label='Energía disipada')
ax1.plot(u_hist, F_hist, 'r-', linewidth=2)

# Backbone curve
u_bb = np.array([-D, 0, D]) * 1000
F_bb = np.array([-F_max, 0, F_max])
ax1.plot(u_bb, F_bb, 'b--', linewidth=2, label='Curva backbone')

# Rigidez secante
k_eff = kp + Qd/D
ax1.plot([-D*1000, D*1000], [-k_eff*D, k_eff*D], 'g:', linewidth=2, label=f'$k_{{eff}}$ = {k_eff:.0f} kN/m')

# Anotaciones
ax1.annotate(f'$Q_d = {Qd:.0f}$ kN', xy=(0, Qd), xytext=(50, Qd + 30),
             fontsize=9, arrowprops=dict(arrowstyle='->', color='gray'))
ax1.annotate(f'$F_{{max}} = {F_max:.0f}$ kN', xy=(D*1000, F_max), xytext=(D*1000 - 100, F_max + 30),
             fontsize=9)

ax1.axhline(y=0, color='k', linewidth=0.5)
ax1.axvline(x=0, color='k', linewidth=0.5)

ax1.set_xlabel('Desplazamiento $u$ [mm]')
ax1.set_ylabel('Fuerza $F$ [kN]')
ax1.set_title('Diagrama F-u del aislador FPS')
ax1.legend(loc='lower right', fontsize=8)
ax1.grid(True, alpha=0.3)
ax1.set_xlim(-400, 400)
ax1.set_ylim(-350, 350)

# ============================================
# SUBPLOT 2: Esquema del FPS
# ============================================
ax2.set_xlim(-3, 3)
ax2.set_ylim(-1, 3)
ax2.set_aspect('equal')
ax2.axis('off')

# Superficie cóncava inferior
theta = np.linspace(-0.5, 0.5, 100)
x_curva = R * np.sin(theta)
y_curva = R * (1 - np.cos(theta))
ax2.plot(x_curva, y_curva, 'b-', linewidth=3)
ax2.fill_between(x_curva, y_curva - 0.15, y_curva, color='lightblue', alpha=0.5)

# Deslizador (articulado)
x_slider = 0.3
y_slider = R * (1 - np.cos(np.arcsin(x_slider/R)))
circle = plt.Circle((x_slider, y_slider + 0.15), 0.15, color='gray', ec='black', linewidth=2)
ax2.add_patch(circle)

# Placa superior
rect = plt.Rectangle((-1, y_slider + 0.3), 2, 0.3, color='lightgray', ec='black', linewidth=2)
ax2.add_patch(rect)

# Estructura encima
ax2.plot([-0.8, -0.8, 0.8, 0.8], [y_slider + 0.6, y_slider + 1.5, y_slider + 1.5, y_slider + 0.6],
         'k-', linewidth=2)
ax2.fill([-0.8, -0.8, 0.8, 0.8], [y_slider + 0.6, y_slider + 1.5, y_slider + 1.5, y_slider + 0.6],
         color='lightyellow', alpha=0.5)
ax2.text(0, y_slider + 1.1, '$W$', ha='center', fontsize=12)

# Base
ax2.plot([-2.5, 2.5], [-0.1, -0.1], 'k-', linewidth=3)
ax2.fill([-2.5, 2.5, 2.5, -2.5], [-0.3, -0.3, -0.1, -0.1], color='gray', alpha=0.5)

# Radio de curvatura
ax2.annotate('', xy=(0, 0), xytext=(0, -R + 0.5),
             arrowprops=dict(arrowstyle='<->', color='red', lw=1.5))
ax2.text(0.15, -R/2 + 0.3, f'$R = {R}$ m', fontsize=10, color='red')

# Desplazamiento
ax2.annotate('', xy=(x_slider, y_slider + 0.45), xytext=(0, y_slider + 0.45),
             arrowprops=dict(arrowstyle='<->', color='green', lw=1.5))
ax2.text(x_slider/2, y_slider + 0.55, '$u$', fontsize=10, color='green')

# Fricción
ax2.annotate('', xy=(x_slider - 0.3, y_slider + 0.15), xytext=(x_slider + 0.1, y_slider + 0.15),
             arrowprops=dict(arrowstyle='->', color='orange', lw=2))
ax2.text(x_slider - 0.5, y_slider + 0.35, f'$\\mu_f = {mu_f}$', fontsize=9, color='orange')

# Título y período
ax2.text(0, 2.5, 'Aislador de Péndulo Friccional (FPS)', ha='center', fontsize=11, fontweight='bold')
T_iso = 2*np.pi*np.sqrt(R/9.81)
ax2.text(0, 2.2, f'$T_{{iso}} = 2\\pi\\sqrt{{R/g}} = {T_iso:.2f}$ s', ha='center', fontsize=10)

plt.tight_layout()

# Guardar figura
output_dir = Path(__file__).parent.parent / 'figs'
output_dir.mkdir(exist_ok=True)
plt.savefig(output_dir / 'fig_aislador_FPS.pdf', bbox_inches='tight', dpi=150)
plt.savefig(output_dir / 'fig_aislador_FPS.png', bbox_inches='tight', dpi=150)
plt.close()

print("Figura guardada: fig_aislador_FPS.pdf/png")
