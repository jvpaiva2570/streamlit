def calcular_tempo_total(qtd_servicos, tempo_por_servico):
    """Calcula o tempo total gasto em um tipo de serviço."""
    return qtd_servicos * tempo_por_servico

def calcular_tempo_parado(dados_caminhao):
    """Calcula o tempo total parado de um caminhão, incluindo corretivas."""
    tempo_servicos = {
        "qtd_250h": 8,
        "qtd_500h": 12,
        "qtd_1000h": 16,
        "qtd_16000h": 168,
    }
    tempo_total_parado = 0
    for servico, tempo_servico in tempo_servicos.items():
        tempo_total_parado += dados_caminhao[servico] * tempo_servico
    
    # Tempo corretivo incluso diretamente
    tempo_total_parado *= (1 + dados_caminhao["taxa_corretiva"])  
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
    Calcula a utilização, a hora não utilizada e as horas trabalhadas de um caminhão.

    Args:
      dados_caminhao: Dicionário com os dados do caminhão.

    Returns:
      Tupla contendo a utilização (em %), as horas não utilizadas e as horas trabalhadas.
    """

    dias_programados = 365  # Informação fixa da planilha
    horas_programadas_dia = 24  # Informação fixa da planilha
    qtd_orientacoes_gerenciais = dias_programados * 3  # Quantidade de orientações gerenciais
    tempo_orientacao_gerencial = 0.08  # Tempo perdido por orientação gerencial (em horas)

    tempo_250h = calcular_tempo_total(dados_caminhao["qtd_250h"], 8)
    tempo_500h = calcular_tempo_total(dados_caminhao["qtd_500h"], 12)
    tempo_1000h = calcular_tempo_total(dados_caminhao["qtd_1000h"], 16)
    tempo_16000h = calcular_tempo_total(dados_caminhao["qtd_16000h"], 168)

    # Tempo total parado já inclui o tempo de corretivas,
    # calculado com base na taxa corretiva
    tempo_total_parado = calcular_tempo_parado(dados_caminhao)

        # Calcula as horas disponíveis
    df = calcular_df(tempo_total_parado)
    horas_disponiveis = dias_programados * horas_programadas_dia * (df/100)  # Divide a DF por 100 para obter o valor decimal

    # Tempo das novas paradas
    tempo_sem_operador = calcular_tempo_total(dados_caminhao["qtd_sem_operador"], 1)
    tempo_parada_desmonte = calcular_tempo_total(dados_caminhao["qtd_parada_desmonte"], 2)
    tempo_parada_climatica = calcular_tempo_total(dados_caminhao["qtd_parada_climatica"], 1)
    tempo_almoco = calcular_tempo_total(dados_caminhao["qtd_almoco"], 1)*365  # 1 hora de almoço
    tempo_troca_turno = calcular_tempo_total(dados_caminhao["qtd_troca_turno"], 0.08)*365  # 0.08 horas por troca de turno
    tempo_orientacao_gerencial = calcular_tempo_total(qtd_orientacoes_gerenciais, tempo_orientacao_gerencial) # Calcula o tempo perdido com orientação gerencial
    tempo_absenteismo = ((dados_caminhao["perc_absenteismo"] / 100) *horas_programadas_dia)*dias_programados
    tempo_treinamento = ((dados_caminhao["perc_treinamento"] / 100) * horas_programadas_dia)*dias_programados

    tempo_total_parado += (
        tempo_sem_operador
        + tempo_parada_desmonte
        + tempo_parada_climatica
        + tempo_almoco
        + tempo_troca_turno
        + tempo_orientacao_gerencial
        + tempo_absenteismo
        + tempo_treinamento

    )

    


    


    # Calcula o tempo perdido em cada operação
    tempo_perdido = calcular_tempo_perdido(dados_caminhao)

    # Calcula a hora não utilizada (HNU) como a soma dos tempos perdidos
    horas_nao_utilizadas = sum(tempo_perdido.values())

    # Calcula as horas trabalhadas
    horas_trabalhadas = horas_disponiveis - horas_nao_utilizadas

    # Calcula a utilização
    if horas_disponiveis == 0:
        return 0, horas_nao_utilizadas, horas_trabalhadas

    utilizacao = (horas_trabalhadas / horas_disponiveis) * 100




    return utilizacao, horas_nao_utilizadas, horas_trabalhadas, horas_disponiveis

def calcular_tempo_perdido(dados_caminhao):  # Adicione horas_trabalhadas como argumento
    """Calcula o tempo perdido em cada operação."""

    tempo_perdido = {}

    # Tempo perdido por falta de operador (considerando 1 hora por parada)
    tempo_perdido["Sem Operador"] = calcular_tempo_total(dados_caminhao["qtd_sem_operador"], 1) 

    # Tempo perdido por parada para desmonte (considerando 2 horas por parada)
    tempo_perdido["Parada Desmonte"] = calcular_tempo_total(dados_caminhao["qtd_parada_desmonte"], 2) 

    # Tempo perdido por parada climática (considerando 1 hora por parada)
    tempo_perdido["Parada Climática"] = calcular_tempo_total(dados_caminhao["qtd_parada_climatica"], 1) 

    # Tempo perdido com almoço (considerando 1 hora por almoço)
    tempo_perdido["Almoço"] = calcular_tempo_total(dados_caminhao["qtd_almoco"], 1) * 365

    # Tempo perdido com troca de turno (considerando 0.08 horas por troca)
    tempo_perdido["Troca de Turno"] = calcular_tempo_total(dados_caminhao["qtd_troca_turno"], 0.08) * 365

    # Tempo perdido com orientação gerencial
    dias_programados = 365
    horas_dia=24
    
    qtd_orientacoes_gerenciais = dias_programados * 3
    tempo_orientacao_gerencial = 0.08
    tempo_perdido["Orientação Gerencial"] = calcular_tempo_total(
        qtd_orientacoes_gerenciais, tempo_orientacao_gerencial
    )

    # Tempo perdido com absenteísmo (em horas)
    tempo_perdido["Absenteísmo"] = ((dados_caminhao["perc_absenteismo"] / 100) * horas_dia)*dias_programados

    # Tempo perdido com treinamento (em horas)
    tempo_perdido["Treinamento"] = ((dados_caminhao["perc_treinamento"] / 100) * horas_dia)*dias_programados

    return tempo_perdido
