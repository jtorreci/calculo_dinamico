#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Problema 04: Caracterizacion Experimental mediante Decremento Logaritmico
=========================================================================

Torre de telecomunicaciones - ensayo de vibracion libre.
Calcula decremento logaritmico, razon de amortiguamiento y ciclos
para reduccion del 50% de amplitud.

Ejecutar: python problema_04_decremento_logaritmico.py
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Backend no interactivo
import matplotlib.pyplot as plt

# =============================================================================
# DATOS DEL PROBLEMA
# =============================================================================

u0 = 10.0   # mm - Amplitud maxima inicial
u4 = 7.5    # mm - Amplitud del 4to pico
N = 4       # Numero de ciclos entre mediciones
omega_n = 5.0  # rad/s - Frecuencia natural (para pregunta 3)

# =============================================================================
# SOLUCION
# =============================================================================

print("=" * 65)
print("PROBLEMA 04: DECREMENTO LOGARITMICO - TORRE DE TELECOMUNICACIONES")
print("=" * 65)
print()

print("Datos del problema:")
print(f"  Amplitud inicial u0 = {u0} mm")
print(f"  Amplitud despues de {N} ciclos u{N} = {u4} mm")
print(f"  Frecuencia natural omega_n = {omega_n} rad/s")
print()

# 1. Decremento logaritmico
ratio = u0 / u4
delta = (1/N) * np.log(ratio)

print("1. DECREMENTO LOGARITMICO (delta):")
print(f"   delta = (1/N) * ln(u0/u{N})")
print(f"   delta = (1/{N}) * ln({u0}/{u4})")
print(f"   delta = (1/{N}) * ln({ratio:.4f})")
print(f"   delta = (1/{N}) * {np.log(ratio):.4f}")
print(f"   delta = {delta:.4f}")
print()

# 2. Razon de amortiguamiento
# Formula exacta: zeta = delta / sqrt((2*pi)^2 + delta^2)
denominator = np.sqrt((2*np.pi)**2 + delta**2)
zeta = delta / denominator

# Aproximacion para zeta pequeno: delta ~ 2*pi*zeta
zeta_approx = delta / (2 * np.pi)

print("2. RAZON DE AMORTIGUAMIENTO (zeta):")
print("   Formula exacta:")
print(f"   zeta = delta / sqrt((2*pi)^2 + delta^2)")
print(f"   zeta = {delta:.4f} / sqrt({(2*np.pi)**2:.3f} + {delta**2:.6f})")
print(f"   zeta = {delta:.4f} / sqrt({(2*np.pi)**2 + delta**2:.4f})")
print(f"   zeta = {delta:.4f} / {denominator:.4f}")
print(f"   zeta = {zeta:.4f} = {zeta*100:.2f}%")
print()
print("   Verificacion con aproximacion (delta ~ 2*pi*zeta para zeta pequeno):")
print(f"   zeta_approx = delta/(2*pi) = {delta:.4f}/{2*np.pi:.4f} = {zeta_approx:.4f}")
print(f"   Diferencia: {abs(zeta - zeta_approx)/zeta*100:.2f}%")
print()

# 3. Ciclos para reduccion del 50%
# u_Nx / u0 = exp(-Nx * delta) = 0.5
# -Nx * delta = ln(0.5)
# Nx = -ln(0.5) / delta = ln(2) / delta
Nx = np.log(2) / delta

print("3. CICLOS PARA REDUCCION AL 50%:")
print("   Condicion: u_Nx / u0 = 0.5")
print("   exp(-Nx * delta) = 0.5")
print("   -Nx * delta = ln(0.5) = -0.693")
print(f"   Nx = ln(2) / delta = 0.693 / {delta:.4f}")
print(f"   Nx = {Nx:.2f} ciclos")
print()

# Tiempo correspondiente
T_n = 2 * np.pi / omega_n
T_d = T_n / np.sqrt(1 - zeta**2)  # Periodo amortiguado
t_50 = Nx * T_d

print(f"   Tiempo para 50% de reduccion:")
print(f"   T_n = 2*pi/omega_n = {T_n:.3f} s")
print(f"   T_d = T_n/sqrt(1-zeta^2) = {T_d:.3f} s")
print(f"   t_50% = Nx * T_d = {Nx:.2f} * {T_d:.3f} = {t_50:.2f} s")
print()

