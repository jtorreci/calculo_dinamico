"""
Problema 21: Combinacion modal CQC vs SRSS
==========================================
Comparacion de metodos de combinacion modal para respuesta sismica.

Datos:
- Sistema 3DOF uniforme
- zeta = 5%
- Espectro de aceleraciones dado
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, '../../../scripts')
from libreria_dinamica import MDOF, shear_building_uniforme

# =============================================================================
# 1. Definicion del sistema
# =============================================================================
print("=" * 60)
print("PROBLEMA 21: COMBINACION MODAL CQC vs SRSS")
print("=" * 60)

# Parametros del edificio 3DOF uniforme
n = 3
m = 1000.0   # kg
k = 200e3    # N/m
zeta = 0.05  # 5%

# Construccion del sistema
M, K = shear_building_uniforme(n, m, k)
sistema = MDOF(M, K)

print("\n1) PROPIEDADES MODALES")
print("-" * 40)
print(f"{'Modo':<6} {'w (rad/s)':<12} {'f (Hz)':<10} {'T (s)':<10}")
print("-" * 40)
for j in range(n):
    print(f"{j+1:<6} {sistema.omega[j]:<12.2f} {sistema.freq[j]:<10.2f} {sistema.T[j]:<10.3f}")

# Ratios de frecuencia
print("\nRatios de frecuencia:")
for i in range(n-1):
    print(f"w_{i+2}/w_{i+1} = {sistema.omega[i+1]/sistema.omega[i]:.2f}")

# =============================================================================
# 2. Espectro de aceleraciones
# =============================================================================
print("\n2) ESPECTRO DE ACELERACIONES")
print("-" * 40)

# Valores espectrales dados
Sa = np.array([2.5, 3.0, 2.8])  # m/s^2
print(f"Sa(T_1) = {Sa[0]} m/s^2")
print(f"Sa(T_2) = {Sa[1]} m/s^2")
print(f"Sa(T_3) = {Sa[2]} m/s^2")

# =============================================================================
# 3. Contribuciones modales
# =============================================================================
print("\n3) CONTRIBUCIONES MODALES MAXIMAS")
print("-" * 40)

# Factores de participacion
r = np.ones(n)
Gamma = sistema.factores_participacion(r)
print(f"Factores de participacion: Gamma = {Gamma}")

# Desplazamientos modales maximos (Sd = Sa/w^2)
Sd = Sa / sistema.omega**2
print(f"Desplazamientos espectrales Sd (mm): {Sd*1000}")

# Contribucion modal para cada DOF
x_modal = np.zeros((n, n))  # x_modal[dof, modo]
for r_mode in range(n):
    x_modal[:, r_mode] = Gamma[r_mode] * sistema.phi[:, r_mode] * Sd[r_mode]

print(f"\nDesplazamientos modales maximos (mm):")
print(f"{'DOF':<6}", end="")
for j in range(n):
    print(f"{'Modo '+str(j+1):<12}", end="")
print()
print("-" * 42)
for i in range(n):
    print(f"{i+1:<6}", end="")
    for j in range(n):
        print(f"{x_modal[i,j]*1000:<12.2f}", end="")
    print()

# =============================================================================
# 4. Combinacion SRSS
# =============================================================================
print("\n4) COMBINACION SRSS")
print("-" * 40)

x_srss = np.sqrt(np.sum(x_modal**2, axis=1))
print(f"x_SRSS = sqrt(Sum x_r^2)")
for i in range(n):
    print(f"x_{i+1}_SRSS = {x_srss[i]*1000:.2f} mm")

# =============================================================================
# 5. Coeficientes de correlacion CQC
# =============================================================================
print("\n5) COEFICIENTES DE CORRELACION CQC")
print("-" * 40)

def coef_cqc(omega_i, omega_j, zeta_i, zeta_j):
    """Coeficiente de correlacion CQC (Der Kiureghian)."""
    beta = omega_i / omega_j
    if beta > 1:
        beta = 1 / beta
    num = 8 * np.sqrt(zeta_i * zeta_j) * (zeta_i + beta * zeta_j) * beta**(3/2)
    den = (1 - beta**2)**2 + 4 * zeta_i * zeta_j * beta * (1 + beta**2) + 4 * (zeta_i**2 + zeta_j**2) * beta**2
    return num / den

# Matriz de correlacion
rho = np.zeros((n, n))
for i in range(n):
    for j in range(n):
        if i == j:
            rho[i, j] = 1.0
        else:
            rho[i, j] = coef_cqc(sistema.omega[i], sistema.omega[j], zeta, zeta)

print("Matriz de correlacion rho_ij:")
print(f"{'':>8}", end="")
for j in range(n):
    print(f"{'Modo '+str(j+1):>10}", end="")
print()
for i in range(n):
    print(f"Modo {i+1}:", end="")
    for j in range(n):
        print(f"{rho[i,j]:>10.4f}", end="")
    print()

# =============================================================================
# 6. Combinacion CQC
# =============================================================================
print("\n6) COMBINACION CQC")
print("-" * 40)

x_cqc = np.zeros(n)
for dof in range(n):
    suma = 0
    for i in range(n):
        for j in range(n):
            suma += rho[i, j] * x_modal[dof, i] * x_modal[dof, j]
    x_cqc[dof] = np.sqrt(suma)

print(f"x_CQC = sqrt(Sum_i Sum_j rho_i_j x_i x_j)")
for i in range(n):
    print(f"x_{i+1}_CQC = {x_cqc[i]*1000:.2f} mm")

# =============================================================================
# 7. Comparacion
# =============================================================================
print("\n7) COMPARACION SRSS vs CQC")
print("-" * 40)
print(f"{'DOF':<6} {'SRSS (mm)':<12} {'CQC (mm)':<12} {'Dif (%)':<10}")
print("-" * 40)
for i in range(n):
    dif = (x_cqc[i] - x_srss[i]) / x_srss[i] * 100
    print(f"{i+1:<6} {x_srss[i]*1000:<12.2f} {x_cqc[i]*1000:<12.2f} {dif:<10.1f}")

# =============================================================================
# 8. Graficas
# =============================================================================
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 8.1 Modos de vibracion
ax1 = axes[0, 0]
plantas = np.arange(n + 1)
colores = ['blue', 'red', 'green']
for j in range(n):
    modo_plot = np.concatenate([[0], sistema.phi[:, j] / np.max(np.abs(sistema.phi[:, j]))])
    ax1.plot(modo_plot, plantas, '-o', color=colores[j], linewidth=2,
             markersize=10, label=f'Modo {j+1} (f={sistema.freq[j]:.2f} Hz)')

ax1.axvline(x=0, color='k', linestyle='--', linewidth=0.5)
ax1.set_xlabel('Desplazamiento normalizado', fontsize=11)
ax1.set_ylabel('Planta', fontsize=11)
ax1.set_yticks(plantas)
ax1.set_yticklabels(['Base', 'P1', 'P2', 'P3'])
ax1.legend()
ax1.set_title('Modos de vibracion', fontsize=12, fontweight='bold')
ax1.grid(True, alpha=0.3)

# 8.2 Contribuciones modales por DOF
ax2 = axes[0, 1]
x_pos = np.arange(n)
width = 0.25
for j in range(n):
    ax2.bar(x_pos + j*width, np.abs(x_modal[:, j])*1000, width,
            label=f'Modo {j+1}', color=colores[j], alpha=0.8)

ax2.set_xlabel('DOF (planta)', fontsize=11)
ax2.set_ylabel('Desplazamiento modal |xᵣ| (mm)', fontsize=11)
ax2.set_xticks(x_pos + width)
ax2.set_xticklabels(['P1', 'P2', 'P3'])
ax2.legend()
ax2.set_title('Contribuciones modales', fontsize=12, fontweight='bold')
ax2.grid(True, alpha=0.3, axis='y')

# 8.3 Matriz de correlacion
ax3 = axes[1, 0]
im = ax3.imshow(rho, cmap='RdYlBu_r', vmin=0, vmax=1)
ax3.set_xticks(np.arange(n))
ax3.set_yticks(np.arange(n))
ax3.set_xticklabels([f'Modo {i+1}' for i in range(n)])
ax3.set_yticklabels([f'Modo {i+1}' for i in range(n)])
for i in range(n):
    for j in range(n):
        color = 'white' if rho[i,j] > 0.5 else 'black'
        ax3.text(j, i, f'{rho[i,j]:.3f}', ha='center', va='center', color=color, fontsize=11)
ax3.set_title('Matriz de correlacion rho_i_j (CQC)', fontsize=12, fontweight='bold')
plt.colorbar(im, ax=ax3)

# 8.4 Comparacion SRSS vs CQC
ax4 = axes[1, 1]
x_pos = np.arange(n)
width = 0.35
bars1 = ax4.bar(x_pos - width/2, x_srss*1000, width, label='SRSS', color='steelblue')
bars2 = ax4.bar(x_pos + width/2, x_cqc*1000, width, label='CQC', color='coral')

ax4.set_xlabel('DOF (planta)', fontsize=11)
ax4.set_ylabel('Desplazamiento maximo (mm)', fontsize=11)
ax4.set_xticks(x_pos)
ax4.set_xticklabels(['P1', 'P2', 'P3'])
ax4.legend()
ax4.set_title('Comparacion SRSS vs CQC', fontsize=12, fontweight='bold')
ax4.grid(True, alpha=0.3, axis='y')

# Etiquetas con diferencia
for i, (b1, b2) in enumerate(zip(bars1, bars2)):
    dif = (x_cqc[i] - x_srss[i]) / x_srss[i] * 100
    max_h = max(b1.get_height(), b2.get_height())
    ax4.text(i, max_h + 0.5, f'Δ={dif:+.1f}%', ha='center', fontsize=10)

plt.tight_layout()
plt.savefig('../figs/fig_problema_21_cqc_srss.png', dpi=150, bbox_inches='tight')
plt.savefig('../figs/fig_problema_21_cqc_srss.pdf', bbox_inches='tight')
print("\n[Grafica guardada en figs/fig_problema_21_cqc_srss.png]")
plt.show()

# =============================================================================
# 9. Cuando usar CQC
# =============================================================================
print("\n" + "=" * 60)
print("CONCLUSION: ¿CUANDO USAR CQC?")
print("=" * 60)
print("""
CQC es importante cuando las frecuencias estan cercanas (w_i/w_j < 1.5).

En este caso:
- w_2/w_1 = {:.2f} (separadas)
- w_3/w_2 = {:.2f} (separadas)

Los coeficientes de correlacion son pequenos (rho < 0.1), por lo que
SRSS y CQC dan resultados muy similares (diferencia < 1%).

Use CQC cuando:
1. Frecuencias cercanas (edificios con simetria, modos de torsion)
2. Alto amortiguamiento (aumenta la correlacion)
3. Modos acoplados por geometria irregular
""".format(sistema.omega[1]/sistema.omega[0], sistema.omega[2]/sistema.omega[1]))
