"""
Problema 09: Placa rectangular simplemente apoyada
===================================================
Calculo de frecuencias naturales y formas modales.

Datos:
- a = 2.0 m, b = 1.5 m
- h = 10 mm
- E = 210 GPa, nu = 0.3, rho = 7850 kg/m^3
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# =============================================================================
# 1. Datos del problema
# =============================================================================
print("=" * 60)
print("PROBLEMA 09: PLACA RECTANGULAR SIMPLEMENTE APOYADA")
print("=" * 60)

a = 2.0       # m
b = 1.5       # m
h = 0.010     # m
E = 210e9     # Pa
nu = 0.3
rho = 7850    # kg/m^3

# Rigidez flexional
D = E * h**3 / (12 * (1 - nu**2))
print(f"\nDatos:")
print(f"  a x b = {a} x {b} m")
print(f"  h = {h*1000} mm")
print(f"  D = {D:.1f} N*m")

# =============================================================================
# 2. Frecuencias naturales
# =============================================================================
print("\n" + "=" * 60)
print("FRECUENCIAS NATURALES")
print("=" * 60)

factor = np.sqrt(D / (rho * h))
print(f"Factor sqrt(D/rho*h) = {factor:.2f} m^2/s")

# Calcular frecuencias para modos (m,n)
modes = [(1,1), (2,1), (1,2), (2,2), (3,1), (1,3), (3,2), (2,3)]
frequencies = []

print(f"\n{'Modo (m,n)':<12} {'lambda_mn':<12} {'omega (rad/s)':<15} {'f (Hz)':<10}")
print("-" * 55)
for m, n in modes:
    lambda_mn = (m/a)**2 + (n/b)**2
    omega = np.pi**2 * lambda_mn * factor
    f = omega / (2 * np.pi)
    frequencies.append((m, n, omega, f))
    print(f"({m},{n}){'':<8} {lambda_mn:<12.3f} {omega:<15.1f} {f:<10.1f}")

# =============================================================================
# 3. Formas modales
# =============================================================================
x = np.linspace(0, a, 50)
y = np.linspace(0, b, 40)
X, Y = np.meshgrid(x, y)

def mode_shape_plate(X, Y, m, n, a, b):
    """Forma modal de placa simplemente apoyada"""
    return np.sin(m * np.pi * X / a) * np.sin(n * np.pi * Y / b)

# =============================================================================
# 4. Graficas
# =============================================================================
fig = plt.figure(figsize=(16, 10))

# Primera fila: 4 primeros modos en 3D
for idx, (m, n, omega, f) in enumerate(frequencies[:4]):
    ax = fig.add_subplot(2, 4, idx+1, projection='3d')
    Z = mode_shape_plate(X, Y, m, n, a, b)
    surf = ax.plot_surface(X, Y, Z, cmap='RdBu', linewidth=0, antialiased=True, alpha=0.8)
    ax.set_xlabel('x (m)')
    ax.set_ylabel('y (m)')
    ax.set_zlabel('w')
    ax.set_title(f'Modo ({m},{n})\nf = {f:.1f} Hz', fontsize=11, fontweight='bold')
    ax.set_zlim(-1.2, 1.2)

# Segunda fila: Vista superior (contornos)
for idx, (m, n, omega, f) in enumerate(frequencies[:4]):
    ax = fig.add_subplot(2, 4, idx+5)
    Z = mode_shape_plate(X, Y, m, n, a, b)
    levels = np.linspace(-1, 1, 21)
    cs = ax.contourf(X, Y, Z, levels=levels, cmap='RdBu')
    ax.contour(X, Y, Z, levels=[0], colors='k', linewidths=2)  # Lineas nodales
    ax.set_xlabel('x (m)')
    ax.set_ylabel('y (m)')
    ax.set_title(f'Modo ({m},{n}) - Lineas nodales', fontsize=10)
    ax.set_aspect('equal')
    plt.colorbar(cs, ax=ax, shrink=0.8)

plt.tight_layout()
plt.savefig('../figs/fig_problema_09_placa.png', dpi=150, bbox_inches='tight')
plt.savefig('../figs/fig_problema_09_placa.pdf', bbox_inches='tight')
print("\n[Figura guardada en figs/fig_problema_09_placa.pdf]")
plt.close()

