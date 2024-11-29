# main.py

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
    calcular_produtividade_horaria
)
from graficos import gerar_grafico, gerar_grafico_df_utilizacao

# Configuração da Página do Streamlit
st.set_page_config(
    page_title="Mina de Minério de Ferro",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- Função para Calcular Métricas ---
def calcular_metricas(caminhoes, dados_caminhoes):
    """
    Calcula DF e Utilização para cada caminhão.

    Retorna:
        dfs_caminhoes (list): Lista de DF para cada caminhão.
        utilizacoes (list): Lista de Utilização para cada caminhão.
    """
    dfs_caminhoes = []
    utilizacoes = []
    for caminhao in caminhões:
        for dados in dados_caminhoes:
            if dados["caminhao"] == caminhao:
                try:
                    tempo_total_parado = calcular_tempo_parado(dados)
                    df = calcular_df(tempo_total_parado)
                    dfs_caminhoes.append(df)

                    utilizacao, _, _, _ = calcular_utilizacao(dados)
                    utilizacoes.append(utilizacao)
                except ValueError:
                    st.error(
                        f"Entrada inválida para o caminhão {dados['caminhao']}. Por favor, verifique os dados."
                    )
                break  # Sai do loop interno após encontrar os dados do caminhão
    return dfs_caminhoes, utilizacoes

# --- Inicialização de Dados ---
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
    # Inicializa com 8 caminhões por padrão
    st.session_state.dados_caminhoes = inicializar_dados(num_caminhoes=8)

# --- Título Principal ---
st.markdown(
    "<h1 style='text-align: center;'>Dimensionamento de uma Mina de Minério de Ferro</h1>",
    unsafe_allow_html=True,
)

# --- Barra Lateral com Parâmetros de Entrada ---
with st.sidebar:
    st.subheader("Parâmetros de Entrada")
    num_caminhoes = st.slider(
        "Quantos caminhões sua frota possui?", 1, 20, 8, 1
    )
    caminhoes = [f"CM-{i+1:03}" for i in range(num_caminhoes)]

    # Ajusta a lista de caminhões no session_state caso o número tenha mudado
    if len(st.session_state.dados_caminhoes) != num_caminhoes:
        if len(st.session_state.dados_caminhoes) < num_caminhoes:
            # Adiciona novos caminhões
            novos = inicializar_dados(num_caminhoes - len(st.session_state.dados_caminhoes))
            st.session_state.dados_caminhoes.extend(novos)
        else:
            # Remove caminhões excedentes
            st.session_state.dados_caminhoes = st.session_state.dados_caminhoes[:num_caminhoes]

    # Lista suspensa para selecionar o caminhão
    selected_caminhao = st.selectbox("Selecione o caminhão para configurar:", caminhoes)

    # Encontrar o índice do caminhão selecionado
    index_caminhao = caminhoes.index(selected_caminhao)

    # Obter os dados do caminhão selecionado
    dados_caminhao = st.session_state.dados_caminhoes[index_caminhao]

    # Exibe as configurações para o caminhão selecionado
    with st.expander(f"Configurações do caminhão {selected_caminhao}", expanded=True):

        # Campos para o usuário inserir a quantidade de cada tipo de serviço e parada
        dados_caminhao["qtd_250h"] = st.number_input(
            f"Qtd Preventiva 250h ({selected_caminhao})",
            min_value=0,
            value=dados_caminhao["qtd_250h"],
            step=1,
        )
        dados_caminhao["qtd_500h"] = st.number_input(
            f"Qtd Preventiva 500h ({selected_caminhao})",
            min_value=0,
            value=dados_caminhao["qtd_500h"],
            step=1,
        )
        dados_caminhao["qtd_1000h"] = st.number_input(
            f"Qtd Preventiva 1000h ({selected_caminhao})",
            min_value=0,
            value=dados_caminhao["qtd_1000h"],
            step=1,
        )
        dados_caminhao["qtd_16000h"] = st.number_input(
            f"Qtd Preventiva 16000h ({selected_caminhao})",
            min_value=0,
            value=dados_caminhao["qtd_16000h"],
            step=1,
        )

        dados_caminhao["taxa_corretiva"] = (
            st.number_input(
                f"Taxa Corretiva (%) ({selected_caminhao})",
                min_value=0,
                max_value=100,
                value=int(dados_caminhao["taxa_corretiva"] * 100),
            )
            / 100
        )

        # Outros campos de parada
        dados_caminhao["qtd_sem_operador"] = st.number_input(
            f"Qtd Sem Operador ({selected_caminhao})",
            min_value=0,
            value=dados_caminhao.get("qtd_sem_operador", 0),
            step=1,
        )
        dados_caminhao["qtd_parada_desmonte"] = st.number_input(
            f"Qtd Parada Desmonte ({selected_caminhao})",
            min_value=0,
            value=dados_caminhao.get("qtd_parada_desmonte", 0),
            step=1,
        )
        dados_caminhao["qtd_parada_climatica"] = st.number_input(
            f"Qtd Parada Climática ({selected_caminhao})",
            min_value=0,
            value=dados_caminhao.get("qtd_parada_climatica", 0),
            step=1,
        )
        dados_caminhao["qtd_almoco"] = st.number_input(
            f"Qtd Almoço ({selected_caminhao})",
            min_value=0,
            value=dados_caminhao.get("qtd_almoco", 0),
            step=1,
        )
        dados_caminhao["qtd_troca_turno"] = st.number_input(
            f"Qtd Troca de Turno ({selected_caminhao})",
            min_value=0,
            value=dados_caminhao.get("qtd_troca_turno", 0),
            step=1,
        )

        # Campos para o usuário inserir o percentual de absenteísmo e treinamento
        dados_caminhao["perc_absenteismo"] = st.number_input(
            f"Percentual Absenteísmo (%) ({selected_caminhao})",
            min_value=0.0,
            max_value=100.0,
            value=dados_caminhao.get("perc_absenteismo", 0.0),
            step=0.1,
            format="%.1f",
        )
        dados_caminhao["perc_treinamento"] = st.number_input(
            f"Percentual Treinamento (%) ({selected_caminhao})",
            min_value=0.0,
            max_value=100.0,
            value=dados_caminhao.get("perc_treinamento", 0.0),
            step=0.1,
            format="%.1f",
        )

        # Atualiza os dados na session_state
        st.session_state.dados_caminhoes[index_caminhao] = dados_caminhao

# --- Conteúdo Principal ---
col1, col2 = st.columns([2, 1])  # Divide o conteúdo principal em duas colunas

# Calcular DF e Utilização
dfs_caminhoes, utilizacoes = calcular_metricas(caminhoes, st.session_state.dados_caminhoes)

# Subseção Gráficos
with col1:
    st.subheader("Gráficos")

    # Gráfico de DF por Caminhão
    if dfs_caminhoes:
        gerar_grafico(caminhoes, dfs_caminhoes)

        # Gráfico de DF x Utilização
        gerar_grafico_df_utilizacao(caminhoes, dfs_caminhoes, utilizacoes)
    else:
        st.write("**Nenhum dado disponível para gerar gráficos.**")

# Subseção Resumo
with col2:
    st.subheader("Resumo")

    # Resumo da disponibilidade e utilização
    st.markdown("<br>", unsafe_allow_html=True)
    if dfs_caminhoes:
        total_df = sum(dfs_caminhoes) / len(dfs_caminhoes)
        total_utilizacao = sum(utilizacoes) / len(utilizacoes)

        # Exibe a disponibilidade da frota em uma caixa com área sombreada
        st.markdown(
            f"""
            <div style="background-color: #f0f0f5; padding: 10px; border-radius: 5px;">
                <h3 style="text-align: center;">Disponibilidade da Frota</h3>
                <h2 style="text-align: center;">{total_df:.2f}%</h2>
            </div>
            """,
            unsafe_allow_html=True,
        )
        # Adiciona um espaçamento entre as caixas
        st.markdown("<br>", unsafe_allow_html=True)
        # Exibe a utilização da frota em outra caixa com área sombreada
        st.markdown(
            f"""
            <div style="background-color: #f0f0f5; padding: 10px; border-radius: 5px;">
                <h3 style="text-align: center;">Utilização da Frota</h3>
                <h2 style="text-align: center;">{total_utilizacao:.2f}%</h2>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.write("**Nenhum dado de caminhão disponível.**")

# --- Página Produtividade ---
def pagina_produtividade():
    # Título da aba
    st.title("Cálculo da Produtividade Horária da Mina")

    # Coleta os dados de entrada do usuário
    st.header("Dados de Distância e Velocidade:")
    distancia_horizontal = st.number_input("Distância Horizontal (metros):", min_value=0.0)
    velocidade_horizontal_carregado = st.number_input(
        "Velocidade Horizontal Carregado (km/h):", min_value=0.0
    )
    velocidade_horizontal_vazio = st.number_input(
        "Velocidade Horizontal Vazio (km/h):", min_value=0.0
    )

    distancia_subida = st.number_input("Distância Subida (metros):", min_value=0.0)
    velocidade_subida_carregado = st.number_input(
        "Velocidade Subida Carregado (km/h):", min_value=0.0
    )
    velocidade_subida_vazio = st.number_input(
        "Velocidade Subida Vazio (km/h):", min_value=0.0
    )

    distancia_descida = st.number_input("Distância Descida (metros):", min_value=0.0)
    velocidade_descida_carregado = st.number_input(
        "Velocidade Descida Carregado (km/h):", min_value=0.0
    )
    velocidade_descida_vazio = st.number_input(
        "Velocidade Descida Vazio (km/h):", min_value=0.0
    )

    st.header("Dados do Caminhão:")
    capacidade_caminhao = st.number_input(
        "Capacidade do Caminhão (toneladas):", min_value=0.0
    )
    fator_enchimento = st.number_input(
        "Fator de Enchimento (%):", min_value=0.0, max_value=100.0
    )

    # Verifica se pelo menos uma distância ou velocidade é maior que zero
    if any(
        [
            distancia_horizontal,
            velocidade_horizontal_carregado,
            velocidade_horizontal_vazio,
            distancia_subida,
            velocidade_subida_carregado,
            velocidade_subida_vazio,
            distancia_descida,
            velocidade_descida_carregado,
            velocidade_descida_vazio,
        ]
    ):
        try:
            # Calcula os tempos de ciclo
            tempo_horizontal_carregado = calcular_tempo_ciclo(
                distancia_horizontal, velocidade_horizontal_carregado
            )
            tempo_horizontal_vazio = calcular_tempo_ciclo(
                distancia_horizontal, velocidade_horizontal_vazio
            )
            tempo_subida_carregado = calcular_tempo_ciclo(
                distancia_subida, velocidade_subida_carregado
            )
            tempo_subida_vazio = calcular_tempo_ciclo(
                distancia_subida, velocidade_subida_vazio
            )
            tempo_descida_carregado = calcular_tempo_ciclo(
                distancia_descida, velocidade_descida_carregado
            )
            tempo_descida_vazio = calcular_tempo_ciclo(
                distancia_descida, velocidade_descida_vazio
            )

            # Calcula o tempo total de ciclo
            tempo_ciclo_total = calcular_tempo_ciclo_total(
                tempo_horizontal_carregado + tempo_horizontal_vazio,
                tempo_subida_carregado + tempo_subida_vazio,
                tempo_descida_carregado + tempo_descida_vazio,
            )

            # Calcula a capacidade líquida do caminhão
            capacidade_liquida = calcular_capacidade_liquida(
                capacidade_caminhao, fator_enchimento
            )

            # Calcula a produtividade horária
            produtividade_horaria = calcular_produtividade_horaria(
                capacidade_liquida, tempo_ciclo_total
            )

            # Exibe os resultados
            st.header("Resultados:")
            st.write(
                f"Tempo de Ciclo Horizontal Carregado: {tempo_horizontal_carregado:.2f} minutos"
            )
            st.write(
                f"Tempo de Ciclo Horizontal Vazio: {tempo_horizontal_vazio:.2f} minutos"
            )
            st.write(f"Tempo de Ciclo Subida Carregado: {tempo_subida_carregado:.2f} minutos")
            st.write(f"Tempo de Ciclo Subida Vazio: {tempo_subida_vazio:.2f} minutos")
            st.write(
                f"Tempo de Ciclo Descida Carregado: {tempo_descida_carregado:.2f} minutos"
            )
            st.write(f"Tempo de Ciclo Descida Vazio: {tempo_descida_vazio:.2f} minutos")
            st.write(f"Tempo Total de Ciclo: {tempo_ciclo_total:.2f} minutos")
            st.write(f"Capacidade Líquida do Caminhão: {capacidade_liquida:.2f} toneladas")
            st.write(f"Produtividade Horária da Mina: {produtividade_horaria:.2f} Ton/h")

        except ValueError as e:
            st.error(f"Erro nos cálculos: {e}")

    else:
        st.error(
            "Pelo menos uma distância ou velocidade deve ser maior que zero. Verifique os dados de entrada."
        )

# --- Navegação Entre Páginas (Usando Tabs Nativas) ---
# Para simplificar e evitar problemas com a classe MultiPage, usaremos tabs nativas do Streamlit.

st.sidebar.markdown("---")
st.sidebar.markdown("<h3 style='text-align: center;'>Navegação</h3>", unsafe_allow_html=True)
pagina = st.sidebar.radio(
    "Selecione a página:", ("Disponibilidade e Utilização", "Produtividade Horária")
)

if pagina == "Disponibilidade e Utilização":
    # Tudo o que está acima referente à Disponibilidade e Utilização já está sendo exibido
    pass  # Nenhuma ação adicional necessária
elif pagina == "Produtividade Horária":
    pagina_produtividade()
