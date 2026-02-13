#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Problema 27: Decremento Logarítmico en Vibración Libre
=====================================================

Identificación de amortiguamiento mediante el método del
decremento logarítmico.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, '../../../scripts')

from libreria_dinamica import SDOF
from libreria_dinamica.utils import decremento_logaritmico, encontrar_picos

# =============================================================================
# DATOS DEL PROBLEMA
# =============================================================================

# Amplitudes de picos consecutivos (mm/s²)
amplitudes = np.array([245, 218, 194, 173, 154, 137])
T_d = 0.48  # s - Período entre picos

# =============================================================================
# CÁLCULOS
# =============================================================================

print("=" * 60)
print("PROBLEMA 27: DECREMENTO LOGARÍTMICO")
print("=" * 60)

print(f"\nDatos medidos:")
print(f"  Período amortiguado T_d = {T_d} s")
print(f"  Amplitudes: {amplitudes}")

# Decrementos entre picos consecutivos
print(f"\n--- Decrementos logarítmicos individuales ---")
deltas = np.log(amplitudes[:-1] / amplitudes[1:])
for i, delta in enumerate(deltas):
    print(f"  delta_{i+1}-{i+2} = ln({amplitudes[i]}/{amplitudes[i+1]}) = {delta:.4f}")

# Decremento promedio
delta_promedio = np.mean(deltas)
print(f"\nDecremento promedio: delta = {delta_promedio:.4f}")

# Método alternativo: primer y último pico
n_ciclos = len(amplitudes) - 1
delta_total = np.log(amplitudes[0] / amplitudes[-1]) / n_ciclos
print(f"\nMétodo alternativo (n={n_ciclos} ciclos):")
print(f"  delta = (1/{n_ciclos})*ln({amplitudes[0]}/{amplitudes[-1]}) = {delta_total:.4f}")

# Calcular amortiguamiento
# Aproximación: zeta = delta / (2*pi)
zeta_aprox = delta_promedio / (2 * np.pi)

# Fórmula exacta: zeta = delta / sqrt(4*pi^2 + delta^2)
zeta_exacto = delta_promedio / np.sqrt(4 * np.pi**2 + delta_promedio**2)

print(f"\n--- Razón de amortiguamiento ---")
print(f"  Aproximación (zeta << 1): zeta = delta/(2*pi) = {zeta_aprox:.4f} ({zeta_aprox*100:.2f}%)")
print(f"  Fórmula exacta: zeta = delta/sqrt(4*pi^2 + delta^2) = {zeta_exacto:.4f} ({zeta_exacto*100:.2f}%)")
print(f"  Diferencia: {abs(zeta_aprox - zeta_exacto)/zeta_exacto*100:.2f}%")

# Frecuencia natural
f_d = 1 / T_d
omega_d = 2 * np.pi * f_d
omega_n = omega_d / np.sqrt(1 - zeta_exacto**2)
f_n = omega_n / (2 * np.pi)

print(f"\n--- Frecuencias ---")
print(f"  f_d = 1/T_d = {f_d:.3f} Hz")
print(f"  f_n = f_d / sqrt(1 - zeta^2) = {f_n:.3f} Hz")
print(f"  Diferencia f_n - f_d = {(f_n - f_d)*1000:.3f} mHz ({(f_n/f_d - 1)*100:.3f}%)")

# Ciclos para reducción al 10%
n_10pct = np.log(10) / delta_promedio
t_10pct = n_10pct * T_d
print(f"\n--- Reducción al 10% ---")
print(f"  Número de ciclos: n = ln(10)/delta = {n_10pct:.1f} ciclos")
print(f"  Tiempo: t = n * T_d = {t_10pct:.1f} s")

# =============================================================================
# SIMULACIÓN DE VIBRACIÓN LIBRE
# =============================================================================

# Crear sistema con los parámetros identificados
m = 1  # kg (arbitrario para la simulación)
k = m * omega_n**2
sistema = SDOF(m, k, zeta=zeta_exacto)

# Simular vibración libre
t = np.linspace(0, 4, 1000)
A0 = amplitudes[0]
u = A0 * np.exp(-zeta_exacto * omega_n * t) * np.cos(omega_d * t)
envolvente_sup = A0 * np.exp(-zeta_exacto * omega_n * t)
envolvente_inf = -envolvente_sup

# =============================================================================
# GRÁFICAS
# =============================================================================

fig, axes = plt.subplots(2, 2, figsize=(12, 9))

