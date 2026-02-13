#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Problema 10: Rigidez Equivalente de Elementos en Voladizo
==========================================================

Compara la respuesta dinámica de una pasarela en voladizo vs simplemente apoyada.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# =============================================================================
# DATOS DEL PROBLEMA
# =============================================================================

m = 3_000           # kg - masa concentrada
L = 8               # m - longitud
E = 2.0e11          # N/m² - módulo de elasticidad
I = 0.005           # m⁴ - momento de inercia
EI = E * I          # N·m² - rigidez a flexión

# =============================================================================
# CÁLCULOS
# =============================================================================

# Viga en voladizo
k_voladizo = 3 * EI / L**3
omega_n_voladizo = np.sqrt(k_voladizo / m)
T_n_voladizo = 2 * np.pi / omega_n_voladizo

# Viga simplemente apoyada
k_apoyada = 48 * EI / L**3
omega_n_apoyada = np.sqrt(k_apoyada / m)
T_n_apoyada = 2 * np.pi / omega_n_apoyada

# Ratios
ratio_k = k_apoyada / k_voladizo
ratio_omega = omega_n_apoyada / omega_n_voladizo

print("=" * 60)
print("PROBLEMA 10: RIGIDEZ EQUIVALENTE EN VOLADIZO")
print("=" * 60)
print(f"\nDatos:")
print(f"  Masa m = {m:,} kg")
print(f"  Longitud L = {L} m")
print(f"  E = {E:.2e} N/m^2")
print(f"  I = {I} m^4")
print(f"  EI = {EI:.2e} N*m^2")

print(f"\n--- Viga en Voladizo ---")
print(f"  k = 3*EI/L^3 = {k_voladizo/1e6:.3f} MN/m = {k_voladizo/1e3:.1f} kN/m")
print(f"  omega_n = {omega_n_voladizo:.2f} rad/s")
print(f"  T_n = {T_n_voladizo:.4f} s")

print(f"\n--- Viga Simplemente Apoyada ---")
print(f"  k' = 48*EI/L^3 = {k_apoyada/1e6:.3f} MN/m = {k_apoyada/1e3:.1f} kN/m")
print(f"  omega_n' = {omega_n_apoyada:.2f} rad/s")
print(f"  T_n' = {T_n_apoyada:.4f} s")

print(f"\n--- Comparacion ---")
print(f"  Ratio k'/k = {ratio_k:.0f} (apoyada es {ratio_k:.0f}x mas rigida)")
print(f"  Ratio omega_n'/omega_n = {ratio_omega:.1f}")
print(f"  El periodo se acorta de {T_n_voladizo:.3f} s a {T_n_apoyada:.4f} s")

# =============================================================================
# GRÁFICA
# =============================================================================

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Gráfica 1: Comparación de propiedades
ax1 = axes[0]

# Datos para el gráfico de barras
categorias = ['Rigidez\n(MN/m)', 'Frecuencia\n(rad/s)', 'Período×100\n(s×100)']
valores_voladizo = [k_voladizo/1e6, omega_n_voladizo, T_n_voladizo*100]
valores_apoyada = [k_apoyada/1e6, omega_n_apoyada, T_n_apoyada*100]

x = np.arange(len(categorias))
width = 0.35

bars1 = ax1.bar(x - width/2, valores_voladizo, width, label='Voladizo', color='coral', edgecolor='black')
bars2 = ax1.bar(x + width/2, valores_apoyada, width, label='Simplemente Apoyada', color='steelblue', edgecolor='black')

ax1.set_ylabel('Valor', fontsize=11)
ax1.set_title('Comparación de Propiedades Dinámicas', fontsize=12, fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(categorias)
ax1.legend(loc='upper left')
ax1.grid(axis='y', alpha=0.3)

# Gráfica 2: Vibración libre comparativa
ax2 = axes[1]
t = np.linspace(0, 0.8, 500)

zeta = 0.02  # amortiguamiento típico estructural
omega_d_vol = omega_n_voladizo * np.sqrt(1 - zeta**2)
omega_d_apo = omega_n_apoyada * np.sqrt(1 - zeta**2)

u0 = 1  # desplazamiento inicial
u_voladizo = u0 * np.exp(-zeta * omega_n_voladizo * t) * np.cos(omega_d_vol * t)
u_apoyada = u0 * np.exp(-zeta * omega_n_apoyada * t) * np.cos(omega_d_apo * t)

ax2.plot(t, u_voladizo, 'coral', linewidth=2, label=f'Voladizo (T={T_n_voladizo:.3f} s)')
ax2.plot(t, u_apoyada, 'steelblue', linewidth=2, label=f'Apoyada (T={T_n_apoyada:.4f} s)')

# Envolventes
env_vol = u0 * np.exp(-zeta * omega_n_voladizo * t)
env_apo = u0 * np.exp(-zeta * omega_n_apoyada * t)
ax2.plot(t, env_vol, 'coral', linestyle='--', linewidth=1, alpha=0.7)
ax2.plot(t, -env_vol, 'coral', linestyle='--', linewidth=1, alpha=0.7)
ax2.plot(t, env_apo, 'steelblue', linestyle='--', linewidth=1, alpha=0.7)
ax2.plot(t, -env_apo, 'steelblue', linestyle='--', linewidth=1, alpha=0.7)

ax2.axhline(y=0, color='gray', linestyle='-', linewidth=0.5)
ax2.set_xlabel('Tiempo (s)', fontsize=11)
ax2.set_ylabel('Desplazamiento normalizado u/u₀', fontsize=11)
ax2.set_title(f'Vibración Libre Amortiguada (ζ = {zeta*100:.0f}%)', fontsize=12, fontweight='bold')
ax2.legend(loc='upper right', fontsize=10)
ax2.grid(True, alpha=0.3)
ax2.set_xlim([0, 0.8])

plt.tight_layout()
plt.savefig('../figs/fig_problema_10_comparacion.pdf', dpi=150, bbox_inches='tight')
plt.close()

print(f"\nFigura guardada: figs/fig_problema_10_comparacion.pdf")
