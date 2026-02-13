"""
Figura para Problema 10 - Relación 4
Placa cuadrada: efecto de las condiciones de contorno

Genera:
- Modos fundamentales para SSSS, CCCC, CFCF
- Comparación de frecuencias
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
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
a = 0.5  # m (lado)
frecuencias = {
    'SSSS': 97.7,   # Hz
    'CFCF': 110.3,  # Hz
    'CCCC': 178.4   # Hz
}

# --- Funciones de forma modal aproximadas ---
def modo_SSSS(x, y, a):
    """Modo (1,1) de placa simplemente apoyada"""
    return np.sin(np.pi * x / a) * np.sin(np.pi * y / a)

def modo_CCCC(x, y, a):
    """Modo (1,1) de placa empotrada (aproximación)"""
    # Función aproximada usando polinomios
    xi = x / a
    eta = y / a
    return (xi * (1 - xi))**2 * (eta * (1 - eta))**2 * 16

def modo_CFCF(x, y, a):
    """Modo (1,1) de placa C-F-C-F (empotrada en x=0,a, libre en y=0,a)"""
    xi = x / a
    eta = y / a
    # Empotrado en x: (xi*(1-xi))^2
    # Libre en y: cos(pi*eta/2) como primera aproximación
    return (xi * (1 - xi))**2 * np.cos(np.pi * (eta - 0.5))

# --- Crear malla ---
n = 50
x = np.linspace(0, a, n)
y = np.linspace(0, a, n)
X, Y = np.meshgrid(x, y)

# --- Crear figura con 4 subplots ---
fig = plt.figure(figsize=(14, 10))

# === SUBPLOT 1: SSSS (3D) ===
ax1 = fig.add_subplot(221, projection='3d')
Z_SSSS = modo_SSSS(X, Y, a)
surf1 = ax1.plot_surface(X*100, Y*100, Z_SSSS, cmap='RdBu', alpha=0.8)
ax1.set_xlabel('x [cm]')
ax1.set_ylabel('y [cm]')
ax1.set_zlabel('w(x,y)')
ax1.set_title(f'(a) SSSS - Simplemente apoyada\n$f_1$ = {frecuencias["SSSS"]:.1f} Hz',
              fontweight='bold')
ax1.view_init(elev=25, azim=45)

# Dibujar bordes con símbolos de apoyo
for i in range(0, n, 10):
    ax1.scatter([0, a*100], [y[i]*100, y[i]*100], [0, 0],
                marker='^', color='green', s=30)
    ax1.scatter([x[i]*100, x[i]*100], [0, a*100], [0, 0],
                marker='^', color='green', s=30)

# === SUBPLOT 2: CCCC (3D) ===
ax2 = fig.add_subplot(222, projection='3d')
Z_CCCC = modo_CCCC(X, Y, a)
surf2 = ax2.plot_surface(X*100, Y*100, Z_CCCC, cmap='RdBu', alpha=0.8)
ax2.set_xlabel('x [cm]')
ax2.set_ylabel('y [cm]')
ax2.set_zlabel('w(x,y)')
ax2.set_title(f'(b) CCCC - Empotrada\n$f_1$ = {frecuencias["CCCC"]:.1f} Hz',
              fontweight='bold')
ax2.view_init(elev=25, azim=45)

# === SUBPLOT 3: CFCF (3D) ===
ax3 = fig.add_subplot(223, projection='3d')
Z_CFCF = modo_CFCF(X, Y, a)
surf3 = ax3.plot_surface(X*100, Y*100, Z_CFCF, cmap='RdBu', alpha=0.8)
ax3.set_xlabel('x [cm]')
ax3.set_ylabel('y [cm]')
ax3.set_zlabel('w(x,y)')
ax3.set_title(f'(c) CFCF - Empotrada-Libre\n$f_1$ = {frecuencias["CFCF"]:.1f} Hz',
              fontweight='bold')
ax3.view_init(elev=25, azim=45)

# === SUBPLOT 4: Comparación de frecuencias ===
ax4 = fig.add_subplot(224)

condiciones = list(frecuencias.keys())
freqs = list(frecuencias.values())
colors = ['#2ecc71', '#e74c3c', '#3498db']
ratios = [f / frecuencias['SSSS'] for f in freqs]

bars = ax4.bar(condiciones, freqs, color=colors, alpha=0.7, edgecolor='black')

# Añadir valores y ratios
for i, (bar, f, r) in enumerate(zip(bars, freqs, ratios)):
    ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
             f'{f:.1f} Hz\n({r:.2f}×)', ha='center', fontsize=10)

ax4.set_ylabel('Frecuencia fundamental $f_1$ [Hz]')
ax4.set_title('(d) Comparación de frecuencias\nsegún condiciones de contorno',
              fontweight='bold')
ax4.set_ylim(0, 220)
ax4.grid(True, alpha=0.3, axis='y')

# Añadir línea de referencia
ax4.axhline(y=frecuencias['SSSS'], color='gray', linestyle='--', alpha=0.5)
ax4.text(2.5, frecuencias['SSSS'] + 3, 'Referencia SSSS', fontsize=8, color='gray')

# Leyenda de condiciones
legend_text = """
S = Simply supported (apoyado)
C = Clamped (empotrado)
F = Free (libre)

SSSS: 4 bordes apoyados
CCCC: 4 bordes empotrados
CFCF: 2 emp. + 2 libres
"""
ax4.text(0.02, 0.98, legend_text, transform=ax4.transAxes,
         fontsize=8, va='top', family='monospace',
         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

plt.tight_layout()
plt.savefig(output_dir / "fig_problema_10_placa_CC.pdf")
plt.savefig(output_dir / "fig_problema_10_placa_CC.png")
plt.close()

print(f"Figura guardada en: {output_dir / 'fig_problema_10_placa_CC.pdf'}")
