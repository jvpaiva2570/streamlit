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


def calcular_utilizacao(dados_caminhao):
    """
    Calcula a utilização e a hora não utilizada de um caminhão.
    
    Args:
      dados_caminhao: Dicionário com os dados do caminhão.

    Returns:
      Tupla contendo a utilização (em %) e as horas não utilizadas.
    """

    dias_programados = 365  # Informação fixa da planilha
    horas_programadas_dia = 24  # Informação fixa da planilha
    tempo_troca_turno = 0.5  # Informação fixa da planilha

    tempo_250h = calcular_tempo_total(dados_caminhao["qtd_250h"], 8)
    tempo_500h = calcular_tempo_total(dados_caminhao["qtd_500h"], 12)
    tempo_1000h = calcular_tempo_total(dados_caminhao["qtd_1000h"], 16)
    tempo_16000h = calcular_tempo_total(dados_caminhao["qtd_16000h"], 168)

    # Tempo total parado já inclui o tempo de corretivas,
    # calculado com base na taxa corretiva
    tempo_total_parado = calcular_tempo_parado(dados_caminhao)

    # Tempo das novas paradas (considerando 8 horas por parada como exemplo)
    tempo_sem_operador = calcular_tempo_total(dados_caminhao["qtd_sem_operador"], 8)
    tempo_parada_desmonte = calcular_tempo_total(dados_caminhao["qtd_parada_desmonte"], 8)
    tempo_parada_climatica = calcular_tempo_total(dados_caminhao["qtd_parada_climatica"], 8)
    tempo_almoco = calcular_tempo_total(dados_caminhao["qtd_almoco"], 1)  # 1 hora de almoço
    tempo_troca_turno = calcular_tempo_total(dados_caminhao["qtd_troca_turno"], 0.5)  # 0.5 horas por troca de turno

    # Tempo de absenteísmo e treinamento (em horas) - precisa ser calculado depois das horas trabalhadas
    # tempo_absenteismo = (dados_caminhao["perc_absenteismo"] / 100) * horas_trabalhadas
    # tempo_treinamento = (dados_caminhao["perc_treinamento"] / 100) * horas_trabalhadas

    tempo_total_parado += (
        tempo_sem_operador
        + tempo_parada_desmonte
        + tempo_parada_climatica
        + tempo_almoco
        + tempo_troca_turno
        # + tempo_absenteismo
        # + tempo_treinamento
    )

    horas_disponiveis = (
        dias_programados * horas_programadas_dia
    ) - tempo_total_parado

    # Calcula a hora não utilizada
    horas_nao_utilizadas = calcular_tempo_total(dados_caminhao["qtd_hnu"], 8)

    # Calcula as horas trabalhadas
    horas_trabalhadas = horas_disponiveis - horas_nao_utilizadas

    # Calcula a utilização
    if horas_disponiveis == 0:
        return 0, horas_nao_utilizadas, horas_trabalhadas  # Retorna a utilização, as horas não utilizadas e as horas trabalhadas

    utilizacao = (horas_trabalhadas / horas_disponiveis) * 100

    # Calcula o tempo de absenteísmo e treinamento (em horas)
    tempo_absenteismo = (dados_caminhao["perc_absenteismo"] / 100) * horas_trabalhadas
    tempo_treinamento = (dados_caminhao["perc_treinamento"] / 100) * horas_trabalhadas

    return utilizacao, horas_nao_utilizadas, horas_trabalhadas


def calcular_tempo_perdido(dados_caminhao):
    """Calcula o tempo perdido em cada operação."""

    tempo_perdido = {}

    # Tempo perdido por falta de operador (considerando 8 horas por parada)
    tempo_perdido["Sem Operador"] = calcular_tempo_total(dados_caminhao["qtd_sem_operador"], 8)

    # Tempo perdido por parada para desmonte (considerando 8 horas por parada)
    tempo_perdido["Parada Desmonte"] = calcular_tempo_total(dados_caminhao["qtd_parada_desmonte"], 8)

    # Tempo perdido por parada climática (considerando 8 horas por parada)
    tempo_perdido["Parada Climática"] = calcular_tempo_total(dados_caminhao["qtd_parada_climatica"], 8)

    # Tempo perdido com almoço (considerando 1 hora por almoço)
    tempo_perdido["Almoço"] = calcular_tempo
