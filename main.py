import streamlit as st
import pandas as pd




# Configuração dos valores fixos (em amarelo)
dias_programados = 365
horas_programadas_por_dia = 24
horas_programadas_ano = dias_programados * horas_programadas_por_dia
tempo_preventiva_250h = 8
tempo_preventiva_500h = 12
tempo_preventiva_1000h = 16
tempo_preventiva_16000h = 168

# Título e layout
st.set_page_config(page_title="Dimensionamento de uma mina")

st.title("Manutenção e Disponibilidade de Caminhões")

# Configuração da tabela de entrada
caminhoes = ["CM-001", "CM-002", "CM-003", "CM-004", "CM-005", "CM-006", "CM-007", "CM-008"]
disponibilidades = []

# Criação das colunas para exibir os dados de cada caminhão
for caminhao in caminhoes:
    with st.expander(f"Configurações para {caminhao}"):
        st.subheader(f"{caminhao}")

        # Campos de entrada para os valores editáveis (quantidades para manutenções preventivas)
        qtd_250h = st.number_input(f"Qtd Preventiva 250h ({caminhao})", min_value=0, value=35)
        qtd_500h = st.number_input(f"Qtd Preventiva 500h ({caminhao})", min_value=0, value=18)
        qtd_1000h = st.number_input(f"Qtd Preventiva 1000h ({caminhao})", min_value=0, value=9)
        qtd_16000h = st.number_input(f"Qtd Preventiva 16000h ({caminhao})", min_value=0, value=0)

        # Campo para taxa de manutenção corretiva
        taxa_corretiva = st.number_input(f"Taxa Corretiva (%) ({caminhao})", min_value=0, max_value=100, value=25) / 100

        # Cálculos do tempo total parado (baseado nas quantidades e tempos preventivos)
        tempo_parado_250h = qtd_250h * tempo_preventiva_250h
        tempo_parado_500h = qtd_500h * tempo_preventiva_500h
        tempo_parado_1000h = qtd_1000h * tempo_preventiva_1000h
        tempo_parado_16000h = qtd_16000h * tempo_preventiva_16000h

        # Tempo corretivo (usando a taxa de corretiva e horas programadas)
        

        # Tempo total parado
        tempo_total_parado = tempo_parado_250h + tempo_parado_500h + tempo_parado_1000h + tempo_parado_16000h 
        tempo_corretivo = taxa_corretiva * tempo_total_parado
        tempo_total_parado+=tempo_corretivo
        # Cálculo da disponibilidade física (DF)
        df = ((horas_programadas_ano - tempo_total_parado) / horas_programadas_ano) * 100
        disponibilidades.append(df)  

        # Exibição dos resultados calculados
        st.write(f"Tempo Total Parado ({caminhao}): {tempo_total_parado:.2f} horas")
        st.write(f"Disponibilidade Física (DF) ({caminhao}): {df:.2f}%")

# Calculo da DF total da frota
if disponibilidades:
    df_total = sum(disponibilidades) / len(disponibilidades)
    st.subheader("Totais da Frota")
    st.write(f"Disponibilidade Física Média da Frota (DF): {df_total:.2f}%")