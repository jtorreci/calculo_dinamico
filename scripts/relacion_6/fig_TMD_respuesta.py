"""
Figura: Respuesta de sistema con TMD
Problema 09 - Relación 6
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
ms = 100e3    # kg
ws = 6.28     # rad/s
zeta_s = 0.02
mu = 0.05     # ratio de masa

# Parámetros óptimos Den Hartog
f_opt = 1 / (1 + mu)
zeta_d_opt = np.sqrt(3*mu / (8*(1+mu)))

# Crear figura
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

# ============================================
# SUBPLOT 1: FRF con y sin TMD
# ============================================
# Rango de frecuencias
r = np.linspace(0.5, 1.5, 500)  # omega/omega_s

# Sin TMD (SDOF simple)
H_sin = 1 / np.sqrt((1 - r**2)**2 + (2*zeta_s*r)**2)

# Con TMD (fórmula completa del sistema 2DOF)
# H = |X1/Xst| donde Xst = F0/ks
f = f_opt  # ratio de frecuencias wd/ws
zd = zeta_d_opt

# Numerador y denominador de la FRF del sistema principal con TMD
# Fórmula simplificada para TMD óptimo
num = np.sqrt((f**2 - r**2)**2 + (2*zd*f*r)**2)
den_real = (1 - r**2)*(f**2 - r**2) - mu*f**2*r**2 - 2*zeta_s*r*2*zd*f*r - (1 - r**2)*2*zd*f*r - 2*zeta_s*r*(f**2 - r**2)
den_imag = 2*zeta_s*r*(f**2 - r**2) + (1 - r**2)*2*zd*f*r - mu*f**2*r*2*zd*f*r
# Simplificar usando aproximación para TMD bien sintonizado
# Usar fórmula numérica directa

# Matrices del sistema
def FRF_TMD(r, mu, f, zs, zd):
    """Calcula FRF del sistema principal con TMD"""
    H = np.zeros_like(r)
    for i, ri in enumerate(r):
        # Matriz de impedancia dinámica
        # [1-r² + 2j*zs*r + mu*f²*(...)  ,  -mu*f²*(...)]
        # [-f²*(...)                      ,  f²-r² + 2j*zd*f*r]

        # Términos
        a = 1 - ri**2 + 2j*zs*ri
        b = f**2 - ri**2 + 2j*zd*f*ri
        c = mu * f**2

        # Det = a*b - c*b + c*a? No, es más complicado
        # Usar forma directa
        Z11 = 1 - ri**2 + 2j*zs*ri
        Z22 = f**2 - ri**2 + 2j*zd*f*ri
        coupling = mu * f**2 * Z22 / (Z22)

        # Aproximación: usar superposición modal
        # Para TMD bien diseñado, dos picos a frecuencias (1±sqrt(mu/2))*ws
        num_val = np.abs(f**2 - ri**2 + 2j*zd*f*ri)
        den_val = np.abs((1 - ri**2 + 2j*zs*ri)*(f**2 - ri**2 + 2j*zd*f*ri) - mu*f**2*ri**2)

        # Corrección para evitar división por cero
        if den_val < 1e-10:
            den_val = 1e-10

        H[i] = num_val / den_val
    return H

H_con = FRF_TMD(r, mu, f_opt, zeta_s, zeta_d_opt)

ax1.semilogy(r, H_sin, 'b-', linewidth=2, label='Sin TMD')
ax1.semilogy(r, H_con, 'r-', linewidth=2, label='Con TMD óptimo')

# Resonancia sin TMD
ax1.axvline(x=1.0, color='gray', linestyle=':', linewidth=1)
ax1.text(1.02, 20, r'$\omega = \omega_s$', fontsize=9)

# Valores máximos
H_max_sin = 1/(2*zeta_s)
H_max_con = np.max(H_con)
ax1.axhline(y=H_max_sin, color='blue', linestyle='--', linewidth=1, alpha=0.5)
ax1.axhline(y=H_max_con, color='red', linestyle='--', linewidth=1, alpha=0.5)

reduccion = (H_max_sin - H_max_con) / H_max_sin * 100
ax1.text(0.55, 15, f'Reducción: {reduccion:.0f}%', fontsize=10,
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

ax1.set_xlabel(r'Frecuencia normalizada $\omega/\omega_s$')
ax1.set_ylabel('Factor de amplificación $|H|$')
ax1.set_title('Función de Respuesta en Frecuencia')
ax1.legend(loc='upper right', fontsize=9)
ax1.grid(True, alpha=0.3, which='both')
ax1.set_xlim(0.5, 1.5)
ax1.set_ylim(0.1, 50)

# ============================================
# SUBPLOT 2: Esquema del TMD
# ============================================
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 10)
ax2.set_aspect('equal')
ax2.axis('off')

# Estructura principal (masa grande)
rect_s = plt.Rectangle((3, 2), 4, 3, fill=True, facecolor='lightblue',
                         edgecolor='black', linewidth=2)
ax2.add_patch(rect_s)
ax2.text(5, 3.5, f'$m_s = {ms/1000:.0f}$ ton', ha='center', va='center', fontsize=11)

# TMD (masa pequeña encima)
rect_d = plt.Rectangle((4, 6.5), 2, 1, fill=True, facecolor='lightcoral',
                         edgecolor='black', linewidth=2)
ax2.add_patch(rect_d)
ax2.text(5, 7, f'$m_d$', ha='center', va='center', fontsize=10)

# Resorte del TMD
x_spring = [4.3, 4.3, 4.1, 4.5, 4.1, 4.5, 4.1, 4.5, 4.3, 4.3]
y_spring = [5, 5.3, 5.5, 5.7, 5.9, 6.1, 6.3, 6.5, 6.5, 6.5]
y_spring = [5, 5.2, 5.4, 5.6, 5.8, 6.0, 6.2, 6.4, 6.5, 6.5]
ax2.plot(x_spring, y_spring, 'k-', linewidth=1.5)
ax2.text(3.8, 5.7, '$k_d$', fontsize=9)

# Amortiguador del TMD
ax2.plot([5.7, 5.7], [5, 5.5], 'k-', linewidth=1.5)
ax2.add_patch(plt.Rectangle((5.5, 5.5), 0.4, 0.8, fill=False, edgecolor='black', linewidth=1.5))
ax2.plot([5.7, 5.7], [6.3, 6.5], 'k-', linewidth=1.5)
ax2.text(6.1, 5.9, '$c_d$', fontsize=9)

# Resorte de la estructura
x_spring_s = [1.5, 1.5, 1.3, 1.7, 1.3, 1.7, 1.3, 1.7, 1.5, 1.5]
y_spring_s = [0, 0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5, 1.7, 2]
ax2.plot(x_spring_s, y_spring_s, 'k-', linewidth=1.5)
ax2.text(1.0, 1, '$k_s$', fontsize=9)

# Amortiguador de la estructura
ax2.plot([8.5, 8.5], [0, 0.5], 'k-', linewidth=1.5)
ax2.add_patch(plt.Rectangle((8.3, 0.5), 0.4, 0.8, fill=False, edgecolor='black', linewidth=1.5))
ax2.plot([8.5, 8.5], [1.3, 2], 'k-', linewidth=1.5)
ax2.text(9.0, 0.9, '$c_s$', fontsize=9)

# Base
ax2.plot([0, 10], [0, 0], 'k-', linewidth=3)
ax2.fill([0, 10, 10, 0], [-0.3, -0.3, 0, 0], color='gray', alpha=0.5)

# Fuerza
ax2.annotate('', xy=(1, 3.5), xytext=(-0.5, 3.5),
             arrowprops=dict(arrowstyle='->', color='red', lw=2))
ax2.text(-0.3, 4, '$F(t)$', fontsize=11, color='red')

# Título
ax2.text(5, 9, 'Sistema con TMD', ha='center', fontsize=12, fontweight='bold')

# Parámetros óptimos
ax2.text(5, 8.2, f'$\\mu = {mu*100:.0f}\\%$, $f_{{opt}} = {f_opt:.3f}$, $\\zeta_d = {zeta_d_opt*100:.1f}\\%$',
         ha='center', fontsize=10)

plt.tight_layout()

# Guardar figura
output_dir = Path(__file__).parent.parent / 'figs'
output_dir.mkdir(exist_ok=True)
plt.savefig(output_dir / 'fig_TMD_respuesta.pdf', bbox_inches='tight', dpi=150)
plt.savefig(output_dir / 'fig_TMD_respuesta.png', bbox_inches='tight', dpi=150)
plt.close()

print("Figura guardada: fig_TMD_respuesta.pdf/png")
