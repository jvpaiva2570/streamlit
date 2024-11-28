def calcular_tempo_total(qtd_servicos, tempo_por_servico):
    """Calcula o tempo total gasto em um tipo de serviço."""
    return qtd_servicos * tempo_por_servico


def calcular_tempo_parado(dados_caminhao):
    """Calcula o tempo total parado de um caminhão."""
    tempo_preventiva_250h = 8
    tempo_preventiva_500h = 12
    tempo_preventiva_1000h = 16
    tempo_preventiva_16000h = 168

    tempo_parado_250h = dados_caminhao["qtd_250h"] * tempo_preventiva_250h
    tempo_parado_500h = dados_caminhao["qtd_500h"] * tempo_preventiva_500h
    tempo_parado_1000h = dados_caminhao["qtd_1000h"] * tempo_preventiva_1000h
    tempo_parado_16000h = (
        dados_caminhao["qtd_16000h"] * tempo_preventiva_16000h
    )
    tempo_total_parado = (
        tempo_parado_250h
        + tempo_parado_500h
        + tempo_parado_1000h
        + tempo_parado_16000h
    )
    tempo_corretivo = dados_caminhao["taxa_corretiva"] * tempo_total_parado
    tempo_total_parado += tempo_corretivo
    return tempo_total_parado


def calcular_df(tempo_total_parado):
    """Calcula a disponibilidade física (DF) de um caminhão."""
    horas_programadas_ano = 365 * 24
    df = (
        (horas_programadas_ano - tempo_total_parado)
        / horas_programadas_ano
    ) * 100
    return df


def calcular_utilizacao(dados_caminhao, horas_trabalhadas):
    """Calcula a utilização e a hora não utilizada de um caminhão."""

    dias_programados = 365  # Informação fixa da planilha
    horas_programadas_dia = 24  # Informação fixa da planilha
    tempo_troca_turno = 0.5  # Informação fixa da planilha

    # Tempo das novas paradas (considerando 8 horas por parada como exemplo)
    tempo_sem_operador = calcular_tempo_total(dados_caminhao["qtd_sem_operador"], 8)
    tempo_parada_desmonte = calcular_tempo_total(dados_caminhao["qtd_parada_desmonte"], 8)
    tempo_parada_climatica = calcular_tempo_total(dados_caminhao["qtd_parada_climatica"], 8)
    tempo_almoco = calcular_tempo_total(dados_caminhao["qtd_almoco"], 1)  # 1 hora de almoço
    tempo_troca_turno = calcular_tempo_total(dados_caminhao["qtd_troca_turno"], 0.5)  # 0.5 horas por troca de turno

    # Tempo de absenteísmo e treinamento (em horas)
    tempo_absenteismo = (dados_caminhao["perc_absenteismo"] / 100) * horas_trabalhadas
    tempo_treinamento = (dados_caminhao["perc_treinamento"] / 100) * horas_trabalhadas

    tempo_total_parado = calcular_tempo_parado(dados_caminhao)  

    horas_disponiveis = (
        dias_programados * horas_programadas_dia
    ) - tempo_total_parado

    # Calcula a hora não utilizada
    horas_nao_utilizadas = horas_disponiveis - horas_trabalhadas  

    # Calcula a utilização
    if horas_disponiveis == 0:
        return 0, horas_nao_utilizadas  # Retorna a utilização e as horas não utilizadas
    return (horas_trabalhadas / horas_disponiveis) * 100, horas_nao_utilizadas


def calcular_tempo_perdido(dados_caminhao):
    """Calcula o tempo perdido em cada operação."""

    tempo_perdido = {}

    # Tempo perdido por falta de operador (considerando 8 horas por parada)
    tempo_perdido["Sem Operador"] = calcular_tempo_total(dados_caminhao["qtd_sem_operador"], 1)

    # Tempo perdido por parada para desmonte (considerando 8 horas por parada)
    tempo_perdido["Parada Desmonte"] = calcular_tempo_total(dados_caminhao["qtd_parada_desmonte"], 2)

    # Tempo perdido por parada climática (considerando 8 horas por parada)
    tempo_perdido["Parada Climática"] = calcular_tempo_total(dados_caminhao["qtd_parada_climatica"], 1)

    # Tempo perdido com almoço (considerando 1 hora por almoço)
    tempo_perdido["Almoço"] = calcular_tempo_total(dados_caminhao["qtd_almoco"], 1)*365

    # Tempo perdido com troca de turno (considerando 0.5 horas por troca)
    tempo_perdido["Troca de Turno"] = calcular_tempo_total(dados_caminhao["qtd_troca_turno"], 0.8)*365

    # Tempo perdido com treinamento (considerando 8 horas por treinamento)
    tempo_perdido["Treinamento"] = calcular_tempo_total(dados_caminhao["qtd_treinamento"], 8)

    return tempo_perdido