# =============================================================================
# GRAFICO DE DECAIMIENTO
# =============================================================================

# Simular vibracion libre
omega_d = omega_n * np.sqrt(1 - zeta**2)
t = np.linspace(0, 15 * T_d, 1000)

# Normalizamos respecto a u0
u = np.exp(-zeta * omega_n * t) * np.cos(omega_d * t)
envelope = np.exp(-zeta * omega_n * t)

# Crear figura
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))

# --- Panel izquierdo: Vibracion libre ---
ax1.plot(t, u * u0, 'b-', linewidth=1.2, label='Respuesta u(t)')
ax1.plot(t, envelope * u0, 'r--', linewidth=1, alpha=0.7,
         label=r'Envolvente $u_0 e^{-\zeta\omega_n t}$')
ax1.plot(t, -envelope * u0, 'r--', linewidth=1, alpha=0.7)

# Marcar mediciones
t_peaks = [0, 4*T_d]
u_peaks = [u0, u4]
ax1.plot(t_peaks, u_peaks, 'go', markersize=8, label=f'Mediciones: $u_0$, $u_4$', zorder=5)
ax1.annotate(f'$u_0$ = {u0} mm', xy=(0, u0), xytext=(0.5, u0+1),
             fontsize=9, ha='left')
ax1.annotate(f'$u_4$ = {u4} mm', xy=(4*T_d, u4), xytext=(4*T_d+0.3, u4+1),
             fontsize=9, ha='left')

# Marcar 50%
t_half_idx = np.argmin(np.abs(envelope * u0 - 0.5*u0))
ax1.axhline(y=0.5*u0, color='orange', linestyle=':', linewidth=1, alpha=0.7)
ax1.axvline(x=t[t_half_idx], color='orange', linestyle=':', linewidth=1, alpha=0.7)
ax1.annotate(f'50% a ~{Nx:.1f} ciclos', xy=(t[t_half_idx], 0.5*u0),
             xytext=(t[t_half_idx]+1, 0.5*u0+1.5), fontsize=9,
             arrowprops=dict(arrowstyle='->', color='orange', lw=0.8))

ax1.set_xlabel('Tiempo (s)', fontsize=11)
ax1.set_ylabel('Amplitud (mm)', fontsize=11)
ax1.set_title(f'Vibracion Libre - Torre de Telecomunicaciones\n' +
              r'$\zeta$ = ' + f'{zeta*100:.2f}%, ' + r'$\delta$ = ' + f'{delta:.4f}',
              fontsize=11)
ax1.grid(True, alpha=0.3)
ax1.legend(loc='upper right', fontsize=9)
ax1.axhline(y=0, color='k', linewidth=0.5)
ax1.set_xlim([0, max(t)])

# --- Panel derecho: Decaimiento de picos ---
n_cycles = np.arange(0, 16)
amplitude_picos = u0 * np.exp(-n_cycles * delta)

ax2.semilogy(n_cycles, amplitude_picos, 'bo-', linewidth=1.5, markersize=6,
             label='Amplitud de picos')
ax2.axhline(y=0.5*u0, color='orange', linestyle='--', linewidth=1.5,
            label=f'50% de $u_0$ = {0.5*u0:.1f} mm')
ax2.axvline(x=Nx, color='orange', linestyle=':', linewidth=1)

# Marcar puntos de medicion
ax2.plot([0, 4], [u0, u4], 'gs', markersize=10, label='Datos experimentales', zorder=5)

ax2.set_xlabel('Numero de ciclos N', fontsize=11)
ax2.set_ylabel('Amplitud de pico (mm)', fontsize=11)
ax2.set_title(f'Decaimiento Logaritmico\n' +
              r'$N_{50\%}$ = ' + f'{Nx:.2f} ciclos',
              fontsize=11)
ax2.grid(True, alpha=0.3, which='both')
ax2.legend(loc='upper right', fontsize=9)
ax2.set_xlim([0, 15])

plt.tight_layout()

# Guardar
output_path = "../figs/fig_problema_04_decremento_log.pdf"
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
print(f"  Decremento logaritmico delta = {delta:.4f}")
print(f"  Razon de amortiguamiento zeta = {zeta:.4f} ({zeta*100:.2f}%)")
print(f"  Ciclos para 50% reduccion Nx = {Nx:.2f}")
print()
