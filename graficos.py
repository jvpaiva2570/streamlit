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

def gerar_grafico_df_utilizacao(caminhoes, dfs, utilizacoes):
  """Gera um gráfico de barras comparando a DF com a Utilização."""

  fig, ax = plt.subplots(figsize=(10, 4))
  bar_width = 0.35
  index = np.arange(len(caminhoes))

  barras_df = ax.bar(index, dfs, bar_width, label="DF", color='skyblue')
  barras_utilizacao = ax.bar(index + bar_width, utilizacoes, bar_width, label="Utilização", color='lightcoral')

  ax.set_xlabel("Caminhões", fontsize=12)
  ax.set_ylabel("Percentual (%)", fontsize=12)
  ax.set_title("Comparativo DF x Utilização", fontsize=14)
  ax.set_xticks(index + bar_width / 2)
  ax.set_xticklabels(caminhoes)
  ax.legend()

  plt.xticks(rotation=45)
  st.pyplot(fig)
