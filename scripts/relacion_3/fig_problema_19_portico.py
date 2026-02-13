"""
Figura para Problema 19 - Relacion 3
Rigidez de portico plano: comparacion viga rigida vs flexible
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, Circle, Arc
from matplotlib.lines import Line2D
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

def dibujar_empotramiento(ax, x, y, ancho=0.3, alto=0.2):
    """Dibuja simbolo de empotramiento en la base"""
    # Rectangulo rayado
    ax.fill_between([x-ancho/2, x+ancho/2], [y-alto, y-alto], [y, y],
                   color='gray', alpha=0.5, hatch='///')
    ax.plot([x-ancho/2, x+ancho/2], [y, y], 'k-', lw=2)

def dibujar_articulacion(ax, x, y, radio=0.08):
    """Dibuja simbolo de articulacion (circulo)"""
    circle = Circle((x, y), radio, facecolor='white', edgecolor='black', lw=1.5, zorder=5)
    ax.add_patch(circle)

def dibujar_masa(ax, x, y, size=0.3):
    """Dibuja simbolo de masa concentrada"""
    rect = FancyBboxPatch((x-size/2, y-size/2), size, size,
                          boxstyle="round,pad=0.02",
                          facecolor='lightcoral', edgecolor='darkred', lw=2)
    ax.add_patch(rect)
    ax.text(x, y, '$m$', ha='center', va='center', fontsize=10, fontweight='bold')

# --- Crear figura ---
fig, axes = plt.subplots(1, 3, figsize=(10, 4.5))

# Dimensiones del portico
h = 3.0  # altura columnas
L = 6.0  # luz viga

# ======================
# Panel (a): Portico original
# ======================
ax = axes[0]
ax.set_xlim(-1, 8)
ax.set_ylim(-1, 5)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title('(a) Portico original', fontweight='bold', fontsize=10)

# Empotramientos en base
dibujar_empotramiento(ax, 1, 0)
dibujar_empotramiento(ax, 7, 0)

# Columnas
ax.plot([1, 1], [0, h], 'b-', lw=3)
ax.plot([7, 7], [0, h], 'b-', lw=3)

# Viga
ax.plot([1, 7], [h, h], 'b-', lw=3)

# Masa en el centro de la viga
dibujar_masa(ax, 4, h + 0.3)

# Cotas
# Altura h
ax.annotate('', xy=(0.2, 0), xytext=(0.2, h),
            arrowprops=dict(arrowstyle='<->', color='green', lw=1.5))
ax.text(-0.1, h/2, f'$h$', ha='right', va='center', fontsize=10, color='green')

# Luz L
ax.annotate('', xy=(1, -0.7), xytext=(7, -0.7),
            arrowprops=dict(arrowstyle='<->', color='green', lw=1.5))
ax.text(4, -0.9, f'$L$', ha='center', va='top', fontsize=10, color='green')

# Etiquetas EI
ax.text(0.5, h/2, '$EI_c$', ha='right', va='center', fontsize=9, color='navy')
ax.text(7.5, h/2, '$EI_c$', ha='left', va='center', fontsize=9, color='navy')
ax.text(4, h-0.4, '$EI_v$', ha='center', va='top', fontsize=9, color='navy')

# Desplazamiento horizontal
ax.annotate('', xy=(7.5, h+0.5), xytext=(8.3, h+0.5),
            arrowprops=dict(arrowstyle='->', color='red', lw=2))
ax.text(7.9, h+0.8, '$u$', fontsize=11, color='red', fontweight='bold')

# ======================
# Panel (b): Modelo viga rigida con nudos articulados
# ======================
ax = axes[1]
ax.set_xlim(-1, 8)
ax.set_ylim(-1, 5)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title('(b) Viga rigida, nudos articulados', fontweight='bold', fontsize=10)

# Empotramientos
dibujar_empotramiento(ax, 1, 0)
dibujar_empotramiento(ax, 7, 0)

# Columnas deformadas (empotradas-articuladas)
# Forma deformada cubica
def deformada_emp_art(x, h, u_top):
    """Deformada de columna empotrada-articulada"""
    xi = x / h
    return u_top * (3*xi**2 - 2*xi**3) / 2  # forma empotrada-articulada

u_top = 0.6  # desplazamiento superior para visualizacion
y_col = np.linspace(0, h, 30)
x_def = deformada_emp_art(y_col, h, u_top)

# Columna izquierda
ax.plot(1 + x_def, y_col, 'b-', lw=3)
# Columna derecha
ax.plot(7 + x_def, y_col, 'b-', lw=3)

# Articulaciones en nodos superiores (debajo de la viga)
r_art = 0.08
dibujar_articulacion(ax, 1 + x_def[-1], h - r_art)
dibujar_articulacion(ax, 7 + x_def[-1], h - r_art)

# Viga (permanece horizontal, se traslada, conecta sobre las articulaciones)
ax.plot([1 + x_def[-1], 7 + x_def[-1]], [h, h], 'b-', lw=4)

# Posicion original (discontinua)
ax.plot([1, 1], [0, h], 'k--', lw=1, alpha=0.3)
ax.plot([7, 7], [0, h], 'k--', lw=1, alpha=0.3)
ax.plot([1, 7], [h, h], 'k--', lw=1, alpha=0.3)

# Formula de rigidez
ax.text(4, 4.3, r'$k_c = \frac{3EI_c}{h^3}$', fontsize=11, ha='center',
        bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9, pad=0.4))

# Texto modelo
ax.text(4, -0.5, 'Viga no gira (articulada)', ha='center', fontsize=9,
        style='italic', color='gray')

# ======================
# Panel (c): Modelo viga flexible con nudos rigidos
# ======================
ax = axes[2]
ax.set_xlim(-1, 8)
ax.set_ylim(-1, 5)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title('(c) Viga flexible, nudos rigidos', fontweight='bold', fontsize=10)

# Empotramientos
dibujar_empotramiento(ax, 1, 0)
dibujar_empotramiento(ax, 7, 0)

# Parametros de deformacion
u_top = 0.6
theta_nudo = 0.12  # rotacion del nudo (aumentado para visualizacion)

# Columnas deformadas (empotradas con rotacion theta en nudo superior)
# Deformada de columna biempotrada con desplazamiento u y giro theta en cabeza
# u(y) = u_top * N1(xi) + theta * h * N2(xi) donde N son funciones de forma
def deformada_col_emp_emp(y, h, u_top, theta):
    """Deformada de columna empotrada-empotrada con rotacion de nudo"""
    xi = y / h
    # Funciones de forma Hermite: desplazamiento + rotacion en cabeza
    # Derivada en xi=1: du/dy = -theta (el pilar gira theta respecto a vertical)
    return u_top * (3*xi**2 - 2*xi**3) + theta * h * (xi**2 - xi**3)

y_col = np.linspace(0, h, 50)
x_def_col = deformada_col_emp_emp(y_col, h, u_top, theta_nudo)

# Columna izquierda
ax.plot(1 + x_def_col, y_col, 'b-', lw=3)
# Columna derecha
ax.plot(7 + x_def_col, y_col, 'b-', lw=3)

# Viga deformada - debe mantener 90 grados con pilares en los nudos
# Con rotacion theta antihoraria del nudo: viga empieza subiendo con pendiente theta
# Deformada de viga biempotrada con giros theta iguales en ambos extremos:
# y(s) = h + theta * s * (1 - s/L) * (1 - 2*s/L)
# Esta formula da: y(0)=h, y(L)=h, y'(0)=theta, y'(L)=theta
s_viga = np.linspace(0, L, 50)
xi_v = s_viga / L
# Escalar theta para visualizacion de la curvatura
theta_viga = theta_nudo * 2.5  # factor para hacer visible la curvatura
y_viga = h + theta_viga * s_viga * (1 - xi_v) * (1 - 2*xi_v)

# Posicion x de la viga (desplazada con el nudo)
x_viga_pos = 1 + x_def_col[-1] + s_viga

ax.plot(x_viga_pos, y_viga, 'b-', lw=3)

# Arcos de rotacion en nudos (muestran el giro theta)
# Angulo del arco: desde la horizontal (viga original) hasta la viga deformada
theta_deg = np.degrees(theta_nudo) * 2  # escalar para visualizacion
arc1 = Arc((1 + x_def_col[-1], h), 0.5, 0.5, angle=0, theta1=0, theta2=theta_deg*3,
           color='purple', lw=1.5)
ax.add_patch(arc1)
arc2 = Arc((7 + x_def_col[-1], h), 0.5, 0.5, angle=0, theta1=180-theta_deg*3, theta2=180,
           color='purple', lw=1.5)
ax.add_patch(arc2)

# Posicion original (discontinua)
ax.plot([1, 1], [0, h], 'k--', lw=1, alpha=0.3)
ax.plot([7, 7], [0, h], 'k--', lw=1, alpha=0.3)
ax.plot([1, 7], [h, h], 'k--', lw=1, alpha=0.3)

# Etiqueta theta
ax.text(1.8 + x_def_col[-1], h + 0.4, r'$\theta$', fontsize=9, color='purple')
ax.text(6.5 + x_def_col[-1], h + 0.4, r'$\theta$', fontsize=9, color='purple')

# Formula de rigidez
ax.text(4, 4.3, r'$k_{eff} = \frac{12EI_c}{h^3} \cdot \frac{1}{1+6\rho}$', fontsize=10, ha='center',
        bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.9, pad=0.4))

# Texto modelo
ax.text(4, -0.5, 'Viga gira con columnas (nudo rigido)', ha='center', fontsize=9,
        style='italic', color='gray')

plt.tight_layout()
plt.savefig(output_dir / "fig_problema_19_portico.pdf")
plt.savefig(output_dir / "fig_problema_19_portico.png")
plt.close()

print(f"Figura guardada en: {output_dir / 'fig_problema_19_portico.pdf'}")
