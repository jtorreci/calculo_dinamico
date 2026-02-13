"""
Figura para Problema 28 - Relación 3
Análisis modal experimental: identificación de parámetros

Genera:
- FRF (Función de Respuesta en Frecuencia) con picos de resonancia
- Diagrama del método del ancho de banda
"""
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Configuración
plt.rcParams.update({
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'legend.fontsize': 9,
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight'
})

output_dir = Path(__file__).parent.parent / "figuras"
output_dir.mkdir(exist_ok=True)

# --- Datos del problema ---
f1, f2 = 5.2, 12.8  # Hz (frecuencias naturales)
zeta1, zeta2 = 0.05, 0.04  # amortiguamientos
H_peak1, H_peak2 = 2.5e-4, 0.8e-4  # m/N (picos)
Delta_f1, Delta_f2 = 0.52, 1.02  # Hz (ancho de banda)

# --- Función FRF teórica (2DOF) ---
def FRF_2dof(f, f1, f2, zeta1, zeta2, A1, A2):
    """FRF aproximada como suma de contribuciones modales"""
    omega = 2 * np.pi * f
    omega1 = 2 * np.pi * f1
    omega2 = 2 * np.pi * f2

    # Contribución de cada modo
    r1 = omega / omega1
    r2 = omega / omega2

    H1 = A1 / np.sqrt((1 - r1**2)**2 + (2*zeta1*r1)**2)
    H2 = A2 / np.sqrt((1 - r2**2)**2 + (2*zeta2*r2)**2)

    return H1 + H2

# Amplitudes modales (ajustadas para coincidir con picos)
A1 = H_peak1 * 2 * zeta1
A2 = H_peak2 * 2 * zeta2

# --- Crear figura ---
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# === SUBPLOT 1: FRF completa ===
ax1 = axes[0]

f = np.linspace(0.5, 20, 1000)
H = FRF_2dof(f, f1, f2, zeta1, zeta2, A1, A2)

ax1.semilogy(f, H, 'b-', linewidth=2, label='$|H_{11}(f)|$')

# Marcar picos
ax1.plot(f1, H_peak1, 'ro', markersize=10, label=f'Resonancia 1: {f1} Hz')
ax1.plot(f2, H_peak2, 'go', markersize=10, label=f'Resonancia 2: {f2} Hz')

# Líneas de referencia
ax1.axvline(x=f1, color='red', linestyle='--', alpha=0.3)
ax1.axvline(x=f2, color='green', linestyle='--', alpha=0.3)

# Anotaciones
ax1.annotate(f'$f_1$ = {f1} Hz\n$\\zeta_1$ = {zeta1*100:.0f}%',
             xy=(f1, H_peak1), xytext=(f1+1.5, H_peak1*1.5),
             fontsize=9, arrowprops=dict(arrowstyle='->', color='red'))
ax1.annotate(f'$f_2$ = {f2} Hz\n$\\zeta_2$ = {zeta2*100:.0f}%',
             xy=(f2, H_peak2), xytext=(f2+1.5, H_peak2*2),
             fontsize=9, arrowprops=dict(arrowstyle='->', color='green'))

ax1.set_xlabel('Frecuencia f [Hz]')
ax1.set_ylabel('|$H_{11}$| [m/N]')
ax1.set_title('(a) Función de Respuesta en Frecuencia (FRF)', fontweight='bold')
ax1.legend(loc='upper right')
ax1.grid(True, alpha=0.3, which='both')
ax1.set_xlim(0, 20)
ax1.set_ylim(1e-6, 1e-3)

# === SUBPLOT 2: Método del ancho de banda (zoom en modo 1) ===
ax2 = axes[1]

# Zoom alrededor de f1
f_zoom = np.linspace(3, 8, 500)
H_zoom = FRF_2dof(f_zoom, f1, f2, zeta1, zeta2, A1, A2)

ax2.plot(f_zoom, H_zoom*1e4, 'b-', linewidth=2)
ax2.plot(f1, H_peak1*1e4, 'ro', markersize=12)

# Nivel -3dB (1/sqrt(2) del pico)
H_3dB = H_peak1 / np.sqrt(2)
ax2.axhline(y=H_3dB*1e4, color='orange', linestyle='--', linewidth=2,
            label=f'-3 dB: {H_3dB*1e4:.2f}×$10^{{-4}}$ m/N')

# Ancho de banda
f_left = f1 - Delta_f1/2
f_right = f1 + Delta_f1/2
ax2.axvline(x=f_left, color='purple', linestyle=':', linewidth=1.5)
ax2.axvline(x=f_right, color='purple', linestyle=':', linewidth=1.5)

# Flecha de ancho de banda
ax2.annotate('', xy=(f_right, H_3dB*1e4), xytext=(f_left, H_3dB*1e4),
             arrowprops=dict(arrowstyle='<->', color='purple', lw=2))
ax2.text(f1, H_3dB*1e4 - 0.3, f'$\\Delta f_1$ = {Delta_f1} Hz',
         ha='center', fontsize=10, color='purple')

# Fórmula
ax2.text(6.5, 2.0, r'$\zeta = \frac{\Delta f}{2 f_r}$' + f'\n\n$\\zeta_1 = \\frac{{{Delta_f1}}}{{2 \\times {f1}}} = {zeta1:.2f}$',
         fontsize=11, ha='center',
         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))

ax2.set_xlabel('Frecuencia f [Hz]')
ax2.set_ylabel('|$H_{11}$| [×$10^{-4}$ m/N]')
ax2.set_title('(b) Método del ancho de banda (-3 dB)', fontweight='bold')
ax2.legend(loc='upper right')
ax2.grid(True, alpha=0.3)
ax2.set_xlim(3, 8)
ax2.set_ylim(0, 3)

# Etiquetas de frecuencias
ax2.text(f_left, -0.2, f'$f_1 - \\frac{{\\Delta f}}{{2}}$', ha='center', fontsize=9, color='purple')
ax2.text(f_right, -0.2, f'$f_1 + \\frac{{\\Delta f}}{{2}}$', ha='center', fontsize=9, color='purple')

plt.tight_layout()
plt.savefig(output_dir / "fig_problema_28_FRF.pdf")
plt.savefig(output_dir / "fig_problema_28_FRF.png")
plt.close()

print(f"Figura guardada en: {output_dir / 'fig_problema_28_FRF.pdf'}")
