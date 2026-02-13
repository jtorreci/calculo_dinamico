"""
Figura para Problema 04 - Relacion 3
Amortiguamiento proporcional de Rayleigh: curva zeta(omega)
"""
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

plt.rcParams.update({
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'font.family': 'sans-serif'
})

output_dir = Path(__file__).parent.parent / "figuras"
output_dir.mkdir(exist_ok=True)

# --- Datos del problema ---
# Frecuencias naturales del edificio 3DOF (Problema 02)
omega = np.array([10.824, 20.000, 26.131])  # rad/s

# Objetivos de amortiguamiento
zeta_obj = np.array([0.02, 0.05])  # zeta_1 = 2%, zeta_3 = 5%
omega_obj = np.array([omega[0], omega[2]])

# Calcular coeficientes Rayleigh
# Sistema: [1/omega_i  omega_i] * [alpha; beta] = [2*zeta_i]
A = np.array([[1/omega_obj[0], omega_obj[0]],
              [1/omega_obj[1], omega_obj[1]]])
b = 2 * zeta_obj
coef = np.linalg.solve(A, b)
alpha, beta = coef

# Funcion de amortiguamiento
def zeta_rayleigh(w, alpha, beta):
    return 0.5 * (alpha/w + beta*w)

# Amortiguamiento resultante en modo 2
zeta_2 = zeta_rayleigh(omega[1], alpha, beta)

# --- Crear figura ---
fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))

# ======================
# Panel (a): Curva zeta(omega)
# ======================
ax = axes[0]

# Rango de frecuencias
w_plot = np.linspace(5, 35, 200)
zeta_plot = zeta_rayleigh(w_plot, alpha, beta) * 100

# Contribuciones individuales
zeta_masa = 0.5 * alpha / w_plot * 100  # Contribucion de masa
zeta_rigidez = 0.5 * beta * w_plot * 100  # Contribucion de rigidez

# Curvas
ax.plot(w_plot, zeta_plot, 'b-', lw=2.5, label=r'$\zeta(\omega) = \frac{1}{2}\left(\frac{\alpha}{\omega} + \beta\omega\right)$')
ax.plot(w_plot, zeta_masa, 'g--', lw=1.5, label=r'Contribucion masa: $\frac{\alpha}{2\omega}$')
ax.plot(w_plot, zeta_rigidez, 'r--', lw=1.5, label=r'Contribucion rigidez: $\frac{\beta\omega}{2}$')

# Puntos de control (objetivos)
ax.scatter([omega[0], omega[2]], [zeta_obj[0]*100, zeta_obj[1]*100],
           c='black', s=100, zorder=5, marker='o', label='Puntos de control')

# Punto resultante modo 2
ax.scatter([omega[1]], [zeta_2*100], c='purple', s=100, zorder=5, marker='s',
           label=f'Modo 2 (resultante): {zeta_2*100:.1f}%')

# Etiquetas de modos
ax.annotate(f'Modo 1\n$\\zeta_1 = {zeta_obj[0]*100:.0f}\\%$',
            xy=(omega[0], zeta_obj[0]*100), xytext=(omega[0]-3, zeta_obj[0]*100+1.5),
            fontsize=9, ha='center',
            arrowprops=dict(arrowstyle='->', color='gray', lw=1))

ax.annotate(f'Modo 3\n$\\zeta_3 = {zeta_obj[1]*100:.0f}\\%$',
            xy=(omega[2], zeta_obj[1]*100), xytext=(omega[2]+3, zeta_obj[1]*100-1),
            fontsize=9, ha='center',
            arrowprops=dict(arrowstyle='->', color='gray', lw=1))

ax.annotate(f'Modo 2\n$\\zeta_2 = {zeta_2*100:.1f}\\%$',
            xy=(omega[1], zeta_2*100), xytext=(omega[1]+4, zeta_2*100+1.5),
            fontsize=9, ha='center', color='purple',
            arrowprops=dict(arrowstyle='->', color='purple', lw=1))

# Marcas de frecuencias en eje x
for i, w in enumerate(omega):
    ax.axvline(w, color='gray', linestyle=':', alpha=0.5)
    ax.text(w, -0.8, f'$\\omega_{i+1}$', ha='center', fontsize=9, color='gray')

ax.set_xlabel('Frecuencia $\\omega$ [rad/s]')
ax.set_ylabel('Amortiguamiento $\\zeta$ [%]')
ax.set_title('(a) Curva de amortiguamiento Rayleigh', fontweight='bold')
ax.set_xlim(5, 35)
ax.set_ylim(-1, 8)
ax.grid(True, alpha=0.3)
ax.legend(loc='upper right', fontsize=8)

# ======================
# Panel (b): Interpretacion fisica
# ======================
ax = axes[1]
ax.axis('off')

# Titulo
ax.text(0.5, 0.95, '(b) Interpretacion del modelo Rayleigh', fontweight='bold',
        fontsize=12, ha='center', va='top', transform=ax.transAxes)

# Ecuaciones y valores
texto = r'''
$\mathbf{C} = \alpha \mathbf{M} + \beta \mathbf{K}$

$\zeta(\omega) = \frac{1}{2}\left(\frac{\alpha}{\omega} + \beta\omega\right)$

\textbf{Sistema de ecuaciones (2 puntos de control):}
$$\begin{cases}
\zeta_1 = \frac{1}{2}\left(\frac{\alpha}{\omega_1} + \beta\omega_1\right) = 2\% \\[0.5em]
\zeta_3 = \frac{1}{2}\left(\frac{\alpha}{\omega_3} + \beta\omega_3\right) = 5\%
\end{cases}$$

\textbf{Coeficientes obtenidos:}
'''

ax.text(0.1, 0.85, r'$\mathbf{C} = \alpha \mathbf{M} + \beta \mathbf{K}$',
        fontsize=14, ha='left', transform=ax.transAxes)

ax.text(0.1, 0.72, r'$\zeta(\omega) = \frac{1}{2}\left(\frac{\alpha}{\omega} + \beta\omega\right)$',
        fontsize=12, ha='left', transform=ax.transAxes)

# Coeficientes
ax.text(0.1, 0.55, 'Coeficientes calculados:', fontsize=11, fontweight='bold',
        ha='left', transform=ax.transAxes)

ax.text(0.15, 0.45, f'$\\alpha = {alpha:.4f}$ s$^{{-1}}$', fontsize=11,
        ha='left', transform=ax.transAxes,
        color='red' if alpha < 0 else 'black')

ax.text(0.15, 0.35, f'$\\beta = {beta:.5f}$ s', fontsize=11,
        ha='left', transform=ax.transAxes)

# Advertencia
if alpha < 0:
    ax.text(0.5, 0.20, r'$\mathbf{\alpha < 0}$: Problema fisico!',
            fontsize=11, ha='center', transform=ax.transAxes,
            color='red', fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='mistyrose', edgecolor='red', pad=0.5))

    ax.text(0.5, 0.08, 'El modelo Rayleigh no puede satisfacer\n'
                       'estos objetivos con coeficientes positivos.',
            fontsize=9, ha='center', transform=ax.transAxes, style='italic')

plt.tight_layout()
plt.savefig(output_dir / "fig_problema_04_rayleigh.pdf")
plt.savefig(output_dir / "fig_problema_04_rayleigh.png")
plt.close()

print(f"Figura guardada en: {output_dir / 'fig_problema_04_rayleigh.pdf'}")
print(f"alpha = {alpha:.4e}, beta = {beta:.4e}")
print(f"zeta_2 = {zeta_2*100:.2f}%")
