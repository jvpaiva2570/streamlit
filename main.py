# Importação de Bibliotecas
import streamlit as st
from calculos import (
    calcular_tempo_parado,
    calcular_df,
    calcular_utilizacao,
    calcular_tempo_perdido,
    calcular_tempo_total,
    calcular_tempo_ciclo,
    calcular_tempo_ciclo_total,
    calcular_capacidade_liquida,
    calcular_produtividade_horaria,
)
from graficos import gerar_grafico, gerar_grafico_df_utilizacao

# Configuração da Página do Streamlit
st.set_page_config(
    page_title="Mina de Minério de Ferro",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- Função de Inicialização ---
def inicializar_dados(num_caminhoes):
    """Inicializa os dados dos caminhões na session_state."""
    dados_caminhoes = []
    for i in range(num_caminhoes):
        caminhao = f"CM-{i + 1:03}"
        dados_caminhoes.append({
            "caminhao": caminhao,
            "qtd_250h": 35,
            "qtd_500h": 18,
            "qtd_1000h": 9,
            "qtd_16000h": 0,
            "taxa_corretiva": 0.25,
            "qtd_sem_operador": 0,
            "qtd_parada_desmonte": 0,
            "qtd_parada_climatica": 0,
            "qtd_almoco": 0,
            "qtd_troca_turno": 0,
            "perc_absenteismo": 0.0,
            "perc_treinamento": 0.0,
        })
    return dados_caminhoes

# --- Carregar Session State ---
if "dados_caminhoes" not in st.session_state:
    st.session_state.dados_caminhoes = inicializar_dados(num_caminhoes=8)

# --- Barra Lateral ---
with st.sidebar:
    st.markdown("### **Parâmetros de Entrada**")
    st.write("Defina os parâmetros gerais da frota e configure os caminhões.")
    num_caminhoes = st.slider(
        "Quantos caminhões sua frota possui?", 1, 20, 8, 1
    )
    caminhoes = [f"CM-{i+1:03}" for i in range(num_caminhoes)]

# --- Página Principal ---
st.title("Gestão da Frota de Caminhões")
st.write("Configure e analise os dados operacionais dos caminhões.")

# --- Exibir Configurações por Caminhão ---
selected_caminhao = st.selectbox("Selecione um caminhão para configurar:", caminhoes)
for i, caminhao in enumerate(caminhoes):
    if caminhao == selected_caminhao:
        with st.expander(f"Configurações do caminhão {caminhao}", expanded=True):
            dados_caminhao = st.session_state.dados_caminhoes[i]
            resultados = calcular_metrica_caminhao(dados_caminhao)
            
            # Exibição de Métricas
            col1, col2 = st.columns(2)
            col1.metric("Utilização", f"{resultados['utilizacao']:.2f}%")
            col2.metric("DF", f"{resultados['df']:.2f}%")
            st.write(f"**Horas Perdidas**: {resultados['tempo_perdido']} h")
            st.write(f"**Horas Disponíveis**: {resultados['horas_disponiveis']} h")

# --- Página Produtividade ---
st.subheader("Cálculo da Produtividade Horária")
with st.form("form_produtividade"):
    st.write("Insira os dados abaixo para calcular a produtividade.")
    col1, col2 = st.columns(2)
    with col1:
        distancia_horizontal = st.number_input("Distância Horizontal (m):", min_value=0.0)
        velocidade_horizontal_carregado = st.number_input("Velocidade Carregado (km/h):", min_value=0.0)
    with col2:
        capacidade_caminhao = st.number_input("Capacidade (ton):", min_value=0.0)
        fator_enchimento = st.number_input("Fator Enchimento (%):", min_value=0.0, max_value=100.0)
    
    submit = st.form_submit_button("Calcular")

if submit:
    if capacidade_caminhao > 0 and fator_enchimento > 0:
        capacidade_liquida = calcular_capacidade_liquida(capacidade_caminhao, fator_enchimento)
        tempo_ciclo = calcular_tempo_ciclo(distancia_horizontal, velocidade_horizontal_carregado)
        produtividade = calcular_produtividade_horaria(capacidade_liquida, tempo_ciclo)
        st.success(f"Produtividade Horária: {produtividade:.2f} ton/h")
    else:
        st.error("Preencha os dados corretamente!")

# --- Exibição de Gráficos ---
if st.button("Gerar Gráficos"):
    dfs_caminhoes = [calcular_df(dados) for dados in st.session_state.dados_caminhoes]
    gerar_grafico(caminhoes, dfs_caminhoes, "Disponibilidade por Caminhão", "Caminhões", "DF (%)")
