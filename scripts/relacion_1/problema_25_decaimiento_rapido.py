#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Problema 25: Amortiguamiento por Decaimiento de la Vibracion
=============================================================

Estructura industrial con amortiguamiento alto (15%).
Calcula omega_n, decremento logaritmico y respuesta tras 4 ciclos.

Ejecutar: python problema_25_decaimiento_rapido.py
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Backend no interactivo
import matplotlib.pyplot as plt

# =============================================================================
# DATOS DEL PROBLEMA
# =============================================================================

T_D = 0.50    # s - Periodo de vibracion amortiguada
zeta = 0.15   # Razon de amortiguamiento (15%)
u0 = 25.0     # mm - Amplitud inicial (desplazamiento inicial)
v0 = 0.0      # mm/s - Velocidad inicial

N_cycles = 4  # Numero de ciclos para calcular respuesta

# =============================================================================
# SOLUCION
# =============================================================================

print("=" * 65)
print("PROBLEMA 25: DECAIMIENTO RAPIDO - ESTRUCTURA INDUSTRIAL")
print("=" * 65)
print()

print("Datos del problema:")
print(f"  Periodo amortiguado T_D = {T_D} s")
print(f"  Razon de amortiguamiento zeta = {zeta} ({zeta*100:.0f}%)")
print(f"  Amplitud inicial u0 = {u0} mm")
print(f"  Velocidad inicial v0 = {v0} mm/s")
print()

# 1. Frecuencia circular natural no amortiguada
omega_D = 2 * np.pi / T_D
omega_n = omega_D / np.sqrt(1 - zeta**2)
T_n = 2 * np.pi / omega_n
f_n = omega_n / (2 * np.pi)

print("1. FRECUENCIA CIRCULAR NATURAL NO AMORTIGUADA (omega_n):")
print("   Primero, la frecuencia amortiguada:")
print(f"   omega_D = 2*pi/T_D = 2*pi/{T_D}")
print(f"   omega_D = {omega_D:.4f} rad/s = 4*pi rad/s")
print()
print("   Luego, despejamos omega_n:")
print(f"   omega_n = omega_D / sqrt(1 - zeta^2)")
print(f"   omega_n = {omega_D:.4f} / sqrt(1 - {zeta}^2)")
print(f"   omega_n = {omega_D:.4f} / sqrt({1 - zeta**2:.4f})")
print(f"   omega_n = {omega_D:.4f} / {np.sqrt(1 - zeta**2):.4f}")
print(f"   omega_n = {omega_n:.2f} rad/s")
print()

# 2. Decremento logaritmico
delta = 2 * np.pi * zeta / np.sqrt(1 - zeta**2)

print("2. DECREMENTO LOGARITMICO (delta):")
print(f"   delta = 2*pi*zeta / sqrt(1 - zeta^2)")
print(f"   delta = 2*pi*{zeta} / sqrt(1 - {zeta}^2)")
print(f"   delta = {2*np.pi*zeta:.4f} / {np.sqrt(1 - zeta**2):.4f}")
print(f"   delta = {delta:.4f}")
print()
print(f"   NOTA: Este valor es significativamente mayor que en estructuras")
print(f"         con bajo amortiguamiento. Indica decaimiento rapido.")
print()

# 3. Desplazamiento despues de 4 ciclos
# Para condiciones iniciales u(0)=u0, v(0)=0:
# u(t) = u0 * exp(-zeta*omega_n*t) * cos(omega_D*t)
# En t = 4*T_D (4 ciclos), cos(omega_D*t) = cos(8*pi) = 1
# u(4*T_D) = u0 * exp(-4*delta) (usando relacion con delta)

t_4cycles = N_cycles * T_D
u_4cycles_pico = u0 * np.exp(-N_cycles * delta)

print(f"3. DESPLAZAMIENTO DESPUES DE {N_cycles} CICLOS:")
print("   Dado que el sistema parte del reposo en u0, la respuesta es:")
print(f"   u(t) = u0 * exp(-zeta*omega_n*t) * cos(omega_D*t)")
print()
print(f"   En t = {N_cycles}*T_D = {t_4cycles} s:")
print(f"   cos(omega_D * {N_cycles}*T_D) = cos({N_cycles}*2*pi) = 1")
print()
print("   Usando la relacion de amplitudes:")
print(f"   u_{N_cycles} = u_0 * exp(-{N_cycles}*delta)")
print(f"   u_{N_cycles} = {u0} * exp(-{N_cycles} * {delta:.4f})")
print(f"   u_{N_cycles} = {u0} * exp({-N_cycles * delta:.4f})")
print(f"   u_{N_cycles} = {u0} * {np.exp(-N_cycles * delta):.4f}")
print(f"   u_{N_cycles} = {u_4cycles_pico:.2f} mm")
print()
print(f"   Reduccion: {(1 - u_4cycles_pico/u0)*100:.1f}% de la amplitud inicial")
print()

