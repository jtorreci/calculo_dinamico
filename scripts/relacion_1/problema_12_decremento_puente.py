#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Problema 12: Determinacion Experimental del Amortiguamiento (Puente Atirantado)
===============================================================================

Ensayo de vibracion libre en puente atirantado.
Calcula decremento logaritmico, razon de amortiguamiento y frecuencia natural.

Ejecutar: python problema_12_decremento_puente.py
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Backend no interactivo
import matplotlib.pyplot as plt

# =============================================================================
# DATOS DEL PROBLEMA
# =============================================================================

u0 = 150.0   # mm - Amplitud inicial maxima
u10 = 90.0   # mm - Amplitud despues de 10 ciclos
N = 10       # Numero de ciclos entre mediciones
T_D = 2.5    # s - Periodo de vibracion amortiguada

# =============================================================================
# SOLUCION
# =============================================================================

print("=" * 65)
print("PROBLEMA 12: DECREMENTO LOGARITMICO - PUENTE ATIRANTADO")
print("=" * 65)
print()

print("Datos del problema:")
print(f"  Amplitud inicial u0 = {u0} mm")
print(f"  Amplitud despues de {N} ciclos u{N} = {u10} mm")
print(f"  Periodo de vibracion amortiguada T_D = {T_D} s")
print()

# 1. Decremento logaritmico
ratio = u0 / u10
delta = (1/N) * np.log(ratio)

print("1. DECREMENTO LOGARITMICO (delta):")
print(f"   delta = (1/N) * ln(u0/u{N})")
print(f"   delta = (1/{N}) * ln({u0}/{u10})")
print(f"   delta = (1/{N}) * ln({ratio:.4f})")
print(f"   delta = (1/{N}) * {np.log(ratio):.4f}")
print(f"   delta = {delta:.4f}")
print()

# 2. Razon de amortiguamiento (aproximacion para zeta pequeno)
# Aproximacion: delta ~ 2*pi*zeta => zeta ~ delta/(2*pi)
zeta_approx = delta / (2 * np.pi)

# Formula exacta: zeta = delta / sqrt((2*pi)^2 + delta^2)
zeta_exact = delta / np.sqrt((2*np.pi)**2 + delta**2)

print("2. RAZON DE AMORTIGUAMIENTO (zeta):")
print("   Usando aproximacion para zeta pequeno (delta ~ 2*pi*zeta):")
print(f"   zeta = delta / (2*pi)")
print(f"   zeta = {delta:.4f} / {2*np.pi:.4f}")
print(f"   zeta = {zeta_approx:.5f} = {zeta_approx*100:.3f}%")
print()
print("   Verificacion con formula exacta:")
print(f"   zeta_exact = {zeta_exact:.5f} = {zeta_exact*100:.3f}%")
print(f"   Diferencia: {abs(zeta_approx - zeta_exact)/zeta_exact*100:.3f}%")
print()

# Usamos zeta de la aproximacion (como indica el problema)
zeta = zeta_approx

# 3. Frecuencia circular natural no amortiguada
# omega_D = 2*pi/T_D
# omega_n = omega_D / sqrt(1 - zeta^2)
omega_D = 2 * np.pi / T_D
omega_n = omega_D / np.sqrt(1 - zeta**2)
f_n = omega_n / (2 * np.pi)
T_n = 2 * np.pi / omega_n

print("3. FRECUENCIA CIRCULAR NATURAL NO AMORTIGUADA (omega_n):")
print("   Primero, la frecuencia amortiguada:")
print(f"   omega_D = 2*pi/T_D = 2*pi/{T_D}")
print(f"   omega_D = {omega_D:.4f} rad/s")
print()
print("   Luego, despejamos omega_n de omega_D = omega_n*sqrt(1-zeta^2):")
print(f"   omega_n = omega_D / sqrt(1 - zeta^2)")
print(f"   omega_n = {omega_D:.4f} / sqrt(1 - ({zeta:.5f})^2)")
print(f"   omega_n = {omega_D:.4f} / sqrt({1 - zeta**2:.6f})")
print(f"   omega_n = {omega_D:.4f} / {np.sqrt(1 - zeta**2):.6f}")
print(f"   omega_n = {omega_n:.4f} rad/s")
print()
print(f"   Equivalente: f_n = {f_n:.4f} Hz, T_n = {T_n:.4f} s")
print()
print("   NOTA: Para amortiguamientos muy pequenos (zeta < 1%),")
print(f"         omega_n ~= omega_D con diferencia despreciable")
print(f"         ({abs(omega_n - omega_D)/omega_n*100:.4f}%)")
print()

