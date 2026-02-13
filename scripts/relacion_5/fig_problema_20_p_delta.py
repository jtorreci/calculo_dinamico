"""
Figura para Problema 20 - Relación 5
Corrección por efecto P-Delta
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

# --- Datos del problema ---
n_plantas = 4
W = 1000  # [kN]
h = 3.5   # [m]
q = 4
Delta = np.array([15, 25, 20, 12])  # [mm]
V = np.array([800, 600, 400, 200])  # [kN]

dr = q * Delta / 1000  # [m]
P = np.array([4, 3, 2, 1]) * W  # [kN]
theta = P * dr / (V * h)
gamma = 1 / (1 - theta)

# --- Figura con 2 filas: paneles arriba, tabla abajo ---
fig = plt.figure(figsize=(10, 7))

gs = fig.add_gridspec(2, 2, height_ratios=[3, 1], hspace=0.3, wspace=0.3)

ax1 = fig.add_subplot(gs[0, 0])  # Edificio
ax2 = fig.add_subplot(gs[0, 1])  # Gráfico theta
ax3 = fig.add_subplot(gs[1, :])  # Tabla

# === Panel izquierdo: Esquema edificio ===
ax1.set_xlim(-1, 4)
ax1.set_ylim(-1, 16)
ax1.axis('off')
ax1.set_title('(a) Edificio con efecto P-$\\Delta$', fontweight='bold', fontsize=10)

alturas = np.array([0, h, 2*h, 3*h, 4*h])
# Escala MUY reducida para desplazamientos (solo visual)
desp_visual = np.array([0, 0.3, 0.7, 1.0, 1.2])  # Valores fijos para visualización

# Base
ax1.fill_between([-0.3, 1.3], [-0.3, -0.3], [0, 0], color='brown', alpha=0.5)
ax1.plot([-0.3, 1.3], [0, 0], 'k-', linewidth=2)

# Estructura deformada
for i in range(n_plantas):
    x_base = desp_visual[i]
    x_top = desp_visual[i+1]
    y_base = alturas[i]
    y_top = alturas[i+1]

    # Pilar
    ax1.plot([x_base, x_top], [y_base, y_top], 'b-', linewidth=2.5)

    # Forjado
    ax1.fill_between([x_top - 0.4, x_top + 0.4],
                      [y_top - 0.1, y_top - 0.1],
                      [y_top + 0.1, y_top + 0.1],
                      color='steelblue', alpha=0.7)

    # Peso (flecha hacia abajo) con etiqueta - más larga
    ax1.annotate('', xy=(x_top, y_top + 0.2), xytext=(x_top, y_top + 1.5),
                arrowprops=dict(arrowstyle='->', color='green', lw=1.5))
    ax1.text(x_top + 0.15, y_top + 0.9, f'{W}', fontsize=7, color='green', va='center')

    # Cortante (flecha horizontal) con etiqueta
    ax1.annotate('', xy=(x_top + 0.5, y_top), xytext=(x_top + 1.3, y_top),
                arrowprops=dict(arrowstyle='->', color='red', lw=1.5))
    ax1.text(x_top + 1.4, y_top, f'{V[i]}', fontsize=7, color='red', va='center')

    # Número de planta (círculo a la izquierda)
    ax1.text(-0.7, y_top, f'{i+1}', fontsize=9, va='center', ha='center',
             bbox=dict(boxstyle='circle', facecolor='lightblue', edgecolor='blue', pad=0.15))

# Leyenda
ax1.text(2.5, 14.5, 'W [kN]', fontsize=8, color='green')
ax1.text(2.5, 13.5, 'V [kN]', fontsize=8, color='red')

# Fórmula (al nivel de la primera planta)
ax1.text(2.5, h, r'$\theta = \frac{P \cdot d_r}{V \cdot h}$', fontsize=10,
         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))

# === Panel derecho: Gráfico theta ===
plantas = np.arange(1, n_plantas + 1)
colors = ['green' if t <= 0.1 else 'orange' if t <= 0.2 else 'red' for t in theta]

bars = ax2.barh(plantas, theta, color=colors, alpha=0.7, edgecolor='black', height=0.6)

# Líneas de referencia EC8
ax2.axvline(x=0.10, color='green', linestyle='--', linewidth=1.5)
ax2.axvline(x=0.20, color='orange', linestyle='--', linewidth=1.5)
ax2.axvline(x=0.30, color='red', linestyle='--', linewidth=1.5)

# Valores en las barras
for i, t in enumerate(theta):
    ax2.text(t + 0.008, i + 1, f'{t:.3f}', fontsize=8, va='center')

ax2.set_xlabel(r'Coeficiente $\theta$', fontsize=10)
ax2.set_ylabel('Planta', fontsize=10)
ax2.set_title('(b) Sensibilidad P-$\\Delta$ (EC8)', fontweight='bold', fontsize=10)
ax2.set_xlim(0, 0.22)
ax2.set_yticks(plantas)
ax2.grid(True, alpha=0.3, axis='x')

# Anotaciones criterios
ax2.text(0.10, 4.5, 'No P-$\\Delta$', fontsize=7, color='green', ha='center')
ax2.text(0.20, 4.5, 'Amplificar', fontsize=7, color='orange', ha='center')

# === Panel inferior: Tabla ===
ax3.axis('off')
ax3.set_title('Resumen de cálculos P-$\\Delta$', fontweight='bold', fontsize=10)

col_labels = ['Planta', 'P [kN]', r'$d_r$ [mm]', 'V [kN]', r'$\theta$', r'$\gamma$', 'Estado']
table_data = []
for i in range(n_plantas):
    estado = 'OK' if theta[i] <= 0.1 else 'Amplificar' if theta[i] <= 0.2 else 'Revisar'
    table_data.append([f'{i+1}', f'{P[i]:.0f}', f'{dr[i]*1000:.0f}',
                       f'{V[i]:.0f}', f'{theta[i]:.3f}', f'{gamma[i]:.3f}', estado])

table = ax3.table(cellText=table_data, colLabels=col_labels,
                  loc='center', cellLoc='center',
                  colColours=['lightgray']*7)
table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1.0, 1.5)

plt.savefig(output_dir / "fig_problema_20_p_delta.pdf")
plt.savefig(output_dir / "fig_problema_20_p_delta.png")
plt.close()

print(f"Figura guardada en: {output_dir / 'fig_problema_20_p_delta.pdf'}")
