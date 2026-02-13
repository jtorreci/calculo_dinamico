"""
Figura para Problema 06 - Relación 3
Excitación sísmica: análisis modal espectral de edificio 2DOF
"""
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

plt.rcParams.update({
    'font.size': 9,
    'axes.labelsize': 10,
    'axes.titlesize': 11,
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight'
})

output_dir = Path(__file__).parent.parent / "figuras"
output_dir.mkdir(exist_ok=True)

# --- Datos ---
m = np.array([1000.0, 1000.0])
k = np.array([200e3, 200e3])
omega = np.array([8.742, 22.882])
phi = np.array([[0.01662, 0.02688],
                [0.02689, -0.01662]])
Gamma = np.array([43.51, 10.26])
M_eff_pct = np.array([94.7, 5.3])
Sa = np.array([2.0, 1.2])

x_modal = np.zeros((2, 2))
for r in range(2):
    x_modal[:, r] = Gamma[r] * phi[:, r] * Sa[r] / omega[r]**2
x_SRSS = np.sqrt(np.sum(x_modal**2, axis=1))

# --- Figura 2x2 más compacta ---
fig, axes = plt.subplots(2, 2, figsize=(8, 6))
h_planta = 3.0

def dibujar_edificio(ax, desplazamientos, titulo, color_flecha, valores_mm=None):
    """Dibuja edificio 2DOF deformado"""
    ax.set_xlim(-0.5, 4)
    ax.set_ylim(-0.5, 7.5)
    ax.axis('off')
    ax.set_title(titulo, fontweight='bold', fontsize=10)

    # Base
    ax.fill_between([-0.2, 2.2], [-0.25, -0.25], [0, 0], color='brown', alpha=0.5)

    # Escala desplazamientos para visualización
    escala = 1.5 / max(abs(desplazamientos)) if max(abs(desplazamientos)) > 0 else 1

    for i in range(2):
        y = (i + 1) * h_planta
        x = 1 + desplazamientos[i] * escala

        # Pilar
        if i == 0:
            ax.plot([1, x], [0, y], 'b-', linewidth=2)
        else:
            x_prev = 1 + desplazamientos[i-1] * escala
            ax.plot([x_prev, x], [(i) * h_planta, y], 'b-', linewidth=2)

        # Forjado
        ax.fill_between([x - 0.4, x + 0.4], [y - 0.1, y - 0.1],
                        [y + 0.1, y + 0.1], color='steelblue', alpha=0.7)

        # Flecha desplazamiento
        if abs(desplazamientos[i]) > 1e-6:
            ax.annotate('', xy=(x, y), xytext=(1, y),
                       arrowprops=dict(arrowstyle='->', color=color_flecha, lw=1.5))

        # Valor
        if valores_mm is not None:
            ax.text(x + 0.5, y, f'{valores_mm[i]:.1f}', fontsize=8, va='center')

    # Línea referencia
    ax.plot([1, 1], [0, 6.5], 'k--', alpha=0.3, linewidth=0.5)

# Panel (a): Sistema
ax1 = axes[0, 0]
ax1.set_xlim(-0.5, 4)
ax1.set_ylim(-0.5, 7.5)
ax1.axis('off')
ax1.set_title('(a) Sistema 2DOF', fontweight='bold', fontsize=10)

ax1.fill_between([-0.2, 2.2], [-0.25, -0.25], [0, 0], color='brown', alpha=0.5)
for i in range(2):
    y = (i + 1) * h_planta
    ax1.plot([0.3, 0.3], [i * h_planta, y], 'b-', linewidth=2)
    ax1.plot([1.7, 1.7], [i * h_planta, y], 'b-', linewidth=2)
    ax1.fill_between([-0.1, 2.1], [y - 0.1, y - 0.1], [y + 0.1, y + 0.1],
                     color='steelblue', alpha=0.7)
    ax1.text(2.3, y, f'm={m[i]:.0f} kg', fontsize=8, va='center')

ax1.text(1, 7, f'$\\omega_1$={omega[0]:.1f} rad/s\n$\\omega_2$={omega[1]:.1f} rad/s',
         fontsize=8, ha='center', va='top',
         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8, pad=0.3))

# Panel (b): Modo 1
desp1 = phi[:, 0] / np.max(np.abs(phi[:, 0]))
dibujar_edificio(axes[0, 1], desp1, f'(b) Modo 1 ({M_eff_pct[0]:.0f}%)', 'green',
                 x_modal[:, 0] * 1000)

# Panel (c): Modo 2
desp2 = phi[:, 1] / np.max(np.abs(phi[:, 1]))
dibujar_edificio(axes[1, 0], desp2, f'(c) Modo 2 ({M_eff_pct[1]:.0f}%)', 'orange',
                 x_modal[:, 1] * 1000)

# Panel (d): SRSS
desp_srss = x_SRSS / np.max(x_SRSS)
dibujar_edificio(axes[1, 1], desp_srss, '(d) SRSS', 'red', x_SRSS * 1000)
axes[1, 1].text(1, 7, r'$x_{max}=\sqrt{\sum x_r^2}$', fontsize=9, ha='center',
                bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7, pad=0.3))

plt.tight_layout()
plt.savefig(output_dir / "fig_problema_06_edificio_espectral.pdf")
plt.savefig(output_dir / "fig_problema_06_edificio_espectral.png")
plt.close()

print(f"Figura guardada en: {output_dir / 'fig_problema_06_edificio_espectral.pdf'}")
