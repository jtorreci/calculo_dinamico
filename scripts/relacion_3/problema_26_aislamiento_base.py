"""
Problema 26: Aislamiento sismico de base
========================================
Analisis del efecto del alargamiento del periodo mediante aisladores.

Datos:
- Superestructura: ms = 100000 kg, ks = 50 MN/m
- Sistema de aislamiento: mb = 20000 kg, kb = 2.0 MN/m, zetab = 15%
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, '../../../scripts')
from libreria_dinamica import MDOF

# =============================================================================
# 1. Sistema de base fija (sin aislamiento)
# =============================================================================
print("=" * 60)
print("PROBLEMA 26: AISLAMIENTO SISMICO DE BASE")
print("=" * 60)

# Parametros de la superestructura
ms = 100000.0  # kg
ks = 50e6      # N/m

# Frecuencia de base fija
omega_fix = np.sqrt(ks / ms)
f_fix = omega_fix / (2 * np.pi)
T_fix = 1 / f_fix

print("\n1) ESTRUCTURA DE BASE FIJA")
print("-" * 40)
print(f"wfijo = sqrt(ks/ms) = sqrt({ks/1e6:.1f}x10^6/{ms}) = {omega_fix:.2f} rad/s")
print(f"ffijo = {f_fix:.2f} Hz")
print(f"Tfijo = {T_fix:.2f} s")

# =============================================================================
# 2. Sistema aislado (2DOF)
# =============================================================================
print("\n2) SISTEMA AISLADO (2DOF)")
print("-" * 40)

# Parametros del sistema de aislamiento
mb = 20000.0   # kg
kb = 2.0e6     # N/m
zeta_b = 0.15  # 15%

# Matrices del sistema (coordenadas: ub, us-ub)
# Masa total sobre el aislador: mt = mb + ms
mt = mb + ms

# Sistema simplificado (superestructura rigida)
# El DOF es solo el desplazamiento de la base
omega_iso = np.sqrt(kb / mt)
f_iso = omega_iso / (2 * np.pi)
T_iso = 1 / f_iso

print("Aproximacion de superestructura rigida:")
print(f"waislado ~ sqrt(kb/(mb+ms)) = sqrt({kb/1e6:.1f}x10^6/{mt}) = {omega_iso:.2f} rad/s")
print(f"faislado = {f_iso:.2f} Hz")
print(f"Taislado = {T_iso:.2f} s")
print(f"\nAlargamiento del periodo: {T_iso/T_fix:.1f}x (de {T_fix:.2f} s a {T_iso:.2f} s)")

# =============================================================================
# 3. Transmisibilidad
# =============================================================================
print("\n3) TRANSMISIBILIDAD DEL AISLADOR")
print("-" * 40)

# Ratio de frecuencias (excitacion a frecuencia de base fija)
r = omega_fix / omega_iso
zeta = zeta_b

print(f"Ratio r = wexc/waislado = {omega_fix:.2f}/{omega_iso:.2f} = {r:.2f}")

# Transmisibilidad
TR_num = np.sqrt(1 + (2*zeta*r)**2)
TR_den = np.sqrt((1 - r**2)**2 + (2*zeta*r)**2)
TR = TR_num / TR_den

print(f"\nTransmisibilidad TR = sqrt[1+(2zetar)^2] / sqrt[(1-r^2)^2+(2zetar)^2]")
print(f"TR = sqrt[1+{(2*zeta*r)**2:.2f}] / sqrt[{(1-r**2)**2:.2f}+{(2*zeta*r)**2:.2f}]")
print(f"TR = {TR_num:.3f} / {TR_den:.3f} = {TR:.4f}")

# Reduccion de aceleracion
reduccion = (1 - TR) * 100
print(f"\nReduccion de aceleracion: {reduccion:.1f}%")

# =============================================================================
# 4. Respuesta a espectro sismico
# =============================================================================
print("\n4) RESPUESTA A ESPECTRO SISMICO")
print("-" * 40)

Sa_input = 4.0  # m/s^2 a frecuencia de base fija
a_transmitida = TR * Sa_input

print(f"Aceleracion espectral de entrada: Sa = {Sa_input} m/s^2")
print(f"Aceleracion transmitida a la superestructura: {a_transmitida:.2f} m/s^2")
print(f"Reduccion: de {Sa_input} m/s^2 a {a_transmitida:.2f} m/s^2 ({reduccion:.1f}%)")

# =============================================================================
# 5. Graficas
# =============================================================================
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 5.1 Curva de transmisibilidad
ax1 = axes[0, 0]
r_range = np.linspace(0.1, 8, 200)
zetas = [0.05, 0.10, 0.15, 0.20, 0.30]
colores = plt.cm.viridis(np.linspace(0, 0.8, len(zetas)))

for zeta_i, color in zip(zetas, colores):
    TR_i = np.sqrt(1 + (2*zeta_i*r_range)**2) / np.sqrt((1 - r_range**2)**2 + (2*zeta_i*r_range)**2)
    ax1.semilogy(r_range, TR_i, '-', color=color, linewidth=1.5, label=f'zeta = {zeta_i*100:.0f}%')

# Punto de operacion
ax1.plot(r, TR, 'ro', markersize=12, markeredgecolor='black', markeredgewidth=2,
         label=f'Operacion (r={r:.1f})')

ax1.axhline(y=1, color='k', linestyle='--', linewidth=1)
ax1.axvline(x=np.sqrt(2), color='gray', linestyle=':', linewidth=1.5)
ax1.text(np.sqrt(2)+0.1, 0.5, 'r=sqrt2', fontsize=10, color='gray')

ax1.set_xlabel('Ratio de frecuencias r = w/wn', fontsize=11)
ax1.set_ylabel('Transmisibilidad TR', fontsize=11)
ax1.set_title('Curva de transmisibilidad', fontsize=12, fontweight='bold')
ax1.legend(loc='upper right')
ax1.set_xlim(0, 8)
ax1.set_ylim(0.01, 10)
ax1.grid(True, alpha=0.3, which='both')

# 5.2 Comparacion de periodos
ax2 = axes[0, 1]
periodos = [T_fix, T_iso]
labels = ['Base fija\n(sin aislamiento)', 'Base aislada\n(con aisladores)']
colors = ['coral', 'steelblue']
bars = ax2.bar(labels, periodos, color=colors, edgecolor='black', linewidth=2)

ax2.set_ylabel('Periodo fundamental T (s)', fontsize=11)
ax2.set_title('Alargamiento del periodo', fontsize=12, fontweight='bold')
for bar, T in zip(bars, periodos):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
             f'T = {T:.2f} s', ha='center', fontsize=12, fontweight='bold')
ax2.set_ylim(0, 2)

# Flecha de alargamiento
ax2.annotate('', xy=(1, T_iso-0.1), xytext=(0, T_fix+0.1),
             arrowprops=dict(arrowstyle='->', color='green', lw=2))
ax2.text(0.5, (T_fix+T_iso)/2, f'{T_iso/T_fix:.1f}x', fontsize=14,
         fontweight='bold', color='green', ha='center')

# 5.3 Espectro de respuesta tipico con ambos periodos
ax3 = axes[1, 0]
T_range = np.linspace(0.05, 3, 200)

# Espectro tipo EC8 simplificado
Tb, Tc, Td = 0.15, 0.5, 2.0
ag = 0.35 * 9.81  # PGA
S = 1.0
eta = 1.0  # 5% damping

def espectro_ec8(T, ag, S, Tb, Tc, Td, eta=1.0):
    Sa = np.zeros_like(T)
    mask1 = T < Tb
    mask2 = (T >= Tb) & (T < Tc)
    mask3 = (T >= Tc) & (T < Td)
    mask4 = T >= Td

    Sa[mask1] = ag * S * (1 + T[mask1]/Tb * (eta*2.5 - 1))
    Sa[mask2] = ag * S * eta * 2.5
    Sa[mask3] = ag * S * eta * 2.5 * Tc / T[mask3]
    Sa[mask4] = ag * S * eta * 2.5 * Tc * Td / T[mask4]**2
    return Sa

Sa_spectrum = espectro_ec8(T_range, ag, S, Tb, Tc, Td)
ax3.plot(T_range, Sa_spectrum, 'b-', linewidth=2, label='Espectro elastico (5%)')

# Marcar periodos
ax3.axvline(x=T_fix, color='coral', linestyle='--', linewidth=2, label=f'Tfijo = {T_fix:.2f} s')
ax3.axvline(x=T_iso, color='steelblue', linestyle='--', linewidth=2, label=f'Taislado = {T_iso:.2f} s')

# Puntos de respuesta
Sa_fix = np.interp(T_fix, T_range, Sa_spectrum)
Sa_iso_base = np.interp(T_iso, T_range, Sa_spectrum)
ax3.plot(T_fix, Sa_fix, 'o', color='coral', markersize=12, markeredgecolor='black')
ax3.plot(T_iso, Sa_iso_base, 's', color='steelblue', markersize=12, markeredgecolor='black')

ax3.set_xlabel('Periodo T (s)', fontsize=11)
ax3.set_ylabel('Aceleracion espectral Sa (m/s^2)', fontsize=11)
ax3.set_title('Reduccion espectral por alargamiento del periodo', fontsize=12, fontweight='bold')
ax3.legend(loc='upper right')
ax3.grid(True, alpha=0.3)
ax3.set_xlim(0, 3)

# Anotacion de reduccion
ax3.annotate('', xy=(T_iso, Sa_iso_base), xytext=(T_fix, Sa_fix),
             arrowprops=dict(arrowstyle='->', color='green', lw=2))

# 5.4 Esquema del sistema
ax4 = axes[1, 1]
ax4.set_xlim(0, 10)
ax4.set_ylim(0, 10)
ax4.set_aspect('equal')
ax4.axis('off')
ax4.set_title('Esquema del sistema aislado', fontsize=12, fontweight='bold')

# Suelo
ax4.fill_between([0, 10], 0, 1, color='brown', alpha=0.5, hatch='///')
ax4.plot([0, 10], [1, 1], 'k-', linewidth=2)

# Aisladores (resortes)
for x in [2.5, 7.5]:
    y_base = 1.0
    y_top = 2.5
    n_coils = 5
    dy = (y_top - y_base) / (n_coils * 2)
    xs = [x]
    ys = [y_base]
    for i in range(n_coils * 2):
        xs.append(x + (0.3 if i % 2 == 0 else -0.3))
        ys.append(y_base + (i + 1) * dy)
    xs.append(x)
    ys.append(y_top)
    ax4.plot(xs, ys, 'b-', linewidth=2)

    # Amortiguador al lado
    ax4.plot([x+0.8, x+0.8], [y_base, (y_base+y_top)/2-0.2], 'k-', linewidth=2)
    ax4.plot([x+0.8, x+0.8], [(y_base+y_top)/2+0.2, y_top], 'k-', linewidth=2)
    rect = plt.Rectangle((x+0.6, (y_base+y_top)/2-0.2), 0.4, 0.4,
                          fill=True, facecolor='gray', edgecolor='black', linewidth=2)
    ax4.add_patch(rect)

# Plataforma de aislamiento
rect = plt.Rectangle((1, 2.5), 8, 1, fill=True, facecolor='gray',
                      edgecolor='black', linewidth=2, alpha=0.7)
ax4.add_patch(rect)
ax4.text(5, 3, f'mb = {mb/1000:.0f} t', ha='center', va='center', fontsize=11, fontweight='bold')

# Superestructura
rect = plt.Rectangle((2, 3.5), 6, 5, fill=True, facecolor='lightblue',
                      edgecolor='black', linewidth=2, alpha=0.8)
ax4.add_patch(rect)
ax4.text(5, 6, f'ms = {ms/1000:.0f} t\nks = {ks/1e6:.0f} MN/m',
         ha='center', va='center', fontsize=11, fontweight='bold')

# Etiquetas
ax4.text(1, 1.8, f'kb = {kb/1e6:.0f} MN/m\nzetab = {zeta_b*100:.0f}%',
         fontsize=10, fontweight='bold', color='blue')

# Resultados
textstr = (f'Periodo base fija: Tfijo = {T_fix:.2f} s\n'
           f'Periodo aislado: Taislado = {T_iso:.2f} s\n'
           f'Alargamiento: {T_iso/T_fix:.1f}x\n'
           f'Transmisibilidad: TR = {TR:.3f}\n'
           f'Reduccion: {reduccion:.1f}%')
props = dict(boxstyle='round', facecolor='wheat', alpha=0.9)
ax4.text(9.5, 9, textstr, fontsize=10, verticalalignment='top',
         horizontalalignment='right', bbox=props)

plt.tight_layout()
plt.savefig('../figs/fig_problema_26_aislamiento_base.png', dpi=150, bbox_inches='tight')
plt.savefig('../figs/fig_problema_26_aislamiento_base.pdf', bbox_inches='tight')
print("\n[Grafica guardada en figs/fig_problema_26_aislamiento_base.png]")
plt.show()
