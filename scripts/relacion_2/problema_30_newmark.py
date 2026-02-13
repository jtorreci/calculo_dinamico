#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Problema 30: Integración Numérica por Método de Newmark
======================================================

Implementación y comparación de métodos de integración numérica:
- Método de Newmark (aceleración promedio)
- Método de diferencias centrales
- Solución analítica (para validación)
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, '../../../scripts')

from libreria_dinamica import newmark, diferencias_centrales, SDOF
from libreria_dinamica.utils import rampa

# =============================================================================
# DATOS DEL PROBLEMA
# =============================================================================

m = 1      # kg - Masa
k = 100    # N/m - Rigidez
c = 2      # N·s/m - Amortiguamiento

# Carga: rampa de 0 a F0 en t1 s, luego constante
F0 = 10    # N
t1 = 0.5   # s

# Parámetros de integración
dt = 0.05  # s - Paso de tiempo
t_final = 3.0  # s

# Condiciones iniciales
u0 = 0.0
v0 = 0.0

# =============================================================================
# CÁLCULOS
# =============================================================================

print("=" * 60)
print("PROBLEMA 30: MÉTODO DE NEWMARK")
print("=" * 60)

# Crear sistema SDOF
sistema = SDOF(m, k, c=c)
print(f"\nPropiedades del sistema:")
print(f"  omega_n = {sistema.omega_n:.2f} rad/s")
print(f"  T_n = {sistema.T_n:.3f} s")
print(f"  zeta = {sistema.zeta:.3f} ({sistema.zeta*100:.1f}%)")

# Verificar estabilidad
print(f"\nVerificación de estabilidad:")
print(f"  dt / T_n = {dt / sistema.T_n:.3f} (recomendado < 0.1)")
dt_critico_dc = 2 / sistema.omega_n
print(f"  dt_critico (dif. centrales) = {dt_critico_dc:.3f} s")
print(f"  dt = {dt} s {'< dt_critico (estable)' if dt < dt_critico_dc else '>= dt_critico (INESTABLE)'}")

# Vector de tiempos y fuerzas
t = np.arange(0, t_final + dt, dt)
F = rampa(t, F0, t1)

# Integración con Newmark (aceleración promedio)
print(f"\n--- Método de Newmark (gamma=0.5, beta=0.25) ---")
u_newmark, v_newmark, a_newmark = newmark(m, c, k, F, dt, u0, v0,
                                           gamma=0.5, beta=0.25)
print(f"  u(0.15 s) = {u_newmark[3]*1000:.2f} mm")
print(f"  u_max = {np.max(u_newmark)*1000:.2f} mm")
print(f"  u_final = {u_newmark[-1]*1000:.2f} mm")
print(f"  u_estatico = {F0/k*1000:.2f} mm")

# Integración con diferencias centrales
print(f"\n--- Método de diferencias centrales ---")
u_dc, v_dc, a_dc = diferencias_centrales(m, c, k, F, dt, u0, v0)
print(f"  u(0.15 s) = {u_dc[3]*1000:.2f} mm")
print(f"  u_max = {np.max(u_dc)*1000:.2f} mm")
print(f"  u_final = {u_dc[-1]*1000:.2f} mm")

# Comparación de resultados
print(f"\n--- Comparación en t = 0.15 s ---")
print(f"  Newmark: {u_newmark[3]*1000:.3f} mm")
print(f"  Dif. centrales: {u_dc[3]*1000:.3f} mm")
print(f"  Diferencia: {abs(u_newmark[3] - u_dc[3])*1000:.4f} mm ({abs(u_newmark[3] - u_dc[3])/u_newmark[3]*100:.2f}%)")

# Tabla de primeros pasos
print(f"\n--- Primeros pasos de integración (Newmark) ---")
print(f"{'n':>3} {'t [s]':>8} {'F [N]':>8} {'u [mm]':>10} {'v [mm/s]':>10} {'a [m/s²]':>10}")
print("-" * 55)
for i in range(min(7, len(t))):
    print(f"{i:>3} {t[i]:>8.3f} {F[i]:>8.2f} {u_newmark[i]*1000:>10.3f} {v_newmark[i]*1000:>10.3f} {a_newmark[i]:>10.3f}")

# =============================================================================
# GRÁFICAS
# =============================================================================

fig, axes = plt.subplots(2, 2, figsize=(12, 9))

# Subplot 1: Fuerza aplicada
ax1 = axes[0, 0]
ax1.plot(t, F, 'k-', linewidth=2)
ax1.fill_between(t, 0, F, alpha=0.3)
ax1.axvline(t1, color='red', linestyle='--', alpha=0.5, label=f'$t_1$ = {t1} s')
ax1.set_xlabel('Tiempo [s]', fontsize=11)
ax1.set_ylabel('Fuerza [N]', fontsize=11)
ax1.set_title('Carga Rampa', fontsize=12, fontweight='bold')
ax1.legend()
ax1.grid(True, alpha=0.3)
ax1.set_xlim([0, t_final])

# Subplot 2: Desplazamiento
ax2 = axes[0, 1]
ax2.plot(t, u_newmark * 1000, 'b-', linewidth=2, label='Newmark ($\\beta$=0.25)')
ax2.plot(t, u_dc * 1000, 'r--', linewidth=2, label='Dif. centrales')
ax2.axhline(F0/k * 1000, color='gray', linestyle=':', label='$u_{est}$ = F₀/k')
ax2.set_xlabel('Tiempo [s]', fontsize=11)
ax2.set_ylabel('Desplazamiento [mm]', fontsize=11)
ax2.set_title('Respuesta de Desplazamiento', fontsize=12, fontweight='bold')
ax2.legend(loc='lower right')
ax2.grid(True, alpha=0.3)
ax2.set_xlim([0, t_final])

# Subplot 3: Velocidad
ax3 = axes[1, 0]
ax3.plot(t, v_newmark * 1000, 'b-', linewidth=2, label='Newmark')
ax3.plot(t, v_dc * 1000, 'r--', linewidth=2, label='Dif. centrales')
ax3.axhline(0, color='gray', linestyle='-', alpha=0.3)
ax3.set_xlabel('Tiempo [s]', fontsize=11)
ax3.set_ylabel('Velocidad [mm/s]', fontsize=11)
ax3.set_title('Velocidad', fontsize=12, fontweight='bold')
ax3.legend()
ax3.grid(True, alpha=0.3)
ax3.set_xlim([0, t_final])

# Subplot 4: Aceleración
ax4 = axes[1, 1]
ax4.plot(t, a_newmark, 'b-', linewidth=2, label='Newmark')
ax4.plot(t, a_dc, 'r--', linewidth=2, label='Dif. centrales')
ax4.axhline(0, color='gray', linestyle='-', alpha=0.3)
ax4.set_xlabel('Tiempo [s]', fontsize=11)
ax4.set_ylabel('Aceleración [m/s²]', fontsize=11)
ax4.set_title('Aceleración', fontsize=12, fontweight='bold')
ax4.legend()
ax4.grid(True, alpha=0.3)
ax4.set_xlim([0, t_final])

plt.suptitle(f'Integración Numérica: m={m} kg, k={k} N/m, $\\zeta$={sistema.zeta:.0%}, $\\Delta t$={dt} s',
             fontsize=13, fontweight='bold', y=1.02)

plt.tight_layout()
plt.savefig('../figs/fig_problema_30_newmark.pdf', dpi=150, bbox_inches='tight')
plt.close()

print(f"\nFigura guardada: figs/fig_problema_30_newmark.pdf")
