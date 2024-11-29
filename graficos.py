import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def gerar_grafico(caminhoes, dfs_caminhoes):
    """Gera um gráfico de barras com a DF de cada caminhão."""
    fig, ax = plt.subplots(
        figsize=(2, 1), facecolor=st.get_option("theme.backgroundColor")
    )
    cores = plt.cm.viridis(np.linspace(0, 1, len(caminhoes)))
    ax.bar(caminhoes, dfs_caminhoes, color=cores)
    ax.set_ylabel("Disponibilidade Física (%)", fontsize=5, color="white")
    ax.set_title(
        "Comparativo de Disponibilidade da Frota",
        fontsize=5,
        color="white",
    )
    ax.set_ylim(0, 100)
    ax.tick_params(axis="x", colors="black", rotation=45, labelsize=5)
    ax.tick_params(axis="y", colors="black", labelsize=5)
    st.pyplot(fig)
