import streamlit as st

from calculos import (
    calcular_tempo_parado,
    calcular_df,
    calcular_utilizacao,
    calcular_tempo_perdido,
    calcular_tempo_total,  # Importe a função calcular_tempo_total
)
from graficos import gerar_grafico

# Configuração da página
st.set_page_config(
    page_title="Dimensionamento da Frota de Caminhões",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Tema escuro (configurado no arquivo config.toml)

# Inicializa dados_caminhoes na session_state se não existir
if "dados_caminhoes" not in st.session_state:
    st.session_state.dados_caminhoes = []

# Título principal
st.markdown(
    "<h1 style='text-align: center;'>Dimensionamento da Frota de Caminhões</h1>",
    unsafe_allow_html=True,
)

# Divide a tela em duas colunas
col1, col2 = st.columns([1, 3])

# Barra lateral com os parâmetros de entrada
with col1:
    st.sidebar.subheader("Parâmetros de Entrada")
    num_caminhoes = st.sidebar.slider(
        "Quantos caminhões sua frota possui?", 1, 20, 8, 1
    )
    caminhoes = [f"CM-{i+1:03}" for i in range(num_caminhoes)]

    # Lista suspensa para selecionar o caminhão
    selected_caminhao = st.sidebar.selectbox("Selecione o caminhão:", caminhoes)

    # Loop para coletar as informações de cada caminhão
    for i, caminhao in enumerate(caminhoes):
        # Verifica se já existem dados para este caminhão na session_state
        if i < len(st.session_state.dados_caminhoes):
            dados_caminhao = st.session_state.dados_caminhoes[i]
        else:
            # Cria um novo dicionário com valores padrão se não houver dados
            dados_caminhao = {
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
            }
            st.session_state.dados_caminhoes.append(dados_caminhao)

        # Exibe as configurações para o caminhão selecionado
        if caminhao == selected_caminhao:
            with st.expander(
                f"Configurações do caminhão {caminhao}", expanded=True
            ):

                # Campos para o usuário inserir a quantidade de cada tipo de serviço e parada
                dados_caminhao["qtd_250h"] = st.number_input(
                    f"Qtd Preventiva 250h ({caminhao})",
                    min_value=0,
                    value=dados_caminhao["qtd_250h"],
                    step=1,
                )
                dados_caminhao["qtd_500h"] = st.number_input(
                    f"Qtd Preventiva 500h ({caminhao})",
                    min_value=0,
                    value=dados_caminhao["qtd_500h"],
                    step=1,
                )
                dados_caminhao["qtd_1000h"] = st.number_input(
                    f"Qtd Preventiva 1000h ({caminhao})",
                    min_value=0,
                    value=dados_caminhao["qtd_1000h"],
                    step=1,
                )
                dados_caminhao["qtd_16000h"] = st.number_input(
                    f"Qtd Preventiva 16000h ({caminhao})",
                    min_value=0,
                    value=dados_caminhao["qtd_16000h"],
                    step=1,
                )

                dados_caminhao["taxa_corretiva"] = (
                    st.number_input(
                        f"Taxa Corretiva (%) ({caminhao})",
                        min_value=0,
                        max_value=100,
                        value=int(dados_caminhao["taxa_corretiva"] * 100),
                    )
                    / 100
                )

                # ... (outros campos de parada) ...
                dados_caminhao["qtd_sem_operador"] = st.number_input(
                    f"Qtd Sem Operador ({caminhao})",
                    min_value=0,
                    value=dados_caminhao.get("qtd_sem_operador", 0),
                    step=1,
                )
                dados_caminhao["qtd_parada_desmonte"] = st.number_input(
                    f"Qtd Parada Desmonte ({caminhao})",
                    min_value=0,
                    value=dados_caminhao.get("qtd_parada_desmonte", 0),
                    step=1,
                )
                dados_caminhao["qtd_parada_climatica"] = st.number_input(
                    f"Qtd Parada Climática ({caminhao})",
                    min_value=0,
                    value=dados_caminhao.get("qtd_parada_climatica", 0),
                    step=1,
                )
                dados_caminhao["qtd_almoco"] = st.number_input(
                    f"Qtd Almoço ({caminhao})",
                    min_value=0,
                    value=dados_caminhao.get("qtd_almoco", 0),
                    step=1,
                )
                dados_caminhao["qtd_troca_turno"] = st.number_input(
                    f"Qtd Troca de Turno ({caminhao})",
                    min_value=0,
                    value=dados_caminhao.get("qtd_troca_turno", 0),
                    step=1,
                )

                # Campos para o usuário inserir o percentual de absenteísmo e treinamento
                dados_caminhao["perc_absenteismo"] = st.number_input(
                    f"Percentual Absenteísmo (%) ({caminhao})",
                    min_value=0.0,
                    max_value=100.0,
                    value=dados_caminhao.get("perc_absenteismo", 0.0),
                    step=0.1,
                    format="%.1f",
                )
                dados_caminhao["perc_treinamento"] = st.number_input(
                    f"Percentual Treinamento (%) ({caminhao})",
                    min_value=0.0,
                    max_value=100.0,
                    value=dados_caminhao.get("perc_treinamento", 0.0),
                    step=0.1,
                    format="%.1f",
                )

                # Calcula e exibe a utilização, horas não utilizadas e horas trabalhadas
                (
                    utilizacao,
                    horas_nao_utilizadas,
                    horas_trabalhadas,
                    horas_disponiveis,
                    
                ) = calcular_utilizacao(dados_caminhao)
                tempo_total_parado = calcular_tempo_parado(dados_caminhao)
                df = calcular_df(tempo_total_parado)  # Calcula a DF aqui
                col_utilizacao, col_tempos = st.columns(2)
                with col_utilizacao:
                    st.container()
                    st.write(f"Utilização: {utilizacao:.2f}%")
                    st.write(f"Horas não utilizadas: {horas_nao_utilizadas:.2f}")
                    st.write(f"Horas trabalhadas: {horas_trabalhadas:.2f}")
                with col_tempos:
                    st.container()
                    st.write(f"Horas disponíveis: {horas_disponiveis:.2f}")
                    st.write(f"DF: {df:.2f}%")  # Exibe a DF aqui
                

                # Calcula e exibe o tempo perdido em cada operação
                tempo_perdido = calcular_tempo_perdido(dados_caminhao)
                for operacao, tempo in tempo_perdido.items():
                    st.write(f"{operacao}: {tempo:.2f} horas")

                # Atualiza os dados na session_state
                st.session_state.dados_caminhoes[i] = dados_caminhao

# Conteúdo principal com o gráfico e o resumo da disponibilidade
with col2:
    st.subheader("Disponibilidade da Frota")

    # Calcula a DF após a atualização da lista de caminhões
    dfs_caminhoes = []
    for caminhao in caminhoes:  # Itera sobre a lista atualizada de caminhões
        for dados in st.session_state.dados_caminhoes:
            if (
                dados["caminhao"] == caminhao
            ):  # Encontra os dados do caminhão
                try:
                    tempo_total_parado = calcular_tempo_parado(dados)
                    df = calcular_df(tempo_total_parado)
                    dfs_caminhoes.append(df)
                except ValueError:
                    st.error(
                        f"Entrada inválida para o caminhão {dados['caminhao']}. Por favor, verifique os dados."
                    )
                    # Interrompe o loop em caso de erro
                    break
                break  # Sai do loop interno após encontrar os dados do caminhão

    # Gráfico com fundo ajustado dinamicamente, tamanho menor e rotação dos rótulos
    if dfs_caminhoes:
        gerar_grafico(caminhoes, dfs_caminhoes)

    # Resumo da disponibilidade centralizado e em destaque
    st.markdown("<br>", unsafe_allow_html=True)
    if dfs_caminhoes:
        total_df = sum(dfs_caminhoes) / len(dfs_caminhoes)
        st.markdown(
            f"<h2 style='text-align: center;'>Disponibilidade da Frota: {total_df:.2f}%</h2>",
            unsafe_allow_html=True,
        )
    else:
        st.write("**Nenhum dado de caminhão disponível.**")
