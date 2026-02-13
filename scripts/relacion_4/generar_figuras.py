# -*- coding: utf-8 -*-
"""
Generador de figuras para Relacion 4 - Sistemas Continuos
Problemas: 02 (viga biapoyada), 03 (viga biempotrada)
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, Polygon
import os

# Configuracion para figuras de calidad
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['font.family'] = 'serif'
plt.rcParams['text.usetex'] = False
plt.rcParams['mathtext.fontset'] = 'cm'

# Directorio de salida
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'figs')
os.makedirs(OUTPUT_DIR, exist_ok=True)


def dibujar_apoyo_simple(ax, x, y, size=0.15, color='gray'):
    """Dibuja un apoyo simple (triangulo)"""
    triangle = Polygon([(x, y), (x-size/2, y-size), (x+size/2, y-size)],
                       closed=True, facecolor=color, edgecolor='black', linewidth=1)
    ax.add_patch(triangle)
    # Linea de suelo
    ax.plot([x-size*0.8, x+size*0.8], [y-size, y-size], 'k-', linewidth=1.5)


def dibujar_empotramiento(ax, x, y, altura=0.4, ancho=0.15, left=True):
    """Dibuja un empotramiento"""
    if left:
        rect = Rectangle((x-ancho, y-altura/2), ancho, altura,
                         facecolor='gray', edgecolor='black', linewidth=1, hatch='///')
    else:
        rect = Rectangle((x, y-altura/2), ancho, altura,
                         facecolor='gray', edgecolor='black', linewidth=1, hatch='///')
    ax.add_patch(rect)


def fig_problema_02():
    """
    Problema 02: Viga biapoyada - Modos de vibracion
    Muestra esquema de la viga y los 4 primeros modos sin(n*pi*x/L)
    """
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle('Problema 2: Viga biapoyada - Modos de vibracion', fontsize=14, fontweight='bold')

    L = 6.0  # m
    x = np.linspace(0, L, 200)

    # Frecuencias calculadas
    freqs = [5.75, 23.0, 51.7, 91.9]  # Hz

    for idx, ax in enumerate(axes.flat):
        n = idx + 1

        # Forma modal: sin(n*pi*x/L)
        phi = np.sin(n * np.pi * x / L)

        # Escalar para visualizacion
        scale = 0.8
        phi_scaled = phi * scale

        # Dibujar viga deformada
        ax.fill_between(x, phi_scaled, alpha=0.3, color='blue')
        ax.plot(x, phi_scaled, 'b-', linewidth=2, label=f'Modo {n}')
        ax.plot(x, np.zeros_like(x), 'k-', linewidth=3)  # Viga sin deformar

        # Apoyos simples
        dibujar_apoyo_simple(ax, 0, 0, size=0.3)
        dibujar_apoyo_simple(ax, L, 0, size=0.3)

        # Nodos (puntos donde phi=0)
        nodos = []
        for i in range(1, n):
            x_nodo = i * L / n
            nodos.append(x_nodo)
            ax.plot(x_nodo, 0, 'ro', markersize=8, zorder=5)

        # Etiquetas
        ax.set_title(f'Modo {n}: $f_{n} = {freqs[idx]:.1f}$ Hz\n' +
                    r'$\phi_' + str(n) + r'(x) = \sin(' + str(n) + r'\pi x/L)$',
                    fontsize=11)
        ax.set_xlim(-0.5, L+0.5)
        ax.set_ylim(-1.5, 1.5)
        ax.set_xlabel('x (m)')
        ax.set_ylabel('Amplitud modal')
        ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.5)
        ax.grid(True, alpha=0.3)

        # Anotar nodos
        if nodos:
            ax.annotate(f'{n-1} nodo(s)', xy=(L/2, -1.2), fontsize=9, ha='center',
                       style='italic', color='red')

    plt.tight_layout()

    filepath = os.path.join(OUTPUT_DIR, 'fig_problema_02_viga_biapoyada.pdf')
    plt.savefig(filepath, bbox_inches='tight')
    plt.close()
    print(f"[OK] Generada: fig_problema_02_viga_biapoyada.pdf")


def fig_problema_03():
    """
    Problema 03: Viga biempotrada vs biapoyada - Comparacion de modos
    """
    fig, axes = plt.subplots(2, 3, figsize=(14, 8))
    fig.suptitle('Problema 3: Comparacion viga biempotrada vs biapoyada',
                 fontsize=14, fontweight='bold')

    L = 8.0  # m
    x = np.linspace(0, L, 300)

    # Frecuencias
    f_biemp = [8.40, 23.2, 45.4]  # Hz
    f_biap = [3.71, 14.8, 33.4]   # Hz

    # Coeficientes beta*L para biempotrada
    beta_L = [4.7300, 7.8532, 10.9956]

    for n in range(3):
        # Biempotrada (arriba)
        ax_top = axes[0, n]
        beta = beta_L[n] / L

        # Forma modal biempotrada (aproximada)
        sigma = (np.cosh(beta_L[n]) - np.cos(beta_L[n])) / (np.sinh(beta_L[n]) - np.sin(beta_L[n]))
        phi_emp = (np.cosh(beta*x) - np.cos(beta*x)) - sigma * (np.sinh(beta*x) - np.sin(beta*x))
        phi_emp = phi_emp / np.max(np.abs(phi_emp)) * 0.8

        ax_top.fill_between(x, phi_emp, alpha=0.3, color='blue')
        ax_top.plot(x, phi_emp, 'b-', linewidth=2)
        ax_top.plot(x, np.zeros_like(x), 'k-', linewidth=3)

        # Empotramientos
        dibujar_empotramiento(ax_top, 0, 0, altura=0.5, left=True)
        dibujar_empotramiento(ax_top, L, 0, altura=0.5, left=False)

        ax_top.set_title(f'Biempotrada - Modo {n+1}\n$f_{n+1} = {f_biemp[n]:.1f}$ Hz', fontsize=11)
        ax_top.set_xlim(-0.5, L+0.5)
        ax_top.set_ylim(-1.2, 1.2)
        ax_top.set_ylabel('Amplitud')
        ax_top.axhline(y=0, color='gray', linestyle='--', linewidth=0.5)
        ax_top.grid(True, alpha=0.3)

        # Biapoyada (abajo)
        ax_bot = axes[1, n]
        phi_ap = np.sin((n+1) * np.pi * x / L) * 0.8

        ax_bot.fill_between(x, phi_ap, alpha=0.3, color='green')
        ax_bot.plot(x, phi_ap, 'g-', linewidth=2)
        ax_bot.plot(x, np.zeros_like(x), 'k-', linewidth=3)

        # Apoyos simples
        dibujar_apoyo_simple(ax_bot, 0, 0, size=0.3)
        dibujar_apoyo_simple(ax_bot, L, 0, size=0.3)

        ax_bot.set_title(f'Biapoyada - Modo {n+1}\n$f_{n+1} = {f_biap[n]:.1f}$ Hz', fontsize=11)
        ax_bot.set_xlim(-0.5, L+0.5)
        ax_bot.set_ylim(-1.2, 1.2)
        ax_bot.set_xlabel('x (m)')
        ax_bot.set_ylabel('Amplitud')
        ax_bot.axhline(y=0, color='gray', linestyle='--', linewidth=0.5)
        ax_bot.grid(True, alpha=0.3)

        # Ratio de frecuencias
        ratio = f_biemp[n] / f_biap[n]
        ax_bot.annotate(f'Ratio: {ratio:.2f}x', xy=(L/2, -0.95), fontsize=10,
                       ha='center', fontweight='bold', color='purple')

    plt.tight_layout()

    filepath = os.path.join(OUTPUT_DIR, 'fig_problema_03_comparacion_vigas.pdf')
    plt.savefig(filepath, bbox_inches='tight')
    plt.close()
    print(f"[OK] Generada: fig_problema_03_comparacion_vigas.pdf")


if __name__ == '__main__':
    print("Generando figuras para Relacion 4 - Sistemas Continuos...")
    print("-" * 50)

    fig_problema_02()
    fig_problema_03()

    print("-" * 50)
    print("Figuras generadas en:", OUTPUT_DIR)
