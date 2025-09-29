import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import math
import matplotlib.patches as patches

# --- Configuración de la Página ---
st.set_page_config(
    layout="wide", page_title="Visualizador de Suma de Fracciones")

st.title("🔢 Visualizador Interactivo de Suma de Fracciones v2")
st.write(
    "Controla manualmente el factor de conversión para ver cómo se subdividen las fracciones y encontrar el denominador común."
)

# --- Funciones de Lógica y Visualización ---


def get_lcm(a, b):
    """Calcula el mínimo común múltiplo (MCM) de dos números."""
    return abs(a * b) // math.gcd(a, b) if a != 0 and b != 0 else 0


def create_fraction_pie(numerator, denominator, subdivision_factor, title, highlight_color):
    """
    Crea una figura de Matplotlib que representa una fracción en un círculo,
    mostrando las subdivisiones según el factor introducido.
    """
    fig, ax = plt.subplots(figsize=(3.5, 3.5))
    ax.set_aspect('equal')
    ax.axis('off')

    # Dibuja las rebanadas seleccionadas (numerador)
    for i in range(numerator):
        start_angle = i * (360 / denominator)
        end_angle = (i + 1) * (360 / denominator)
        wedge = patches.Wedge((0, 0), 1, start_angle, end_angle,
                              facecolor=highlight_color, edgecolor='black', lw=1.5, alpha=0.8)
        ax.add_patch(wedge)

    # Dibuja las rebanadas no seleccionadas
    for i in range(numerator, denominator):
        start_angle = i * (360 / denominator)
        end_angle = (i + 1) * (360 / denominator)
        wedge = patches.Wedge((0, 0), 1, start_angle, end_angle,
                              facecolor='lightgray', alpha=0.4, edgecolor='black', lw=1.5)
        ax.add_patch(wedge)

    # Dibuja las líneas de subdivisión basadas en el factor (NUEVO)
    total_subdivisions = denominator * subdivision_factor
    if total_subdivisions > denominator:
        angles_sub = np.linspace(0, 360, total_subdivisions + 1)
        for angle in angles_sub:
            rad = np.deg2rad(angle)
            ax.plot([0, np.cos(rad)], [0, np.sin(rad)],
                    color='gray', lw=0.8, linestyle='--')

    # Dibuja un círculo exterior para que se vea limpio
    outer_circle = plt.Circle((0, 0), 1, color='black', fill=False, lw=2)
    ax.add_artist(outer_circle)

    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    ax.set_title(title, fontsize=20, pad=10)

    return fig

# --- Interfaz de Usuario (UI) ---


st.sidebar.header("⚙️ 1. Configura las Fracciones")
d1 = st.sidebar.number_input(
    "Denominador de la Fracción 1", min_value=1, max_value=20, value=6, step=1)
d2 = st.sidebar.number_input(
    "Denominador de la Fracción 2", min_value=1, max_value=20, value=9, step=1)

st.sidebar.header("🎨 2. Selecciona las Partes")
n1 = st.sidebar.slider(f"Numerador 1 (Partes de {d1})", 0, d1, 1)
n2 = st.sidebar.slider(f"Numerador 2 (Partes de {d2})", 0, d2, 1)

# --- Cálculos y Lógica ---
common_denominator = get_lcm(d1, d2)
correct_factor1 = common_denominator // d1
correct_factor2 = common_denominator // d2

# --- Visualización y Entradas de Factor (NUEVO) ---
st.header("Fracciones y Proceso de Subdivisión")

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"### Fracción 1: ${n1}/{d1}$")
    # Ventanita para el factor 1
    factor1 = st.number_input(
        "Multiplicar por el factor:", min_value=1, max_value=20, value=1, key='factor1')

    # El color cambia a verde si se ha seleccionado un numerador
    color1 = 'mediumseagreen' if n1 > 0 or n2 > 0 else 'cornflowerblue'

    fig1 = create_fraction_pie(
        n1, d1, factor1, f"$\\frac{{{n1}}}{{{d1}}}$", color1)
    st.pyplot(fig1, use_container_width=False)

    # Muestra la conversión en tiempo real
    st.latex(f"\\frac{{{n1}}}{{{d1}}} \\times \\frac{{{factor1}}}{{{
             factor1}}} = \\frac{{{n1 * factor1}}}{{{d1 * factor1}}}")
    if factor1 == correct_factor1 and d1 * factor1 == common_denominator:
        st.success(f"¡Factor correcto! El denominador es {
                   common_denominator}.")

with col2: 
    st.markdown(f"### Fracción 2: ${n2}/{d2}$")
    # Ventanita para el factor 2
    factor2 = st.number_input(
        "Multiplicar por el factor:", min_value=1, max_value=20, value=1, key='factor2')

    # El color cambia a verde si se ha seleccionado un numerador
    color2 = 'mediumseagreen' if n1 > 0 or n2 > 0 else 'salmon'

    fig2 = create_fraction_pie(
        n2, d2, factor2, f"$\\frac{{{n2}}}{{{d2}}}$", color2 )
    st.pyplot(fig2,use_container_width=False)
    # Muestra la conversión en tiempo real
    st.latex(f"\\frac{{{n2}}}{{{d2}}} \\times \\frac{{{factor2}}}{{{
             factor2}}} = \\frac{{{n2 * factor2}}}{{{d2 * factor2}}}")
    if factor2 == correct_factor2 and d2 * factor2 == common_denominator:
        st.success(f"¡Factor correcto! El denominador es {
                   common_denominator}.")

# --- Resultado Final ---
st.header("Resultado de la Suma")


# Solo muestra el resultado si los factores son correctos
if factor1 == correct_factor1 and factor2 == correct_factor2:
    new_n1 = n1 * factor1
    new_n2 = n2 * factor2
    sum_numerator = new_n1 + new_n2

    maxcdiv = math.gcd(sum_numerator, common_denominator)

    st.markdown(
        "Una vez que ambas fracciones tienen el mismo denominador, podemos sumar los numeradores:")
    sum_latex = f"\\frac{{{new_n1}}}{{{common_denominator}}} + \\frac{{{new_n2}}}{{{
        common_denominator}}} = \\frac{{{sum_numerator}}}{{{common_denominator}}}"
    st.latex(sum_latex)
    st.success(f"**El resultado final es {sum_numerator //
               maxcdiv}/{common_denominator // maxcdiv}.**")
else:
    st.warning(
        "Introduce los factores correctos en ambas fracciones para poder calcular la suma.")
