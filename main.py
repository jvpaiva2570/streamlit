import streamlit as st
from multipage import MultiPage



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

# Configuração da página
st.set_page_config(
    page_title="mina minério de ferro",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Tema escuro (configurado no arquivo config.toml)

# Inicializa dados_caminhoes na session_state se não existir
if "dados_caminhoes" not in st.session_state:
    st.session_state.dados_caminhoes = []

# Título principal
st.markdown(
    "<h1 style='text-align: center;'>Dimensionamento de uma mina de minério de ferro</h1>",
    unsafe_allow_html=True,
)

# Divide a tela em duas colunas com larguras ajustadas
col1, col2 = st.columns([2, 1])  # Ajuste a proporção conforme necessário

# Barra lateral com os parâmetros de entrada
with st.sidebar:
    st.subheader("Parâmetros de Entrada")
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

                # Calcula a DF
                tempo_total_parado = calcular_tempo_parado(dados_caminhao)
                df = calcular_df(tempo_total_parado)  # Calcula a DF aqui

                # Divide a área em duas colunas
                col_utilizacao, col_tempos = st.columns(2)

                # Primeira coluna: Utilização, Horas Não Utilizadas, Horas Trabalhadas
                with col_utilizacao:
                    st.container()
                    st.write(f"Utilização: {utilizacao:.2f}%")
                    st.write(f"Horas não utilizadas: {horas_nao_utilizadas:.2f}")
                    st.write(f"Horas trabalhadas: {horas_trabalhadas:.2f}")

                # Segunda coluna: Horas Disponíveis, DF, Tempo Perdido
                with col_tempos:
                    st.container()
                    st.write(f"Horas disponíveis: {horas_disponiveis:.2f}")
                    st.write(f"DF: {df:.2f}%")

                    # Calcula e exibe o tempo perdido em cada operação
                    tempo_perdido = calcular_tempo_perdido(
                        dados_caminhao
                    )  # Passe horas_trabalhadas como argumento
                    for operacao, tempo in tempo_perdido.items():
                        st.write(f"{operacao}: {tempo:.2f} horas")

                # Atualiza os dados na session_state
                st.session_state.dados_caminhoes[i] = dados_caminhao

# Conteúdo principal
col1, col2 = st.columns([2, 1])  # Divide o conteúdo principal em duas colunas

# Subseção Gráficos
with col1:
    st.subheader("Gráficos")

    # Calcula a DF após a atualização da lista de caminhões
    dfs_caminhoes = []
    utilizacoes = []  # Lista para armazenar as utilizações
    for caminhao in caminhoes:  # Itera sobre a lista atualizada de caminhões
        for dados in st.session_state.dados_caminhoes:
            if (
                dados["caminhao"] == caminhao
            ):  # Encontra os dados do caminhão
                try:
                    tempo_total_parado = calcular_tempo_parado(dados)
                    df = calcular_df(tempo_total_parado)
                    dfs_caminhoes.append(df)

                    # Calcula a utilização e adiciona à lista
                    (
                        utilizacao,
                        _,
                        _,
                        _,
                    ) = calcular_utilizacao(dados_caminhao)
                    utilizacoes.append(utilizacao)

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

        # Gera o gráfico de DF x Utilização
        gerar_grafico_df_utilizacao(caminhoes, dfs_caminhoes, utilizacoes)

# Subseção Resumo
with col2:
    st.subheader("Resumo")

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

    # Resumo da disponibilidade centralizado e em destaque
    st.markdown("<br>", unsafe_allow_html=True)
    if dfs_caminhoes:
        total_df = sum(dfs_caminhoes) / len(dfs_caminhoes)
        total_utilizacao= sum(utilizacoes)/len(utilizacoes)
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

# Cria uma nova página
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

    else:
        st.error(
            "Pelo menos uma distância ou velocidade deve ser maior que zero. Verifique os dados de entrada."
        )
# Mecanismo de navegação
app = MultiPage()

ef pagina_inicial():
    import streamlit as st
    st.title("Página Inicial")

def pagina_outra():
    import streamlit as st
    st.title("Outra Página")

app.add_page("Página Inicial", pagina_inicial)
app.add_page("Outra Página", pagina_outra)

 Executa o app
if __name__ == "__main__":
    app.run()
