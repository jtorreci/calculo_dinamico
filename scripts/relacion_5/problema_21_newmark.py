"""
Problema 21: Análisis time-history con Newmark
===============================================
Integración temporal de un SDOF sometido a pulso sísmico.
"""

import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# Parámetros del sistema
# =============================================================================
print("=" * 60)
print("PROBLEMA 21: INTEGRACIÓN TEMPORAL NEWMARK")
print("=" * 60)

m = 1000  # kg
k = 40000  # N/m
zeta = 0.05

omega_n = np.sqrt(k/m)
T_n = 2*np.pi/omega_n
c = 2 * zeta * m * omega_n

print(f"\nPropiedades del sistema:")
print(f"  m = {m} kg")
print(f"  k = {k} N/m")
print(f"  c = {c:.1f} Ns/m")
print(f"  omega_n = {omega_n:.2f} rad/s")
print(f"  T_n = {T_n:.3f} s")
print(f"  zeta = {zeta}")

# =============================================================================
# Excitación (pulso sinusoidal)
# =============================================================================
A0 = 2.0  # m/s²
omega_exc = 10  # rad/s
t_p = np.pi / omega_exc  # duración del pulso

def ag(t):
    """Aceleración en la base (pulso sinusoidal)"""
    if isinstance(t, np.ndarray):
        return np.where(t <= t_p, A0 * np.sin(omega_exc * t), 0.0)
    return A0 * np.sin(omega_exc * t) if t <= t_p else 0.0

print(f"\nExcitación:")
print(f"  A0 = {A0} m/s²")
print(f"  omega_exc = {omega_exc} rad/s")
print(f"  t_p = {t_p:.3f} s")
print(f"  r = omega_exc/omega_n = {omega_exc/omega_n:.2f}")

# =============================================================================
# Método de Newmark
# =============================================================================
gamma = 0.5
beta = 0.25
dt = 0.005
t_max = 1.5

t = np.arange(0, t_max + dt, dt)
n = len(t)

# Coeficientes de Newmark
a0 = 1/(beta*dt**2)
a1 = gamma/(beta*dt)
a2 = 1/(beta*dt)
a3 = 1/(2*beta) - 1
a4 = gamma/beta - 1
a5 = dt*(gamma/(2*beta) - 1)

k_eff = k + a0*m + a1*c

# Arrays de respuesta
u = np.zeros(n)
v = np.zeros(n)
a = np.zeros(n)
ag_hist = ag(t)

# Integración
for i in range(n-1):
    p_eff = -m*ag_hist[i+1] + m*(a0*u[i] + a2*v[i] + a3*a[i]) + c*(a1*u[i] + a4*v[i] + a5*a[i])
    u[i+1] = p_eff / k_eff
    a[i+1] = a0*(u[i+1] - u[i]) - a2*v[i] - a3*a[i]
    v[i+1] = v[i] + dt*((1-gamma)*a[i] + gamma*a[i+1])

# Aceleración absoluta
a_abs = a + ag_hist

# =============================================================================
# Resultados
# =============================================================================
print("\n" + "=" * 60)
print("RESULTADOS")
print("=" * 60)
print(f"  u_max = {np.max(np.abs(u))*1000:.2f} mm en t = {t[np.argmax(np.abs(u))]:.3f} s")
print(f"  v_max = {np.max(np.abs(v))*1000:.2f} mm/s")
print(f"  a_abs_max = {np.max(np.abs(a_abs)):.2f} m/s²")

# =============================================================================
# Gráficas
# =============================================================================
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Panel 1: Excitación
ax1 = axes[0, 0]
ax1.plot(t, ag_hist, 'r-', linewidth=2)
ax1.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
ax1.axvline(x=t_p, color='gray', linestyle='--', alpha=0.7, label=f't_p = {t_p:.3f} s')
ax1.fill_between(t, ag_hist, alpha=0.3, color='red')
ax1.set_xlabel('Tiempo (s)', fontsize=11)
ax1.set_ylabel('Aceleración base (m/s²)', fontsize=11)
ax1.set_title('Excitación sísmica (pulso sinusoidal)', fontsize=12, fontweight='bold')
ax1.legend()
ax1.grid(True, alpha=0.3)
ax1.set_xlim(0, t_max)

# Panel 2: Desplazamiento
ax2 = axes[0, 1]
ax2.plot(t, u*1000, 'b-', linewidth=1.5)
ax2.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
i_max = np.argmax(np.abs(u))
ax2.plot(t[i_max], u[i_max]*1000, 'ro', markersize=10, label=f'u_max = {u[i_max]*1000:.1f} mm')
ax2.set_xlabel('Tiempo (s)', fontsize=11)
ax2.set_ylabel('Desplazamiento (mm)', fontsize=11)
ax2.set_title('Respuesta en desplazamiento', fontsize=12, fontweight='bold')
ax2.legend()
ax2.grid(True, alpha=0.3)
ax2.set_xlim(0, t_max)

# Panel 3: Velocidad
ax3 = axes[1, 0]
ax3.plot(t, v*1000, 'g-', linewidth=1.5)
ax3.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
ax3.set_xlabel('Tiempo (s)', fontsize=11)
ax3.set_ylabel('Velocidad (mm/s)', fontsize=11)
ax3.set_title('Respuesta en velocidad', fontsize=12, fontweight='bold')
ax3.grid(True, alpha=0.3)
ax3.set_xlim(0, t_max)

# Panel 4: Aceleración absoluta
ax4 = axes[1, 1]
ax4.plot(t, a_abs, 'm-', linewidth=1.5, label='Aceleración absoluta')
ax4.plot(t, ag_hist, 'r--', linewidth=1, alpha=0.5, label='Excitación')
ax4.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
ax4.set_xlabel('Tiempo (s)', fontsize=11)
ax4.set_ylabel('Aceleración (m/s²)', fontsize=11)
ax4.set_title('Aceleración absoluta', fontsize=12, fontweight='bold')
ax4.legend()
ax4.grid(True, alpha=0.3)
ax4.set_xlim(0, t_max)

plt.tight_layout()
plt.savefig('../figs/fig_problema_21_newmark.png', dpi=150, bbox_inches='tight')
plt.savefig('../figs/fig_problema_21_newmark.pdf', bbox_inches='tight')
print("\n[Figura guardada en figs/fig_problema_21_newmark.pdf]")
plt.close()
