#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Problema 13: Cálculo de Rigidez Adicional por Atirantamiento
=============================================================

Control de período mediante aumento de rigidez.
Muestra la relación T ∝ 1/√k.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# =============================================================================
# DATOS DEL PROBLEMA
# =============================================================================

m = 100_000         # kg - masa concentrada
T_actual = 1.8      # s - período actual
T_deseado = 1.0     # s - período objetivo

# =============================================================================
# CÁLCULOS
# =============================================================================

# Frecuencias naturales
omega_actual = 2 * np.pi / T_actual
omega_deseado = 2 * np.pi / T_deseado

# Rigideces
k_actual = m * omega_actual**2
k_deseado = m * omega_deseado**2
Delta_k = k_deseado - k_actual

# Ratios
ratio_T = T_actual / T_deseado
ratio_k = k_deseado / k_actual
aumento_porcentual = (Delta_k / k_actual) * 100

print("=" * 60)
print("PROBLEMA 13: RIGIDEZ ADICIONAL POR ATIRANTAMIENTO")
print("=" * 60)
print(f"\nDatos:")
print(f"  Masa m = {m:,} kg")
print(f"  Periodo actual T = {T_actual} s")
print(f"  Periodo deseado T' = {T_deseado} s")

print(f"\n--- Estado Actual ---")
print(f"  omega_n = 2*pi/T = {omega_actual:.3f} rad/s")
print(f"  k_actual = m*omega^2 = {k_actual/1e6:.3f} MN/m = {k_actual/1e3:.0f} kN/m")

print(f"\n--- Estado Deseado ---")
print(f"  omega_n' = 2*pi/T' = {omega_deseado:.3f} rad/s")
print(f"  k_deseado = m*omega'^2 = {k_deseado/1e6:.3f} MN/m = {k_deseado/1e3:.0f} kN/m")

print(f"\n--- Rigidez Adicional ---")
print(f"  Delta_k = k_deseado - k_actual = {Delta_k/1e6:.3f} MN/m = {Delta_k/1e3:.0f} kN/m")
print(f"  Aumento de rigidez: {aumento_porcentual:.0f}%")
print(f"  Ratio k_deseado/k_actual = {ratio_k:.2f}")
print(f"  Verificacion: (T_actual/T_deseado)^2 = {ratio_T**2:.2f} ~ {ratio_k:.2f}")

# =============================================================================
# GRÁFICA
# =============================================================================

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Gráfica 1: Relación Período vs Rigidez
ax1 = axes[0]

k_range = np.linspace(0.5e6, 6e6, 200)
T_range = 2 * np.pi * np.sqrt(m / k_range)

ax1.plot(k_range/1e6, T_range, 'b-', linewidth=2, label=r'$T = 2\pi\sqrt{m/k}$')

# Puntos actual y deseado
ax1.plot(k_actual/1e6, T_actual, 'ro', markersize=12, markeredgecolor='black',
         label=f'Actual: T={T_actual} s, k={k_actual/1e3:.0f} kN/m')
ax1.plot(k_deseado/1e6, T_deseado, 'g^', markersize=12, markeredgecolor='black',
         label=f'Deseado: T={T_deseado} s, k={k_deseado/1e3:.0f} kN/m')

# Flechas indicando la transición
ax1.annotate('', xy=(k_deseado/1e6, T_deseado), xytext=(k_actual/1e6, T_actual),
             arrowprops=dict(arrowstyle='->', color='purple', lw=2))
ax1.text((k_actual + k_deseado)/(2e6), (T_actual + T_deseado)/2 + 0.15,
         f'Δk = {Delta_k/1e3:.0f} kN/m', fontsize=10, color='purple', fontweight='bold')

ax1.set_xlabel('Rigidez k (MN/m)', fontsize=11)
ax1.set_ylabel('Período T (s)', fontsize=11)
ax1.set_title('Relación Período-Rigidez', fontsize=12, fontweight='bold')
ax1.legend(loc='upper right', fontsize=9)
ax1.grid(True, alpha=0.3)
ax1.set_xlim([0, 6])
ax1.set_ylim([0, 3])

# Gráfica 2: Comparación de respuesta temporal
ax2 = axes[1]
t = np.linspace(0, 8, 500)

zeta = 0.05  # amortiguamiento típico
omega_d_actual = omega_actual * np.sqrt(1 - zeta**2)
omega_d_deseado = omega_deseado * np.sqrt(1 - zeta**2)

u0 = 1  # desplazamiento inicial
u_actual = u0 * np.exp(-zeta * omega_actual * t) * np.cos(omega_d_actual * t)
u_deseado = u0 * np.exp(-zeta * omega_deseado * t) * np.cos(omega_d_deseado * t)

ax2.plot(t, u_actual, 'r-', linewidth=2, label=f'Actual: T={T_actual} s')
ax2.plot(t, u_deseado, 'g-', linewidth=2, label=f'Con atirantamiento: T={T_deseado} s')

ax2.axhline(y=0, color='gray', linestyle='-', linewidth=0.5)
ax2.set_xlabel('Tiempo (s)', fontsize=11)
ax2.set_ylabel('Desplazamiento normalizado u/u₀', fontsize=11)
ax2.set_title(f'Vibración Libre (ζ = {zeta*100:.0f}%)', fontsize=12, fontweight='bold')
ax2.legend(loc='upper right', fontsize=10)
ax2.grid(True, alpha=0.3)
ax2.set_xlim([0, 8])

plt.tight_layout()
plt.savefig('../figs/fig_problema_13_control_periodo.pdf', dpi=150, bbox_inches='tight')
plt.close()

print(f"\nFigura guardada: figs/fig_problema_13_control_periodo.pdf")
