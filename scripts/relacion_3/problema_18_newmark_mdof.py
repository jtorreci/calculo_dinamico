"""
Problema 18: Integracion temporal MDOF por Newmark
=================================================
Sistema 2DOF con amortiguamiento de Rayleigh bajo impulso.

Datos:
- m1 = m2 = 1000 kg
- k1 = k2 = 200 kN/m
- zeta1 = zeta2 = 5%
- Impulso F2 = 5000 N durante 0 <= t <= 0.1 s
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, '../../../scripts')
from libreria_dinamica import MDOF, shear_building, amortiguamiento_rayleigh, newmark_mdof

# =============================================================================
# 1. Definicion del sistema
# =============================================================================
print("=" * 60)
print("PROBLEMA 18: INTEGRACION NEWMARK MDOF")
print("=" * 60)

# Parametros
m = np.array([1000.0, 1000.0])  # kg
k = np.array([200e3, 200e3])     # N/m
zeta = 0.05                      # 5%

# Construccion de matrices
M, K = shear_building(m, k)
sistema = MDOF(M, K)

print("\n1) PROPIEDADES MODALES")
print("-" * 40)
print(f"w_1 = {sistema.omega[0]:.3f} rad/s  (T_1 = {sistema.T[0]:.3f} s)")
print(f"w_2 = {sistema.omega[1]:.3f} rad/s  (T_2 = {sistema.T[1]:.3f} s)")

# =============================================================================
# 2. Amortiguamiento de Rayleigh
# =============================================================================
print("\n2) AMORTIGUAMIENTO DE RAYLEIGH")
print("-" * 40)

omega1, omega2 = sistema.omega[0], sistema.omega[1]
C = amortiguamiento_rayleigh(M, K, omega1, omega2, zeta, zeta)

# Coeficientes alpha y beta
alpha = 2 * zeta * omega1 * omega2 / (omega1 + omega2)
beta = 2 * zeta / (omega1 + omega2)

print(f"alpha = {alpha:.4f} s^-^1")
print(f"beta = {beta:.6f} s")
print(f"\nMatriz C = alphaM + betaK (N*s/m):")
print(C)

# Verificacion de amortiguamientos modales
C_modal = sistema.phi.T @ C @ sistema.phi
print(f"\nAmortiguamiento modal c_1_1 = {C_modal[0,0]:.2f} -> zeta_1 = {C_modal[0,0]/(2*omega1):.3f}")
print(f"Amortiguamiento modal c_2_2 = {C_modal[1,1]:.2f} -> zeta_2 = {C_modal[1,1]/(2*omega2):.3f}")

# =============================================================================
# 3. Definicion de la carga
# =============================================================================
print("\n3) CARGA APLICADA")
print("-" * 40)

dt = 0.01        # Paso temporal (s)
t_final = 2.0    # Tiempo final (s)
t = np.arange(0, t_final + dt, dt)
n_steps = len(t)

# Impulso en DOF 2
F = np.zeros((2, n_steps))
F0 = 5000.0  # N
t_impulse = 0.1  # s
F[1, t <= t_impulse] = F0

print(f"Impulso F_2 = {F0} N durante t  in  [0, {t_impulse}] s")
print(f"Paso temporal Deltat = {dt} s ({n_steps} pasos)")

# =============================================================================
# 4. Integracion de Newmark
# =============================================================================
print("\n4) INTEGRACION DE NEWMARK")
print("-" * 40)

# Condiciones iniciales
u0 = np.zeros(2)
v0 = np.zeros(2)

# Parametros de Newmark (aceleracion promedio)
gamma = 0.5
beta_newmark = 0.25

print(f"Parametros: gamma = {gamma}, beta = {beta_newmark} (aceleracion promedio)")

# Ejecutar integracion
u, v, a = newmark_mdof(M, C, K, F, dt, u0, v0, gamma, beta_newmark)

# =============================================================================
# 5. Resultados
# =============================================================================
print("\n5) RESULTADOS")
print("-" * 40)

# Maximos
idx_max_u1 = np.argmax(np.abs(u[0, :]))
idx_max_u2 = np.argmax(np.abs(u[1, :]))

print(f"{'Tiempo (s)':<12} {'x_1 (mm)':<12} {'x_2 (mm)':<12}")
print("-" * 36)
for ti in [0.1, 0.2, 0.5, 1.0, 2.0]:
    idx = int(ti / dt)
    print(f"{t[idx]:<12.1f} {u[0,idx]*1000:<12.2f} {u[1,idx]*1000:<12.2f}")

print(f"\nMaximos:")
print(f"x_1_max = {np.max(np.abs(u[0,:]))*1000:.2f} mm en t = {t[idx_max_u1]:.2f} s")
print(f"x_2_max = {np.max(np.abs(u[1,:]))*1000:.2f} mm en t = {t[idx_max_u2]:.2f} s")

# Verificacion del decaimiento
print("\n6) VERIFICACION DEL DECAIMIENTO")
print("-" * 40)
delta = 2 * np.pi * zeta
print(f"Decremento logaritmico delta = 2pizeta = {delta:.4f}")
print(f"Tras 10 ciclos del modo 1 ({10*sistema.T[0]:.2f} s):")
print(f"  Amplitud relativa esperada: e^(-10delta) = {np.exp(-10*delta)*100:.1f}%")

# =============================================================================
# 6. Graficas
# =============================================================================
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 6.1 Desplazamientos
ax1 = axes[0, 0]
ax1.plot(t, u[0, :] * 1000, 'b-', linewidth=1.5, label='x_1(t) - Planta 1')
ax1.plot(t, u[1, :] * 1000, 'r-', linewidth=1.5, label='x_2(t) - Planta 2')
ax1.axvline(x=t_impulse, color='g', linestyle='--', linewidth=1, label=f'Fin impulso (t={t_impulse} s)')
ax1.set_xlabel('Tiempo (s)', fontsize=11)
ax1.set_ylabel('Desplazamiento (mm)', fontsize=11)
ax1.set_title('Respuesta en desplazamiento', fontsize=12, fontweight='bold')
ax1.legend()
ax1.grid(True, alpha=0.3)

# 6.2 Velocidades
ax2 = axes[0, 1]
ax2.plot(t, v[0, :], 'b-', linewidth=1.5, label='ẋ_1(t)')
ax2.plot(t, v[1, :], 'r-', linewidth=1.5, label='ẋ_2(t)')
ax2.axvline(x=t_impulse, color='g', linestyle='--', linewidth=1)
ax2.set_xlabel('Tiempo (s)', fontsize=11)
ax2.set_ylabel('Velocidad (m/s)', fontsize=11)
ax2.set_title('Respuesta en velocidad', fontsize=12, fontweight='bold')
ax2.legend()
ax2.grid(True, alpha=0.3)

# 6.3 Carga aplicada
ax3 = axes[1, 0]
ax3.plot(t, F[1, :] / 1000, 'g-', linewidth=2)
ax3.fill_between(t, 0, F[1, :] / 1000, alpha=0.3, color='green')
ax3.set_xlabel('Tiempo (s)', fontsize=11)
ax3.set_ylabel('Fuerza (kN)', fontsize=11)
ax3.set_title('Carga aplicada en DOF 2', fontsize=12, fontweight='bold')
ax3.grid(True, alpha=0.3)
ax3.set_ylim(-0.5, 6)

# 6.4 Envolvente de desplazamiento (log para ver decaimiento)
ax4 = axes[1, 1]
# Calcular envolvente mediante valor absoluto
from scipy.signal import hilbert
try:
    env1 = np.abs(hilbert(u[0, :]))
    env2 = np.abs(hilbert(u[1, :]))
    ax4.semilogy(t[t > t_impulse], env2[t > t_impulse] * 1000, 'r-', linewidth=1.5, label='|x_2(t)|')

    # Linea de decaimiento teorico
    t_decay = t[t > t_impulse]
    A0 = env2[int(t_impulse/dt)] * 1000
    decay_teorico = A0 * np.exp(-zeta * omega1 * (t_decay - t_impulse))
    ax4.semilogy(t_decay, decay_teorico, 'k--', linewidth=1.5, label=f'Teorico e^(-zetaw_1t)')
except:
    ax4.semilogy(t, np.abs(u[1, :]) * 1000 + 1e-6, 'r-', linewidth=1.5)

ax4.set_xlabel('Tiempo (s)', fontsize=11)
ax4.set_ylabel('Amplitud (mm)', fontsize=11)
ax4.set_title('Decaimiento de la respuesta', fontsize=12, fontweight='bold')
ax4.legend()
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('../figs/fig_problema_18_newmark_mdof.png', dpi=150, bbox_inches='tight')
plt.savefig('../figs/fig_problema_18_newmark_mdof.pdf', bbox_inches='tight')
print("\n[Grafica guardada en figs/fig_problema_18_newmark_mdof.png]")
plt.show()
