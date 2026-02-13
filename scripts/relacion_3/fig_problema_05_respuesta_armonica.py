"""
Figura para Problema 05 - Relacion 3
Respuesta forzada armonica (2DOF) por superposicion modal
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from pathlib import Path

plt.rcParams.update({
    'font.size': 9,
    'axes.labelsize': 10,
    'axes.titlesize': 11,
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'font.family': 'sans-serif'
})

output_dir = Path(__file__).parent.parent / "figuras"
output_dir.mkdir(exist_ok=True)

# --- Datos del problema ---
m = np.array([1000.0, 1000.0])
k = np.array([200e3, 200e3])
F0 = 1000  # N

# Frecuencias y modos (del Problema 01)
omega = np.array([8.742, 22.882])
phi = np.array([[0.01662, 0.02688],
                [0.02689, -0.01662]])

# Fuerza aplicada en masa 2
p0 = np.array([0, F0])

# Proyeccion modal
f_modal = phi.T @ p0

# Rango de frecuencias de excitacion
Omega_range = np.linspace(0.5, 30, 500)

# FRF (Funciones de Respuesta en Frecuencia) sin amortiguamiento
def calcular_respuesta(Omega, omega, phi, f_modal, zeta=0.0):
    """Calcula amplitud de respuesta para frecuencia de excitacion Omega"""
    n_dof = len(omega)
    H = np.zeros(n_dof, dtype=complex)

    for r in range(n_dof):
        # Factor de amplificacion modal
        if zeta > 0:
            H[r] = f_modal[r] / (omega[r]**2 - Omega**2 + 2j*zeta*omega[r]*Omega)
        else:
            # Sin amortiguamiento
            if abs(omega[r]**2 - Omega**2) > 1e-6:
                H[r] = f_modal[r] / (omega[r]**2 - Omega**2)
            else:
                H[r] = np.inf

    x = phi @ H
    return np.abs(x)

# Calcular respuestas
x_amp = np.zeros((2, len(Omega_range)))
for i, Om in enumerate(Omega_range):
    x_amp[:, i] = calcular_respuesta(Om, omega, phi, f_modal, zeta=0.02)

# Excitacion especifica del problema
Omega_prob = 0.9 * omega[0]
x_prob = calcular_respuesta(Omega_prob, omega, phi, f_modal, zeta=0.02)

# --- Crear figura ---
fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))

# ======================
# Panel (a): Esquema del sistema
# ======================
ax = axes[0]
ax.set_xlim(-0.5, 4)
ax.set_ylim(-0.5, 7.5)
ax.axis('off')
ax.set_title('(a) Sistema 2DOF con fuerza armonica', fontweight='bold', fontsize=10)

# Base (suelo)
ax.fill_between([-0.2, 2.2], [-0.35, -0.35], [0, 0], color='brown', alpha=0.5, hatch='///')
ax.plot([-0.2, 2.2], [0, 0], 'k-', lw=2)

h_planta = 3.0

# Dibujar edificio
for i in range(2):
    y = (i + 1) * h_planta

    # Pilares
    ax.plot([0.3, 0.3], [i * h_planta, y], 'b-', linewidth=3)
    ax.plot([1.7, 1.7], [i * h_planta, y], 'b-', linewidth=3)

    # Forjado
    ax.fill_between([-0.1, 2.1], [y - 0.12, y - 0.12], [y + 0.12, y + 0.12],
                     color='steelblue', alpha=0.8)

    # Etiqueta masa
    ax.text(2.3, y, f'$m_{i+1}$', fontsize=10, va='center')

# Fuerza armonica en masa 2
y_fuerza = 2 * h_planta
ax.annotate('', xy=(3.2, y_fuerza), xytext=(2.4, y_fuerza),
            arrowprops=dict(arrowstyle='->', color='red', lw=2.5))
ax.text(2.8, y_fuerza + 0.5, '$F_0 \\sin(\\Omega t)$', fontsize=10, color='red',
        ha='center', fontweight='bold')

# Rigideces entre plantas
for i in range(2):
    y_mid = (i + 0.5) * h_planta
    ax.text(-0.4, y_mid, f'$k_{i+1}$', fontsize=9, va='center', ha='right', color='navy')

# Informacion
info_text = f'''$m_1 = m_2 = 1000$ kg
$k_1 = k_2 = 200$ kN/m
$\\omega_1 = {omega[0]:.2f}$ rad/s
$\\omega_2 = {omega[1]:.2f}$ rad/s
$F_0 = {F0}$ N
$\\Omega = 0.9\\omega_1$'''

ax.text(1, 7.2, info_text, fontsize=8, ha='center', va='top',
        bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9, pad=0.4))

# ======================
# Panel (b): FRF
# ======================
ax = axes[1]

# Curvas de amplitud
ax.semilogy(Omega_range, x_amp[0, :] * 1000, 'b-', lw=2, label='$|x_1|$ (masa 1)')
ax.semilogy(Omega_range, x_amp[1, :] * 1000, 'r-', lw=2, label='$|x_2|$ (masa 2)')

# Frecuencias naturales
for i, w in enumerate(omega):
    ax.axvline(w, color='gray', linestyle='--', alpha=0.5)
    ax.text(w, ax.get_ylim()[1] * 0.5, f'$\\omega_{i+1}$', fontsize=9,
            ha='center', va='bottom', color='gray')

# Punto de operacion
ax.axvline(Omega_prob, color='green', linestyle='-', lw=1.5, alpha=0.7)
ax.scatter([Omega_prob, Omega_prob], [x_prob[0]*1000, x_prob[1]*1000],
           c='green', s=80, zorder=5, marker='o')

# Etiquetas de respuesta
ax.annotate(f'$|x_1| = {x_prob[0]*1000:.1f}$ mm',
            xy=(Omega_prob, x_prob[0]*1000), xytext=(Omega_prob+5, x_prob[0]*1000*1.5),
            fontsize=9, arrowprops=dict(arrowstyle='->', color='blue', lw=1),
            color='blue')

ax.annotate(f'$|x_2| = {x_prob[1]*1000:.1f}$ mm',
            xy=(Omega_prob, x_prob[1]*1000), xytext=(Omega_prob+5, x_prob[1]*1000*2),
            fontsize=9, arrowprops=dict(arrowstyle='->', color='red', lw=1),
            color='red')

ax.text(Omega_prob, 0.8, f'$\\Omega = 0.9\\omega_1$\n$= {Omega_prob:.1f}$ rad/s',
        fontsize=8, ha='center', va='top', color='green',
        bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7, pad=0.3))

ax.set_xlabel('Frecuencia de excitacion $\\Omega$ [rad/s]')
ax.set_ylabel('Amplitud de desplazamiento [mm]')
ax.set_title('(b) Funcion de respuesta en frecuencia (FRF)', fontweight='bold')
ax.set_xlim(0, 30)
ax.set_ylim(0.5, 500)
ax.grid(True, alpha=0.3, which='both')
ax.legend(loc='upper right', fontsize=9)

plt.tight_layout()
plt.savefig(output_dir / "fig_problema_05_respuesta_armonica.pdf")
plt.savefig(output_dir / "fig_problema_05_respuesta_armonica.png")
plt.close()

print(f"Figura guardada en: {output_dir / 'fig_problema_05_respuesta_armonica.pdf'}")
