"""
Figura para Problema 05 - Relación 5
Construcción del espectro de respuesta a partir de pulso rectangular

Genera:
- Diagrama del proceso: acelerograma -> SDOF -> espectro
- Espectro de pseudoaceleración Sa(T)
"""
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Configuración para figuras de calidad
plt.rcParams.update({
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'legend.fontsize': 9,
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight'
})

# Crear directorio de salida
output_dir = Path(__file__).parent.parent / "figuras"
output_dir.mkdir(exist_ok=True)

# --- Parámetros del pulso rectangular ---
a0 = 3.0   # [m/s^2] Amplitud
td = 0.3   # [s] Duración

# --- Crear figura con 3 subplots ---
fig = plt.figure(figsize=(14, 5))

# === SUBPLOT 1: Pulso rectangular (acelerograma) ===
ax1 = fig.add_subplot(131)

t = np.linspace(0, 1.5, 500)
ag = np.where(t <= td, a0, 0)

ax1.fill_between(t, 0, ag, alpha=0.3, color='red')
ax1.plot(t, ag, 'r-', linewidth=2)
ax1.axhline(y=0, color='k', linewidth=0.5)
ax1.axvline(x=td, color='gray', linestyle='--', linewidth=1)

ax1.set_xlabel('Tiempo t [s]')
ax1.set_ylabel(r'$a_g(t)$ [m/s²]')
ax1.set_title('(a) Pulso rectangular', fontweight='bold')
ax1.set_xlim(0, 1.5)
ax1.set_ylim(-0.5, 4)
ax1.grid(True, alpha=0.3)

# Anotaciones
ax1.annotate(f'$a_0$ = {a0} m/s²', xy=(td/2, a0), xytext=(td/2, a0+0.5),
             ha='center', fontsize=10)
ax1.annotate(f'$t_d$ = {td} s', xy=(td, 0), xytext=(td+0.1, -0.3),
             fontsize=10)
ax1.text(0.8, 3.5, 'PGA = 3.0 m/s²', fontsize=9,
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# === SUBPLOT 2: Esquema SDOF ===
ax2 = fig.add_subplot(132)
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 10)
ax2.axis('off')
ax2.set_title('(b) Oscilador SDOF', fontweight='bold')

# Base móvil
ax2.fill_between([1, 9], [1, 1], [1.5, 1.5], color='brown', alpha=0.5)
ax2.plot([1, 9], [1.5, 1.5], 'k-', linewidth=2)

# Ruedas
for x in [2, 8]:
    circle = plt.Circle((x, 0.7), 0.3, color='gray', alpha=0.7)
    ax2.add_patch(circle)

# Resorte (zigzag)
spring_x = [3, 3.3, 3.6, 3.3, 3.6, 3.3, 3.6, 3.3, 3]
spring_y = [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5]
ax2.plot(spring_x, spring_y, 'b-', linewidth=2)
ax2.text(2.3, 3.5, 'k', fontsize=12, color='blue')

# Amortiguador
ax2.plot([6, 6], [1.5, 3], 'k-', linewidth=2)
ax2.fill_between([5.5, 6.5], [3, 3], [4.5, 4.5], color='gray', alpha=0.5)
ax2.plot([6, 6], [4.5, 5.5], 'k-', linewidth=2)
ax2.text(6.8, 3.5, 'c', fontsize=12, color='gray')

# Masa
ax2.fill_between([2.5, 7.5], [5.5, 5.5], [7, 7], color='steelblue', alpha=0.7)
ax2.plot([2.5, 7.5, 7.5, 2.5, 2.5], [5.5, 5.5, 7, 7, 5.5], 'k-', linewidth=2)
ax2.text(5, 6.25, 'm', fontsize=14, ha='center', va='center', fontweight='bold')

# Flecha de excitación
ax2.annotate('', xy=(0.5, 1.25), xytext=(1.5, 1.25),
             arrowprops=dict(arrowstyle='->', color='red', lw=2))
ax2.text(0.5, 0.5, r'$a_g(t)$', fontsize=11, color='red')

# Flecha de desplazamiento
ax2.annotate('', xy=(8.5, 6.25), xytext=(7.5, 6.25),
             arrowprops=dict(arrowstyle='->', color='green', lw=2))
ax2.text(8.7, 6.25, 'u(t)', fontsize=11, color='green')

# Ecuación
ax2.text(5, 8.5, r'$m\ddot{u} + c\dot{u} + ku = -ma_g(t)$',
         fontsize=11, ha='center',
         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

# Parámetros
ax2.text(5, 9.5, r'$T = 2\pi/\omega_n$,  $\zeta = c/(2m\omega_n)$',
         fontsize=10, ha='center')

# === SUBPLOT 3: Espectro de respuesta ===
ax3 = fig.add_subplot(133)

# Calcular espectro completo
T_array = np.linspace(0.05, 3.0, 200)
Sa_array = np.zeros_like(T_array)

for i, T in enumerate(T_array):
    ratio = td / T
    if ratio >= 0.5:
        Rd = 2.0
    else:
        Rd = 2 * np.sin(np.pi * ratio)
    Sa_array[i] = a0 * Rd

ax3.plot(T_array, Sa_array, 'b-', linewidth=2, label=r'$S_a(T)$')
ax3.axhline(y=a0, color='r', linestyle='--', linewidth=1.5, label=f'PGA = {a0} m/s²')
ax3.axhline(y=2*a0, color='orange', linestyle=':', linewidth=1.5, label=f'2×PGA = {2*a0} m/s²')

# Marcar puntos del problema
T_puntos = [0.2, 0.5, 1.0, 2.0]
for T in T_puntos:
    ratio = td / T
    Rd = 2.0 if ratio >= 0.5 else 2 * np.sin(np.pi * ratio)
    Sa = a0 * Rd
    ax3.plot(T, Sa, 'ko', markersize=8)
    ax3.annotate(f'T={T}s\n$S_a$={Sa:.1f}', xy=(T, Sa),
                xytext=(T+0.1, Sa+0.3), fontsize=8)

# Región de meseta
ax3.axvspan(0, 2*td, alpha=0.1, color='blue', label=f'Meseta ($T < 2t_d = {2*td}$ s)')

ax3.set_xlabel('Período T [s]')
ax3.set_ylabel(r'Pseudoaceleración $S_a$ [m/s²]')
ax3.set_title('(c) Espectro de respuesta', fontweight='bold')
ax3.legend(loc='upper right', fontsize=8)
ax3.grid(True, alpha=0.3)
ax3.set_xlim(0, 3)
ax3.set_ylim(0, 8)

plt.tight_layout()
plt.savefig(output_dir / "fig_problema_05_espectro_respuesta.pdf")
plt.savefig(output_dir / "fig_problema_05_espectro_respuesta.png")
plt.close()

print(f"Figura guardada en: {output_dir / 'fig_problema_05_espectro_respuesta.pdf'}")
