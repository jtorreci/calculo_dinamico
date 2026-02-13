"""
Problema 01: Viga en voladizo - Frecuencias y modos
===================================================
Calculo de frecuencias naturales y formas modales de viga Euler-Bernoulli.

Datos:
- L = 3 m
- E = 210 GPa
- I = 8.5e-5 m^4
- mu = 25 kg/m
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brentq

# =============================================================================
# 1. Datos del problema
# =============================================================================
print("=" * 60)
print("PROBLEMA 01: VIGA EN VOLADIZO (EULER-BERNOULLI)")
print("=" * 60)

L = 3.0       # m
E = 210e9     # Pa
I = 8.5e-5    # m^4
mu = 25.0     # kg/m

print(f"\nDatos:")
print(f"  L = {L} m")
print(f"  E = {E/1e9} GPa")
print(f"  I = {I*1e4:.2f} cm^4")
print(f"  mu = {mu} kg/m")

# =============================================================================
# 2. Ecuacion de frecuencias del voladizo
# =============================================================================
print("\n" + "=" * 60)
print("ECUACION DE FRECUENCIAS")
print("=" * 60)

def freq_equation(beta_L):
    """Ecuacion: cos(beta*L)*cosh(beta*L) + 1 = 0"""
    return np.cos(beta_L) * np.cosh(beta_L) + 1

# Buscar raices
beta_L_roots = []
x_search = np.linspace(0.1, 25, 1000)
for i in range(len(x_search)-1):
    if freq_equation(x_search[i]) * freq_equation(x_search[i+1]) < 0:
        root = brentq(freq_equation, x_search[i], x_search[i+1])
        beta_L_roots.append(root)
        if len(beta_L_roots) >= 5:
            break

beta_L_roots = np.array(beta_L_roots)
print(f"\nRaices beta_n*L: {beta_L_roots[:3]}")

# =============================================================================
# 3. Frecuencias naturales
# =============================================================================
print("\n" + "=" * 60)
print("FRECUENCIAS NATURALES")
print("=" * 60)

# Factor de frecuencia
factor = np.sqrt(E * I / (mu * L**4))
print(f"Factor sqrt(EI/mu*L^4) = {factor:.3f} rad/s")

omega = (beta_L_roots**2) * factor
f = omega / (2 * np.pi)
T = 1 / f

print(f"\n{'Modo':<6} {'beta*L':<10} {'omega (rad/s)':<15} {'f (Hz)':<10} {'T (ms)':<10}")
print("-" * 55)
for n in range(min(5, len(omega))):
    print(f"{n+1:<6} {beta_L_roots[n]:<10.4f} {omega[n]:<15.2f} {f[n]:<10.2f} {T[n]*1000:<10.1f}")

# =============================================================================
# 4. Formas modales
# =============================================================================
def mode_shape(x, beta):
    """Forma modal del voladizo normalizada"""
    bL = beta * L
    sigma = (np.sinh(bL) - np.sin(bL)) / (np.cosh(bL) + np.cos(bL))
    phi = (np.cosh(beta*x) - np.cos(beta*x)) - sigma * (np.sinh(beta*x) - np.sin(beta*x))
    return phi / np.max(np.abs(phi))  # Normalizar a 1

x = np.linspace(0, L, 200)

# =============================================================================
# 5. Graficas
# =============================================================================
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# 5.1 Ecuacion de frecuencias
ax1 = axes[0]
beta_L_plot = np.linspace(0.1, 12, 500)
y = freq_equation(beta_L_plot)
ax1.plot(beta_L_plot, y, 'b-', linewidth=2)
ax1.axhline(y=0, color='k', linestyle='--', linewidth=0.5)
for i, root in enumerate(beta_L_roots[:3]):
    ax1.plot(root, 0, 'ro', markersize=10)
    ax1.annotate(f'  $\\beta_{i+1}L = {root:.3f}$', (root, 0), fontsize=10)
ax1.set_xlabel('$\\beta L$', fontsize=12)
ax1.set_ylabel('$\\cos(\\beta L)\\cosh(\\beta L) + 1$', fontsize=12)
ax1.set_title('Ecuacion de frecuencias', fontsize=12, fontweight='bold')
ax1.set_ylim(-5, 15)
ax1.grid(True, alpha=0.3)

# 5.2 Formas modales
ax2 = axes[1]
colors = ['b', 'r', 'g']
for n in range(3):
    beta = beta_L_roots[n] / L
    phi = mode_shape(x, beta)
    ax2.plot(x, phi, colors[n], linewidth=2, label=f'Modo {n+1} (f = {f[n]:.1f} Hz)')

ax2.axhline(y=0, color='k', linestyle='--', linewidth=0.5)
ax2.set_xlabel('Posicion x (m)', fontsize=12)
ax2.set_ylabel('Desplazamiento normalizado', fontsize=12)
ax2.set_title('Formas modales', fontsize=12, fontweight='bold')
ax2.legend(loc='upper left')
ax2.grid(True, alpha=0.3)

# 5.3 Espectro de frecuencias
ax3 = axes[2]
modes = np.arange(1, len(omega)+1)
ax3.bar(modes, f[:len(modes)], color='steelblue', edgecolor='black', linewidth=1.2)
ax3.set_xlabel('Numero de modo', fontsize=12)
ax3.set_ylabel('Frecuencia (Hz)', fontsize=12)
ax3.set_title('Espectro de frecuencias', fontsize=12, fontweight='bold')
ax3.set_xticks(modes)
for i, freq in enumerate(f[:len(modes)]):
    ax3.text(i+1, freq + 5, f'{freq:.1f}', ha='center', fontsize=10, fontweight='bold')
ax3.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('../figs/fig_problema_01_voladizo.png', dpi=150, bbox_inches='tight')
plt.savefig('../figs/fig_problema_01_voladizo.pdf', bbox_inches='tight')
print("\n[Figura guardada en figs/fig_problema_01_voladizo.pdf]")
plt.close()