# Subplot 1: Datos medidos
ax1 = axes[0, 0]
t_picos = np.arange(len(amplitudes)) * T_d
ax1.stem(t_picos, amplitudes, linefmt='b-', markerfmt='bo', basefmt='gray')
ax1.plot(t_picos, amplitudes, 'r--', alpha=0.5)
ax1.set_xlabel('Tiempo [s]', fontsize=11)
ax1.set_ylabel('Amplitud [mm/s²]', fontsize=11)
ax1.set_title('Amplitudes Medidas', fontsize=12, fontweight='bold')
ax1.grid(True, alpha=0.3)

# Añadir anotaciones
for i, (ti, ai) in enumerate(zip(t_picos, amplitudes)):
    ax1.annotate(f'{ai}', xy=(ti, ai), xytext=(5, 5),
                 textcoords='offset points', fontsize=8)

# Subplot 2: Vibración libre simulada
ax2 = axes[0, 1]
ax2.plot(t, u, 'b-', linewidth=1.5, label='Respuesta')
ax2.plot(t, envolvente_sup, 'r--', linewidth=1, label='Envolvente')
ax2.plot(t, envolvente_inf, 'r--', linewidth=1)
ax2.scatter(t_picos, amplitudes, color='green', s=50, zorder=5, label='Medidas')
ax2.axhline(0, color='gray', linestyle='-', alpha=0.3)
ax2.set_xlabel('Tiempo [s]', fontsize=11)
ax2.set_ylabel('Amplitud [mm/s²]', fontsize=11)
ax2.set_title(f'Vibración Libre ($\\zeta$ = {zeta_exacto*100:.2f}%)', fontsize=12, fontweight='bold')
ax2.legend(loc='upper right')
ax2.grid(True, alpha=0.3)

# Subplot 3: Log de amplitudes (linealización)
ax3 = axes[1, 0]
ax3.semilogy(t_picos, amplitudes, 'bo-', linewidth=2, markersize=8)

# Línea de regresión
coef = np.polyfit(t_picos, np.log(amplitudes), 1)
t_fit = np.linspace(0, t_picos[-1], 100)
ax3.semilogy(t_fit, np.exp(coef[1]) * np.exp(coef[0] * t_fit), 'r--',
             label=f'Pendiente = {coef[0]:.3f} 1/s')

ax3.set_xlabel('Tiempo [s]', fontsize=11)
ax3.set_ylabel('ln(Amplitud)', fontsize=11)
ax3.set_title('Decaimiento Exponencial (Escala Log)', fontsize=12, fontweight='bold')
ax3.legend()
ax3.grid(True, alpha=0.3, which='both')

# Relación: pendiente = -zeta*omega_n
zeta_desde_pendiente = -coef[0] / omega_n
print(f"\n--- Verificación desde pendiente ---")
print(f"  Pendiente = {coef[0]:.4f} 1/s")
print(f"  zeta = -pendiente/omega_n = {zeta_desde_pendiente:.4f}")

# Subplot 4: Decrementos individuales
ax4 = axes[1, 1]
intervalos = [f'{i+1}-{i+2}' for i in range(len(deltas))]
colores = ['steelblue'] * len(deltas)
ax4.bar(intervalos, deltas, color=colores, edgecolor='black')
ax4.axhline(delta_promedio, color='red', linestyle='--', linewidth=2,
            label=f'$\\delta$ promedio = {delta_promedio:.4f}')
ax4.set_xlabel('Intervalo entre picos', fontsize=11)
ax4.set_ylabel('Decremento logarítmico $\\delta$', fontsize=11)
ax4.set_title('Decrementos Logarítmicos', fontsize=12, fontweight='bold')
ax4.legend()
ax4.grid(True, alpha=0.3, axis='y')

# Añadir valor en cada barra
for i, d in enumerate(deltas):
    ax4.text(i, d + 0.002, f'{d:.4f}', ha='center', fontsize=9)

plt.suptitle(f'Análisis de Decremento Logarítmico: $\\zeta$ = {zeta_exacto*100:.2f}%, $f_n$ = {f_n:.3f} Hz',
             fontsize=13, fontweight='bold', y=1.02)

plt.tight_layout()
plt.savefig('../figs/fig_problema_27_decremento.pdf', dpi=150, bbox_inches='tight')
plt.close()

print(f"\nFigura guardada: figs/fig_problema_27_decremento.pdf")