# =============================================================================
# GRAFICO DE DECAIMIENTO RAPIDO
# =============================================================================

# Simular vibracion libre
t = np.linspace(0, 6 * T_D, 500)

# Respuesta
u = u0 * np.exp(-zeta * omega_n * t) * np.cos(omega_D * t)
envelope = u0 * np.exp(-zeta * omega_n * t)

# Crear figura con comparacion de amortiguamientos
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))

# --- Panel izquierdo: Respuesta temporal ---
ax1.plot(t, u, 'b-', linewidth=1.5, label=f'Respuesta u(t), zeta={zeta*100:.0f}%')
ax1.plot(t, envelope, 'r--', linewidth=1.2, alpha=0.8,
         label=r'Envolvente $u_0 e^{-\zeta\omega_n t}$')
ax1.plot(t, -envelope, 'r--', linewidth=1.2, alpha=0.8)

# Marcar pico en 4 ciclos
ax1.plot(t_4cycles, u_4cycles_pico, 'go', markersize=10,
         label=f'$u_4$ = {u_4cycles_pico:.2f} mm', zorder=5)
ax1.annotate(f'{u_4cycles_pico:.2f} mm\n({(1-u_4cycles_pico/u0)*100:.0f}% reduccion)',
             xy=(t_4cycles, u_4cycles_pico),
             xytext=(t_4cycles+0.3, u_4cycles_pico+5),
             fontsize=9, arrowprops=dict(arrowstyle='->', color='green', lw=0.8))

ax1.set_xlabel('Tiempo (s)', fontsize=11)
ax1.set_ylabel('Desplazamiento (mm)', fontsize=11)
ax1.set_title(f'Vibracion Libre con Alto Amortiguamiento\n' +
              r'$\zeta$ = ' + f'{zeta*100:.0f}%, ' +
              r'$\delta$ = ' + f'{delta:.3f}', fontsize=11)
ax1.grid(True, alpha=0.3)
ax1.legend(loc='upper right', fontsize=9)
ax1.axhline(y=0, color='k', linewidth=0.5)
ax1.set_xlim([0, max(t)])
ax1.set_ylim([-u0*1.1, u0*1.1])

# --- Panel derecho: Comparacion de amortiguamientos ---
zetas_comp = [0.02, 0.05, 0.10, 0.15, 0.25]
colors = ['blue', 'green', 'orange', 'red', 'purple']

for z, color in zip(zetas_comp, colors):
    omega_n_z = omega_D / np.sqrt(1 - z**2)
    env_z = np.exp(-z * omega_n_z * t)
    style = '-' if z != zeta else '--'
    lw = 2 if z == zeta else 1
    ax2.plot(t, env_z, color=color, linestyle=style, linewidth=lw,
             label=r'$\zeta$ = ' + f'{z*100:.0f}%')

ax2.axhline(y=0.5, color='gray', linestyle=':', linewidth=1,
            label='50% reduccion')

ax2.set_xlabel('Tiempo (s)', fontsize=11)
ax2.set_ylabel('Envolvente normalizada u/u0', fontsize=11)
ax2.set_title('Comparacion de Tasas de Decaimiento\n' +
              f'(linea discontinua: zeta = {zeta*100:.0f}%)', fontsize=11)
ax2.grid(True, alpha=0.3)
ax2.legend(loc='upper right', fontsize=9)
ax2.set_xlim([0, max(t)])
ax2.set_ylim([0, 1.05])

plt.tight_layout()

# Guardar
output_path = "../figs/fig_problema_25_decaimiento_rapido.pdf"
plt.savefig(output_path, dpi=150, bbox_inches='tight')
print(f"Figura guardada: {output_path}")
plt.close()

# =============================================================================
# RESUMEN
# =============================================================================

print()
print("=" * 65)
print("RESUMEN")
print("=" * 65)
print(f"  Frecuencia natural omega_n = {omega_n:.2f} rad/s")
print(f"  Decremento logaritmico delta = {delta:.4f}")
print(f"  Desplazamiento en 4 ciclos u_4 = {u_4cycles_pico:.2f} mm")
print(f"  Reduccion: {(1 - u_4cycles_pico/u0)*100:.1f}% respecto a u0")
print()
print("  INTERPRETACION: Con zeta=15%, la amplitud se reduce al")
print(f"  {u_4cycles_pico/u0*100:.1f}% en solo 4 ciclos (2 segundos).")
print("  Esto es tipico de estructuras con sistemas de amortiguamiento")
print("  adicionales o materiales con alta disipacion interna.")
print()