# =============================================================================
# GRAFICO DE DECAIMIENTO
# =============================================================================

# Simular vibracion libre
t = np.linspace(0, 15 * T_D, 1000)

# Respuesta normalizada
u = np.exp(-zeta * omega_n * t) * np.cos(omega_D * t) * u0
envelope = np.exp(-zeta * omega_n * t) * u0

# Crear figura con dos paneles
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))

# --- Panel izquierdo: Respuesta temporal ---
ax1.plot(t, u, 'b-', linewidth=1.2, label='Respuesta u(t)')
ax1.plot(t, envelope, 'r--', linewidth=1, alpha=0.7,
         label=r'Envolvente $u_0 e^{-\zeta\omega_n t}$')
ax1.plot(t, -envelope, 'r--', linewidth=1, alpha=0.7)

# Marcar mediciones
ax1.plot([0, 10*T_D], [u0, u10], 'go', markersize=8,
         label='Mediciones experimentales', zorder=5)
ax1.annotate(f'$u_0$ = {u0:.0f} mm', xy=(0, u0), xytext=(1, u0+15),
             fontsize=9, ha='left')
ax1.annotate(f'$u_{{10}}$ = {u10:.0f} mm', xy=(10*T_D, u10),
             xytext=(10*T_D+1, u10+15), fontsize=9, ha='left')

ax1.set_xlabel('Tiempo (s)', fontsize=11)
ax1.set_ylabel('Desplazamiento (mm)', fontsize=11)
ax1.set_title(f'Vibracion Libre - Puente Atirantado\n' +
              r'$\zeta$ = ' + f'{zeta*100:.2f}%, ' +
              r'$T_D$ = ' + f'{T_D} s', fontsize=11)
ax1.grid(True, alpha=0.3)
ax1.legend(loc='upper right', fontsize=9)
ax1.axhline(y=0, color='k', linewidth=0.5)
ax1.set_xlim([0, 40])

# --- Panel derecho: Decaimiento logaritmico ---
n_cycles = np.arange(0, 16)
amplitude_picos = u0 * np.exp(-n_cycles * delta)

ax2.semilogy(n_cycles, amplitude_picos, 'bo-', linewidth=1.5, markersize=6,
             label='Amplitud de picos')

# Marcar puntos de medicion
ax2.plot([0, 10], [u0, u10], 'gs', markersize=10,
         label='Datos experimentales', zorder=5)

# Linea de regresion en escala log
ax2.plot(n_cycles, u0 * np.exp(-n_cycles * delta), 'r--', linewidth=1,
         alpha=0.7, label=r'Ajuste: $u_N = u_0 e^{-N\delta}$')

ax2.set_xlabel('Numero de ciclos N', fontsize=11)
ax2.set_ylabel('Amplitud de pico (mm)', fontsize=11)
ax2.set_title(f'Decaimiento Logaritmico\n' +
              r'$\delta$ = ' + f'{delta:.4f}', fontsize=11)
ax2.grid(True, alpha=0.3, which='both')
ax2.legend(loc='upper right', fontsize=9)
ax2.set_xlim([0, 15])
ax2.set_ylim([50, 200])

plt.tight_layout()

# Guardar
output_path = "../figs/fig_problema_12_puente_decremento.pdf"
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
print(f"  Razon de amortiguamiento zeta = {zeta*100:.3f}% (~0.81%)")
print(f"  Frecuencia amortiguada omega_D = {omega_D:.4f} rad/s")
print(f"  Frecuencia natural omega_n = {omega_n:.4f} rad/s (~2.51 rad/s)")
print()
