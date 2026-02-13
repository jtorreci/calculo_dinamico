#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Problema 22: Rigidez Equivalente de Sistemas Combinados (Viga y Resorte)
=========================================================================

Sistema con viga en voladizo y resorte en paralelo.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# =============================================================================
# DATOS DEL PROBLEMA (unidades SI)
# =============================================================================

W = 7_000           # N - peso del equipo
L = 2.5             # m - longitud de la viga
EI = 5.0e5          # N·m² - rigidez a flexión
k_resorte = 90_000  # N/m - rigidez del resorte helicoidal
g = 9.81            # m/s² - aceleración de gravedad

# =============================================================================
# CÁLCULOS
# =============================================================================

# Masa
m = W / g  # kg

# Rigidez de la viga en voladizo
k_viga = 3 * EI / L**3

# Rigidez equivalente (paralelo)
k_eq = k_viga + k_resorte

# Frecuencia natural
omega_n = np.sqrt(k_eq / m)
T_n = 2 * np.pi / omega_n
f_n = 1 / T_n

# Contribuciones porcentuales
pct_viga = (k_viga / k_eq) * 100
pct_resorte = (k_resorte / k_eq) * 100

print("=" * 60)
print("PROBLEMA 22: RIGIDEZ EQUIVALENTE (VIGA + RESORTE)")
print("=" * 60)
print(f"\nDatos:")
print(f"  Peso W = {W} N")
print(f"  Longitud L = {L} m")
print(f"  EI = {EI:.2e} N*m^2")
print(f"  k_resorte = {k_resorte} N/m")
print(f"  g = {g} m/s^2")
print(f"  Masa m = W/g = {m:.1f} kg")

print(f"\n--- Rigidez de la Viga ---")
print(f"  k_viga = 3*EI/L^3 = {k_viga:.0f} N/m")

print(f"\n--- Rigidez Equivalente (Paralelo) ---")
print(f"  k_eq = k_viga + k_resorte = {k_viga:.0f} + {k_resorte} = {k_eq:.0f} N/m")
print(f"  Contribucion viga: {pct_viga:.1f}%")
print(f"  Contribucion resorte: {pct_resorte:.1f}%")

print(f"\n--- Propiedades Dinamicas ---")
print(f"  omega_n = sqrt(k_eq/m) = {omega_n:.2f} rad/s")
print(f"  T_n = 2*pi/omega_n = {T_n:.3f} s")
print(f"  f_n = {f_n:.2f} Hz")

# =============================================================================
# GRÁFICA
# =============================================================================

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Gráfica 1: Contribución de rigidez
ax1 = axes[0]

# Gráfico de barras apiladas
componentes = ['k_viga', 'k_resorte']
valores = [k_viga, k_resorte]
colores = ['steelblue', 'coral']

# Barra única apilada
bottom = 0
for comp, val, color in zip(componentes, valores, colores):
    ax1.bar('Rigidez Total', val/1000, bottom=bottom/1000, color=color, edgecolor='black',
            label=f'{comp} = {val/1000:.0f} kN/m ({val/k_eq*100:.1f}%)')
    # Etiqueta centrada en cada sección
    ax1.text(0, (bottom + val/2)/1000, f'{val/1000:.0f}', ha='center', va='center',
             fontsize=11, fontweight='bold', color='white')
    bottom += val

ax1.set_ylabel('Rigidez (kN/m)', fontsize=11)
ax1.set_title('Composición de Rigidez Equivalente', fontsize=12, fontweight='bold')
ax1.legend(loc='upper right', fontsize=10)
ax1.set_ylim([0, k_eq/1000 * 1.15])
ax1.text(0, k_eq/1000 + 5, f'k_eq = {k_eq/1000:.0f} kN/m', ha='center', va='bottom',
         fontsize=12, fontweight='bold')

# Gráfica 2: Respuesta en vibración libre
ax2 = axes[1]
t = np.linspace(0, 1.5, 500)

zeta = 0.02  # amortiguamiento ligero
omega_d = omega_n * np.sqrt(1 - zeta**2)

u0 = 1  # desplazamiento inicial
u = u0 * np.exp(-zeta * omega_n * t) * np.cos(omega_d * t)
env = u0 * np.exp(-zeta * omega_n * t)

ax2.plot(t, u, 'b-', linewidth=2, label=f'Respuesta (ω_n = {omega_n:.1f} rad/s)')
ax2.plot(t, env, 'r--', linewidth=1.5, alpha=0.7, label='Envolvente')
ax2.plot(t, -env, 'r--', linewidth=1.5, alpha=0.7)

ax2.axhline(y=0, color='gray', linestyle='-', linewidth=0.5)
ax2.set_xlabel('Tiempo (s)', fontsize=11)
ax2.set_ylabel('Desplazamiento normalizado u/u₀', fontsize=11)
ax2.set_title(f'Vibración Libre (T = {T_n:.3f} s, ζ = {zeta*100:.0f}%)',
              fontsize=12, fontweight='bold')
ax2.legend(loc='upper right', fontsize=10)
ax2.grid(True, alpha=0.3)
ax2.set_xlim([0, 1.5])

plt.tight_layout()
plt.savefig('../figs/fig_problema_22_sistema_combinado.pdf', dpi=150, bbox_inches='tight')
plt.close()

print(f"\nFigura guardada: figs/fig_problema_22_sistema_combinado.pdf")
