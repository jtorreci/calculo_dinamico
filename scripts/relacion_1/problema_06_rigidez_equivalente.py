#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Problema 06: Rigidez Equivalente en Sistemas Generalizados
===========================================================

Compara la rigidez y respuesta dinámica de una viga simplemente apoyada
vs una viga en voladizo con las mismas propiedades.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# =============================================================================
# DATOS DEL PROBLEMA
# =============================================================================

M = 10_000          # kg - masa concentrada
L = 20              # m - longitud
EI = 1.2e10         # N·m² - rigidez a flexión

# =============================================================================
# CÁLCULOS
# =============================================================================

# Viga simplemente apoyada
k_apoyada = 48 * EI / L**3
omega_n_apoyada = np.sqrt(k_apoyada / M)
T_n_apoyada = 2 * np.pi / omega_n_apoyada
f_n_apoyada = 1 / T_n_apoyada

# Viga en voladizo
k_voladizo = 3 * EI / L**3
omega_n_voladizo = np.sqrt(k_voladizo / M)
T_n_voladizo = 2 * np.pi / omega_n_voladizo
f_n_voladizo = 1 / T_n_voladizo

# Ratio de rigideces
ratio_k = k_apoyada / k_voladizo
ratio_T = T_n_voladizo / T_n_apoyada

print("=" * 60)
print("PROBLEMA 06: RIGIDEZ EQUIVALENTE EN SISTEMAS GENERALIZADOS")
print("=" * 60)
print(f"\nDatos:")
print(f"  Masa concentrada M = {M:,} kg")
print(f"  Longitud L = {L} m")
print(f"  Rigidez a flexion EI = {EI:.2e} N*m^2")

print(f"\n--- Viga Simplemente Apoyada ---")
print(f"  k_eq = 48*EI/L^3 = {k_apoyada/1e6:.2f} MN/m = {k_apoyada/1e3:.0f} kN/m")
print(f"  omega_n = {omega_n_apoyada:.2f} rad/s")
print(f"  T_n = {T_n_apoyada:.4f} s")
print(f"  f_n = {f_n_apoyada:.2f} Hz")

print(f"\n--- Viga en Voladizo ---")
print(f"  k_eq = 3*EI/L^3 = {k_voladizo/1e6:.2f} MN/m = {k_voladizo/1e3:.0f} kN/m")
print(f"  omega_n = {omega_n_voladizo:.2f} rad/s")
print(f"  T_n = {T_n_voladizo:.4f} s")
print(f"  f_n = {f_n_voladizo:.2f} Hz")

print(f"\n--- Comparacion ---")
print(f"  Ratio de rigideces: k_apoyada/k_voladizo = {ratio_k:.0f}")
print(f"  Ratio de periodos: T_voladizo/T_apoyada = {ratio_T:.1f}")

# =============================================================================
# GRÁFICA COMPARATIVA
# =============================================================================

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Gráfica 1: Comparación de rigideces
ax1 = axes[0]
tipos = ['Simplemente\nApoyada', 'Voladizo']
rigideces = [k_apoyada/1e6, k_voladizo/1e6]
colores = ['steelblue', 'coral']

bars = ax1.bar(tipos, rigideces, color=colores, edgecolor='black', linewidth=1.5)
ax1.set_ylabel('Rigidez Equivalente (MN/m)', fontsize=11)
ax1.set_title('Comparación de Rigidez según Condición de Apoyo', fontsize=12, fontweight='bold')
ax1.grid(axis='y', alpha=0.3)

# Añadir valores sobre las barras
for bar, val in zip(bars, rigideces):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
             f'{val:.1f} MN/m', ha='center', va='bottom', fontsize=10, fontweight='bold')

# Añadir anotación del ratio
ax1.annotate(f'×{ratio_k:.0f}', xy=(0.5, (rigideces[0]+rigideces[1])/2),
             fontsize=14, fontweight='bold', color='red',
             ha='center', va='center')

# Gráfica 2: Respuesta en vibración libre
ax2 = axes[1]
t = np.linspace(0, 1.5, 500)

# Respuesta para desplazamiento inicial u0 = 1 (sin amortiguamiento)
u0 = 1  # desplazamiento inicial normalizado
u_apoyada = u0 * np.cos(omega_n_apoyada * t)
u_voladizo = u0 * np.cos(omega_n_voladizo * t)

ax2.plot(t, u_apoyada, 'steelblue', linewidth=2,
         label=f'Apoyada: T = {T_n_apoyada:.3f} s')
ax2.plot(t, u_voladizo, 'coral', linewidth=2,
         label=f'Voladizo: T = {T_n_voladizo:.3f} s')

ax2.axhline(y=0, color='gray', linestyle='-', linewidth=0.5)
ax2.set_xlabel('Tiempo (s)', fontsize=11)
ax2.set_ylabel('Desplazamiento normalizado u/u₀', fontsize=11)
ax2.set_title('Vibración Libre (sin amortiguamiento)', fontsize=12, fontweight='bold')
ax2.legend(loc='upper right', fontsize=10)
ax2.grid(True, alpha=0.3)
ax2.set_xlim([0, 1.5])
ax2.set_ylim([-1.3, 1.3])

plt.tight_layout()
plt.savefig('../figs/fig_problema_06_comparacion_vigas.pdf', dpi=150, bbox_inches='tight')
plt.close()

print(f"\nFigura guardada: figs/fig_problema_06_comparacion_vigas.pdf")
