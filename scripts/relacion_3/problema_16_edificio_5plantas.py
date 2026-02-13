"""
Problema 16: Edificio de 5 plantas uniforme
===========================================
Analisis modal completo con masas efectivas.

Datos:
- m = 800 kg por planta
- k = 150 kN/m por entreplanta
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, '../../../scripts')
from libreria_dinamica import MDOF, shear_building_uniforme, frecuencias_shear_uniforme

# =============================================================================
# 1. Definicion del sistema
# =============================================================================
print("=" * 60)
print("PROBLEMA 16: EDIFICIO DE 5 PLANTAS UNIFORME")
print("=" * 60)

n = 5        # Numero de plantas
m = 800.0    # kg
k = 150e3    # N/m

# Construccion de matrices
M, K = shear_building_uniforme(n, m, k)

print("\n1) MATRICES DEL SISTEMA")
print("-" * 40)
print("Matriz de masa M (kg):")
print(M)
print("\nMatriz de rigidez K (N/m):")
print(K / 1000)  # Mostrar en kN/m

# =============================================================================
# 2. Frecuencias - Formula cerrada vs numerica
# =============================================================================
print("\n2) FRECUENCIAS NATURALES")
print("-" * 40)

# Formula cerrada
omega_closed = frecuencias_shear_uniforme(n, m, k)
print("Formula cerrada: w^2 = (2k/m)[1 - cos(jpi/(n+1))]")
print(f"2k/m = {2*k/m:.1f} s^-^2\n")

# Sistema MDOF
sistema = MDOF(M, K)

print(f"{'Modo':<6} {'w (rad/s)':<12} {'f (Hz)':<10} {'T (s)':<10}")
print("-" * 40)
for j in range(n):
    print(f"{j+1:<6} {sistema.omega[j]:<12.3f} {sistema.freq[j]:<10.3f} {sistema.T[j]:<10.3f}")

# =============================================================================
# 3. Modos de vibracion
# =============================================================================
print("\n3) MODOS DE VIBRACION (normalizados masa-unidad)")
print("-" * 40)
for j in range(n):
    modo_str = ", ".join([f"{v:.4f}" for v in sistema.phi[:, j]])
    print(f"Modo {j+1}: [{modo_str}]")

# =============================================================================
# 4. Masas efectivas
# =============================================================================
r = np.ones(n)
Gamma = sistema.factores_participacion(r)
M_ef, M_ef_pct, M_total = sistema.masas_efectivas(r)

print("\n4) FACTORES DE PARTICIPACION Y MASAS EFECTIVAS")
print("-" * 40)
print(f"{'Modo':<6} {'Gamma':<10} {'M_ef (kg)':<12} {'%':<8} {'% acum':<10}")
print("-" * 40)
acum = 0
for j in range(n):
    acum += M_ef_pct[j]
    print(f"{j+1:<6} {Gamma[j]:<10.2f} {M_ef[j]:<12.1f} {M_ef_pct[j]:<8.1f} {acum:<10.1f}")

print(f"\nMasa total: {M_total:.1f} kg")
print(f"Suma masas efectivas: {np.sum(M_ef):.1f} kg ({100*np.sum(M_ef)/M_total:.1f}%)")

# Modos necesarios para 90%
modos_90 = np.where(np.cumsum(M_ef_pct) >= 90)[0][0] + 1
print(f"\nModos necesarios para >=90%: {modos_90}")

# =============================================================================
# 5. Graficas
# =============================================================================
fig, axes = plt.subplots(1, 3, figsize=(15, 6))

# 5.1 Modos de vibracion
ax1 = axes[0]
plantas = np.arange(n + 1)  # 0 a n
colores = plt.cm.viridis(np.linspace(0, 0.8, n))

for j in range(n):
    modo_plot = np.concatenate([[0], sistema.phi[:, j] / np.max(np.abs(sistema.phi[:, j]))])
    ax1.plot(modo_plot, plantas, '-o', color=colores[j], linewidth=2,
             markersize=8, label=f'Modo {j+1} (f={sistema.freq[j]:.2f} Hz)')

ax1.axvline(x=0, color='k', linestyle='--', linewidth=0.5)
ax1.set_xlabel('Desplazamiento normalizado', fontsize=11)
ax1.set_ylabel('Planta', fontsize=11)
ax1.set_yticks(plantas)
ax1.set_yticklabels(['Base'] + [f'P{i}' for i in range(1, n+1)])
ax1.legend(loc='upper left', fontsize=9)
ax1.set_title('Modos de vibracion', fontsize=12, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.set_xlim(-1.3, 1.3)

# 5.2 Masas efectivas
ax2 = axes[1]
x_pos = np.arange(n)
bars = ax2.bar(x_pos, M_ef_pct, color=colores, edgecolor='black', linewidth=1.2)

# Linea de 90%
ax2.axhline(y=90, color='red', linestyle='--', linewidth=2, label='90% requerido')

# Linea de acumulado
acum_pct = np.cumsum(M_ef_pct)
ax2.plot(x_pos, acum_pct, 'ko-', linewidth=2, markersize=8, label='Acumulado')

ax2.set_xlabel('Modo', fontsize=11)
ax2.set_ylabel('Masa efectiva (%)', fontsize=11)
ax2.set_xticks(x_pos)
ax2.set_xticklabels([f'{i+1}' for i in range(n)])
ax2.legend(loc='right')
ax2.set_title('Participacion modal', fontsize=12, fontweight='bold')
ax2.set_ylim(0, 105)
ax2.grid(True, alpha=0.3, axis='y')

# Etiquetas
for i, (bar, pct) in enumerate(zip(bars, M_ef_pct)):
    if pct > 5:
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                 f'{pct:.1f}%', ha='center', fontsize=9, fontweight='bold')

# 5.3 Espectro de frecuencias
ax3 = axes[2]
ax3.stem(np.arange(1, n+1), sistema.freq, linefmt='b-', markerfmt='bo', basefmt='k-')
ax3.set_xlabel('Numero de modo', fontsize=11)
ax3.set_ylabel('Frecuencia (Hz)', fontsize=11)
ax3.set_title('Espectro de frecuencias naturales', fontsize=12, fontweight='bold')
ax3.set_xticks(np.arange(1, n+1))
ax3.grid(True, alpha=0.3)

# Tabla de frecuencias
textstr = '\n'.join([f'f{i+1} = {sistema.freq[i]:.2f} Hz' for i in range(n)])
props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
ax3.text(0.95, 0.95, textstr, transform=ax3.transAxes, fontsize=10,
         verticalalignment='top', horizontalalignment='right', bbox=props)

plt.tight_layout()
plt.savefig('../figs/fig_problema_16_edificio_5plantas.png', dpi=150, bbox_inches='tight')
plt.savefig('../figs/fig_problema_16_edificio_5plantas.pdf', bbox_inches='tight')
print("\n[Grafica guardada en figs/fig_problema_16_edificio_5plantas.png]")
plt.show()
