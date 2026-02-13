"""
Figura para Problema 04 - Relación 4
Voladizo con masa concentrada: método de Rayleigh

Genera:
- Esquema del sistema (voladizo + masa)
- Comparación de funciones de forma
- Deformadas modales
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

# --- Datos del problema ---
L = 2.0  # [m] Longitud
M = 500  # [kg] Masa en extremo

# --- Funciones de forma ---
def psi_coseno(x, L):
    """Función de forma: 1 - cos(pi*x/(2L))"""
    return 1 - np.cos(np.pi * x / (2*L))

def psi_polinomica(x, L):
    """Función de forma polinómica: 3(x/L)^2 - 2(x/L)^3"""
    xi = x / L
    return 3*xi**2 - 2*xi**3

def psi_exacta(x, L, beta_L=1.8751):
    """Forma modal exacta de voladizo (aproximación)"""
    beta = beta_L / L
    # Fórmula exacta normalizada
    return (np.cosh(beta*x) - np.cos(beta*x) -
            0.7341 * (np.sinh(beta*x) - np.sin(beta*x)))

# --- Crear figura con 2 subplots ---
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# === SUBPLOT 1: Esquema del sistema ===
ax1 = axes[0]
ax1.set_xlim(-0.5, 3)
ax1.set_ylim(-1, 1.5)
ax1.set_aspect('equal')
ax1.axis('off')
ax1.set_title('(a) Voladizo con masa concentrada', fontweight='bold')

# Empotramiento (rayado)
ax1.fill_between([-0.3, 0], [-0.6, -0.6], [0.6, 0.6],
                  color='gray', alpha=0.3, hatch='///')
ax1.plot([0, 0], [-0.6, 0.6], 'k-', linewidth=2)

# Viga
ax1.fill_between([0, L], [-0.08, -0.08], [0.08, 0.08],
                  color='steelblue', alpha=0.7)
ax1.plot([0, L], [0.08, 0.08], 'k-', linewidth=1.5)
ax1.plot([0, L], [-0.08, -0.08], 'k-', linewidth=1.5)

# Masa en el extremo
circle = plt.Circle((L, 0), 0.2, color='darkred', alpha=0.8)
ax1.add_patch(circle)
ax1.text(L, 0, 'M', ha='center', va='center', fontsize=12,
         color='white', fontweight='bold')

# Cotas y etiquetas
ax1.annotate('', xy=(L, -0.5), xytext=(0, -0.5),
             arrowprops=dict(arrowstyle='<->', color='black'))
ax1.text(L/2, -0.7, f'L = {L} m', ha='center', fontsize=10)

ax1.text(-0.15, 0.8, 'HEB 200', ha='center', fontsize=9, rotation=90)
ax1.text(L + 0.5, 0, f'M = {M} kg', ha='left', fontsize=10)

# Ejes de referencia
ax1.annotate('', xy=(2.5, -0.8), xytext=(2.2, -0.8),
             arrowprops=dict(arrowstyle='->', color='gray'))
ax1.text(2.6, -0.8, 'x', fontsize=10, color='gray')

# === SUBPLOT 2: Comparación de funciones de forma ===
ax2 = axes[1]
x = np.linspace(0, L, 100)

# Calcular funciones de forma
psi1 = psi_coseno(x, L)
psi2 = psi_polinomica(x, L)
psi3 = psi_exacta(x, L)

# Normalizar todas a máximo = 1
psi1 = psi1 / psi1[-1]
psi2 = psi2 / psi2[-1]
psi3 = psi3 / np.max(np.abs(psi3))

ax2.plot(x, psi1, 'b-', linewidth=2, label=r'$\psi_1 = 1 - \cos(\pi x/2L)$ (Error: 71%)')
ax2.plot(x, psi2, 'r--', linewidth=2, label=r'$\psi_2 = 3(x/L)^2 - 2(x/L)^3$ (Error: 4%)')
ax2.plot(x, psi3, 'g:', linewidth=2.5, label=r'Modo exacto (voladizo)')

ax2.set_xlabel('Posición x [m]')
ax2.set_ylabel(r'Función de forma normalizada $\psi(x)$')
ax2.set_title('(b) Comparación de funciones de forma', fontweight='bold')
ax2.legend(loc='upper left', framealpha=0.9)
ax2.grid(True, alpha=0.3)
ax2.set_xlim(0, L)
ax2.set_ylim(0, 1.1)

# Añadir punto de masa
ax2.plot(L, 1, 'ko', markersize=10, label='_nolegend_')
ax2.annotate('Masa M', xy=(L, 1), xytext=(L-0.3, 1.05),
             fontsize=9, ha='right')

plt.tight_layout()
plt.savefig(output_dir / "fig_problema_04_voladizo_masa.pdf")
plt.savefig(output_dir / "fig_problema_04_voladizo_masa.png")
plt.close()

print(f"Figura guardada en: {output_dir / 'fig_problema_04_voladizo_masa.pdf'}")
